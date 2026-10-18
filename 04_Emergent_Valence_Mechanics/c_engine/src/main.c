#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>

#include "vec3.h"
#include "forcefield.h"
#include "xyz_io.h"
#include "engine.h"

#ifdef _OPENMP
#include <omp.h>
#endif

#if defined(_WIN32)
  #include <dirent.h>   /* MinGW-w64 ships a POSIX-compatible dirent.h */
#else
  #include <dirent.h>
#endif

typedef struct {
    const char *input;
    const char *out;
    const char *forcefield;
    int frozen_steps;
    int free_steps;
    double dt;
    int sample_every;
    int raw;           /* --raw: skip the velocity-clamp fix, exact old math */
    double nuc_vmax;
    double e_vmax;
    long seed;
    int seed_given;
    int threads;
    int quiet;
    const char *batch_dir;
    const char *batch_list;
    const char *batch_csv;
} Args;

/* High-resolution, cross-platform wall clock (clock() on Windows/MinGW has
 * ~10-15ms granularity, which is useless for timing individual small
 * molecules -- this is why the batch mode exists: one process, one clock
 * baseline, no per-molecule process-launch noise on top of that). */
static double now_seconds(void) {
    struct timespec ts;
    timespec_get(&ts, TIME_UTC);
    return (double)ts.tv_sec + (double)ts.tv_nsec * 1e-9;
}

static void print_usage(const char *prog) {
    fprintf(stderr,
        "EVM 4.0 C engine -- faithful port of the Python EVM 4.0 physics core.\n\n"
        "Single molecule:\n"
        "  %s --input mol.xyz [options]\n\n"
        "Batch (one process, no per-molecule process-launch overhead):\n"
        "  %s --batch-dir DIR [options]      Every *.xyz file in DIR\n"
        "  %s --batch-list FILE [options]    One XYZ path per line in FILE\n\n"
        "  --input FILE          Starting geometry, standard XYZ\n"
        "  --out FILE            Trajectory output, multi-frame XYZ (single-molecule mode only;\n"
        "                        default: trajectory.xyz)\n"
        "  --batch-dir DIR       Run every *.xyz file in DIR, one process, no trajectory output\n"
        "  --batch-list FILE     Run every XYZ path listed in FILE (one per line)\n"
        "  --batch-csv FILE      Per-molecule batch results (default: batch_results.csv)\n"
        "  --forcefield FILE     Forcefield JSON (default: built-in EVM 4.0 defaults)\n"
        "  --frozen-steps N      Phase 1 steps, electrons relax, nuclei frozen (default 500)\n"
        "  --free-steps N        Phase 2 steps, free propagation (default 500)\n"
        "  --dt F                Timestep (default 0.005)\n"
        "  --sample-every N      Write a trajectory frame + RMSD every N free steps (single mode)\n"
        "  --raw                 Disable the velocity-clamp fix: exact old EVM 4.0 math\n"
        "                        (see docs/EVM_Simulation_Best_Practices.md for why the\n"
        "                        clamp exists -- default ON, this flag turns it OFF)\n"
        "  --nuc-vmax F          Override nuclear velocity clamp (default 0.05, ignored with --raw)\n"
        "  --e-vmax F            Override electron velocity clamp (default 0.5, ignored with --raw)\n"
        "  --seed N              Accepted for CLI/API consistency; this engine's physics has no\n"
        "                        RNG anywhere, so this currently changes nothing.\n"
        "  --threads N           OpenMP thread count (default: OpenMP's own default)\n"
        "  --quiet               Suppress progress output\n"
        "  --help                Show this message\n",
        prog, prog, prog);
}

static int parse_args(int argc, char **argv, Args *a) {
    memset(a, 0, sizeof(*a));
    a->out = "trajectory.xyz";
    a->frozen_steps = 500;
    a->free_steps = 500;
    a->dt = 0.005;
    a->sample_every = 10;
    a->raw = 0;
    a->nuc_vmax = 0.05;
    a->e_vmax = 0.5;
    a->threads = 0;
    a->batch_csv = "batch_results.csv";

    for (int i = 1; i < argc; i++) {
        #define NEXT() (++i < argc ? argv[i] : NULL)
        if (strcmp(argv[i], "--input") == 0) { a->input = NEXT(); }
        else if (strcmp(argv[i], "--out") == 0) { a->out = NEXT(); }
        else if (strcmp(argv[i], "--batch-dir") == 0) { a->batch_dir = NEXT(); }
        else if (strcmp(argv[i], "--batch-list") == 0) { a->batch_list = NEXT(); }
        else if (strcmp(argv[i], "--batch-csv") == 0) { a->batch_csv = NEXT(); }
        else if (strcmp(argv[i], "--forcefield") == 0) { a->forcefield = NEXT(); }
        else if (strcmp(argv[i], "--frozen-steps") == 0) { a->frozen_steps = atoi(NEXT()); }
        else if (strcmp(argv[i], "--free-steps") == 0) { a->free_steps = atoi(NEXT()); }
        else if (strcmp(argv[i], "--dt") == 0) { a->dt = atof(NEXT()); }
        else if (strcmp(argv[i], "--sample-every") == 0) { a->sample_every = atoi(NEXT()); }
        else if (strcmp(argv[i], "--raw") == 0) { a->raw = 1; }
        else if (strcmp(argv[i], "--nuc-vmax") == 0) { a->nuc_vmax = atof(NEXT()); }
        else if (strcmp(argv[i], "--e-vmax") == 0) { a->e_vmax = atof(NEXT()); }
        else if (strcmp(argv[i], "--seed") == 0) { a->seed = atol(NEXT()); a->seed_given = 1; }
        else if (strcmp(argv[i], "--threads") == 0) { a->threads = atoi(NEXT()); }
        else if (strcmp(argv[i], "--quiet") == 0) { a->quiet = 1; }
        else if (strcmp(argv[i], "--help") == 0) { print_usage(argv[0]); exit(0); }
        else { fprintf(stderr, "unknown argument: %s\n", argv[i]); return -1; }
        #undef NEXT
    }
    if (!a->input && !a->batch_dir && !a->batch_list) {
        fprintf(stderr, "error: one of --input, --batch-dir, --batch-list is required\n");
        return -1;
    }
    return 0;
}

/* Runs the frozen+free schedule on an already-built System. Writes a
 * trajectory frame every sample_every steps IFF traj_path is non-NULL
 * (batch mode passes NULL -- no per-molecule trajectory file). Returns
 * final/max RMSD and wall-clock via out-params. */
static void run_schedule(System *sys, const Vec3 *reference, const Args *a,
                          const char *traj_path, const int *Zs,
                          double *out_final_rmsd, double *out_max_rmsd, double *out_wall_s) {
    double nuc_vmax = a->raw ? -1.0 : a->nuc_vmax;
    double e_vmax = a->raw ? -1.0 : a->e_vmax;

    double t0 = now_seconds();

    sys->damping_nuc = 0.0;
    Vec3 *frozen_ref = (Vec3 *)malloc(sizeof(Vec3) * (size_t)sys->n_nuclei);
    memcpy(frozen_ref, sys->nuc_pos, sizeof(Vec3) * (size_t)sys->n_nuclei);
    for (int step = 0; step < a->frozen_steps; step++) {
        integrator_step(sys, a->dt, -1.0, -1.0);
        memcpy(sys->nuc_pos, frozen_ref, sizeof(Vec3) * (size_t)sys->n_nuclei);
        memset(sys->nuc_vel, 0, sizeof(Vec3) * (size_t)sys->n_nuclei);
    }
    free(frozen_ref);

    sys->damping_nuc = 0.99;
    double max_rmsd = 0.0, final_rmsd = 0.0;
    for (int step = 0; step < a->free_steps; step++) {
        integrator_step(sys, a->dt, nuc_vmax, e_vmax);
        if (step % a->sample_every == 0 || step == a->free_steps - 1) {
            double rmsd = positions_rmsd(sys->nuc_pos, reference, sys->n_nuclei);
            if (rmsd > max_rmsd) max_rmsd = rmsd;
            final_rmsd = rmsd;
            if (traj_path) {
                xyz_append_frame(traj_path, sys->nuc_pos, Zs, sys->n_nuclei, step, step * a->dt);
                if (!a->quiet) fprintf(stderr, "step %6d: RMSD vs. input %.4f A\n", step, rmsd);
            }
        }
    }

    *out_wall_s = now_seconds() - t0;
    *out_final_rmsd = final_rmsd;
    *out_max_rmsd = max_rmsd;
}

static int run_single(const Args *args) {
    XYZAtom *atoms = NULL;
    int n_atoms = xyz_read_first_frame(args->input, &atoms);
    if (n_atoms < 0) return 1;

    ForceField ff;
    if (args->forcefield) {
        if (forcefield_load(args->forcefield, &ff) != 0) {
            fprintf(stderr, "error: could not load forcefield '%s'\n", args->forcefield);
            free(atoms);
            return 1;
        }
    } else {
        forcefield_defaults(&ff);
        if (!args->quiet) fprintf(stderr, "[info] using built-in default forcefield\n");
    }

    System sys;
    if (system_build(atoms, n_atoms, &ff, &sys) != 0) {
        fprintf(stderr, "error: failed to build system\n");
        free(atoms);
        return 1;
    }
    if (!args->quiet) {
        fprintf(stderr, "[info] %d nuclei, %d electrons, mode=%s\n",
                sys.n_nuclei, sys.n_electrons, args->raw ? "RAW (no velocity clamp)" : "default (clamped)");
    }

    Vec3 *reference = (Vec3 *)malloc(sizeof(Vec3) * (size_t)sys.n_nuclei);
    memcpy(reference, sys.nuc_pos, sizeof(Vec3) * (size_t)sys.n_nuclei);

    FILE *f = fopen(args->out, "w");
    if (f) fclose(f);

    double final_rmsd, max_rmsd, wall_s;
    run_schedule(&sys, reference, args, args->out, sys.nuc_Z, &final_rmsd, &max_rmsd, &wall_s);

    printf("final_rmsd_A=%.6f\n", final_rmsd);
    printf("max_rmsd_A=%.6f\n", max_rmsd);
    printf("stable_0.15A=%s\n", max_rmsd <= 0.15 ? "yes" : "no");
    printf("wall_clock_total_s=%.6f\n", wall_s);

    free(reference);
    system_free(&sys);
    free(atoms);
    return 0;
}

/* Collects XYZ file paths from --batch-dir (every *.xyz entry) or
 * --batch-list (one path per line). Returns count, fills *paths_out
 * (array of malloc'd strings, caller frees each + the array). */
static int collect_batch_paths(const Args *a, char ***paths_out) {
    char **paths = NULL;
    int n = 0, cap = 0;

    #define PUSH(p) do { \
        if (n == cap) { cap = cap ? cap * 2 : 64; paths = realloc(paths, sizeof(char *) * (size_t)cap); } \
        paths[n++] = strdup(p); \
    } while (0)

    if (a->batch_dir) {
        DIR *d = opendir(a->batch_dir);
        if (!d) { fprintf(stderr, "error: cannot open directory '%s'\n", a->batch_dir); return -1; }
        struct dirent *entry;
        while ((entry = readdir(d)) != NULL) {
            size_t len = strlen(entry->d_name);
            if (len > 4 && strcmp(entry->d_name + len - 4, ".xyz") == 0) {
                char full[2048];
                snprintf(full, sizeof(full), "%s/%s", a->batch_dir, entry->d_name);
                PUSH(full);
            }
        }
        closedir(d);
    } else if (a->batch_list) {
        FILE *f = fopen(a->batch_list, "r");
        if (!f) { fprintf(stderr, "error: cannot open list '%s'\n", a->batch_list); return -1; }
        char line[2048];
        while (fgets(line, sizeof(line), f)) {
            size_t len = strlen(line);
            while (len > 0 && (line[len - 1] == '\n' || line[len - 1] == '\r')) line[--len] = '\0';
            if (len > 0) PUSH(line);
        }
        fclose(f);
    }
    #undef PUSH

    *paths_out = paths;
    return n;
}

static int run_batch(const Args *args) {
    char **paths;
    int n_paths = collect_batch_paths(args, &paths);
    if (n_paths < 0) return 1;
    if (n_paths == 0) {
        fprintf(stderr, "error: no .xyz files found\n");
        return 1;
    }

    ForceField ff;
    if (args->forcefield) {
        if (forcefield_load(args->forcefield, &ff) != 0) {
            fprintf(stderr, "error: could not load forcefield '%s'\n", args->forcefield);
            return 1;
        }
    } else {
        forcefield_defaults(&ff);
    }

    FILE *csv = fopen(args->batch_csv, "w");
    if (!csv) { fprintf(stderr, "error: cannot open '%s' for writing\n", args->batch_csv); return 1; }
    fprintf(csv, "name,n_atoms,final_rmsd_A,max_rmsd_A,stable,wall_clock_s\n");

    fprintf(stderr, "[info] batch: %d molecules, mode=%s, %d frozen + %d free steps\n",
            n_paths, args->raw ? "RAW" : "default (clamped)", args->frozen_steps, args->free_steps);
#ifdef _OPENMP
    fprintf(stderr, "[info] OpenMP: %d threads, one molecule per thread "
                     "(molecule-level parallelism -- see PARALLEL_THRESHOLD in engine.c "
                     "for why the per-molecule physics itself stays single-threaded here)\n",
            args->threads > 0 ? args->threads : omp_get_max_threads());
    if (args->threads > 0) omp_set_num_threads(args->threads);
    /* Molecules above PARALLEL_THRESHOLD would otherwise try to spawn their
     * own inner thread team too -- in a batch that mixes small and large
     * molecules that's N_outer x N_inner oversubscription. Capping active
     * nesting to 1 level keeps this loop as the only parallel region that
     * actually forks, regardless of what's in the batch. */
    omp_set_max_active_levels(1);
#endif

    int n_stable = 0, n_errors = 0;
    double batch_t0 = now_seconds();

    #pragma omp parallel for schedule(dynamic) reduction(+:n_stable,n_errors)
    for (int k = 0; k < n_paths; k++) {
        XYZAtom *atoms = NULL;
        int n_atoms = xyz_read_first_frame(paths[k], &atoms);
        if (n_atoms < 0) { n_errors++; continue; }

        System sys;
        if (system_build(atoms, n_atoms, &ff, &sys) != 0) {
            free(atoms); n_errors++; continue;
        }

        Vec3 *reference = (Vec3 *)malloc(sizeof(Vec3) * (size_t)sys.n_nuclei);
        memcpy(reference, sys.nuc_pos, sizeof(Vec3) * (size_t)sys.n_nuclei);

        double final_rmsd, max_rmsd, wall_s;
        run_schedule(&sys, reference, args, NULL, NULL, &final_rmsd, &max_rmsd, &wall_s);

        int stable = max_rmsd <= 0.15;
        if (stable) n_stable++;

        /* basename only, for a tidier CSV */
        const char *base = strrchr(paths[k], '/');
        base = base ? base + 1 : paths[k];

        #pragma omp critical(csv_write)
        {
            fprintf(csv, "%s,%d,%.6f,%.6f,%s,%.6f\n", base, n_atoms, final_rmsd, max_rmsd,
                    stable ? "yes" : "no", wall_s);
            if (!args->quiet && (k + 1) % 100 == 0) {
                fprintf(stderr, "  ...%d/%d\n", k + 1, n_paths);
            }
        }

        free(reference);
        system_free(&sys);
        free(atoms);
    }

    double batch_total_s = now_seconds() - batch_t0;
    fclose(csv);

    int n_run = n_paths - n_errors;
    printf("batch_molecules=%d\n", n_run);
    printf("batch_errors=%d\n", n_errors);
    printf("batch_total_wall_clock_s=%.4f\n", batch_total_s);
    printf("batch_throughput_molecules_per_sec=%.2f\n", n_run > 0 ? n_run / batch_total_s : 0.0);
    printf("batch_stable_fraction=%.4f\n", n_run > 0 ? (double)n_stable / n_run : 0.0);
    printf("batch_csv=%s\n", args->batch_csv);

    for (int k = 0; k < n_paths; k++) free(paths[k]);
    free(paths);
    return 0;
}

int main(int argc, char **argv) {
    Args args;
    if (parse_args(argc, argv, &args) != 0) {
        print_usage(argv[0]);
        return 1;
    }

#ifdef _OPENMP
    if (args.threads > 0) omp_set_num_threads(args.threads);
#endif
    if (args.seed_given && !args.quiet) {
        fprintf(stderr, "[info] --seed %ld accepted but unused: this engine's physics is fully "
                         "deterministic, there is no RNG in it to seed.\n", args.seed);
    }

    if (args.batch_dir || args.batch_list) {
        return run_batch(&args);
    }
    return run_single(&args);
}

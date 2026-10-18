#include "engine.h"

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <math.h>

#ifdef _OPENMP
#include <omp.h>
#endif

#define EPS 1e-6

/* Below this electron count, OpenMP's per-region thread fork/join overhead
 * costs more than the parallel work saves -- measured directly on QM9-scale
 * molecules (tens of electrons): 12 threads was 7x SLOWER than 1 thread
 * there, while the same threading gave a real ~3-4x speedup on the larger
 * (160-458 electron) peptide benchmark systems. This gates all five
 * pairwise loops below on N_e so --threads N only kicks in when it's
 * actually worth it, without the caller needing to know or tune this. */
#define PARALLEL_THRESHOLD 150

int system_build(const XYZAtom *atoms, int n_atoms, const ForceField *ff, System *sys) {
    memset(sys, 0, sizeof(*sys));
    sys->ff = ff;
    sys->damping_e = 0.8;
    sys->damping_nuc = 0.99;
    sys->has_acc = 0;

    sys->n_nuclei = n_atoms;
    sys->nuc_pos = (Vec3 *)calloc((size_t)n_atoms, sizeof(Vec3));
    sys->nuc_vel = (Vec3 *)calloc((size_t)n_atoms, sizeof(Vec3));
    sys->nuc_acc = (Vec3 *)calloc((size_t)n_atoms, sizeof(Vec3));
    sys->nuc_Z = (int *)calloc((size_t)n_atoms, sizeof(int));
    sys->nuc_mass = (double *)calloc((size_t)n_atoms, sizeof(double));
    if (!sys->nuc_pos || !sys->nuc_vel || !sys->nuc_acc || !sys->nuc_Z || !sys->nuc_mass) {
        system_free(sys);
        return -1;
    }

    int total_electrons = 0;
    for (int a = 0; a < n_atoms; a++) {
        sys->nuc_pos[a] = atoms[a].pos;
        sys->nuc_Z[a] = atoms[a].Z;
        /* EVM 4.0 Car-Parrinello shortcut: every nucleus gets mass=1.0,
         * not its real atomic mass (see system_builder.py's comment on
         * this). True dynamic masses are an EVM 5.0 thing, out of scope
         * for a faithful 4.0 port. */
        sys->nuc_mass[a] = 1.0;
        total_electrons += atoms[a].Z;
    }

    sys->n_electrons = total_electrons;
    sys->e_pos = (Vec3 *)calloc((size_t)total_electrons, sizeof(Vec3));
    sys->e_vel = (Vec3 *)calloc((size_t)total_electrons, sizeof(Vec3));
    sys->e_acc = (Vec3 *)calloc((size_t)total_electrons, sizeof(Vec3));
    sys->e_phase = (double *)calloc((size_t)total_electrons, sizeof(double));
    sys->e_elem_Z = (int *)calloc((size_t)total_electrons, sizeof(int));
    if (!sys->e_pos || !sys->e_vel || !sys->e_acc || !sys->e_phase || !sys->e_elem_Z) {
        system_free(sys);
        return -1;
    }

    /* Fibonacci-sphere electron placement + global alternating phase,
     * exactly matching EVMBuilder.build_engine()'s electron initializer. */
    int e_idx_global = 0;
    const double golden = M_PI * (1.0 + sqrt(5.0));
    for (int a = 0; a < n_atoms; a++) {
        int Z = atoms[a].Z;
        for (int i = 0; i < Z; i++) {
            double phi = acos(1.0 - 2.0 * (i + 0.5) / (double)Z);
            double theta = golden * i;
            Vec3 offset;
            offset.x = 0.3 * sin(phi) * cos(theta);
            offset.y = 0.3 * sin(phi) * sin(theta);
            offset.z = 0.3 * cos(phi);
            sys->e_pos[e_idx_global] = vec3_add(atoms[a].pos, offset);
            sys->e_phase[e_idx_global] = (e_idx_global % 2 == 0) ? 1.0 : -1.0;
            sys->e_elem_Z[e_idx_global] = Z;
            e_idx_global++;
        }
    }
    /* e_vel, nuc_vel already zero from calloc -- matches engine.e_vel.zero_() */

    return 0;
}

void system_free(System *sys) {
    free(sys->nuc_pos); free(sys->nuc_vel); free(sys->nuc_acc);
    free(sys->nuc_Z); free(sys->nuc_mass);
    free(sys->e_pos); free(sys->e_vel); free(sys->e_acc);
    free(sys->e_phase); free(sys->e_elem_Z);
    memset(sys, 0, sizeof(*sys));
}

void compute_forces(const System *sys, Vec3 *F_e_out, Vec3 *F_n_out) {
    const int N_e = sys->n_electrons;
    const int N_n = sys->n_nuclei;
    const ForceField *ff = sys->ff;

    for (int i = 0; i < N_e; i++) F_e_out[i] = vec3_zero();
    for (int n = 0; n < N_n; n++) F_n_out[n] = vec3_zero();

    /* --- Pass 1: U_coulomb[i] = sum_n Z_n / dist_en, for the compressibility
     * factor (engine.py: compression_factor = exp(-U_coulomb/U_0)). Computed
     * separately from the e-n force pass below because e_excl_eff (which
     * needs compression_factor) is required by the e-e block, and computing
     * it here avoids storing the full [N_e x N_n] distance matrix. */
    double *compression = (double *)malloc(sizeof(double) * (size_t)N_e);
    #pragma omp parallel for schedule(static) if(N_e > PARALLEL_THRESHOLD)
    for (int i = 0; i < N_e; i++) {
        double U_coulomb = 0.0;
        for (int n = 0; n < N_n; n++) {
            Vec3 diff = vec3_sub(sys->e_pos[i], sys->nuc_pos[n]);
            double dist_sq = vec3_norm_sq(diff) + EPS;
            U_coulomb += sys->nuc_Z[n] / sqrt(dist_sq);
        }
        compression[i] = exp(-U_coulomb / ff->U_0);
    }

    double *e_excl_eff = (double *)malloc(sizeof(double) * (size_t)N_e);
    for (int i = 0; i < N_e; i++) {
        e_excl_eff[i] = fabs(ff->Excl[sys->e_elem_Z[i]]) * compression[i];
    }

    /* R_i^12 only depends on the electron's element, not on which nucleus
     * it's paired with -- precomputed once per electron instead of once
     * per (i,n) pair (that redundant pow() call was the main reason an
     * early version of this port was barely faster than the Python/PyTorch
     * CPU path despite being a native compiled loop). */
    double *R12 = (double *)malloc(sizeof(double) * (size_t)N_e);
    for (int i = 0; i < N_e; i++) {
        double R_i = fabs(ff->R[sys->e_elem_Z[i]]);
        double r2 = R_i * R_i, r4 = r2 * r2, r8 = r4 * r4;
        R12[i] = r8 * r4; /* R_i^12 via repeated squaring, no pow() */
    }

    /* --- e-n block: Coulomb attraction + 1/r^13 steric repulsion.
     * Computed twice (once per electron for F_e, once per nucleus for the
     * reaction force on F_n) so that BOTH loops can be parallelized without
     * a race on the shared output arrays -- cheaper than atomics here since
     * each pair's actual math (sqrt, divisions) is cheap once pow() is gone. */
    #pragma omp parallel for schedule(static) if(N_e > PARALLEL_THRESHOLD)
    for (int i = 0; i < N_e; i++) {
        Vec3 f_i = vec3_zero();
        for (int n = 0; n < N_n; n++) {
            Vec3 diff = vec3_sub(sys->e_pos[i], sys->nuc_pos[n]); /* e_pos - nuc_pos */
            double dist_sq = vec3_norm_sq(diff) + EPS;
            double dist = sqrt(dist_sq);
            double d6 = dist_sq * dist_sq * dist_sq;        /* dist_sq^3 */
            double dist_sq_pow6_5 = d6 * d6 * dist;          /* dist_sq^6 * dist == dist_sq^6.5 == dist^13 */
            double f_coulomb = -sys->nuc_Z[n] / dist_sq;     /* attraction (pulls toward nucleus) */
            double f_steric = 12.0 * R12[i] / dist_sq_pow6_5;
            double f_mag = f_coulomb + f_steric;
            f_i = vec3_add(f_i, vec3_scale(diff, f_mag / dist));
        }
        F_e_out[i] = f_i;
    }
    #pragma omp parallel for schedule(static) if(N_e > PARALLEL_THRESHOLD)
    for (int n = 0; n < N_n; n++) {
        Vec3 f_n = vec3_zero();
        for (int i = 0; i < N_e; i++) {
            Vec3 diff = vec3_sub(sys->e_pos[i], sys->nuc_pos[n]);
            double dist_sq = vec3_norm_sq(diff) + EPS;
            double dist = sqrt(dist_sq);
            double d6 = dist_sq * dist_sq * dist_sq;
            double dist_sq_pow6_5 = d6 * d6 * dist;
            double f_coulomb = -sys->nuc_Z[n] / dist_sq;
            double f_steric = 12.0 * R12[i] / dist_sq_pow6_5;
            double f_mag = f_coulomb + f_steric;
            f_n = vec3_sub(f_n, vec3_scale(diff, f_mag / dist));
        }
        F_n_out[n].x += f_n.x; F_n_out[n].y += f_n.y; F_n_out[n].z += f_n.z;
    }
    free(R12);

    /* --- e-e block: Coulomb (with spin-pairing) + phase-matched 1/r^6 exclusion. --- */
    #pragma omp parallel for schedule(static) if(N_e > PARALLEL_THRESHOLD)
    for (int i = 0; i < N_e; i++) {
        Vec3 f_i = vec3_zero();
        for (int j = 0; j < N_e; j++) {
            if (j == i) continue;
            Vec3 diff = vec3_sub(sys->e_pos[i], sys->e_pos[j]);
            double dist_sq = vec3_norm_sq(diff) + EPS;
            double dist = sqrt(dist_sq);

            int phase_match = (sys->e_phase[i] == sys->e_phase[j]);
            double phase_mismatch = phase_match ? 0.0 : 1.0;

            double f_coulomb = (1.0 - ff->spin_pairing * phase_mismatch) / dist_sq;

            double excl_pair = (e_excl_eff[i] + e_excl_eff[j]) / 2.0;
            double dist_sq3 = dist_sq * dist_sq * dist_sq; /* dist_sq^3, no pow() */
            double f_exclusion = phase_match ? (excl_pair / dist_sq3) : 0.0;

            double f_mag = f_coulomb + f_exclusion;
            f_i = vec3_add(f_i, vec3_scale(diff, f_mag / dist));
        }
        F_e_out[i].x += f_i.x; F_e_out[i].y += f_i.y; F_e_out[i].z += f_i.z;
    }

    /* --- n-n block: Coulomb repulsion + steric core. Note the epsilon
     * convention differs from e-n/e-e on purpose, matching engine.py:
     * dist_sq_nn itself is NOT epsilon-padded; epsilon is added only at
     * the point of division (both in the 1/dist_sq terms and after the
     * sqrt for the direction norm). --- */
    #pragma omp parallel for schedule(static) if(N_e > PARALLEL_THRESHOLD)
    for (int n = 0; n < N_n; n++) {
        Vec3 f_n = vec3_zero();
        for (int m = 0; m < N_n; m++) {
            if (m == n) continue;
            Vec3 diff = vec3_sub(sys->nuc_pos[n], sys->nuc_pos[m]);
            double dist_sq = vec3_norm_sq(diff); /* no epsilon here, matches Python */
            double dsq = dist_sq + EPS;
            double d2 = dsq * dsq, d4 = d2 * d2, d6 = d4 * d2; /* dsq^6, no pow() */
            double f_coulomb = (double)sys->nuc_Z[n] * sys->nuc_Z[m] / dsq;
            double f_steric = ff->nn_steric / d6;
            double f_mag = f_coulomb + f_steric;
            double norm = sqrt(dist_sq) + EPS;
            f_n = vec3_add(f_n, vec3_scale(diff, f_mag / norm));
        }
        F_n_out[n].x += f_n.x; F_n_out[n].y += f_n.y; F_n_out[n].z += f_n.z;
    }

    free(compression);
    free(e_excl_eff);
}

static Vec3 clamp_components(Vec3 v, double lo, double hi) {
    Vec3 r;
    r.x = v.x < lo ? lo : (v.x > hi ? hi : v.x);
    r.y = v.y < lo ? lo : (v.y > hi ? hi : v.y);
    r.z = v.z < lo ? lo : (v.z > hi ? hi : v.z);
    return r;
}

void integrator_step(System *sys, double dt, double nuc_vmax, double e_vmax) {
    const int N_e = sys->n_electrons;
    const int N_n = sys->n_nuclei;

    if (!sys->has_acc) {
        Vec3 *F_e = (Vec3 *)malloc(sizeof(Vec3) * (size_t)N_e);
        Vec3 *F_n = (Vec3 *)malloc(sizeof(Vec3) * (size_t)N_n);
        compute_forces(sys, F_e, F_n);
        for (int i = 0; i < N_e; i++) sys->e_acc[i] = clamp_components(F_e[i], -1000.0, 1000.0);
        for (int n = 0; n < N_n; n++) {
            Vec3 c = clamp_components(F_n[n], -1000.0, 1000.0);
            sys->nuc_acc[n] = vec3_scale(c, 1.0 / sys->nuc_mass[n]);
        }
        free(F_e); free(F_n);
        sys->has_acc = 1;
    }

    /* Velocity Verlet part 1: position update using current acceleration. */
    for (int i = 0; i < N_e; i++)
        sys->e_pos[i] = vec3_add(sys->e_pos[i],
            vec3_add(vec3_scale(sys->e_vel[i], dt), vec3_scale(sys->e_acc[i], 0.5 * dt * dt)));
    for (int n = 0; n < N_n; n++)
        sys->nuc_pos[n] = vec3_add(sys->nuc_pos[n],
            vec3_add(vec3_scale(sys->nuc_vel[n], dt), vec3_scale(sys->nuc_acc[n], 0.5 * dt * dt)));

    /* New forces at the updated positions. */
    Vec3 *F_e_new = (Vec3 *)malloc(sizeof(Vec3) * (size_t)N_e);
    Vec3 *F_n_new = (Vec3 *)malloc(sizeof(Vec3) * (size_t)N_n);
    compute_forces(sys, F_e_new, F_n_new);

    Vec3 *e_acc_new = (Vec3 *)malloc(sizeof(Vec3) * (size_t)N_e);
    Vec3 *nuc_acc_new = (Vec3 *)malloc(sizeof(Vec3) * (size_t)N_n);
    for (int i = 0; i < N_e; i++) e_acc_new[i] = clamp_components(F_e_new[i], -1000.0, 1000.0);
    for (int n = 0; n < N_n; n++) {
        Vec3 c = clamp_components(F_n_new[n], -1000.0, 1000.0);
        nuc_acc_new[n] = vec3_scale(c, 1.0 / sys->nuc_mass[n]);
    }

    /* Velocity Verlet part 2: velocity update using the average acceleration. */
    for (int i = 0; i < N_e; i++)
        sys->e_vel[i] = vec3_add(sys->e_vel[i],
            vec3_scale(vec3_add(sys->e_acc[i], e_acc_new[i]), 0.5 * dt));
    for (int n = 0; n < N_n; n++)
        sys->nuc_vel[n] = vec3_add(sys->nuc_vel[n],
            vec3_scale(vec3_add(sys->nuc_acc[n], nuc_acc_new[n]), 0.5 * dt));

    for (int i = 0; i < N_e; i++) sys->e_acc[i] = e_acc_new[i];
    for (int n = 0; n < N_n; n++) sys->nuc_acc[n] = nuc_acc_new[n];

    /* Thermostat / damping. */
    for (int i = 0; i < N_e; i++) sys->e_vel[i] = vec3_scale(sys->e_vel[i], sys->damping_e);
    for (int n = 0; n < N_n; n++) sys->nuc_vel[n] = vec3_scale(sys->nuc_vel[n], sys->damping_nuc);

    /* Safety velocity clamp -- the documented EVM best-practice fix
     * (docs/EVM_Simulation_Best_Practices.md), applied by default, skipped
     * entirely in --raw mode (nuc_vmax/e_vmax <= 0). */
    if (nuc_vmax > 0.0) {
        for (int n = 0; n < N_n; n++)
            sys->nuc_vel[n] = clamp_components(sys->nuc_vel[n], -nuc_vmax, nuc_vmax);
    }
    if (e_vmax > 0.0) {
        for (int i = 0; i < N_e; i++)
            sys->e_vel[i] = clamp_components(sys->e_vel[i], -e_vmax, e_vmax);
    }

    free(F_e_new); free(F_n_new); free(e_acc_new); free(nuc_acc_new);
}

double positions_rmsd(const Vec3 *current, const Vec3 *reference, int n) {
    double sum_sq = 0.0;
    for (int i = 0; i < n; i++) {
        Vec3 d = vec3_sub(current[i], reference[i]);
        sum_sq += vec3_norm_sq(d);
    }
    return sqrt(sum_sq / (double)n);
}

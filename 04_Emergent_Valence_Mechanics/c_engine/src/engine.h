#ifndef EVM_ENGINE_H
#define EVM_ENGINE_H

#include "vec3.h"
#include "forcefield.h"
#include "xyz_io.h"

/* Faithful C port of EVM 4.0 (core/base_engine.py + core/engine.py +
 * core/system_builder.py). Single-configuration (no batch dimension --
 * the Python engine's batch_size=1 case), double precision throughout
 * (the Python engine uses float32; double here is strictly more accurate,
 * not less faithful -- see README for why this is an intentional,
 * documented deviation rather than a silent one). */

typedef struct {
    int n_nuclei;
    Vec3 *nuc_pos, *nuc_vel, *nuc_acc;
    int *nuc_Z;
    double *nuc_mass;

    int n_electrons;
    Vec3 *e_pos, *e_vel, *e_acc;
    double *e_phase;   /* +1.0 or -1.0 */
    int *e_elem_Z;     /* element (Z) of the nucleus this electron was spawned from */

    double damping_e, damping_nuc;
    int has_acc; /* lazy-init flag, matches base_engine.py's `if not hasattr(self,'e_acc')` */

    const ForceField *ff;
} System;

/* Builds the system exactly as EVMBuilder.build_engine() does:
 * Fibonacci-sphere electron placement at 0.3 A around each nucleus,
 * global-alternating-parity phase assignment, mass=1.0 for every
 * nucleus (EVM 4.0's Car-Parrinello shortcut), zero electron/nuclear
 * velocity, damping_e=0.8 / damping_nuc=0.99 defaults. */
int system_build(const XYZAtom *atoms, int n_atoms, const ForceField *ff, System *sys);
void system_free(System *sys);

/* F_e_out / F_n_out must be pre-allocated by the caller with n_electrons /
 * n_nuclei entries. Replicates EVMCompressibleEngine.compute_forces()
 * exactly, including its per-block epsilon conventions. */
void compute_forces(const System *sys, Vec3 *F_e_out, Vec3 *F_n_out);

/* One Velocity Verlet step (matches EVMBaseEngine.step()): the internal
 * force clamp to +-1000 is always applied (that's not a toggled "fix",
 * it's part of every published EVM 4.0 version). nuc_vmax / e_vmax <= 0
 * disables the velocity clamp (the --raw / old-math path); positive
 * values apply it every step (the default, documented fix). */
void integrator_step(System *sys, double dt, double nuc_vmax, double e_vmax);

/* Whole-structure RMSD (no alignment -- matches the Python evaluator's
 * convention) between `current` and `reference`, both length n. */
double positions_rmsd(const Vec3 *current, const Vec3 *reference, int n);

#endif

# EVM Simulation Best Practices (Initialization Rules)

This document describes critical engineering and physical principles for initializing molecular simulations in the EVM (Emergent Valence Mechanics) engine.
Because EVM does not use quantum probability densities, but rather classical point charges with steep force barriers, **the initial coordinates of the particles are of critical importance**.

## 1. The Steep Potential Gradient Problem ($1/r^6$ and $1/r^{12}$)

In classical molecular dynamics (MD), forces often exhibit extremely steep gradients near the coordinate origin ($r \to 0$). In our engine, we have two such critical forces:
* **Pauli Phase Exclusion ($1/r^6$ force magnitude)**: Repels electrons of identical phase orientation (spin).
* **Steric Nuclear Shielding ($1/r^{12}$ potential, yielding $1/r^{13}$ force)**: Repels electrons from nuclei to prevent coordinate overlap (divide-by-zero fusion).

**What happens during incorrect initialization?**
If two electrons with the same spin phase are spawned too close to each other (e.g., at a distance of 0.1 Å), the $1/r^6$ repulsive force magnitude becomes astronomical (on the order of millions of units). On the very first simulation step (`dt`), this massive force imparts an near-infinite velocity to the electrons, shooting them out of the simulation bounds (explosion to infinity). This numerical instability cannot be compensated for by velocity damping, as it occurs instantaneously on the first timestep.

## 2. The Golden Rule: "Outside-In Relaxation"

To prevent numerical explosions when initializing a new element or molecule, the following design principle must be adhered to:
> **Particles (especially electrons) must always be initialized at mutual distances that are LARGER than their expected equilibrium radii.**

### Practical Steps for Designing New Experiments:
1. **Wide Spawn Radius:** Distribute the electrons at least 1.0 - 2.0 Å away from the nuclei during the initial step. Coulomb attraction ($1/r^2$) is strong enough to draw them smoothly inward.
2. **Avoid Spatial Overlap:** Never place two electrons of the same spin phase in the same (or very close) coordinate. Their geometric distribution (e.g., along X, Y, Z axes) should guarantee at least a 1.0 Å initial separation.
3. **Heavy Initial Damping (Thermostat):** When searching for the Ground State (global energy minimum), apply heavy velocity damping (`damping_e = 0.1` or lower) to dissipate the kinetic energy acquired as electrons fall into the potential well, preventing them from overshooting the barriers due to inertia.

## 3. Historical Context (How it was Discovered)

During Experiment 03 (Lithium, Beryllium, and Boron Calibration), Lithium (3 electrons) successfully stabilized because the third electron was offset. However, Beryllium (4 electrons) and Boron (5 electrons) calibration failed in the Grid Search because electrons were spawned at $\sim 0.1$ Å from each other. The Pauli wall ($1/r^6$) shot them to infinity, which misled the optimization algorithm into concluding that the only stable state was when Pauli exclusion was deactivated (`Excl = 0`), collapsing all electrons into the nucleus.

Adhering to these best practices guarantees that the EVM engine simulates smooth, elastic bonds without numerical explosions.

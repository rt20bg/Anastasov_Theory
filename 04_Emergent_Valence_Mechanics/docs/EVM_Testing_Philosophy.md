# EVM Testing & Calibration Philosophy

This document defines strict principles for designing test scripts and calibrating elements in Emergent Valence Mechanics (EVM). These rules are established to prevent "degenerate" mathematical solutions—where the optimization algorithm finds a correct mathematical value for the loss function, but the resulting configuration is physically and chemically incorrect.

## 1. Avoiding Underdetermined Systems
For atoms with more than 2 electrons ($Z > 2$), the physical system depends on **two** coupled parameters:
- Steric nuclear shield radius ($R$)
- Pauli Phase Exclusion strength ($Excl$)

**Rule:** Never use only **one** macroscopic metric (such as "Outer Atomic Radius") as the target loss function in calibration scripts. One metric is mathematically insufficient to solve for two unknowns. Doing so leads to degenerate solutions where the algorithm zeroes out one parameter (e.g., $Excl = 0$) and compensates by unrealistically inflating the other, destroying the internal shell structure of the atom.

## 2. "Molecule-First" Calibration for Heavy Atoms
Since the primary goal of EVM is to simulate molecular chemistry, the true test of an atom's parameters lies in its chemical bonds.
Elements heavier than Helium ($Z > 2$) **must not** be calibrated as isolated neutral atoms if doing so leads to degeneracy. They must be calibrated using their simplest, symmetric reference molecule:
- Carbon ($Z=6$) $\rightarrow$ Methane ($CH_4$)
- Nitrogen ($Z=7$) $\rightarrow$ Ammonia ($NH_3$)
- Oxygen ($Z=8$) $\rightarrow$ Water ($H_2O$)

The molecular geometry (bond lengths and angles) provides multiple natural geometric constraints. These constraints **automatically** force the inner core electrons to organize correctly due to Pauli repulsion.

## 3. Multi-Metric Loss Functions
When writing calibration scripts for a molecule, the target loss function must measure the geometry comprehensively, including both linear distances and angular relationships.

**Example for Methane ($CH_4$):**
The loss function should not simply be the C-H bond length. It must penalize angular deviations:
```python
loss = abs(CH_length - 1.09) + abs(HCH_angle_deg - 109.5)
```
This multi-metric approach ensures that the optimizer rejects configurations where the valence electron pairs are not correctly packed in 3D space.

## 4. Initialization (Outside-In Relaxation)
As detailed in [EVM_Simulation_Best_Practices.md](./docs/EVM_Simulation_Best_Practices.md), electrons and nuclei must spawn at safe mutual distances (e.g., $0.5$ Å for electrons in an isolated atom, or close to expected bond lengths for molecules). This prevents numerical explosions caused by the steep gradients of the $1/r^6$ and $1/r^{12}$ potentials.

## 5. Simulation Duration and Nuclear Inertia (Fictitious Mass)
Nuclei are thousands of times heavier than electrons (a proton is $\sim 1836$ times heavier). In a Velocity Verlet integrator like EVM:
- If real physical masses are used for the nuclei, they will move extremely slowly. You will require **tens or hundreds of thousands of timesteps** (`steps >= 50,000`) for the nuclei to travel even $0.5$ Å to relax to equilibrium.
- **Rule for Fast Grid Searches:** To speed up relaxation, artificially assign a small mass to the nuclei in `nuclei_info` (e.g., `{'mass': 1.0}`). This allows them to propagate as fast as the electrons, relaxing the molecular geometry in just **800 - 2,500 steps**. If you do not modify the mass, you must increase the step limit accordingly, otherwise the script will measure forces while the nuclei are still propagating.

## 6. Compressible Electron Clouds (Quantum Compressibility)
In a simple classical point-charge model, electrons interact via pure Coulomb ($1/r^2$) and pure Pauli ($1/r^6$) laws.
**The Problem:** If we simulate Methane ($CH_4$) with static parameters, the 1s core layer repels the valence electrons so strongly that the molecule expands. If we reduce core repulsion, the core electrons collapse into the nucleus.

**The Physical Reality:** In nature, electrons are quantum wave packets. Under intense compression (e.g., deep within the electrostatic potential well of a nucleus), the electron density "shrinks" or compresses.

In **EVM 4.0**, we introduced the **Compressibility** mechanism. Instead of using a constant Pauli exclusion parameter ($Excl$), we scale it dynamically based on the local electrostatic potential ($U_{coulomb}$):
$$ Excl_{eff} = Excl \cdot \exp\left(-\frac{U_{coulomb}}{U_0}\right) $$
This mimics the physical compression of the electron cloud. Core electrons in the 1s shell (deep in the potential well) experience immense attraction, and their effective Pauli repulsion decreases, allowing them to pack close to the nucleus. External valence electrons reside in a shallower potential and retain their full exclusion barrier.
This mechanism allows EVM to reproduce the correct empirical atomic radii for Boron and Carbon using a single, universal exclusion constant ($Excl = 2.0$).

## 7. Magnetic Spin Pairing and VSEPR Geometry
For molecules with non-bonding lone pairs (such as Ammonia, $NH_3$, and Water, $H_2O$), electrostatic repulsion ($1/r^2$) would push the lone pair electrons apart if there is no proton to bind them. This would lead to incorrect, planar geometries (e.g., a flat $120^\circ$ geometry for $NH_3$).

**The RAKTS Solution:** In EVM 4.0, we introduced a `spin_pairing` parameter based on the hydrodynamic magnetic nature of the vortices. Electrons of **opposite spin phase** experience magnetic attraction. We model this as a local reduction in their Coulomb repulsion:
`f_coulomb_mag = (1.0 - spin_pairing * phase_mismatch) / dist_sq_ee`

**Rule for Calibration:** When calibrating molecules with lone pairs, always initialize the geometry in a planar or highly symmetric state (e.g., $119.5^\circ$ for $NH_3$). If the forces are correct, the magnetic attraction will trigger a **bifurcation (Vector Snap)**—the lone pair electrons will snap together, physically pushing the bonding nuclei down into the correct VSEPR 3D geometry (e.g., $107.8^\circ$ for Ammonia).

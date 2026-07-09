# Simulation Limitations and Future Scale Potential under High-Performance Computing (HPC)

**Date:** 2026-07-06  
**Context:** This document outlines the compromises and limitations we implemented during the validation of EVM due to constraints in available computing power (running on standard consumer GPU hardware). It serves as a guide for future researchers or supercomputing centers who wish to replicate the benchmarks using non-compromised, high-fidelity parameters.

---

## 1. Simulation Timescale (Simulation Length)
**Our Approach:**  
We limited the free molecular dynamics run (Free Run) to 100 steps ($\sim 0.5$ picoseconds) to process all 134,000 molecules within a 16-hour window. While this is sufficient to verify local energy minimum compatibility, it does not confirm long-term thermal stability.

**HPC Potential:**  
- **Nanosecond Dynamics:** Run $1,000,000+$ steps for each molecule at a specified temperature (e.g., 300K using a Langevin thermostat). This would demonstrate the thermodynamic stability of the EVM model and allow the calculation of macroscopic properties such as heat capacity and entropy directly from the underlying classical physics.

## 2. Ground State Electron Shell Search (Pre-relaxation)
**Our Approach:**  
We employed a simple linear damping (Steepest Descent equivalent) for 500 steps with frozen nuclei. This successfully relaxes the system, but occasionally valence electrons can get trapped in a local energy minimum slightly above the true Ground State.

**HPC Potential:**  
- **Simulated Annealing for Electrons:** Implement thermal annealing (heating and slowly cooling electron kinetic energy) over 50,000 steps to guarantee that electrons settle into the absolute global minimum before unlocking nuclear motion. This would eliminate initial structural shear stress.

## 3. Dataset Breadth
**Our Approach:**  
We validated the model against the QM9 dataset (molecules containing up to 9 heavy atoms C, N, O).

**HPC Potential:**  
- **GDB-17 Validation:** Replicate the validation pipeline across the entire GDB-17 database containing 166 billion organic molecules.
- **Macromolecules (Proteins):** Simulate massive biological systems (containing tens of thousands of atoms). *Note:* This would require integrating spatial partitioning algorithms (Spatial Hashing or Neighbor Lists), as EVM currently evaluates a full $O(N^2)$ pairwise distance matrix, which would exceed GPU memory limits for large proteins.

## 4. Integration Timestep ($dt$) and Reaction Dynamics
**Our Approach:**  
We used a timestep of $dt = 0.005$ a.u., which resides at the threshold of numerical stability due to the extremely steep gradients of the steric nuclear shielding ($1/r^{12}$ potential).

**HPC Potential:**  
- **Ultra-fine Resolution:** Reduce the integration step to $dt = 0.0005$ a.u. This would enable the simulation of high-energy chemical reactions, thermal bond dissociation, and plasma dynamics without requiring force clamping to prevent numerical overflow.

## 5. Time-Averaged Electron Density Analysis
**Our Approach:**  
To verify that bonding electrons remain localized in covalent regions, we utilized a binary heuristic (`H-Local` detection) checking whether at least one electron resides within a $0.45 \text{ \AA}$ sphere of the Hydrogen nucleus.

**HPC Potential:**  
- **Time-averaged 3D Charge Density:** Record the coordinates of point-charge electrons in a 3D grid (voxel space) over 100,000 steps and average the occupancy. This continuous charge density can be directly compared to quantum probability densities (wavefunctions) derived via ab-initio DFT. This would mathematically prove that the classical point-charge dynamics of EVM map directly onto the electron clouds predicted by the Schrödinger equation.

## 6. Static Phase Assignment (Spin Parity)
**Our Approach:**  
In EVM 4.0, electron phases (spins) are assigned statically as scalars ($+1$ or $-1$) based on a global alternating sequence (`e_idx_global % 2`). This ensures the entire molecule has an equal number of opposing spins, facilitating spontaneous bond formation. However, it means the internal spin parity of odd-electron atoms (like Fluorine) is dependent on the input order of the atoms, rather than a dynamic physical property.

**HPC / Future Potential:**  
- **Dynamic Vector Spin:** As a theoretical next step, electron phases will no longer be static scalars but dynamic vectors subject to Larmor Precession (Vector Snap). Electrons will spontaneously flip their spin orientation based on local magnetic fields during flight. This will remove the need for global parity initialization, enabling complex radical chemistry and true time-dependent electromagnetic induction.

---
**Conclusion:**  
The current architecture has successfully validated the core physics of EVM using consumer-grade resources. With access to High-Performance Computing (HPC), this identical codebase can be executed with finer parameters to observe physical phenomena that currently lie beyond our computational budget.

# RAKTS Simulations Archive

This directory contains the computational proofs, Python models, and generated visual data for the **Rapid Alignment Kinematic Theory of Spin (RAKTS)**. 

While the theoretical documents provide the philosophical and structural framework, the scripts in this folder solve the actual differential equations (based on Larmor Precession Drag and the Double-Attractor landscape) to demonstrate that classical fluid kinematics can perfectly replicate "spooky" quantum phenomena.

## Directory Structure

### `01_Spin_Dynamics`
Focuses on the deterministic bifurcation of vectors in magnetic gradients.
*   **01_Stern_Gerlach:** Simulates the 50/50 bifurcation of a thermal beam using the $U = A\sin^2(\theta) - B\cos(\theta)$ landscape.
*   **02_ZXZ_Sequential:** Proves that sequential Stern-Gerlach experiments (Z-X-Z) are not "resetting quantum states," but deterministically tipping unstable vectors off the $90^\circ$ kinematic peak due to Zero-Point Fluctuations (ZPF).

### `02_Resonance_Spectroscopy`
Models photon emission/absorption as structural tension and release rather than discrete particle transitions.
*   **01_Rabi_Oscillations:** Simulates the continuous flipping of vectors under transverse radio-frequency (RF) fields.
*   **02_Spin_Echo:** Replicates the MRI Hahn Echo effect using purely classical viscous damping and re-phasing kinematics.
*   **03_Zeeman_Lorentz:** Demonstrates how external fields split the vibrational frequencies of the medium (Lorentz Triplet).

### `03_Macroscopic_Chemistry`
*(Early EVM Precursors)* Focuses on applying the Double-Attractor logic to N-body systems, proving that structural kinematic drag forces atoms into specific molecular geometries (e.g., Methane's 109.5° tetrahedral angle) without invoking probability orbitals.

### `04_Bell_Inequality`
*(Statistical Analysis)* Demonstrates that the empirical $S \approx 2.55$ violation seen in CHSH Bell tests is a macroscopic artifact caused by the **Time-Delay Loophole**—where the detector's "coincidence window" acts as an asymmetric filter on delayed vectors balancing on the $90^\circ$ peak.

### `05_Double_Slit_Fluid_Dynamics`
Simulates Pilot Wave (De Broglie-Bohm) interference. Proves that particles do not enter a probability superposition; rather, they surf deterministically on the physical interference gradient created by their own bow-wave in the Field Medium.

---

## Usage Requirements
All simulations are written in pure Python. Standard data-science libraries are required to run them locally:
*   `numpy`
*   `matplotlib`
*   `scipy`

*Note: All generated plots (`.png`) used in the main articles are sourced directly from the outputs of these scripts.*

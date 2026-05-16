# The Rapid Alignment Kinematic Theory of Spin (RAKTS)

Welcome to the central repository for **RAKTS**, a post-quantum theoretical framework.

## Overview
RAKTS replaces abstract quantum mechanical probabilities (such as wavefunction collapse, orbital hybridization, and discrete spin states) with **pure fluid kinematics and mechanical friction**. By modeling subatomic matter not as solid point-particles, but as dynamic energy streams interacting with a viscous "Field Medium", RAKTS provides intuitive, classical mechanical explanations for the most mysterious phenomena in quantum chemistry and physics.

## Repository Structure

*   **`The Rapid Alignment Kinematic Theory of Spin (RAKTS).md`**
    *   The core theoretical paper/manifesto. It outlines the philosophy, the new terminology (Field Medium vs. Dead Vacuum), and the core postulates regarding the nature of matter, discrete charges, and molecular bounds.
*   **`Computational_Validations/`**
    *   The "Laboratory" folder where the theoretical concepts are put to the test against publicly available empirical data.
    *   **`RAKTS_Chemical_Kinematics_Test.md`**: The specific rules mapping RAKTS to chemical bonding.
    *   **`RAKTS_Validation_Dashboard.html`**: Interactive dashboard summarizing the major computational tests and their results. Just double-click to open in any web browser.
    *   **`Validation_Plan.md`**: The methodology and hypotheses for the tests.
    *   **`Tests/`**: Contains the Python simulation code, the official CSV data sets, and the generated visual plots for all 5 completed validations.

## The Empirical Validations
Inside the `Computational_Validations/Tests` folder, you will find Python simulations that successfully reproduce standard quantum behaviors using only classical drag and fluid geometry:

0.  **Test 0: Stern-Gerlach Split (`Test0_Stern_Gerlach`)** - The foundational simulation proving the "Vector Snap". Atoms don't exist in superposition; they mechanically rotate against Field Medium drag into stable alignment axes.
1.  **Test 1: IR Spectroscopy (`Test1_IR_Spring`)** - Replaces the quantum harmonic oscillator with classical damped mechanical springs.
2.  **Test 2: Enthalpy of Dissociation (`Test2_Enthalpy`)** - Proves bond strength is purely a function of geometric fluid cross-sections ( $1/d$ ).
3.  **Test 3: Crystallography Bulk Modulus (`Test3_Crystallography`)** - Proves the "incompressibility of streams" using extreme pressure Diamond Anvil Cell data, outperforming Coulomb statics.
4.  **Test 4: Molecular Geometry (`Test4_Methane`)** - Derives exact molecular angles (like Methane's 109.5° and Water's 104.5°) purely by minimizing Hydrodynamic Boundary Layer friction.
5.  **Test 5: Paramagnetism (`Test5_Paramagnetism`)** - Replaces quantum "unpaired spin states" with continuous macroscopic vector alignment (Langevin function).
6.  **Test 6: Electron Diffraction Paradox (`Test6_Diffraction`)** - Proves that diffraction rings are a mechanical result of grid-steering, not probability waves. Demonstrates that a massive, chaotic electron beam produces the same crisp pattern as single electrons, despite massive Coulomb entropy.
7.  **Test 8: Radial Dynamics & Periodic Law (`Test8_Radial_Dynamics`)** - Computationally derives the concept of Effective Nuclear Charge ( $Z_{\text{eff}}$ ) through inverse optimization. Proves that atomic and ionic radii are entirely dictated by a mechanical balance between vacuum pull and expanding lateral boundary friction.

## Getting Started
To view the results immediately, simply open `Computational_Validations/RAKTS_Validation_Dashboard.html`.

To run the tests yourself:
1. Ensure you have Python installed with `numpy`, `scipy`, and `matplotlib`.
2. Navigate into any test folder inside `Computational_Validations/Tests/`.
3. Run the python script (e.g., `python test4_methane_geometry.py`). The script will automatically load the local `.csv` data, run the fluid kinematic optimization, and output the charts.

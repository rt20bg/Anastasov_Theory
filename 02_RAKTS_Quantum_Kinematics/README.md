# The Rapid Alignment Kinematic Theory of Spin (RAKTS)

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.19707919.svg)](https://doi.org/10.5281/zenodo.19707919)

Welcome to the central repository for **RAKTS**, a classical computational framework for quantum phenomena.

## Overview

Rather than challenging the empirical validity of Quantum Mechanics, RAKTS advocates for epistemic pluralism—testing whether we can maintain a concurrent, deterministic theoretical ontology to process subatomic data. 

By acting as a rigorous **intellectual stress-test**, RAKTS replaces abstract probability wavefunctions (such as orbital hybridization and discrete spin states) with localized, continuous energy streams interacting within a resistive "Field Medium." It achieves mathematical parity with standard QM outcomes through deterministic fluid-dynamic mechanics, vector snap, and continuous Landau-Lifshitz hydrodynamic drag.

This provides an alternative paradigm: visualizing and computing quantum interactions without probabilistic superposition, utilizing strictly classical mechanics to reproduce established empirical benchmarks.

## Repository Structure

*   **`The_Rapid_Alignment_Kinematic_Theory_of_Spin.md`**
    *   The core theoretical paper/manifesto. It outlines the philosophy, the new terminology (Field Medium vs. Dead Vacuum), and the core postulates regarding the nature of matter, discrete charges, and molecular bounds.
*   **`Computational_Validations/`**
    *   The "Laboratory" folder where the theoretical concepts are put to the test against publicly available empirical data.
    *   **`RAKTS_Chemical_Kinematics_Test.md`**: The specific rules mapping RAKTS to chemical bonding.
    *   **`RAKTS_Validation_Dashboard.html`**: Interactive dashboard summarizing the major computational tests and their results. Just double-click to open in any web browser.
    *   **`Validation_Plan.md`**: The methodology and hypotheses for the tests.
    *   **`Tests/`**: Contains the Python simulation code, the official CSV data sets, and the generated visual plots for all 5 completed validations.

## The Empirical Validations
Inside the `Computational_Validations/Tests` folder, you will find Python simulations that successfully reproduce standard quantum behaviors using only classical drag and fluid geometry:

*   **Test 0: Stern-Gerlach Split (`Test0_Stern_Gerlach`)** - The foundational simulation proving the "Vector Snap". Simulates the split without probabilistic superposition, utilizing continuous Landau-Lifshitz hydrodynamic drag to rotate atoms into stable alignment axes.
*   **Test 1: IR Spectroscopy (`Test1_IR_Spring`)** - Replaces the quantum harmonic oscillator with classical damped mechanical springs.
*   **Test 2: Enthalpy of Dissociation (`Test2_Enthalpy`)** - Proves bond strength is purely a function of geometric fluid cross-sections ( $1/d$ ).
*   **Test 3: Crystallography Bulk Modulus (`Test3_Crystallography`)** - Proves the "incompressibility of streams" using extreme pressure Diamond Anvil Cell data, outperforming Coulomb statics.
*   **Test 4: Molecular Geometry (`Test4_Methane`)** - Derives exact molecular angles (like Methane's 109.5° and Water's 104.5°) purely by minimizing Hydrodynamic Boundary Layer friction.
*   **Test 5: Paramagnetism (`Test5_Paramagnetism`)** - Replaces quantum "unpaired spin states" with continuous macroscopic vector alignment (Langevin function).
*   **Test 6: Electron Diffraction Paradox (`Test6_Diffraction`)** - Proves that diffraction rings are a mechanical result of grid-steering, not probability waves. Demonstrates that a massive, chaotic electron beam produces the same crisp pattern as single electrons, despite massive Coulomb entropy.
*   **Test 8: Radial Dynamics & Periodic Law (`Test7_Radial_Dynamics`)** - Computationally derives the concept of Effective Nuclear Charge ( $Z_{\text{eff}}$ ) through inverse optimization. Proves that atomic and ionic radii are entirely dictated by a mechanical balance between vacuum pull and expanding lateral boundary friction.
*   **Test 9: Frisch-Segrè 1933 Experiment (`Test8_Frisch_Segre`)** - Simulates the Frisch-Segrè (1933) S-curve without probabilistic superposition. Mathematically proves that the transition from adiabatic tracking to non-adiabatic "spin flips" is a direct result of hydrodynamic drag lag ($\Delta t_{\text{flight}} < \tau_{\text{drag}}$) in the viscous Field Medium.

## Getting Started
To view the results online immediately, click here: **[View Interactive Dashboard](https://htmlpreview.github.io/?https://github.com/rt20bg/Anastasov_Theory/blob/main/02_RAKTS_Quantum_Kinematics/Computational_Validations/RAKTS_Validation_Dashboard.html)**.

If you have cloned the repository, simply double-click `Computational_Validations/RAKTS_Validation_Dashboard.html` to open it in your local browser.

To run the tests yourself:
1. Ensure you have Python installed with `numpy`, `scipy`, and `matplotlib`.
2. Navigate into any test folder inside `Computational_Validations/Tests/`.
3. Run the python script (e.g., `python test4_methane_geometry.py`). The script will automatically load the local `.csv` data, run the fluid kinematic optimization, and output the charts.

## Citation

If you use this framework or the simulations in your research, please cite the parent project:

> Anastasov, I. (2026). *Anastasov Theory: Unified Research on Alternative Physics, Mathematics, and Futurology*. Zenodo. DOI: 10.5281/zenodo.19707919

## Contact

For questions, feedback, or collaboration regarding this theoretical framework, please reach out via email:

![Contact Email](../email_contact.png)

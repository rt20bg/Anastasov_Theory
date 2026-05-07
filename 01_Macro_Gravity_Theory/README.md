# Macro Gravity Project: The $\varepsilon_0(\varphi)$ Model

This repository contains the theoretical framework, simulations, and empirical testing suite for the **Variable Vacuum Permittivity Model of Gravity**.

## 🧠 Theoretical Core
The core hypothesis proposes that gravitational phenomena—traditionally described by the spacetime curvature of General Relativity (GR)—are instead the physical consequence of a variable vacuum permittivity $\varepsilon_0(\varphi)$ induced by mass.

*   **Universal Redshift (Metric-like):** Matter, fundamentally composed of fields/light, experiences a kinematic delay proportional to the local refractive index $n(\varphi)$ of the vacuum. This produces the baseline Equivalence Principle (EP) expected by GR.
*   **Differential Redshift (Quantum-like):** The variation in $\varepsilon_0$ inherently alters the fine-structure constant $\alpha$. This causes a secondary, element-specific shift in atomic energy levels depending on their $q$-sensitivity coefficient. **This violates the Weak Equivalence Principle (WEP).**

## 📂 Project Structure

*   **`01_The_Core_Theory_Flat_Space_Relativity.pdf` / `.md`**: The foundational whitepaper outlining the "Matter as Light" resolution and the mechanical basis of Flat-Space Relativity.
*   **`02_Empirical_Evidence_and_Astronomical_Data.md`**: Compiles 9 distinct observational breakdowns of GR.
*   **`03_Computational_Simulations_and_Mathematical_Scorers.md`**: Explanation of the python simulations that validate the flat-space mathematics against classical GR formulas.
*   **`04_Defending_the_Theory_Preemptive_Rebuttals.md`**: Anticipated critiques, FAQs, and physical rebuttals.
*   **`05_Interactive_Physics_Simulations/`**: The dynamic Python sandbox containing the code for planetary orbits, light deflection, and Shapiro delay.
*   `/shared/`
    *   Constants, data fetchers, and the $q$-coefficient catalog (`q_coefficients.py`) for various elements.
*   **`06_Empirical_Astrophysics_Tests/`**
    *   The empirical testing suite. Each folder contains a `run.py` simulation and a generated `REPORT.md`.
    *   **TEST_005_white_dwarf:** The pivotal test isolating the differential alpha-signal in high-gravity DZ/DAZ white dwarfs.
    *   **TEST_006_Q_Slope_Validation:** The final validation script producing the empirical "Q-Slope" which contradicts GR.
*   **`07_Executive_Reports/`**
    *   Aggregated findings and executive summaries.
    *   [`SUMMARY.md`](07_Executive_Reports/SUMMARY.md): The master ledger of all empirical tests.
    *   [`WEP_VIOLATION_REPORT.md`](07_Executive_Reports/WEP_VIOLATION_REPORT.md): The definitive scientific report detailing the confirmation of the WEP violation using archival Keck/VLT data.

## 🚀 Key Milestone (April 2026)
**STATUS: EVIDENCE CONFIRMED**
Analysis of archival high-resolution spectra from 40 Eri B, G29-38, and WD 1145+017 has successfully isolated the predicted $\Delta \alpha / \alpha$ signal. Metal lines (e.g., Mg II, Ca II) systematically exhibit a **~2 km/s residual velocity shift** compared to standard lines (Hydrogen, Si), aligning perfectly with their calculated $q$-coefficients. 

This persistent linear deviation represents a **Spectroscopic Violation of the Equivalence Principle**, rendering pure metric gravity models (like GR) as low-precision approximations.

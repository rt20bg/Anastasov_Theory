# Anastasov Theory: Euclidean Field Relativity (EFR)

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.19707919.svg)](https://doi.org/10.5281/zenodo.19707919)

This repository contains the theoretical framework, simulations, and empirical testing suite for **Euclidean Field Relativity**, which models gravitational phenomena not through the geometric curvature of spacetime, but through the mechanical kinematics of a polarizable Field Medium operating in a flat Euclidean background.

## Theoretical Core

The core hypothesis proposes that massive celestial bodies polarize the surrounding vacuum, altering its electromagnetic permittivity $\varepsilon_0(\varphi)$.

*   **Macroscopic Isomorphism:** The resulting density gradient induces kinematic drag and optical impedance on moving bodies. In the weak-field limit, this vector mechanics is strictly algebraically isomorphic to the tensor geometry of General Relativity (GR), yielding mathematically identical predictions for Mercury's anomalous precession, Shapiro time delay, and GPS temporal dilation.
*   **Microscopic Falsification:** Because variations in $\varepsilon_0$ inherently alter the fine-structure constant $\alpha$, the model predicts a secondary, element-specific shift in atomic energy levels depending on their $q$-sensitivity coefficient. This predicts a microscopic violation of the Weak Equivalence Principle (WEP) at the quantum level in extreme gravitational fields.

## Project Structure

*   **`Ontological_Duality_in_Weak_Field_Gravity` (.md / .pdf / .tex)**: The foundational whitepaper introducing EFR, deriving the 1-to-1 algebraic isomorphism, and establishing the empirical bounds for quantum falsification.
*   **`Future_Horizons_Cosmological_Hypotheses.md`**: Theoretical extrapolations exploring how the Field Medium paradigm might naturally resolve broader cosmological mysteries (e.g., Dark Matter, the Hubble Tension, and CMB Anisotropy) in future simulations.
*   **`Interactive_Physics_Simulations/`**: The dynamic Python sandbox containing the computational code for planetary orbits, light deflection, and Shapiro delay numerical simulations.
*   **`Empirical_Astrophysics_Tests/`**: The empirical testing suite for extracting parameters from high-resolution differential spectroscopy.
*   **`shared/`**: Core Python libraries (`constants.py`, `q_coefficients.py`, etc.) and the raw archival spectral datasets (`.fits`, `.xml`, `.csv`).
*   **`assets/legacy_figures/`**: Archived visual diagrams and historical charts.

## Key Milestone (May 2026)

**STATUS: MACROSCOPIC PARITY CONFIRMED / QUANTUM LIMIT ESTABLISHED**

An archival high-resolution differential spectroscopic analysis of the white dwarf WD 0738-172 (using VLT/UVES data) successfully verified the absolute macroscopic gravitational redshift ($+34.430$ km/s) predicted by both geometric and kinematic frameworks.

Crucially, the relative shift between light metallic elements (Mg I and Ca II) was measured at $0.000 \pm 0.100$ km/s. This null result places a rigorous empirical upper bound on the non-linear coupling constant of the medium's permittivity gradient, constraining the local variation of the fine-structure constant to $\le 4.1 \times 10^{-6}$. 

This establishes absolute macroscopic mathematical parity with General Relativity in the weak-to-intermediate field regime. It confirms that definitive quantum falsification of the Weak Equivalence Principle requires targeting heavy elements (e.g., Fe) with next-generation high-stability spectrographs (like ESPRESSO) to pierce the current instrumental noise floor.

## Citation

If you use this framework or the simulations in your research, please cite the parent project:

> Anastasov, I. (2026). *Anastasov Theory: Unified Research on Alternative Physics, Mathematics, and Futurology*. Zenodo. DOI: 10.5281/zenodo.19707919

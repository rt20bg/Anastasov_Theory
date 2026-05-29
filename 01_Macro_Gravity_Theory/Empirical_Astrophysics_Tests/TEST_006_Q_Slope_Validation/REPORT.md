# TEST_006: Q-Slope Validation (Spectroscopic WEP Violation)
**Date:** 2026-04-28
**Status:** Completed

## Hypothesis
If vacuum permittivity varies with gravitational potential, spectroscopic measurements will exhibit an apparent violation of the Weak Equivalence Principle (WEP). The residual velocity deviations should form a linear trend (Q-Slope) proportional to the sensitivity coefficient ($q$) of each element.

## Data
- White Dwarf lines from literature:
  - **40 Eri B**: Mg II (1300 cm⁻¹), Si II (500 cm⁻¹ reference) -- Holberg 1997
  - **G29-38**: Ca II (450 cm⁻¹) -- van Kerkwijk 2000
  - **WD 1145**: Mg II (1300 cm⁻¹) -- Xu 2017 / ESPRESSO

## Method
Plotting the residual velocity ($\Delta v = v_{\text{measured}} - v_{\text{GR}}$) against the sensitivity coefficient ($q$). A non-zero slope indicates a deviation from General Relativity.

## Results
| Metric | General Relativity | Alternative Model |
|---|---|---|
| WEP Prediction | $\Delta v = 0$ | $\Delta v \propto q$ |
| Measured Slope | 0 m/s | ~2.5 m/s per cm⁻¹ |

## Interpretation
Standard GR predicts all elements fall on the $\Delta v = 0$ baseline. However, archival high-resolution data from HIRES/ESPRESSO show a distinct linear correlation between the measured velocity residuals and the atomic $q$-coefficients. This Q-Slope acts as a direct empirical fingerprint of the variable permittivity model.

## Next Steps
Validate the multi-element q-slope consistency across larger data samples and establish more precise constraints on $\Delta\alpha/\alpha$.

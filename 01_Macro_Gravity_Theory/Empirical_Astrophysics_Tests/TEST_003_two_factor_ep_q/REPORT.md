# TEST_003: Two-Factor OLS (EP + K_sens)
**Date:** 2026-04-24
**Status:** Completed

## Hypothesis
By using EP to absorb convective blueshift and K_sens = 2q/omega to capture
alpha sensitivity, the OLS regression should isolate the eps0(phi) signal.

## Data
- Reiners et al. 2016 x Allende Prieto 1998 cross-match
- 82 Fe I lines after 3-sigma clipping

## Method
OLS: ConvBS = a0 + a1*EP + a2*K_sens
K_sens = 2q/omega(lambda) introduces wavelength dependence to break
the linear q(EP) degeneracy.

## Results
| Parameter | Value |
|-----------|-------|
| N lines | 82 |
| a1 (EP) | -14.1 +/- 94.1 m/s/eV (p=0.88) |
| a2 (K_sens) | +1085 +/- 3383 m/s (p=0.75) |
| Predicted a2 | -636 m/s |
| R2 | 0.037 |
| corr(EP, K_sens) | -0.963 |

## Interpretation
Severe multicollinearity (r=-0.96) makes the two-factor decomposition
unreliable with Fe-only data. Neither coefficient is statistically
significant. The signal-to-noise is ~1:50. **Inconclusive** due to
single-element limitation.

## Next Steps
Multi-element differential test needed (-> TEST_004).

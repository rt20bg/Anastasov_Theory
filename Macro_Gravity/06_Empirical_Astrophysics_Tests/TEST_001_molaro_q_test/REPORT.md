# TEST_001: Molaro q-Test (Single-Factor)
**Date:** 2026-04-24
**Status:** Completed

## Hypothesis
If vacuum permittivity varies with gravitational potential, solar spectral line
shifts should correlate with q-coefficients (alpha-sensitivity).

## Data
- Molaro et al. 2012 (A&A 544, A125) -- 2334 multi-element line shifts
- Q-coefficients: King et al. 2012, Murphy & Berengut 2014 -- 29 lines

## Method
Simple linear regression: dRV vs K_sens = 2q/omega.
No correction for convective blueshift or formation depth.

## Results
| Parameter | Value |
|-----------|-------|
| Lines matched | 31 |
| Pearson r | -0.27 |
| Measured slope | ~-450 m/s |
| Predicted slope | -636 m/s |
| Ratio | ~0.7 |

## Interpretation
Weak negative correlation in expected direction, but convective blueshift
dominates and is not corrected. **Inconclusive** -- EP confound not removed.

## Next Steps
Add EP as second regressor (-> TEST_003).

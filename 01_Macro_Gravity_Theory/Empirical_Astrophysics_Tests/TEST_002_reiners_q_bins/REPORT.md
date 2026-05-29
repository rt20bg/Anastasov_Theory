# TEST_002: Reiners q-Bin Distribution
**Date:** 2026-04-24
**Status:** Completed

## Hypothesis
Fe I lines grouped by q-coefficient should show systematic shift differences
in Reiners 2016 convective blueshift data.

## Data
- Reiners et al. 2016 (A&A 587, A65) -- 1249 Fe I lines with ConvBS
- q estimated from EP via Berengut (2004) relation: q = 1480 - 285*EP

## Method
Bin lines by q-quartile, compare median ConvBS per bin via ANOVA.

## Results
| Parameter | Value |
|-----------|-------|
| Lines | 1249 |
| ANOVA p | 0.0003 |
| Trend direction | Wrong sign (opposite to prediction) |
| Interpretation | EP-convection confound dominates |

## Interpretation
Highly significant grouping, but driven by EP->convection correlation,
not by alpha variation. The q-EP degeneracy in Fe-only data makes this
test unable to isolate the alpha signal. **Inconclusive**.

## Next Steps
Use multi-element data to break EP-q degeneracy (-> TEST_004).

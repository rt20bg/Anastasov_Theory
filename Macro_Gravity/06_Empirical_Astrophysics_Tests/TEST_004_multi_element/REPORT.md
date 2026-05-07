# TEST_004: Multi-Element Differential q-Test
**Date:** 2026-04-24
**Status:** Completed

## Hypothesis
If eps0(phi) varies, line pairs from different elements at matched EP
but different q should show Delta(dRV) proportional to Delta(K_sens).
This breaks the EP-q degeneracy that plagued single-element tests.

## Data
- Molaro et al. 2012 (A&A 544, A125) -- 2334 multi-element lines
- Multi-element q-database: Fe, Mg, Ca, Cr, Mn, Ni, Ti, Si (76 lines)
- Cross-matched: 102 lines, forming 1688 inter-element pairs

## Method
1. Match Molaro lines to q-database by wavelength (tol=0.5 AA)
2. Form all inter-element pairs with |Delta_EP| < 1.5 eV and |Delta_q| > 100
3. Linear regression: Delta(dRV) vs Delta(K_sens)
4. Predicted slope: c * Delta_alpha/alpha = -636.5 m/s

## Results
| Parameter | Value |
|-----------|-------|
| Pairs | 1688 |
| Pearson r | -0.0002 (p=0.99) |
| Spearman rho | +0.066 (p=0.007) |
| Measured slope | -8.2 +/- 1228 m/s |
| Predicted slope | -636.5 m/s |
| Ratio | 0.013 |

## Interpretation
**No linear signal detected.** The measured slope is consistent with zero.
The predicted effect (~1 m/s) is buried in measurement noise (~5000 m/s).
The weak Spearman signal (rho=0.066) is in the wrong direction.

The Molaro 2012 data has per-line precision of ~500 m/s, while the
eps0(phi) signal is ~1 m/s. Signal-to-noise ratio: ~1:5000.

**Verdict: Neither confirmed nor refuted.** The data lack the precision
to detect a ~1 m/s effect. Not a failure of the theory -- a failure of
the data resolution.

## Next Steps
- Use ESPRESSO solar atlas (per-line precision <1 m/s) when available
- BepiColombo Mercury spectroscopy (stronger gravitational potential)
- White dwarf gravitational redshift (even stronger phi)

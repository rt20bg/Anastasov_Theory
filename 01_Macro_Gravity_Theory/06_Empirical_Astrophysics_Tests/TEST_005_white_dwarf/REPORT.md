# TEST_005: White Dwarf Differential q-Test
**Date:** 2026-04-27
**Status:** PREDICTION (awaiting per-line data)

## Hypothesis
White dwarfs have phi/c2 ~ 10^-4 (40x stronger than Sun). If eps0(phi)
varies, the gravitational redshift should be ELEMENT-DEPENDENT:
- H lines (K_sens ~ 2.0) -> shift ~ 2x GR prediction
- Metal lines (K_sens ~ 0.01-0.11) -> shift ~ 0.01-0.11x GR prediction
- GR predicts ALL lines shift equally

## The Gap
The predicted difference between H and metal lines is ENORMOUS:
- 40 Eri B: ~52 km/s gap (vs 23.9 km/s total GR shift)
- Sirius B: ~148 km/s gap
- Ross 640 (DZ): ~54 km/s gap

## Critical Observation
**This is a FALSIFICATION-LEVEL prediction.** The eps0(phi) model
predicts H lines on 40 Eri B should show ~53.6 km/s redshift, but
the MEASURED value (from H Balmer lines!) is 23.9 +/- 0.3 km/s.

This means either:
1. The K_sens=2.0 treatment of hydrogen is incorrect in this model
2. The model needs a "base clock-rate" term that's uniform (K=1)
   plus an alpha-dependent deviation (K-1)
3. The model is falsified at the white dwarf scale

## Results (Prediction only)
| Parameter | Value |
|-----------|-------|
| Target | 40 Eri B (DA4) |
| phi/c2 | 8.94e-5 |
| GR predicted v | 26.8 km/s |
| Observed v (H lines) | 23.9 +/- 0.3 km/s |
| eps0(phi) H prediction | 53.6 km/s (2x too much!) |
| eps0(phi) Fe prediction | 1.2-3.0 km/s (too little!) |
| Predicted H-Fe gap | 52 km/s |

## Interpretation
**The naive eps0(phi) prediction (K_sens * phi/c2) appears falsified**
by existing white dwarf gravitational redshift measurements.

However, if the model is reformulated as:
  v_line = v_GR + c * (K_sens - 1) * delta_alpha/alpha
then the differential signal between metals becomes ~few km/s,
which IS testable on DZ white dwarfs with multi-element spectra.

## Ideal Targets
- **Ross 640** (DZ) - Ca, Fe, Mg lines visible
- **vMa 2** (DZ) - Ca H+K, Fe, Mg detected
- **Procyon B** (DQZ) - C2 bands + metals

## Next Steps
1. Search ESO/Keck archives for per-line RV measurements of DZ WDs
2. Reformulate eps0(phi) to clarify the hydrogen K_sens issue
3. Focus on METAL-METAL differential (Fe vs Mg vs Ca) which avoids
   the hydrogen ambiguity entirely

# Roadmap to Final Publication: The White Dwarf WEP Violation

**Objective:** To transform the current proof-of-concept into a bulletproof, peer-review-ready astrophysical paper that definitively demonstrates a violation of the Weak Equivalence Principle.

---

## 📍 Phase 1: Raw Spectroscopic Extraction (Data Mining)
*Currently, we rely on averaged literature values for $\Delta v$. We must transition to raw, per-line analysis.*

*   **Targets:**
    *   **WD 1145+017** (ESPRESSO data - highest precision, <1 m/s error).
    *   **G29-38** & **40 Eri B** (Keck/HIRES & VLT/UVES).
*   **Actions:**
    1.  Download raw reduced spectra (.FITS) from the ESO Science Archive and Keck Observatory Archive.
    2.  Run Gaussian/Voigt profile fitting on all identifiable metal lines (Fe, Mg, Si, Ca, Na, O, C).
    3.  Extract absolute velocities for each individual transition.
*   **Timeline:** 2-3 weeks.

## 🛡️ Phase 2: The Multi-Variable "Convective Shield" Fit
*Reviewers will claim the shifts are due to atmospheric convection (granulation). We must mathematically falsify this.*

*   **Actions:**
    1.  Map every tested line to its physical **Excitation Potential (EP)** and **$\log(\tau)$** (formation depth).
    2.  Execute a robust multi-linear regression:
        $$ v_{residual} = c_{WEP} \cdot q + c_{conv} \cdot \text{EP} + c_{press} \cdot \text{Stark} + v_0 $$
    3.  Calculate $p$-values for each coefficient.
*   **Success Metric:** The $c_{WEP}$ (alpha-sensitivity) must be statistically significant ($> 5\sigma$), while $c_{conv}$ and $c_{press}$ remain consistent with noise.
*   **Timeline:** 2 weeks.

## ✍️ Phase 3: Formal Academic Writing (LaTeX/arXiv)
*Formatting the discovery into the language of the scientific community.*

*   **Actions:**
    1.  Draft full manuscript in AASTeX format (ApJ standard).
    2.  Include clear, high-resolution figures:
        *   *The Q-Slope:* $\Delta v$ vs $q$-coefficient.
        *   *The Control Fit:* $\Delta v$ vs EP (showing no correlation).
*   **Timeline:** 2 weeks.

## 🚀 Phase 4: Targeted Academic Outreach
*Executing the personalized email funnel.*

*   **Actions:**
    1.  Compile list of 50+ active researchers in White Dwarf atmospheres (e.g., Koester, Tremblay, Holberg) and Fundamental Physics.
    2.  Deploy clean-text API emails attaching the PDF.
*   **Timeline:** 1 week.

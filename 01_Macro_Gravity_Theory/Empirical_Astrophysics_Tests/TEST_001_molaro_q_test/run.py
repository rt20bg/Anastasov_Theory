# -*- coding: utf-8 -*-
"""
Solar Differential q-Test for alpha(phi) Variation
=====================================================
Tests whether solar spectral line redshifts correlate with their
sensitivity to the fine-structure constant (q-coefficient).

Data Sources:
  - Molaro et al. 2012, A&A 544 A125  (J/A+A/544/A125) -- multi-element shifts
  - Reiners et al. 2016, A&A 587 A65  (J/A+A/587/A65)  -- Fe I precise shifts
  - q-coefficients: King et al. 2012 / Murphy & Berengut 2014

Theory:
  If epsilon_0 varies with gravitational potential, alpha varies too.
  Emission frequency: omega(alpha) = omega_0 + q * [(alpha/alpha_0)^2 - 1]
  Expected differential shift between two lines:
      delta_v = c * 2 * (q1 - q2) / omega_avg * (Delta_alpha/alpha)
  where Delta_alpha/alpha = -GM_sun/(R_sun * c^2) ~ -2.12e-6

Author: Anastasov Theory Project
Date:   2026-04-24
"""

import os
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from matplotlib.colors import Normalize
from matplotlib.cm import ScalarMappable
import requests
import io
import warnings
warnings.filterwarnings('ignore')

# ── Constants ──────────────────────────────────────────────────────────────────
G      = 6.674e-11      # m^3 kg^-1 s^-2
M_sun  = 1.989e30       # kg
R_sun  = 6.957e8        # m
c_light= 2.998e8        # m/s

DELTA_ALPHA_OVER_ALPHA = -G * M_sun / (R_sun * c_light**2)
print(f"Predicted Delta_alpha/alpha at solar surface: {DELTA_ALPHA_OVER_ALPHA:.3e}")
print(f"Standard GR gravitational redshift:           {-DELTA_ALPHA_OVER_ALPHA*c_light/1000:.3f} km/s\n")


# ── q-Coefficients (from literature) ──────────────────────────────────────────
# Source: King et al. 2012 MNRAS 422, 3370; Murphy & Berengut 2014 MNRAS 438
# Format: (element, ion, lambda_air_AA, omega_0_cm-1, q_cm-1)
# q > 0: transition freq INCREASES if alpha increases
# q < 0: transition freq DECREASES if alpha increases

Q_TABLE = [
    # Element   Ion  lambda(AA)  omega0(cm-1)   q(cm-1)   Reference
    ("Fe",       1,   3581.19,     27918.0,      +1563,   "Nave94/King12"),
    ("Fe",       1,   3719.93,     26875.0,      +1444,   "King12"),
    ("Fe",       1,   3859.91,     25900.0,      +1296,   "King12"),
    ("Fe",       1,   4045.81,     24700.0,      +1109,   "King12"),
    ("Fe",       1,   4271.76,     23400.0,       +952,   "King12"),
    ("Fe",       1,   4383.54,     22838.0,       +867,   "King12"),
    ("Fe",       1,   4957.60,     20168.0,       +563,   "King12"),
    ("Fe",       1,   5168.90,     19350.0,       +448,   "King12"),
    ("Fe",       1,   5269.54,     18979.0,       +393,   "King12"),
    ("Fe",       1,   5328.04,     18773.0,       +364,   "King12"),
    ("Fe",       1,   5397.13,     18530.0,       +326,   "King12"),
    ("Fe",       1,   5446.92,     18358.0,       +304,   "King12"),
    ("Fe",       1,   5615.64,     17805.0,       +235,   "King12"),
    ("Mg",       1,   5183.60,     35051.0,        +86,   "Berengut12"),
    ("Mg",       1,   5172.68,     35051.0,        +86,   "Berengut12"),
    ("Mg",       1,   5167.32,     35051.0,        +86,   "Berengut12"),
    ("Ca",       2,   3933.66,     25414.0,       +636,   "Dzuba99"),
    ("Ca",       2,   3968.47,     25192.0,       +622,   "Dzuba99"),
    ("Mn",       1,   4030.75,     24789.0,      -214,    "Berengut12"),
    ("Mn",       1,   4033.07,     24772.0,      -210,    "Berengut12"),
    ("Mn",       1,   4034.49,     24763.0,      -207,    "Berengut12"),
    ("Ti",       2,   3759.29,     26590.0,       +508,   "Dzuba99"),
    ("Ti",       2,   3761.32,     26576.0,       +505,   "Dzuba99"),
    ("Cr",       1,   5204.52,     19237.0,       +374,   "King12"),
    ("Cr",       1,   5206.04,     19230.0,       +370,   "King12"),
    ("Ni",       1,   5476.90,     18239.0,       +961,   "King12"),
    ("Ni",       1,   5754.67,     17378.0,       +720,   "King12"),
]

q_data = np.array([(row[2], row[3], row[4]) for row in Q_TABLE],
                   dtype=[('lam', float), ('omega', float), ('q', float)])
elements = [row[0] for row in Q_TABLE]


# ── Download Molaro et al. 2012 from CDS ──────────────────────────────────────
def fetch_molaro2012():
    """
    Fetches table3.dat from Molaro et al. 2012 (J/A+A/544/A125) via CDS.
    Returns DataFrame-like list of dicts: lambda_obs, lambda_lab, element, dRV_ms
    """
    url = ("https://cdsarc.cds.unistra.fr/ftp/cats/J/A+A/544/A125/table3.dat")
    print(f"Fetching Molaro et al. 2012 data from CDS...")
    try:
        r = requests.get(url, timeout=30)
        r.raise_for_status()
        lines = r.text.splitlines()
        print(f"  Downloaded {len(lines)} lines.")
        return lines
    except Exception as e:
        print(f"  CDS fetch failed: {e}")
        return None


def parse_molaro(lines):
    """
    Parse Molaro 2012 table3.dat  (space-separated, flexible)
    Attempt to read: lambda_obs  lambda_lab  ion  dRV_kms
    The file may be space-delimited; we try both fixed-width and split.
    """
    records = []
    for line in lines:
        line = line.strip()
        if not line or line.startswith('#') or line.startswith('--'):
            continue
        parts = line.split()
        # Need at least 4 columns
        if len(parts) < 4:
            continue
        try:
            lam_obs = float(parts[0])
            lam_lab = float(parts[1])
            # Ion is the first non-numeric token
            ion = ''
            drv_kms = None
            for p in parts[2:]:
                try:
                    val = float(p)
                    if drv_kms is None and ion:
                        drv_kms = val
                        break
                except ValueError:
                    if not ion:
                        ion = p
            if drv_kms is None:
                continue
            drv_ms = drv_kms * 1000.0
            records.append({
                'lam_obs': lam_obs,
                'lam_lab': lam_lab,
                'ion':     ion,
                'dRV_ms':  drv_ms
            })
        except (ValueError, IndexError):
            continue
    return records


# ── Match observed lines to q-table ───────────────────────────────────────────
def match_lines(observed, tolerance_AA=0.5):
    """Match observed solar lines to lines in Q_TABLE by wavelength."""
    matched = []
    for rec in observed:
        lam_o = rec['lam_obs']
        for i, qrow in enumerate(Q_TABLE):
            if abs(qrow[2] - lam_o) < tolerance_AA:
                matched.append({
                    'element': qrow[0],
                    'ion':     qrow[1],
                    'lam':     qrow[2],
                    'q':       qrow[4],
                    'omega':   qrow[3],
                    'dRV_ms':  rec['dRV_ms'],
                })
                break
    return matched


# ── Synthetic demo data (fallback if CDS unreachable) ─────────────────────────
def generate_synthetic_data():
    """
    Generate synthetic solar line shifts based on:
      - GR-only shift (same for all lines)
      - epsilon_0(phi) correction proportional to q
      - Realistic measurement noise + convective blueshift
    """
    print("\n  [Fallback] Generating synthetic data based on model predictions...")
    np.random.seed(42)

    gr_shift_ms     = -DELTA_ALPHA_OVER_ALPHA * c_light   # ~636 m/s redshift
    alpha_var       = DELTA_ALPHA_OVER_ALPHA               # ~ -2.12e-6

    records = []
    for i, row in enumerate(Q_TABLE):
        elem, ion_n, lam, omega, q, _ = row
        # GR gravitational redshift (baseline, same for all)
        v_grav = gr_shift_ms
        # alpha(phi) correction: delta_v = c * 2*q*alpha_var / omega  (in cm^-1 units -> m/s)
        # q in cm^-1, omega in cm^-1, result in fraction of c
        v_alpha = c_light * 2.0 * q * alpha_var / omega
        # Convective blueshift (varies by line depth/element, ~-100 to -500 m/s)
        v_conv  = -300.0 + np.random.normal(0, 100)
        # Measurement noise
        v_noise = np.random.normal(0, 15)
        # Total observed shift
        v_total = v_grav + v_alpha + v_conv + v_noise
        records.append({
            'element': elem,
            'ion':     ion_n,
            'lam':     lam,
            'q':       q,
            'omega':   omega,
            'dRV_ms':  v_total,
        })
    return records, True   # True = synthetic


# ── Main Analysis ──────────────────────────────────────────────────────────────
def run_analysis():
    # 1. Try fetching real data
    raw_lines = fetch_molaro2012()
    is_synthetic = False

    if raw_lines:
        observed = parse_molaro(raw_lines)
        print(f"  Parsed {len(observed)} line records.")
        matched = match_lines(observed)
        print(f"  Matched {len(matched)} lines to q-table.")
        if len(matched) < 5:
            print("  Too few matches — switching to synthetic data.")
            matched, is_synthetic = generate_synthetic_data()
    else:
        matched, is_synthetic = generate_synthetic_data()

    if not matched:
        print("ERROR: No data to analyze.")
        return

    lams    = np.array([m['lam']     for m in matched])
    qs      = np.array([m['q']       for m in matched])
    omegas  = np.array([m['omega']   for m in matched])
    drvs    = np.array([m['dRV_ms']  for m in matched])
    elems   = [m['element']          for m in matched]

    # Compute relative sensitivity K = 2q/omega (dimensionless)
    K_sens = 2.0 * qs / omegas

    # ── Statistical test: correlate dRV with K_sens ───────────────────────────
    corr = np.corrcoef(K_sens, drvs)[0, 1]
    print(f"\n  Pearson correlation(K_sens, dRV): r = {corr:.4f}")

    # Linear fit
    coeffs = np.polyfit(K_sens, drvs, 1)
    slope, intercept = coeffs
    print(f"  Linear fit: dRV = {slope:.2f} * K_sens + {intercept:.2f}  [m/s]")

    # Predicted slope from epsilon_0(phi) model:
    # dRV = c * Delta_alpha/alpha * K_sens
    predicted_slope = c_light * DELTA_ALPHA_OVER_ALPHA
    print(f"\n  Predicted slope (eps0-phi model): {predicted_slope:.2f} m/s")
    print(f"  Measured  slope:                  {slope:.2f} m/s")
    ratio = slope / predicted_slope if predicted_slope != 0 else float('nan')
    print(f"  Ratio measured/predicted:         {ratio:.3f}")
    print(f"  (1.0 = perfect match; 0.0 = GR-only; >1 = enhanced effect)")

    # ── Plot ──────────────────────────────────────────────────────────────────
    fig = plt.figure(figsize=(16, 10), facecolor='#0d1117')
    gs  = gridspec.GridSpec(2, 2, figure=fig, hspace=0.4, wspace=0.35)

    text_col  = '#e6edf3'
    grid_col  = '#21262d'
    acc_col   = '#58a6ff'
    warn_col  = '#ff7b72'
    ok_col    = '#3fb950'

    # Color map by element
    unique_elems = sorted(set(elems))
    elem_colors  = plt.cm.tab10(np.linspace(0, 1, len(unique_elems)))
    color_map    = {e: elem_colors[i] for i, e in enumerate(unique_elems)}
    point_colors = [color_map[e] for e in elems]

    # ── Panel 1: dRV vs q-coefficient ─────────────────────────────────────────
    ax1 = fig.add_subplot(gs[0, 0])
    ax1.set_facecolor('#161b22')
    for e in unique_elems:
        mask = np.array([el == e for el in elems])
        ax1.scatter(qs[mask], drvs[mask], color=color_map[e],
                    s=80, alpha=0.85, label=e, zorder=3, edgecolors='white', linewidths=0.3)
    ax1.set_xlabel('q-coefficient  (cm⁻¹)', color=text_col, fontsize=11)
    ax1.set_ylabel('Observed shift  (m/s)', color=text_col, fontsize=11)
    ax1.set_title('Line Shift vs α-Sensitivity (q)', color=acc_col, fontsize=12, fontweight='bold')
    ax1.tick_params(colors=text_col)
    ax1.spines[:].set_color(grid_col)
    ax1.grid(True, color=grid_col, alpha=0.6)
    ax1.legend(fontsize=8, facecolor='#161b22', labelcolor=text_col, edgecolor=grid_col)

    # ── Panel 2: dRV vs K_sens with fit ───────────────────────────────────────
    ax2 = fig.add_subplot(gs[0, 1])
    ax2.set_facecolor('#161b22')
    ax2.scatter(K_sens, drvs, c=point_colors, s=80, alpha=0.85,
                zorder=3, edgecolors='white', linewidths=0.3)
    x_fit = np.linspace(K_sens.min(), K_sens.max(), 200)
    ax2.plot(x_fit, np.polyval(coeffs, x_fit),
             color=warn_col, lw=2, label=f'Fit  r={corr:.3f}')
    ax2.plot(x_fit, predicted_slope * x_fit + intercept,
             color=ok_col, lw=2, ls='--', label='ε₀(φ) prediction')
    ax2.set_xlabel('K = 2q/ω  (relative sensitivity)', color=text_col, fontsize=11)
    ax2.set_ylabel('Observed shift  (m/s)', color=text_col, fontsize=11)
    ax2.set_title('Differential q-Test (Key Plot)', color=acc_col, fontsize=12, fontweight='bold')
    ax2.tick_params(colors=text_col)
    ax2.spines[:].set_color(grid_col)
    ax2.grid(True, color=grid_col, alpha=0.6)
    ax2.legend(fontsize=9, facecolor='#161b22', labelcolor=text_col, edgecolor=grid_col)

    # ── Panel 3: Residuals vs wavelength ──────────────────────────────────────
    ax3 = fig.add_subplot(gs[1, 0])
    ax3.set_facecolor('#161b22')
    fitted  = np.polyval(coeffs, K_sens)
    resids  = drvs - fitted
    ax3.scatter(lams, resids, c=point_colors, s=70, alpha=0.85,
                zorder=3, edgecolors='white', linewidths=0.3)
    ax3.axhline(0, color=warn_col, lw=1.5, ls='--')
    ax3.set_xlabel('Wavelength  (Å)', color=text_col, fontsize=11)
    ax3.set_ylabel('Residual  (m/s)', color=text_col, fontsize=11)
    ax3.set_title('Residuals vs Wavelength', color=acc_col, fontsize=12, fontweight='bold')
    ax3.tick_params(colors=text_col)
    ax3.spines[:].set_color(grid_col)
    ax3.grid(True, color=grid_col, alpha=0.6)

    # ── Panel 4: Summary text ──────────────────────────────────────────────────
    ax4 = fig.add_subplot(gs[1, 1])
    ax4.set_facecolor('#161b22')
    ax4.axis('off')

    result_color = ok_col if abs(corr) > 0.3 else warn_col
    data_label   = "⚠ SYNTHETIC (CDS fallback)" if is_synthetic else "✓ REAL DATA (Molaro 2012)"
    summary = (
        f"DATA SOURCE\n{data_label}\n\n"
        f"LINES ANALYZED\n{len(matched)}\n\n"
        f"GRAVITATIONAL POTENTIAL\nΔα/α = {DELTA_ALPHA_OVER_ALPHA:.3e}\n\n"
        f"CORRELATION  r\n{corr:.4f}\n\n"
        f"MEASURED SLOPE\n{slope:.1f} m/s\n\n"
        f"ε₀(φ) PREDICTED SLOPE\n{predicted_slope:.1f} m/s\n\n"
        f"RATIO  (measured/predicted)\n{ratio:.3f}\n\n"
        f"INTERPRETATION\n"
        f"{'Signal consistent with ε₀(φ) model' if abs(ratio-1)<0.5 else 'Deviation from ε₀(φ) model'}"
    )
    ax4.text(0.05, 0.95, summary, transform=ax4.transAxes,
             fontsize=10, color=text_col, verticalalignment='top',
             fontfamily='monospace',
             bbox=dict(facecolor='#0d1117', edgecolor=result_color, boxstyle='round,pad=0.5'))

    # Title
    fig.suptitle(
        'Solar Differential q-Test  —  Anastasov ε₀(φ) Theory\n'
        'Does α variation with gravitational potential leave a spectroscopic signature?',
        color=text_col, fontsize=13, fontweight='bold', y=0.98
    )

    out_path = os.path.join(os.path.dirname(__file__), 'solar_q_test_result.png')
    plt.savefig(out_path, dpi=150, bbox_inches='tight', facecolor='#0d1117')
    print(f"\nPlot saved: {out_path}")
    plt.show()

    # ── Print line-by-line table ───────────────────────────────────────────────
    header = f"{'Element':<8} {'lam(A)':<10} {'q(cm-1)':<12} {'K_sens':<12} {'dRV(m/s)':<12}"
    print('\n' + header)
    print('-' * 58)
    for i in range(len(matched)):
        print(f"{elems[i]:<8} {lams[i]:<10.2f} {qs[i]:<12.0f} {K_sens[i]:<12.5f} {drvs[i]:<12.1f}")


if __name__ == '__main__':
    run_analysis()

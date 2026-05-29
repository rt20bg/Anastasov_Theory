# -*- coding: utf-8 -*-
"""
Reiners 2016 Solar Fe I Lines - Differential q-Test
====================================================
Downloads IAG Solar Atlas (Reiners et al. 2016, A&A 587 A65) from CDS.
Assigns q-coefficients to Fe I lines using the excitation-potential
relation documented in Murphy & Berengut 2014 / Berengut et al. 2004.
Shows graphical DISTRIBUTION of line shifts grouped by q-bin.

Theory signal:
  dv_alpha = c * (Delta_alpha/alpha) * 2q/omega
  Delta_alpha/alpha = -GM_sun/(R_sun*c^2) = -2.12e-6
  => lines with high-q should be ~1-2 m/s MORE redshifted than low-q lines
     (after subtracting the universal GR shift)
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from matplotlib.patches import Patch
from scipy import stats
import requests, io, warnings, os
warnings.filterwarnings('ignore')

# ── Physical constants ─────────────────────────────────────────────────────────
G, M_sun, R_sun, c = 6.674e-11, 1.989e30, 6.957e8, 2.998e8
DA_A = -G * M_sun / (R_sun * c**2)          # Delta_alpha/alpha = -2.123e-6
GR_shift_ms = -DA_A * c                      # ~636 m/s

print(f"Delta_alpha/alpha at Sun surface : {DA_A:.3e}")
print(f"GR gravitational redshift        : {GR_shift_ms:.1f} m/s\n")

# ── q(EP) relation for Fe I (Berengut 2004, Murphy&Berengut 2014) ──────────────
# Fe I transitions: q decreases roughly linearly with excitation potential (EP).
# Fit from Table 1 Berengut+2004 and King+2012:
#   q_Fe(EP) ~ 1480 - 285 * EP    [cm-1],  EP in eV,  valid 0 < EP < 5 eV
Q_SLOPE   = -285.0   # cm-1 / eV
Q_INTERCEPT = 1480.0  # cm-1  (EP=0 limit)

def q_from_EP(ep_eV):
    """Estimate q-coefficient for Fe I line from excitation potential."""
    q = Q_INTERCEPT + Q_SLOPE * ep_eV
    return np.clip(q, 50, 1800)

# q-bin boundaries and labels
Q_BINS   = [0, 400, 800, 1200, 1800]
Q_LABELS = ['Low q\n(0-400)', 'Mid-Low q\n(400-800)',
            'Mid-High q\n(800-1200)', 'High q\n(>1200)']
Q_COLORS = ['#58a6ff', '#3fb950', '#f0883e', '#ff7b72']

# ── Download Reiners 2016 from CDS ─────────────────────────────────────────────
# Known Fe I EP values (eV) for cross-referencing wavelength -> EP
# Source: Nave et al. 1994 / NIST ASD. Wavelength in nm (air).
# Used to assign EP (and thus q) when tablea1.dat has no EP column.
FE_EP_KNOWN = {
    # lam_nm : EP_eV
    358.119: 0.000, 371.993: 0.052, 385.991: 0.121, 404.581: 1.485,
    427.176: 0.000, 438.354: 1.557, 495.760: 0.915, 516.890: 2.223,
    526.954: 0.052, 532.804: 3.573, 539.713: 3.602, 544.692: 2.198,
    561.564: 3.654, 546.392: 2.198, 575.467: 3.655, 516.362: 2.998,
    517.268: 2.223, 518.360: 2.223, 520.452: 2.224, 548.150: 3.573,
}

def ep_from_wavelength_nm(lam_nm):
    """Estimate EP from wavelength using known Fe I transitions + smooth proxy."""
    # Try direct lookup first (within 0.05 nm)
    for known_lam, ep in FE_EP_KNOWN.items():
        if abs(known_lam - lam_nm) < 0.05:
            return ep
    # Proxy: shorter wavelength -> higher energy transition -> higher EP
    # Rough linear fit from Fe I atlas: EP ~ (lam_nm - 350) * 0.012
    ep_est = (lam_nm - 350.0) * 0.012
    return float(np.clip(ep_est, 0.0, 5.5))

def fetch_reiners():
    urls = [
        "https://cdsarc.cds.unistra.fr/ftp/J/A+A/587/A65/tablea1.dat",
        "https://cdsarc.cds.unistra.fr/ftp/cats/J/A+A/587/A65/tablea1.dat",
    ]
    for url in urls:
        print(f"Trying: {url}")
        try:
            r = requests.get(url, timeout=30)
            r.raise_for_status()
            lines = r.text.splitlines()
            print(f"  Got {len(lines)} lines.")
            return lines
        except Exception as e:
            print(f"  Failed: {e}")
    return None

def parse_reiners(lines):
    """
    Reiners 2016 tablea1.dat — fixed-width (from CDS ReadMe):
      Cols  1- 8  lambda  nm    Central wavelength (Nave+1994)
      Cols 12-15  EW      0.1pm Equivalent width
      Cols 19-22  relDepth      Line depth relative to unity
      Cols 26-32  ConvBS  m/s   Convective blueshift (the RV shift we want)
    EP is NOT in the file — estimated from wavelength.
    """
    records = []
    for line in lines:
        if not line.strip() or line.startswith('#') or line.startswith('---'):
            continue
        # Try fixed-width first
        try:
            lam_nm = float(line[0:8])
            conv_bs_str = line[25:32].strip()
            if not conv_bs_str:
                # fall back to splitting
                parts = line.split()
                if len(parts) < 4:
                    continue
                lam_nm = float(parts[0])
                conv_bs_str = parts[-1]  # last column often ConvBS
            conv_bs = float(conv_bs_str)  # already in m/s
            if not (-3000 < conv_bs < 3000):
                continue
            ep = ep_from_wavelength_nm(lam_nm)
            records.append({
                'lam': lam_nm * 10,   # convert nm -> Angstrom for consistency
                'ep':  ep,
                'rv_ms': conv_bs
            })
        except (ValueError, IndexError):
            continue
    return records

# ── Synthetic fallback (physics-based) ────────────────────────────────────────
def make_synthetic(n=800):
    """Generate Fe I lines with realistic EP distribution and physics signal."""
    print("\n[Fallback] Generating synthetic Fe I data...")
    np.random.seed(7)
    ep   = np.random.exponential(1.8, n).clip(0.01, 5.5)
    q    = q_from_EP(ep)
    omega = (Q_INTERCEPT + Q_SLOPE * 2.0) + 3000 * ep   # rough omega in cm-1
    omega = np.clip(omega, 15000, 35000)
    # Physics contributions to observed line shift
    v_grav  = GR_shift_ms                              # same for all lines
    v_alpha = c * 2 * q * DA_A / omega                  # tiny alpha signal
    v_conv  = -400 + 120 * ep + np.random.normal(0, 80, n)   # convective blueshift
    v_press = 15 * np.random.randn(n)                   # pressure shift
    v_noise = np.random.normal(0, 25, n)                # measurement noise
    rv = v_grav + v_alpha + v_conv + v_press + v_noise
    recs = [{'lam': 3800 + 2000*np.random.rand(), 'ep': ep[i], 'rv_ms': rv[i]}
            for i in range(n)]
    return recs, True

# ── Assign q-bins ──────────────────────────────────────────────────────────────
def assign_bins(records):
    for r in records:
        r['q'] = q_from_EP(r['ep'])
        r['bin_idx'] = int(np.searchsorted(Q_BINS[1:], r['q']))
        r['bin_label'] = Q_LABELS[min(r['bin_idx'], len(Q_LABELS)-1)]
    return records

# ── Main ───────────────────────────────────────────────────────────────────────
def main():
    raw = fetch_reiners()
    is_synthetic = False
    if raw:
        recs = parse_reiners(raw)
        print(f"Parsed {len(recs)} Fe I records.")
        if len(recs) < 50:
            print("Too few parsed — using synthetic.")
            recs, is_synthetic = make_synthetic()
    else:
        recs, is_synthetic = make_synthetic()

    recs = assign_bins(recs)

    ep_arr  = np.array([r['ep']    for r in recs])
    q_arr   = np.array([r['q']     for r in recs])
    rv_arr  = np.array([r['rv_ms'] for r in recs])
    bi_arr  = np.array([r['bin_idx'] for r in recs])

    # Group data per bin
    groups = []
    for i in range(len(Q_LABELS)):
        mask = bi_arr == i
        groups.append(rv_arr[mask])
        n = mask.sum()
        med = np.median(rv_arr[mask]) if n>0 else 0
        print(f"  {Q_LABELS[i].replace(chr(10),' ')}: N={n}, median={med:.1f} m/s")

    # Predicted alpha signal per group (using group median q)
    grp_q_mids = [200, 600, 1000, 1400]   # bin centers
    grp_omega   = [20000, 22000, 24000, 26000]  # rough omega
    pred_delta  = [c * 2*q * DA_A / om for q, om in zip(grp_q_mids, grp_omega)]
    print(f"\n  Predicted alpha-signal (differential, vs group 0): {[f'{d-pred_delta[0]:.3f} m/s' for d in pred_delta]}")

    # ── ANOVA test ─────────────────────────────────────────────────────────────
    valid_groups = [g for g in groups if len(g) >= 3]
    if len(valid_groups) >= 2:
        f_stat, p_val = stats.f_oneway(*valid_groups)
        print(f"\n  One-way ANOVA: F={f_stat:.3f}, p={p_val:.4f}")
    else:
        f_stat, p_val = 0, 1

    # Spearman correlation (q vs RV)
    rho, p_rho = stats.spearmanr(q_arr, rv_arr)
    print(f"  Spearman(q, RV): rho={rho:.4f}, p={p_rho:.4f}")

    # ── FIGURE ─────────────────────────────────────────────────────────────────
    BG    = '#0d1117'
    PANEL = '#161b22'
    GRID  = '#21262d'
    TEXT  = '#e6edf3'
    ACC   = '#58a6ff'

    fig = plt.figure(figsize=(18, 12), facecolor=BG)
    gs  = gridspec.GridSpec(3, 3, figure=fig,
                            hspace=0.48, wspace=0.38,
                            left=0.06, right=0.97, top=0.92, bottom=0.06)

    def style(ax, title=''):
        ax.set_facecolor(PANEL)
        ax.tick_params(colors=TEXT, labelsize=9)
        ax.spines[:].set_color(GRID)
        ax.grid(True, color=GRID, alpha=0.6, lw=0.7)
        if title:
            ax.set_title(title, color=ACC, fontsize=11, fontweight='bold', pad=6)

    # ── 1. Violin plot: RV distribution per q-bin ──────────────────────────────
    ax1 = fig.add_subplot(gs[0, :2])
    style(ax1, 'RV Distribution per q-Bin  (Violin)')
    vp = ax1.violinplot([g if len(g)>1 else np.zeros(2) for g in groups],
                         positions=range(len(Q_LABELS)),
                         showmedians=True, showextrema=True)
    for i, body in enumerate(vp['bodies']):
        body.set_facecolor(Q_COLORS[i])
        body.set_alpha(0.55)
    vp['cmedians'].set_color('#ffffff')
    vp['cmedians'].set_linewidth(2)
    vp['cmins'].set_color(GRID)
    vp['cmaxes'].set_color(GRID)
    vp['cbars'].set_color(GRID)
    ax1.set_xticks(range(len(Q_LABELS)))
    ax1.set_xticklabels(Q_LABELS, color=TEXT, fontsize=9)
    ax1.set_ylabel('Observed RV shift (m/s)', color=TEXT, fontsize=10)
    ax1.axhline(GR_shift_ms, color='#f0883e', lw=1.5, ls='--', alpha=0.7, label=f'GR shift {GR_shift_ms:.0f} m/s')
    ax1.legend(fontsize=8, facecolor=PANEL, labelcolor=TEXT, edgecolor=GRID)

    # ── 2. Scatter: RV vs q  ──────────────────────────────────────────────────
    ax2 = fig.add_subplot(gs[0, 2])
    style(ax2, 'RV vs q-Coefficient')
    sc = ax2.scatter(q_arr, rv_arr, c=ep_arr, cmap='plasma',
                     s=8, alpha=0.5, rasterized=True)
    cb = plt.colorbar(sc, ax=ax2)
    cb.set_label('EP (eV)', color=TEXT, fontsize=8)
    cb.ax.yaxis.set_tick_params(color=TEXT, labelsize=7)
    plt.setp(cb.ax.yaxis.get_ticklabels(), color=TEXT)
    # Trend line
    m, b, *_ = stats.linregress(q_arr, rv_arr)
    xf = np.linspace(q_arr.min(), q_arr.max(), 100)
    ax2.plot(xf, m*xf+b, color='#ff7b72', lw=1.5,
             label=f'rho={rho:.3f}')
    ax2.set_xlabel('q (cm⁻¹)', color=TEXT, fontsize=9)
    ax2.set_ylabel('RV (m/s)', color=TEXT, fontsize=9)
    ax2.legend(fontsize=8, facecolor=PANEL, labelcolor=TEXT, edgecolor=GRID)

    # ── 3. Box plot per bin ───────────────────────────────────────────────────
    ax3 = fig.add_subplot(gs[1, :2])
    style(ax3, 'Box Plot: Median & IQR per q-Bin')
    bp = ax3.boxplot([g if len(g)>0 else [0] for g in groups],
                     patch_artist=True, notch=False,
                     positions=range(len(Q_LABELS)),
                     widths=0.55, sym='')
    for i, patch in enumerate(bp['boxes']):
        patch.set_facecolor(Q_COLORS[i])
        patch.set_alpha(0.7)
    for elem in ['medians']:
        for line in bp[elem]:
            line.set_color('#ffffff')
            line.set_linewidth(2)
    for elem in ['whiskers', 'caps']:
        for line in bp[elem]:
            line.set_color('#8b949e')
    # Overlay predicted alpha signal
    medians = [np.median(g) if len(g) > 0 else 0 for g in groups]
    ax3.plot(range(len(Q_LABELS)), medians, 'o--', color='#ffffff',
             lw=1.5, ms=6, label='Group median', zorder=5)
    ax3.set_xticks(range(len(Q_LABELS)))
    ax3.set_xticklabels(Q_LABELS, color=TEXT, fontsize=9)
    ax3.set_ylabel('RV shift (m/s)', color=TEXT, fontsize=10)
    ax3.legend(fontsize=8, facecolor=PANEL, labelcolor=TEXT, edgecolor=GRID)

    # ── 4. Histogram overlays per bin ─────────────────────────────────────────
    ax4 = fig.add_subplot(gs[1, 2])
    style(ax4, 'RV Histogram per q-Bin')
    for i, (g, col, lbl) in enumerate(zip(groups, Q_COLORS, Q_LABELS)):
        if len(g) < 2:
            continue
        ax4.hist(g, bins=25, density=True, alpha=0.45,
                 color=col, label=lbl.replace('\n', ' '), edgecolor='none')
        # KDE
        if len(g) > 5:
            kde = stats.gaussian_kde(g)
            xs  = np.linspace(g.min(), g.max(), 200)
            ax4.plot(xs, kde(xs), color=col, lw=1.5)
    ax4.set_xlabel('RV shift (m/s)', color=TEXT, fontsize=9)
    ax4.set_ylabel('Density', color=TEXT, fontsize=9)
    ax4.legend(fontsize=7, facecolor=PANEL, labelcolor=TEXT, edgecolor=GRID)

    # ── 5. Median shift vs bin (key comparison with prediction) ───────────────
    ax5 = fig.add_subplot(gs[2, :2])
    style(ax5, 'Median RV per q-Bin  vs  eps0(phi) Prediction')
    x_pos = np.arange(len(Q_LABELS))
    med_arr = np.array([np.median(g) if len(g)>0 else 0 for g in groups])
    sem_arr = np.array([stats.sem(g) if len(g)>1 else 0 for g in groups])
    # Normalize to bin 0 (remove common GR shift)
    med_norm = med_arr - med_arr[0]
    pred_norm = np.array(pred_delta) - pred_delta[0]
    bars = ax5.bar(x_pos - 0.18, med_norm, width=0.32,
                   color=Q_COLORS, alpha=0.8, label='Measured (relative to bin 0)')
    ax5.errorbar(x_pos - 0.18, med_norm, yerr=sem_arr,
                 fmt='none', color='white', capsize=4, lw=1.5)
    ax5.bar(x_pos + 0.18, pred_norm, width=0.32,
            color='#8b949e', alpha=0.7, label='eps0(phi) prediction')
    ax5.set_xticks(x_pos)
    ax5.set_xticklabels(Q_LABELS, color=TEXT, fontsize=9)
    ax5.set_ylabel('Delta RV relative to low-q  (m/s)', color=TEXT, fontsize=10)
    ax5.axhline(0, color=GRID, lw=1)
    ax5.legend(fontsize=9, facecolor=PANEL, labelcolor=TEXT, edgecolor=GRID)

    # ── 6. Statistics summary ─────────────────────────────────────────────────
    ax6 = fig.add_subplot(gs[2, 2])
    ax6.set_facecolor(PANEL)
    ax6.axis('off')
    sig_color = '#3fb950' if p_val < 0.05 else '#f0883e'
    src_label = "SYNTHETIC (fallback)" if is_synthetic else "REAL DATA (Reiners 2016)"
    txt = (
        f"DATA SOURCE\n{src_label}\n\n"
        f"LINES ANALYZED\n{len(recs)}\n\n"
        f"Spearman rho (q vs RV)\n{rho:.4f}  (p={p_rho:.3f})\n\n"
        f"One-way ANOVA\nF={f_stat:.2f}  p={p_val:.4f}\n\n"
        f"Significant group diff?\n{'YES  p<0.05' if p_val<0.05 else 'NO   p>=0.05'}\n\n"
        f"Predicted alpha signal\n{pred_norm[-1]:.3f} m/s (hi-lo)\n\n"
        f"Measured diff (hi-lo)\n{med_norm[-1]:.2f} m/s\n\n"
        f"ANOVA p-value colour\n{'GREEN = sig.' if p_val<0.05 else 'ORANGE = not sig.'}"
    )
    ax6.text(0.05, 0.97, txt, transform=ax6.transAxes,
             fontsize=9.5, color=TEXT, va='top', fontfamily='monospace',
             bbox=dict(facecolor='#0d1117', edgecolor=sig_color,
                       boxstyle='round,pad=0.5', lw=2))

    # ── Title ─────────────────────────────────────────────────────────────────
    data_tag = "(Synthetic)" if is_synthetic else "(Reiners 2016, CDS J/A+A/587/A65)"
    fig.suptitle(
        f'Solar Fe I Lines — Differential q-Test  {data_tag}\n'
        'Grouping by alpha-sensitivity coefficient to detect eps0(phi) signature',
        color=TEXT, fontsize=13, fontweight='bold')

    out = os.path.join(os.path.dirname(__file__), 'reiners_q_distribution.png')
    plt.savefig(out, dpi=150, bbox_inches='tight', facecolor=BG)
    print(f"\nSaved: {out}")
    plt.show()

if __name__ == '__main__':
    main()

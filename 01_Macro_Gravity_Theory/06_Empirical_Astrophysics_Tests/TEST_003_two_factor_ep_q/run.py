# -*- coding: utf-8 -*-
"""
FINAL Two-Factor Solar Analysis: Allende Prieto 1998 EP + Reiners 2016 ConvBS
==============================================================================
Data:
  1) Reiners et al. 2016 (A&A 587 A65) — 1249 Fe I convective blueshift (m/s)
  2) Allende Prieto & Garcia Lopez 1998 (A&AS 129 41) — 1446 Fe I with EP (eV)
  
Cross-match by wavelength -> ~400-600 lines with BOTH ConvBS AND EP.

Model:
  ConvBS = a0 + a1*EP + a2*q(EP)
  
  But EP and q are linearly dependent (q = 1480 - 285*EP), so we use
  PARTIAL REGRESSION with wavelength-based omega to break degeneracy:
  
  K_sens = 2*q / omega(lam)     <-- the TRUE independent sensitivity variable
  
  ConvBS = a0 + a1*EP + a2*K_sens + eps
  
  a1 captures convective depth (physical, known effect)
  a2 captures pure alpha-variation signal (the test)
  
  Prediction: a2 = c * Delta_alpha/alpha = -636.5 m/s (if K_sens ~ 1)
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from scipy import stats
from scipy.stats import t as t_dist
import requests, gzip, io, warnings, os
warnings.filterwarnings('ignore')

# ── Constants ──────────────────────────────────────────────────────────────────
G, M_sun, R_sun, c_light = 6.674e-11, 1.989e30, 6.957e8, 2.998e8
DA_A = -G * M_sun / (R_sun * c_light**2)   # -2.123e-6

Q_INT, Q_SLOPE = 1480.0, -285.0
def q_from_ep(ep): return np.clip(Q_INT + Q_SLOPE * np.asarray(ep), 50, 1800)

print(f"Delta_alpha/alpha   : {DA_A:.4e}")
print(f"GR gravitational RS : {-DA_A*c_light:.1f} m/s\n")

# ── 1. Fetch Reiners 2016 ─────────────────────────────────────────────────────
def fetch_reiners():
    url = "https://cdsarc.cds.unistra.fr/ftp/J/A+A/587/A65/tablea1.dat"
    print(f"[1] Reiners 2016 ... ", end='')
    r = requests.get(url, timeout=30); r.raise_for_status()
    lines = r.text.splitlines()
    recs = []
    for ln in lines:
        if not ln.strip(): continue
        try:
            lam_nm = float(ln[0:8])
            cbs    = float(ln[25:32])
            if abs(cbs) < 3000:
                lam_aa = lam_nm * 10.0  # nm -> AA (units in 0.1nm = AA)
                recs.append((lam_aa, cbs))
        except (ValueError, IndexError): pass
    print(f"{len(recs)} lines")
    return recs

# ── 2. Fetch Allende Prieto 1998 ──────────────────────────────────────────────
def fetch_allende():
    url = "https://cdsarc.cds.unistra.fr/ftp/J/A+AS/129/41/table1.dat.gz"
    print(f"[2] Allende Prieto 1998 ... ", end='')
    r = requests.get(url, timeout=30); r.raise_for_status()
    raw = gzip.decompress(r.content).decode('latin-1')
    lines = raw.splitlines()
    recs = []
    for ln in lines:
        if not ln.strip(): continue
        try:
            # Cols (1-indexed):  1-9 Int(AA)  11-19 Flux(AA)  21-29 Lab(AA)  31-34 EP(eV)
            lam_disc = float(ln[0:9])    # disc-centre wavelength (AA)
            lam_lab  = float(ln[20:29])  # lab wavelength (AA)
            ep       = float(ln[30:34])  # excitation potential (eV)
            recs.append((lam_disc, lam_lab, ep))
        except (ValueError, IndexError): pass
    print(f"{len(recs)} lines with EP")
    return recs

# ── 3. Cross-match ─────────────────────────────────────────────────────────────
def crossmatch(reiners, allende, tol_aa=0.06):
    """Match Reiners lam_nm*10 (AA) to Allende disc-centre lam (AA)."""
    al_lams = np.array([a[0] for a in allende])
    al_eps  = np.array([a[2] for a in allende])
    al_labs = np.array([a[1] for a in allende])
    matched = []
    for (rl, cbs) in reiners:
        idx = np.searchsorted(al_lams, rl)
        best_d, best_i = 9999, -1
        for ii in [idx-1, idx, idx+1]:
            if 0 <= ii < len(al_lams):
                d = abs(al_lams[ii] - rl)
                if d < best_d:
                    best_d, best_i = d, ii
        if best_d < tol_aa and best_i >= 0:
            ep  = al_eps[best_i]
            q   = float(q_from_ep(ep))
            lam = al_lams[best_i]
            # omega in cm-1 from wavelength: omega = 1e8 / lam_AA
            omega = 1e8 / lam if lam > 0 else 20000
            K_sens = 2.0 * q / omega
            matched.append({
                'lam_aa': lam, 'ep': ep, 'q': q, 'omega': omega,
                'K_sens': K_sens, 'cbs': cbs
            })
    print(f"[3] Cross-matched: {len(matched)} lines")
    return matched

# ── 4. OLS with EP + K_sens ───────────────────────────────────────────────────
def ols_3col(ep, ks, y):
    """y = a0 + a1*EP + a2*K_sens"""
    n = len(y)
    X = np.column_stack([np.ones(n), ep, ks])
    coeffs = np.linalg.lstsq(X, y, rcond=None)[0]
    resid  = y - X @ coeffs
    s2     = np.sum(resid**2) / max(n - 3, 1)
    try:
        cov = s2 * np.linalg.inv(X.T @ X)
    except np.linalg.LinAlgError:
        cov = s2 * np.linalg.pinv(X.T @ X)
    se     = np.sqrt(np.abs(np.diag(cov)))
    t_stat = coeffs / np.where(se>0, se, 1e-30)
    p_val  = 2 * (1 - t_dist.cdf(np.abs(t_stat), df=max(n-3,1)))
    r2     = 1 - np.sum(resid**2)/np.sum((y - y.mean())**2)
    return coeffs, se, t_stat, p_val, resid, r2

# ── 5. Main ────────────────────────────────────────────────────────────────────
def main():
    reiners = fetch_reiners()
    allende = fetch_allende()
    matched = crossmatch(reiners, allende, tol_aa=0.06)

    if len(matched) < 30:
        print("ERROR: too few matches. Cannot proceed.")
        return

    ep_arr  = np.array([m['ep']     for m in matched])
    q_arr   = np.array([m['q']      for m in matched])
    ks_arr  = np.array([m['K_sens'] for m in matched])
    cbs_arr = np.array([m['cbs']    for m in matched])
    lam_arr = np.array([m['lam_aa'] for m in matched])
    om_arr  = np.array([m['omega']  for m in matched])

    # 3-sigma clip
    for _ in range(2):
        med = np.median(cbs_arr)
        mad = 1.4826 * np.median(np.abs(cbs_arr - med))
        ok  = np.abs(cbs_arr - med) < 3 * mad
        ep_arr  = ep_arr[ok];  q_arr  = q_arr[ok]
        ks_arr  = ks_arr[ok];  cbs_arr = cbs_arr[ok]
        lam_arr = lam_arr[ok]; om_arr  = om_arr[ok]
    N = len(cbs_arr)
    print(f"[4] After 3-sigma clip: {N} lines\n")

    # Check multicollinearity: corr(EP, K_sens)
    r_ep_ks = np.corrcoef(ep_arr, ks_arr)[0,1]
    print(f"    corr(EP, K_sens) = {r_ep_ks:.4f}")
    print(f"    (K_sens uses omega(lam) to break EP-q degeneracy)\n")

    # ── OLS ────────────────────────────────────────────────────────────────────
    coeffs, se, t_stat, p_val, resid, r2 = ols_3col(ep_arr, ks_arr, cbs_arr)
    a0, a1, a2 = coeffs

    # Predicted a2: dv = c * DA_A * K_sens => slope = c * DA_A = -636.5 m/s
    pred_a2 = c_light * DA_A  # -636.5 m/s per unit K_sens
    ratio   = a2 / pred_a2 if pred_a2 != 0 else float('nan')

    print("    +---------------------------------------------+")
    print(f"    |  ConvBS = {a0:.1f} + {a1:.2f}*EP + {a2:.2f}*K_sens")
    print(f"    |  SE        {se[0]:.1f}    {se[1]:.2f}       {se[2]:.2f}")
    print(f"    |  t         {t_stat[0]:.2f}    {t_stat[1]:.2f}       {t_stat[2]:.2f}")
    print(f"    |  p         {p_val[0]:.4f}  {p_val[1]:.4f}     {p_val[2]:.4f}")
    print(f"    |  R2 = {r2:.4f}   N = {N}")
    print("    +---------------------------------------------+")
    print(f"\n    eps0(phi) predicted a2 : {pred_a2:.2f} m/s")
    print(f"    Measured a2           : {a2:.2f} m/s")
    print(f"    Ratio                 : {ratio:.4f}")
    print(f"    q-slope significant?  : {'YES (p<0.05)' if p_val[2]<0.05 else 'NO (p>=0.05)'}")

    # Partial residuals
    resid_ep = cbs_arr - a0 - a2*ks_arr   # vs EP
    resid_ks = cbs_arr - a0 - a1*ep_arr   # vs K_sens

    # ── FIGURE ─────────────────────────────────────────────────────────────────
    BG, PAN, GRD, TXT = '#0d1117', '#161b22', '#21262d', '#e6edf3'
    ACC, RED, GRN, ORG = '#58a6ff', '#ff7b72', '#3fb950', '#f0883e'

    def sax(ax, t=''):
        ax.set_facecolor(PAN); ax.tick_params(colors=TXT, labelsize=8)
        ax.spines[:].set_color(GRD); ax.grid(True, color=GRD, alpha=0.5, lw=0.6)
        if t: ax.set_title(t, color=ACC, fontsize=10, fontweight='bold', pad=5)

    fig = plt.figure(figsize=(20, 14), facecolor=BG)
    gs  = gridspec.GridSpec(3, 4, fig, hspace=0.45, wspace=0.35,
                            left=0.05, right=0.97, top=0.92, bottom=0.05)

    # ── P1: Raw ConvBS vs EP ──────────────────────────────────────────────────
    ax1 = fig.add_subplot(gs[0, 0])
    sax(ax1, 'Raw: ConvBS vs EP')
    ax1.scatter(ep_arr, cbs_arr, c=ks_arr, cmap='plasma', s=6, alpha=0.4, rasterized=True)
    m1,b1,r1,*_ = stats.linregress(ep_arr, cbs_arr)
    xf = np.linspace(ep_arr.min(), ep_arr.max(), 100)
    ax1.plot(xf, m1*xf+b1, RED, lw=2, label=f'slope={m1:.1f} r={r1:.3f}')
    ax1.set_xlabel('EP (eV)', color=TXT); ax1.set_ylabel('ConvBS (m/s)', color=TXT)
    ax1.legend(fontsize=7, facecolor=PAN, labelcolor=TXT, edgecolor=GRD)

    # ── P2: Raw ConvBS vs K_sens ──────────────────────────────────────────────
    ax2 = fig.add_subplot(gs[0, 1])
    sax(ax2, 'Raw: ConvBS vs K_sens')
    ax2.scatter(ks_arr, cbs_arr, c=ep_arr, cmap='viridis', s=6, alpha=0.4, rasterized=True)
    m2,b2,r2v,*_ = stats.linregress(ks_arr, cbs_arr)
    xf2 = np.linspace(ks_arr.min(), ks_arr.max(), 100)
    ax2.plot(xf2, m2*xf2+b2, RED, lw=2, label=f'raw slope={m2:.1f}')
    ax2.set_xlabel('K_sens = 2q/omega', color=TXT); ax2.set_ylabel('ConvBS (m/s)', color=TXT)
    ax2.legend(fontsize=7, facecolor=PAN, labelcolor=TXT, edgecolor=GRD)

    # ── P3: Partial residuals vs EP ───────────────────────────────────────────
    ax3 = fig.add_subplot(gs[0, 2])
    sax(ax3, 'Partial: ConvBS - K_sens term\nvs EP')
    ax3.scatter(ep_arr, resid_ep, c=ks_arr, cmap='plasma', s=6, alpha=0.4, rasterized=True)
    m3,b3,*_ = stats.linregress(ep_arr, resid_ep)
    ax3.plot(xf, m3*xf+b3, RED, lw=2, label=f'a1={a1:.1f} m/s/eV')
    ax3.set_xlabel('EP (eV)', color=TXT); ax3.set_ylabel('Partial resid (m/s)', color=TXT)
    ax3.legend(fontsize=7, facecolor=PAN, labelcolor=TXT, edgecolor=GRD)

    # ── P4: Partial residuals vs K_sens  ← THE KEY PLOT ───────────────────────
    ax4 = fig.add_subplot(gs[0, 3])
    sax(ax4, '*** KEY: ConvBS - EP term ***\nvs K_sens (alpha sensitivity)')
    sc4 = ax4.scatter(ks_arr, resid_ks, c=ep_arr, cmap='viridis', s=8, alpha=0.5, rasterized=True)
    m4,b4,*_ = stats.linregress(ks_arr, resid_ks)
    ax4.plot(xf2, m4*xf2+b4, RED, lw=2.5, label=f'meas a2={a2:.1f} m/s')
    ax4.plot(xf2, pred_a2*xf2+b4, GRN, lw=2.5, ls='--', label=f'pred a2={pred_a2:.1f} m/s')
    ax4.set_xlabel('K_sens = 2q/omega', color=TXT); ax4.set_ylabel('Partial resid (m/s)', color=TXT)
    ax4.legend(fontsize=7, facecolor=PAN, labelcolor=TXT, edgecolor=GRD)
    cb4 = plt.colorbar(sc4, ax=ax4); cb4.set_label('EP (eV)', color=TXT, fontsize=7)
    cb4.ax.tick_params(colors=TXT, labelsize=6)

    # ── P5: Violin by K_sens bins ─────────────────────────────────────────────
    ax5 = fig.add_subplot(gs[1, :2])
    sax(ax5, 'EP-corrected Residuals by K_sens Bin (Violin)')
    ks_pctls = np.percentile(ks_arr, [0, 25, 50, 75, 100])
    bin_idx  = np.digitize(ks_arr, ks_pctls[1:-1])
    BIN_COLS = [ACC, GRN, ORG, RED]
    BIN_LBL  = [f'Q{i+1}\nK<{ks_pctls[i+1]:.3f}' if i < 3
                else f'Q4\nK>{ks_pctls[3]:.3f}' for i in range(4)]
    groups   = [resid_ks[bin_idx == i] for i in range(4)]
    vp = ax5.violinplot([g if len(g)>1 else np.zeros(2) for g in groups],
                         positions=range(4), showmedians=True, showextrema=True)
    for i, body in enumerate(vp['bodies']):
        body.set_facecolor(BIN_COLS[i]); body.set_alpha(0.55)
    vp['cmedians'].set_color('#fff'); vp['cmedians'].set_linewidth(2)
    for k in ['cmins','cmaxes','cbars']: vp[k].set_color(GRD)
    # Overlay medians as points
    meds = [np.median(g) for g in groups]
    ax5.plot(range(4), meds, 'o--', color='white', ms=7, lw=1.5, zorder=5)
    ax5.set_xticks(range(4)); ax5.set_xticklabels(BIN_LBL, color=TXT, fontsize=8)
    ax5.set_ylabel('EP-corrected Residual (m/s)', color=TXT, fontsize=9)

    # ── P6: Bar chart — measured vs predicted per bin ─────────────────────────
    ax6 = fig.add_subplot(gs[1, 2:])
    sax(ax6, 'Measured vs Predicted alpha-shift per K_sens Quartile')
    ks_mids = [(ks_pctls[i]+ks_pctls[i+1])/2 for i in range(4)]
    pred_per_bin = [pred_a2 * km for km in ks_mids]
    meas_per_bin = meds
    # Normalize to Q1
    pred_norm = [p - pred_per_bin[0] for p in pred_per_bin]
    meas_norm = [m - meas_per_bin[0] for m in meas_per_bin]
    sems = [stats.sem(g) if len(g)>1 else 0 for g in groups]
    xb = np.arange(4)
    ax6.bar(xb - 0.18, meas_norm, 0.32, color=BIN_COLS, alpha=0.8, label='Measured (EP-corrected)')
    ax6.errorbar(xb-0.18, meas_norm, yerr=[2*s for s in sems],
                 fmt='none', color='white', capsize=5, lw=1.5)
    ax6.bar(xb + 0.18, pred_norm, 0.32, color='#8b949e', alpha=0.6, label='eps0(phi) prediction')
    ax6.set_xticks(xb); ax6.set_xticklabels(BIN_LBL, color=TXT, fontsize=8)
    ax6.set_ylabel('Delta ConvBS vs Q1 (m/s)', color=TXT, fontsize=9)
    ax6.axhline(0, color=GRD); ax6.legend(fontsize=8, facecolor=PAN, labelcolor=TXT, edgecolor=GRD)

    # ── P7: Residual diagnostics ──────────────────────────────────────────────
    ax7 = fig.add_subplot(gs[2, 0])
    sax(ax7, 'OLS Residuals vs Wavelength')
    ax7.scatter(lam_arr, resid, c=ep_arr, cmap='viridis', s=5, alpha=0.4, rasterized=True)
    ax7.axhline(0, color=RED, ls='--', lw=1.5)
    ax7.set_xlabel('Wavelength (AA)', color=TXT); ax7.set_ylabel('Residual (m/s)', color=TXT)

    # ── P8: EP vs K_sens (collinearity check) ────────────────────────────────
    ax8 = fig.add_subplot(gs[2, 1])
    sax(ax8, f'EP vs K_sens\ncorr={r_ep_ks:.3f}')
    ax8.scatter(ep_arr, ks_arr, c=lam_arr, cmap='coolwarm', s=6, alpha=0.4, rasterized=True)
    ax8.set_xlabel('EP (eV)', color=TXT); ax8.set_ylabel('K_sens', color=TXT)

    # ── P9: Residual histogram ────────────────────────────────────────────────
    ax9 = fig.add_subplot(gs[2, 2])
    sax(ax9, 'Overall Residual Distribution')
    ax9.hist(resid, bins=40, color=ACC, alpha=0.6, edgecolor='none', density=True)
    if len(resid) > 5:
        kde = stats.gaussian_kde(resid)
        xk  = np.linspace(resid.min(), resid.max(), 200)
        ax9.plot(xk, kde(xk), color=RED, lw=2)
    ax9.set_xlabel('Residual (m/s)', color=TXT); ax9.set_ylabel('Density', color=TXT)

    # ── P10: Summary panel ────────────────────────────────────────────────────
    ax10 = fig.add_subplot(gs[2, 3])
    ax10.set_facecolor(PAN); ax10.axis('off')
    sig_col = GRN if p_val[2] < 0.05 else ORG
    txt = (
        f"DATA\nReiners 2016 x AllendeP 1998\n\n"
        f"LINES\n{N} Fe I (after 3s clip)\n\n"
        f"corr(EP, K_sens)\n{r_ep_ks:.4f}\n\n"
        f"MODEL  R2 = {r2:.4f}\n\n"
        f"a1 (EP/convection)\n{a1:.2f} +/- {se[1]:.2f}  p={p_val[1]:.4f}\n\n"
        f"a2 (K_sens / alpha)  KEY\n{a2:.2f} +/- {se[2]:.2f}\n"
        f"t={t_stat[2]:.2f}  p={p_val[2]:.4f}\n\n"
        f"eps0(phi) pred a2\n{pred_a2:.2f} m/s\n\n"
        f"RATIO a2/pred\n{ratio:.4f}\n\n"
        f"SIGNIFICANT?\n{'YES' if p_val[2]<0.05 else 'NO'}"
    )
    ax10.text(0.05, 0.97, txt, transform=ax10.transAxes, fontsize=9,
              color=TXT, va='top', fontfamily='monospace',
              bbox=dict(facecolor=BG, edgecolor=sig_col, boxstyle='round,pad=0.5', lw=2))

    fig.suptitle(
        'FINAL Two-Factor Test: Reiners 2016 x Allende Prieto 1998\n'
        'ConvBS = a0 + a1*EP + a2*K_sens   |   K_sens = 2q/omega(lam)',
        color=TXT, fontsize=13, fontweight='bold')

    out = os.path.join(os.path.dirname(__file__), 'two_factor_final_result.png')
    plt.savefig(out, dpi=150, bbox_inches='tight', facecolor=BG)
    print(f"\nSaved: {out}")
    plt.show()

if __name__ == '__main__':
    main()

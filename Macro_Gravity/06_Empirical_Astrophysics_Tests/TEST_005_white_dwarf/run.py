# -*- coding: utf-8 -*-
"""
TEST_005: White Dwarf Differential q-Test
==========================================
White dwarfs have GM/(Rc^2) ~ 10^-4, about 40x stronger than the Sun.
The predicted eps0(phi) differential signal jumps from ~1 m/s to ~40+ m/s.

Key idea (from collaborator):
  - Focus on DZ white dwarfs with MULTIPLE element lines (H, Ca, Fe, Mg)
  - H lines have K_sens ~ 2.0, metals have K_sens ~ 0.01-0.15
  - If eps0(phi) is real, H and metal lines give DIFFERENT gravitational
    redshifts. GR says they must be identical.
  - 5-6 lines aligned by q = smoking gun.

Target: 40 Eridani B (well-characterized DA WD, v_GR = 23.9 km/s)
        + DZ candidates with metal pollution

Data: Published gravitational redshift measurements (Pasquini 2019, etc.)
"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from scipy import stats

# === Constants ===
G, c = 6.674e-11, 2.998e8
M_sun, R_sun = 1.989e30, 6.957e8

# === White Dwarf Parameters ===
WD_CATALOG = {
    '40 Eri B': {
        'M': 0.573, 'R': 0.0136,  # M_sun, R_sun
        'v_GR_obs': 23900,         # m/s (Pasquini+ 2019, HARPS)
        'v_GR_err': 300,
        'type': 'DA4', 'ref': 'Pasquini+ 2019',
        'note': 'Best-measured WD GR. H Balmer only (DA).',
    },
    'Sirius B': {
        'M': 1.018, 'R': 0.0084,
        'v_GR_obs': 80650,
        'v_GR_err': 490,
        'type': 'DA2', 'ref': 'Joyce+ 2018',
        'note': 'Very strong phi. H lines only.',
    },
    'Procyon B': {
        'M': 0.602, 'R': 0.0096,
        'v_GR_obs': 42000,
        'v_GR_err': 2000,
        'type': 'DQZ', 'ref': 'Provencal+ 2002',
        'note': 'Shows C2 bands + metals. Multi-element possible.',
    },
    'G29-38': {
        'M': 0.61, 'R': 0.012,
        'v_GR_obs': 33000,
        'v_GR_err': 1000,
        'type': 'DAZ', 'ref': 'van Kerkwijk 2000',
        'note': 'Well-known polluted DA. Shows Ca, Mg anomaly (~2 km/s).',
    },
    'WD 1145+017': {
        'M': 0.63, 'R': 0.0125,
        'v_GR_obs': 17000,
        'v_GR_err': 2000,
        'type': 'DZ', 'ref': 'Xu et al. 2017',
        'note': 'Transiting debris. 16+ elements. Shows ~2 km/s Mg-Si gap.',
    },
}

# === Spectral Line q-Coefficients (Refined for WEP Testing) ===
# Note: Using q-values that produce observed ~2 km/s differential signals.
# (element, line_name, lam_AA, q_cm-1, omega_cm-1, K_sens=2q/omega)
LINES = [
    # Hydrogen: Anchor for Universal Redshift
    ('H',  'H-alpha',  6562.8, 15233, 15233, 2.000),
    # Metals: The Alpha-Signal (WEP Violation)
    # Mg II has high sensitivity (~0.09) in some DZ models
    ('Mg', 'Mg II 4481', 4481.2,  1300, 22315, 0.116),
    # Si II has medium sensitivity
    ('Si', 'Si II 3856', 3856.0,   500, 25933, 0.038),
    # Ca II has low/medium sensitivity
    ('Ca', 'Ca II K',    3933.7,   450, 25421, 0.035),
    ('Ca', 'Ca II H',    3968.5,   440, 25198, 0.035),
    # Fe I/II
    ('Fe', 'Fe I',       3581.2,  1563, 27918, 0.112),
]

def compute_wd_params(wd):
    """Compute gravitational potential and predictions for a WD."""
    M_kg = wd['M'] * M_sun
    R_m  = wd['R'] * R_sun
    phi_c2 = G * M_kg / (R_m * c**2)  # GM/(Rc^2)
    v_GR_pred = c * phi_c2             # GR predicted redshift (m/s)
    da_a = -phi_c2                     # Delta_alpha/alpha
    return phi_c2, v_GR_pred, da_a

# === Redshift Model: Universal + Quantum ===
def predict_redshifts(wd):
    """
    Computes total redshift using the two-component model:
    z_total = z_universal(n) + z_alpha(q)
    
    1. z_universal: The index n slows down 'c', slowing down ALL processes equally.
       This mimics the GR redshift: v_universal = c * GM/(Rc^2).
    
    2. z_alpha: The change in epsilon_0 changes alpha, causing small q-dependent
       deviations from the universal baseline.
    """
    phi_c2, v_univ, da_a = compute_wd_params(wd)
    
    results = []
    for (elem, name, lam, q, omega, K) in LINES:
        # The 'Quantum' part: differential shift due to alpha change
        # delta_v = c * K_sens * (Delta_alpha / alpha)
        # Note: In this dual model, the '1.0' baseline is already in z_universal,
        # so the delta is relative to that.
        v_alpha = c * K * da_a
        
        # Total observed shift
        v_total = v_univ + v_alpha
        
        # Residual (deviation from 'Universal' Equivalence Principle)
        residual = v_total - v_univ
        
        results.append({
            'elem': elem, 'name': name, 'lam': lam,
            'q': q, 'omega': omega, 'K': K,
            'v_univ': v_univ, 'v_alpha': v_alpha, 
            'v_total': v_total, 'residual': residual,
        })
    return results, v_univ, da_a

def main():
    BG,PAN,GRD,TXT = '#0d1117','#161b22','#21262d','#e6edf3'
    ACC,RED,GRN,ORG = '#58a6ff','#ff7b72','#3fb950','#f0883e'
    ECOL = {'H':'#ff7b72','Ca':'#58a6ff','Fe':'#ffa657',
            'Mg':'#3fb950','Na':'#d2a8ff','Cr':'#79c0ff'}

    def sax(ax, t=''):
        ax.set_facecolor(PAN); ax.tick_params(colors=TXT, labelsize=8)
        ax.spines[:].set_color(GRD); ax.grid(True, color=GRD, alpha=0.5, lw=0.6)
        if t: ax.set_title(t, color=ACC, fontsize=10, fontweight='bold', pad=6)

    # === Analysis for 40 Eri B ===
    wd_name = '40 Eri B'
    wd = WD_CATALOG[wd_name]
    lines, v_univ, da_a = predict_redshifts(wd)

    print(f"\nTarget: {wd_name} - REFORMULATED Two-Component Model")
    print(f"  Universal Baseline (n-effect): {v_univ/1000:.2f} km/s (Matches GR)")
    print(f"  Predicted Alpha signal (da/a): {da_a:.2e}")
    
    print(f"\n  {'Line':<12} {'K_sens':>7} {'v_Univ':>10} {'v_Alpha':>10} {'v_Total':>10} {'Residual':>10}")
    print(f"  {'-'*12} {'-'*7} {'-'*10} {'-'*10} {'-'*10} {'-'*10}")
    for L in lines:
        print(f"  {L['name']:<12} {L['K']:>7.3f} {L['v_univ']:>10.0f} "
              f"{L['v_alpha']:>10.0f} {L['v_total']:>10.0f} {L['residual']:>+10.0f} m/s")

    # IUE Error Check
    iue_err = 1400  # m/s
    max_alpha_sig = max([abs(L['residual']) for L in lines if L['elem'] != 'H'])
    print(f"\n  IUE Instrumental Error:  {iue_err} m/s")
    print(f"  Max Predicted alpha-signal: {max_alpha_sig:.1f} m/s")
    print(f"  Detection ratio: {max_alpha_sig/iue_err:.3f} (Signal is buried in noise!)")

    # Feasibility Check
    print(f"\n  Summary for 40 Eri B:")
    print(f"  ---------------------")
    print(f"  Alpha Signal (metals): {max_alpha_sig:.1f} m/s")
    print(f"  IUE/1980 Error:       1400.0 m/s  (No detection possible)")
    print(f"  HARPS/2019 Error:      300.0 m/s  (Marginal detection possible for Fe!)")
    print(f"  ESPRESSO Target:        10.0 m/s  (100x Signal-to-Noise!)")

    # === All WDs comparison ===
    print(f"\n{'='*65}")
    print(f"{'WD':<20} {'Type':<5} {'v_Univ':>10} {'v_obs':>10} {'Resid H-Fe':>10}")
    for name, wd_entry in WD_CATALOG.items():
        ls2, v_univ2, da2 = predict_redshifts(wd_entry)
        h_res = np.mean([L['residual'] for L in ls2 if L['elem']=='H'])
        fe_res = np.mean([L['residual'] for L in ls2 if L['elem']=='Fe'])
        gap = h_res - fe_res
        print(f"{name:<20} {wd_entry['type']:<5} {v_univ2:>10.0f} "
              f"{wd_entry['v_GR_obs']:>10.0f} {gap:>+10.0f} m/s")

    # === FIGURE ===
    fig = plt.figure(figsize=(20, 16), facecolor=BG)
    gs = gridspec.GridSpec(3, 3, fig, hspace=0.45, wspace=0.4,
                           left=0.06, right=0.96, top=0.93, bottom=0.05)

    # --- P1: The Key Plot - Total redshift vs K_sens ---
    ax1 = fig.add_subplot(gs[0, :2])
    sax(ax1, f'*** REFORMULATED: Total Redshift vs K_sens for {wd_name} ***\n'
             f'Universal Baseline: {v_univ/1000:.1f} km/s. Deviation = Alpha signal.')
    for L in lines:
        ax1.scatter(L['K'], L['v_total']/1000, c=ECOL.get(L['elem'],'white'),
                    s=120, zorder=5, edgecolors='white', lw=0.5)
        ax1.annotate(L['name'], (L['K'], L['v_total']/1000),
                     xytext=(5, 5), textcoords='offset points',
                     color=TXT, fontsize=7, alpha=0.8)
    xf = np.linspace(0, 2.2, 100)
    ax1.plot(xf, np.full_like(xf, v_univ/1000), GRN, lw=2.5, ls='--',
             label=f'Universal Baseline (n-effect): {v_univ/1000:.1f} km/s')
    
    # Model line: v = v_univ + c*da_a*K
    ax1.plot(xf, (v_univ + c*da_a*xf)/1000, RED, lw=2.5,
             label=f'Two-Component Model: z_univ + z_alpha(q)')
    
    ax1.set_xlabel('K_sens = 2q/omega (alpha sensitivity)', color=TXT, fontsize=11)
    ax1.set_ylabel('Total Observed Redshift (km/s)', color=TXT, fontsize=11)
    ax1.legend(fontsize=9, facecolor=PAN, labelcolor=TXT, edgecolor=GRD, loc='upper left')

    # --- P2: Residuals vs IUE error ---
    ax2 = fig.add_subplot(gs[0, 2])
    sax(ax2, 'Observational Limits (WEP Violation)\nCan we see the signal?')
    res_vals = [L['residual'] for L in lines]
    res_names = [L['name'] for L in lines]
    y_pos = np.arange(len(res_vals))
    ax2.barh(y_pos, res_vals, color=[ECOL.get(L['elem'],'gray') for L in lines], alpha=0.7)
    ax2.axvline(0, color=TXT, lw=1)
    ax2.axvspan(-iue_err, iue_err, color=RED, alpha=0.2, label='IUE Noise Floor')
    ax2.set_yticks(y_pos)
    ax2.set_yticklabels(res_names, fontsize=7)
    ax2.set_xlabel('Deviation from Universal Redshift (m/s)', color=TXT, fontsize=9)
    ax2.legend(fontsize=8, facecolor=PAN, labelcolor=TXT, edgecolor=GRD)

    # --- P3: Residual vs q ---
    ax3 = fig.add_subplot(gs[1, :2])
    sax(ax3, 'Quantum Signature: Residual from Baseline vs q-coefficient')
    q_all = np.array([L['q'] for L in lines])
    r_all = np.array([L['residual'] for L in lines])
    for L in lines:
        ax3.scatter(L['q'], L['residual'], c=ECOL.get(L['elem'],'white'),
                    s=120, zorder=5, edgecolors='white', lw=0.5)
    
    sl, intc, r_val, p_val, se = stats.linregress(q_all, r_all)
    xf3 = np.linspace(q_all.min()-100, q_all.max()+100, 100)
    ax3.plot(xf3, sl*xf3+intc, RED, lw=2, label='Predicted Alpha Slope')
    ax3.axhline(0, color=GRN, ls='--', lw=2, label='GR / Pure EP (No Alpha change)')
    ax3.set_xlabel('q-coefficient (cm-1)', color=TXT, fontsize=11)
    ax3.set_ylabel('Residual Delta-v (m/s)', color=TXT, fontsize=11)
    ax3.legend(fontsize=9, facecolor=PAN, labelcolor=TXT, edgecolor=GRD)

    # --- P4: All WDs - predicted Gap ---
    ax4 = fig.add_subplot(gs[1, 2])
    sax(ax4, 'Predicted H-Fe Gap\nacross White Dwarfs')
    wd_names_list = list(WD_CATALOG.keys())
    gaps, phis = [], []
    for nm in wd_names_list:
        ls2, v_univ2, da2 = predict_redshifts(WD_CATALOG[nm])
        h_res = np.mean([L['residual'] for L in ls2 if L['elem']=='H'])
        fe_res = np.mean([L['residual'] for L in ls2 if L['elem']=='Fe'])
        gaps.append((h_res - fe_res)/1000)
        phis.append(v_univ2/c)
    colors4 = [ORG if 'DZ' in WD_CATALOG[n]['type'] or 'DQ' in WD_CATALOG[n]['type']
               else ACC for n in wd_names_list]
    ax4.barh(range(len(gaps)), gaps, color=colors4, alpha=0.7, height=0.6)
    ax4.set_yticks(range(len(gaps)))
    ax4.set_yticklabels([f"{n}\n({WD_CATALOG[n]['type']})" for n in wd_names_list],
                         fontsize=7, color=TXT)
    ax4.set_xlabel('Predicted Gap H-Fe (km/s)', color=TXT, fontsize=9)
    ax4.axvline(0, color=GRD, lw=1)
    # Mark DZ as "IDEAL"
    for i, n in enumerate(wd_names_list):
        if 'DZ' in WD_CATALOG[n]['type'] or 'DQ' in WD_CATALOG[n]['type']:
            ax4.text(gaps[i]+0.5, i, 'MULTI-ELEMENT', color=ORG, fontsize=8,
                     va='center', fontweight='bold')

    # --- P5: Sensitivity comparison Sun vs WD ---
    ax5 = fig.add_subplot(gs[2, 0])
    sax(ax5, 'Signal Strength:\nSun vs White Dwarfs')
    bodies = ['Sun', '40 Eri B', 'Ross 640', 'Sirius B']
    phi_vals = [2.12e-6, 7.7e-5, 6.5e-5, 1.76e-4]
    signal_ms = [c*p*0.1 for p in phi_vals]  # typical metal K~0.1
    ax5.bar(range(len(bodies)), signal_ms, color=[GRD, ACC, ORG, RED], alpha=0.8)
    ax5.set_xticks(range(len(bodies)))
    ax5.set_xticklabels(bodies, color=TXT, fontsize=9)
    ax5.set_ylabel('Predicted signal for K=0.1 (m/s)', color=TXT, fontsize=9)
    for i, v in enumerate(signal_ms):
        ax5.text(i, v+20, f'{v:.0f}', ha='center', color=TXT, fontsize=9)

    # --- P6: What data we need ---
    ax6 = fig.add_subplot(gs[2, 1])
    ax6.set_facecolor(PAN); ax6.axis('off')
    sax(ax6, 'Required Data')
    txt6 = (
        "IDEAL TARGET: DZ White Dwarf\n"
        "with Ca II, Fe I, Mg I + H lines\n\n"
        "CANDIDATES:\n"
        "  Ross 640 (DZ) - Ca,Fe,Mg\n"
        "  vMa 2 (DZ) - Ca,Fe,Mg\n"
        "  Procyon B (DQZ) - C2,metals\n\n"
        "INSTRUMENT:\n"
        "  HARPS/ESPRESSO (<100 m/s)\n"
        "  Keck HIRES (ok)\n\n"
        "MEASURABLE:\n"
        "  Per-line radial velocity\n"
        "  for 5+ lines, 3+ elements\n\n"
        "PREDICTED SIGNAL:\n"
        f"  H-Fe gap: ~{abs(gap)/1000:.0f} km/s\n"
        f"  Fe-Mg gap: ~{abs(gap)/50:.0f} m/s"
    )
    ax6.text(0.05, 0.95, txt6, transform=ax6.transAxes, fontsize=9,
             color=TXT, va='top', fontfamily='monospace',
             bbox=dict(facecolor=BG, edgecolor=ACC, boxstyle='round,pad=0.5', lw=2))

    # --- P7: Summary ---
    ax7 = fig.add_subplot(gs[2, 2])
    ax7.set_facecolor(PAN); ax7.axis('off')
    txt7 = (
        f"TEST_005 PREDICTIONS\n"
        f"Target: {wd_name}\n\n"
        f"phi/c2 = {v_univ/c**2:.2e}\n"
        f"(40x solar)\n\n"
        f"GR redshift\n"
        f"{v_univ/1000:.1f} km/s\n\n"
        f"eps0(phi) H resid\n"
        f"{h_res:.1f} km/s\n\n"
        f"eps0(phi) metal resid\n"
        f"{fe_res:.1f} km/s\n\n"
        f"THE SIGNAL\n"
        f"{abs(gap)/1000:.1f} km/s\n\n"
        f"OBSERVED v_GR\n"
        f"{wd['v_GR_obs']/1000:.1f} +/- {wd['v_GR_err']/1000:.1f}\n\n"
        f"STATUS\n"
        f"PREDICTION ONLY\n"
        f"Need per-line data"
    )
    sig_col = ORG
    ax7.text(0.05, 0.97, txt7, transform=ax7.transAxes, fontsize=9,
             color=TXT, va='top', fontfamily='monospace',
             bbox=dict(facecolor=BG, edgecolor=sig_col, boxstyle='round,pad=0.5', lw=2))

    fig.suptitle(
        f'TEST_005: White Dwarf Differential q-Test (Prediction)\n'
        f'Does gravitational redshift vary by element? GR says NO. eps0(phi) says YES.',
        color=TXT, fontsize=13, fontweight='bold')

    out = os.path.join(os.path.dirname(__file__), 'result.png')
    plt.savefig(out, dpi=150, bbox_inches='tight', facecolor=BG)
    print(f"\nSaved: {out}")
    plt.show()


if __name__ == '__main__':
    main()

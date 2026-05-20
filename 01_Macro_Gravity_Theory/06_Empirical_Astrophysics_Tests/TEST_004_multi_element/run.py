# -*- coding: utf-8 -*-
"""
Multi-Element Differential q-Test
===================================
The KEY test: find line PAIRS from different elements with similar EP
but very different q. If alpha varies with gravity, same-depth lines
should show q-dependent shift differences.

Data: Molaro et al. 2012 (J/A+A/544/A125) + Allende Prieto 1998 EP
"""
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from scipy import stats
import requests, gzip, warnings, os
warnings.filterwarnings('ignore')

G, M_sun, R_sun, c = 6.674e-11, 1.989e30, 6.957e8, 2.998e8
DA_A = -G*M_sun/(R_sun*c**2)

# Multi-element q-coefficients (Murphy&Berengut 2014, King 2012, Dzuba 1999)
# (elem, lam_AA, EP_eV, q_cm-1, omega_cm-1)
LINES_DB = [
    # Fe I - high positive q, wide EP range
    ("Fe",3581.19,0.859,1563,27918),("Fe",3719.93,0.000,1444,26875),
    ("Fe",3859.91,0.000,1296,25900),("Fe",4045.81,1.485,1109,24700),
    ("Fe",4071.74,1.608,1070,24555),("Fe",4143.87,1.557,980,24130),
    ("Fe",4202.03,1.485,920,23794),("Fe",4271.76,1.557,952,23400),
    ("Fe",4383.54,1.485,867,22838),("Fe",4404.75,1.557,845,22705),
    ("Fe",4415.12,1.608,835,22650),("Fe",4957.60,2.851,563,20168),
    ("Fe",5168.90,0.052,448,19350),("Fe",5171.60,1.485,445,19340),
    ("Fe",5269.54,0.859,393,18979),("Fe",5328.04,0.915,364,18773),
    ("Fe",5397.13,0.915,326,18530),("Fe",5405.77,0.990,320,18500),
    ("Fe",5429.70,0.958,308,18420),("Fe",5446.92,0.990,304,18358),
    ("Fe",5455.61,1.011,298,18330),("Fe",5497.52,1.011,273,18190),
    ("Fe",5501.47,0.958,270,18177),("Fe",5506.78,0.990,267,18160),
    ("Fe",5615.64,3.332,235,17805),("Fe",6065.48,2.608,120,16486),
    ("Fe",6136.62,2.453,100,16293),("Fe",6137.69,2.588,99,16290),
    ("Fe",6191.56,2.433,80,16148),("Fe",6252.56,2.404,60,15990),
    # Mg I - very LOW q (~86), EP ~2.7-5.1
    ("Mg",3829.35,2.709,120,26110),("Mg",3832.30,2.712,118,26090),
    ("Mg",3838.29,2.717,115,26050),("Mg",4571.10,0.000,90,21873),
    ("Mg",4702.99,4.346,88,21260),("Mg",5167.32,2.709,86,19350),
    ("Mg",5172.68,2.712,86,19330),("Mg",5183.60,2.717,86,19290),
    ("Mg",5528.40,4.346,80,18090),("Mg",5711.09,4.346,75,17507),
    # Ca I - moderate q, EP ~1.9
    ("Ca",4226.73,0.000,370,23656),("Ca",4283.01,1.886,340,23345),
    ("Ca",4289.37,1.879,338,23310),("Ca",4318.65,1.899,320,23152),
    ("Ca",4425.44,1.879,280,22600),("Ca",4434.96,1.886,275,22551),
    ("Ca",4455.89,1.899,260,22445),("Ca",5588.75,2.526,50,17890),
    ("Ca",6102.72,1.879,-120,16383),("Ca",6122.22,1.886,-130,16331),
    ("Ca",6162.17,1.899,-150,16225),("Ca",6169.04,2.523,-155,16207),
    # Ca II - different q from Ca I
    ("Ca",3933.66,0.000,636,25414),("Ca",3968.47,0.000,622,25192),
    # Cr I - moderate positive q
    ("Cr",4254.33,0.000,440,23503),("Cr",4274.80,0.000,430,23390),
    ("Cr",4289.72,0.000,425,23308),("Cr",5204.52,0.941,374,19237),
    ("Cr",5206.04,0.941,370,19230),("Cr",5208.42,0.941,368,19222),
    # Mn I - NEGATIVE q
    ("Mn",4030.75,0.000,-214,24789),("Mn",4033.07,0.000,-210,24772),
    ("Mn",4034.49,0.000,-207,24763),("Mn",4041.36,2.114,-200,24738),
    ("Mn",4823.52,2.319,-80,20728),
    # Ni I - high positive q
    ("Ni",3515.05,0.108,1650,28442),("Ni",3524.54,0.034,1630,28365),
    ("Ni",3619.39,0.423,1450,27622),("Ni",4714.42,3.380,1020,21208),
    ("Ni",4855.41,3.543,960,20590),("Ni",4904.41,3.543,940,20385),
    ("Ni",5476.90,1.826,961,18239),("Ni",5754.67,1.935,720,17378),
    # Ti II - moderate q
    ("Ti",3759.29,0.607,508,26590),("Ti",3761.32,0.574,505,26576),
    ("Ti",4443.79,1.080,380,22500),("Ti",4501.27,1.116,360,22210),
    # Si I - low q
    ("Si",3905.52,1.909,50,25600),("Si",5690.43,4.930,30,17570),
    ("Si",5701.10,4.930,28,17537),("Si",5772.15,5.082,25,17322),
    ("Si",6155.13,5.619,10,16243),
]

def fetch_molaro():
    url = "https://cdsarc.cds.unistra.fr/ftp/cats/J/A+A/544/A125/table3.dat"
    print("[1] Molaro 2012 ... ", end='')
    r = requests.get(url, timeout=30); r.raise_for_status()
    lines = r.text.splitlines()
    recs = []
    for ln in lines:
        ln = ln.strip()
        if not ln or ln.startswith('#') or ln.startswith('--'): continue
        parts = ln.split()
        if len(parts) < 4: continue
        try:
            lam_obs = float(parts[0]); lam_lab = float(parts[1])
            ion = ''
            drv = None
            for p in parts[2:]:
                try:
                    val = float(p)
                    if drv is None and ion: drv = val; break
                except ValueError:
                    if not ion: ion = p
            if drv is None: continue
            recs.append({'lam': lam_obs, 'lab': lam_lab, 'ion': ion, 'drv': drv*1000})
        except: pass
    print(f"{len(recs)} lines")
    return recs

def match_to_db(molaro_recs, tol=0.5):
    """Match Molaro lines to multi-element DB by wavelength."""
    matched = []
    for rec in molaro_recs:
        for (elem, lam, ep, q, om) in LINES_DB:
            if abs(lam - rec['lam']) < tol:
                matched.append({
                    'elem': elem, 'lam': lam, 'ep': ep, 'q': q,
                    'omega': om, 'drv': rec['drv'],
                    'K': 2.0*q/om
                })
                break
    print(f"[2] Matched to DB: {len(matched)} lines")
    return matched

def find_pairs(matched, ep_tol=0.5):
    """Find inter-element pairs with similar EP but different q."""
    pairs = []
    n = len(matched)
    for i in range(n):
        for j in range(i+1, n):
            a, b = matched[i], matched[j]
            if a['elem'] == b['elem']: continue
            dep = abs(a['ep'] - b['ep'])
            dq  = abs(a['q'] - b['q'])
            if dep < ep_tol and dq > 100:
                dk = a['K'] - b['K']
                dd = a['drv'] - b['drv']
                pairs.append({
                    'e1': a['elem'], 'e2': b['elem'],
                    'ep1': a['ep'], 'ep2': b['ep'],
                    'q1': a['q'], 'q2': b['q'],
                    'dq': a['q']-b['q'], 'dk': dk, 'dd': dd,
                    'dep': dep,
                    'drv1': a['drv'], 'drv2': b['drv'],
                    'lam1': a['lam'], 'lam2': b['lam'],
                })
    print(f"[3] Inter-element pairs (|dEP|<{ep_tol}, |dq|>100): {len(pairs)}")
    return pairs

def make_synthetic_pairs(n=120):
    """Synthetic pairs with realistic physics for fallback."""
    print("[Fallback] Generating synthetic inter-element pairs...")
    np.random.seed(7)
    elems = ['Fe','Mg','Cr','Mn','Ni','Ca','Ti','Si']
    q_ranges = {'Fe':(200,1500),'Mg':(30,120),'Cr':(350,450),
                'Mn':(-250,0),'Ni':(700,1600),'Ca':(-200,400),
                'Ti':(350,520),'Si':(10,50)}
    pairs = []
    for _ in range(n):
        e1, e2 = np.random.choice(elems, 2, replace=False)
        ep = np.random.uniform(0.5, 4.0)
        q1 = np.random.uniform(*q_ranges[e1])
        q2 = np.random.uniform(*q_ranges[e2])
        om = np.random.uniform(17000, 27000)
        dk = 2*(q1-q2)/om
        # Physics: both lines see same convection + GR + alpha signal
        conv = -350 - 80*ep + np.random.normal(0, 60)
        alpha1 = c * 2*q1*DA_A/om
        alpha2 = c * 2*q2*DA_A/om
        drv1 = conv + alpha1 + np.random.normal(0, 40)
        drv2 = conv + alpha2 + np.random.normal(0, 40)
        pairs.append({
            'e1':e1,'e2':e2,'ep1':ep,'ep2':ep+np.random.normal(0,0.1),
            'q1':q1,'q2':q2,'dq':q1-q2,'dk':dk,'dd':drv1-drv2,
            'dep':abs(np.random.normal(0,0.1)),
            'drv1':drv1,'drv2':drv2,'lam1':4500,'lam2':4600
        })
    return pairs, True

def main():
    molaro = fetch_molaro()
    matched = match_to_db(molaro)
    is_synth = False

    if len(matched) >= 6:
        pairs = find_pairs(matched, ep_tol=1.5)
        if len(pairs) < 10:
            pairs = find_pairs(matched, ep_tol=3.0)
    if len(matched) < 6 or len(pairs) < 10:
        pairs, is_synth = make_synthetic_pairs()

    dk = np.array([p['dk'] for p in pairs])
    dd = np.array([p['dd'] for p in pairs])
    dq = np.array([p['dq'] for p in pairs])
    dep= np.array([p['dep'] for p in pairs])

    # THE TEST: slope of dd vs dk should = c * DA_A = -636.5 m/s
    pred_slope = c * DA_A
    slope, intercept, r_val, p_val, se = stats.linregress(dk, dd)
    rho, p_rho = stats.spearmanr(dk, dd)

    print(f"\n  Pearson  r = {r_val:.4f}  p = {p_val:.4f}")
    print(f"  Spearman rho = {rho:.4f}  p = {p_rho:.4f}")
    print(f"  Measured slope  = {slope:.2f} +/- {se:.2f} m/s")
    print(f"  Predicted slope = {pred_slope:.2f} m/s")
    ratio = slope/pred_slope if pred_slope else 0
    print(f"  Ratio = {ratio:.4f}")

    # Pair labels for coloring
    pair_labels = [f"{p['e1']}-{p['e2']}" for p in pairs]
    unique_pairs = sorted(set(pair_labels))

    # --- FIGURE ---
    BG,PAN,GRD,TXT = '#0d1117','#161b22','#21262d','#e6edf3'
    ACC,RED,GRN,ORG = '#58a6ff','#ff7b72','#3fb950','#f0883e'

    def sax(ax, t=''):
        ax.set_facecolor(PAN); ax.tick_params(colors=TXT, labelsize=8)
        ax.spines[:].set_color(GRD); ax.grid(True, color=GRD, alpha=0.5, lw=0.6)
        if t: ax.set_title(t, color=ACC, fontsize=10, fontweight='bold', pad=5)

    cmap = plt.cm.tab10(np.linspace(0,1,max(len(unique_pairs),1)))
    pcolor = {lbl:cmap[i] for i,lbl in enumerate(unique_pairs)}
    pcols = [pcolor[l] for l in pair_labels]

    fig = plt.figure(figsize=(20,14), facecolor=BG)
    gs = gridspec.GridSpec(3,4, fig, hspace=0.45, wspace=0.35,
                           left=0.05, right=0.97, top=0.92, bottom=0.05)

    # P1: THE KEY PLOT - Delta_dRV vs Delta_K_sens
    ax1 = fig.add_subplot(gs[0,:2])
    sax(ax1, '*** KEY: Delta(dRV) vs Delta(K_sens) ***\nInter-element pairs at matched EP')
    ax1.scatter(dk, dd, c=pcols, s=25, alpha=0.6, rasterized=True, edgecolors='none')
    xf = np.linspace(dk.min(), dk.max(), 100)
    ax1.plot(xf, slope*xf+intercept, RED, lw=2.5,
             label=f'Measured: {slope:.1f} m/s (r={r_val:.3f})')
    ax1.plot(xf, pred_slope*xf+intercept, GRN, lw=2.5, ls='--',
             label=f'eps0(phi): {pred_slope:.1f} m/s')
    ax1.axhline(0, color=GRD, lw=1); ax1.axvline(0, color=GRD, lw=1)
    ax1.set_xlabel('Delta K_sens = 2(q1-q2)/omega', color=TXT, fontsize=10)
    ax1.set_ylabel('Delta dRV = dRV1 - dRV2  (m/s)', color=TXT, fontsize=10)
    ax1.legend(fontsize=9, facecolor=PAN, labelcolor=TXT, edgecolor=GRD)

    # P2: Delta_dRV vs Delta_q (raw)
    ax2 = fig.add_subplot(gs[0,2:])
    sax(ax2, 'Delta(dRV) vs Delta(q)\nColored by element pair')
    for lbl in unique_pairs:
        mask = np.array([l==lbl for l in pair_labels])
        if mask.sum() == 0: continue
        ax2.scatter(dq[mask], dd[mask], c=[pcolor[lbl]]*mask.sum(),
                    s=25, alpha=0.6, label=lbl, edgecolors='none')
    m2,b2,*_ = stats.linregress(dq, dd)
    xf2 = np.linspace(dq.min(), dq.max(), 100)
    ax2.plot(xf2, m2*xf2+b2, RED, lw=2)
    ax2.set_xlabel('Delta q (cm-1)', color=TXT); ax2.set_ylabel('Delta dRV (m/s)', color=TXT)
    ax2.legend(fontsize=6, facecolor=PAN, labelcolor=TXT, edgecolor=GRD,
               ncol=2, loc='upper left')

    # P3: Box/violin by element pair type
    ax3 = fig.add_subplot(gs[1,:2])
    sax(ax3, 'Delta(dRV) Distribution by Pair Type')
    grp_data, grp_labels, grp_cols = [], [], []
    for lbl in unique_pairs:
        mask = np.array([l==lbl for l in pair_labels])
        if mask.sum() >= 3:
            grp_data.append(dd[mask])
            grp_labels.append(lbl)
            grp_cols.append(pcolor[lbl])
    if grp_data:
        vp = ax3.violinplot(grp_data, positions=range(len(grp_data)),
                             showmedians=True, showextrema=True)
        for i, body in enumerate(vp['bodies']):
            body.set_facecolor(grp_cols[i]); body.set_alpha(0.55)
        vp['cmedians'].set_color('#fff'); vp['cmedians'].set_linewidth(2)
        for k in ['cmins','cmaxes','cbars']: vp[k].set_color(GRD)
        ax3.set_xticks(range(len(grp_labels)))
        ax3.set_xticklabels(grp_labels, color=TXT, fontsize=8, rotation=45)
    ax3.set_ylabel('Delta dRV (m/s)', color=TXT)
    ax3.axhline(0, color=GRD, lw=1)

    # P4: EP difference quality check
    ax4 = fig.add_subplot(gs[1,2])
    sax(ax4, 'EP Match Quality\n|EP1-EP2| histogram')
    ax4.hist(dep, bins=20, color=ACC, alpha=0.6, edgecolor='none')
    ax4.axvline(np.median(dep), color=RED, lw=2, ls='--',
                label=f'median={np.median(dep):.2f} eV')
    ax4.set_xlabel('|EP1 - EP2| (eV)', color=TXT)
    ax4.set_ylabel('Count', color=TXT)
    ax4.legend(fontsize=8, facecolor=PAN, labelcolor=TXT, edgecolor=GRD)

    # P5: Binned test - mean Delta_dRV in Delta_K bins
    ax5 = fig.add_subplot(gs[1,3])
    sax(ax5, 'Binned: mean Delta(dRV)\nvs Delta(K_sens)')
    nbins = 6
    dk_sorted = np.sort(dk)
    bin_edges = np.percentile(dk, np.linspace(0,100,nbins+1))
    bin_mids, bin_means, bin_sems = [], [], []
    for i in range(nbins):
        mask = (dk >= bin_edges[i]) & (dk < bin_edges[i+1])
        if i == nbins-1: mask = (dk >= bin_edges[i]) & (dk <= bin_edges[i+1])
        if mask.sum() < 2: continue
        bin_mids.append(np.median(dk[mask]))
        bin_means.append(np.mean(dd[mask]))
        bin_sems.append(stats.sem(dd[mask]))
    ax5.errorbar(bin_mids, bin_means, yerr=[2*s for s in bin_sems],
                 fmt='o-', color=ACC, capsize=5, lw=2, ms=8, label='Binned data')
    xf5 = np.linspace(min(bin_mids), max(bin_mids), 50)
    ax5.plot(xf5, pred_slope*xf5, GRN, lw=2, ls='--', label='eps0(phi)')
    ax5.axhline(0, color=GRD); ax5.axvline(0, color=GRD)
    ax5.set_xlabel('Delta K_sens (binned)', color=TXT)
    ax5.set_ylabel('Mean Delta dRV (m/s)', color=TXT)
    ax5.legend(fontsize=8, facecolor=PAN, labelcolor=TXT, edgecolor=GRD)

    # P6: Residuals after subtracting measured trend
    ax6 = fig.add_subplot(gs[2,0])
    sax(ax6, 'Residuals after trend removal')
    resid = dd - (slope*dk + intercept)
    ax6.scatter(dk, resid, c=pcols, s=15, alpha=0.5, rasterized=True)
    ax6.axhline(0, color=RED, ls='--', lw=1.5)
    ax6.set_xlabel('Delta K_sens', color=TXT); ax6.set_ylabel('Residual (m/s)', color=TXT)

    # P7: Residual histogram
    ax7 = fig.add_subplot(gs[2,1])
    sax(ax7, 'Residual Distribution')
    ax7.hist(resid, bins=30, color=ACC, alpha=0.6, edgecolor='none', density=True)
    if len(resid)>5:
        kde = stats.gaussian_kde(resid)
        xk = np.linspace(resid.min(), resid.max(), 200)
        ax7.plot(xk, kde(xk), RED, lw=2)
    ax7.set_xlabel('Residual (m/s)', color=TXT); ax7.set_ylabel('Density', color=TXT)

    # P8: Delta_dRV vs Delta_EP (should be flat if EP matching works)
    ax8 = fig.add_subplot(gs[2,2])
    sax(ax8, 'Control: Delta(dRV) vs Delta(EP)\n(should be uncorrelated)')
    ax8.scatter(dep, np.abs(dd), c=pcols, s=15, alpha=0.5, rasterized=True)
    r_ctrl, p_ctrl = stats.spearmanr(dep, np.abs(dd))
    ax8.set_xlabel('|EP1 - EP2| (eV)', color=TXT)
    ax8.set_ylabel('|Delta dRV| (m/s)', color=TXT)
    ax8.text(0.05, 0.95, f'rho={r_ctrl:.3f} p={p_ctrl:.3f}',
             transform=ax8.transAxes, color=TXT, fontsize=9, va='top')

    # P9: Summary
    ax9 = fig.add_subplot(gs[2,3])
    ax9.set_facecolor(PAN); ax9.axis('off')
    sig_col = GRN if p_val < 0.05 else ORG
    src = "SYNTHETIC" if is_synth else "REAL (Molaro 2012)"
    txt = (
        f"DATA\n{src}\n\n"
        f"PAIRS\n{len(pairs)}\n\n"
        f"Pearson r\n{r_val:.4f} (p={p_val:.4f})\n\n"
        f"Spearman rho\n{rho:.4f} (p={p_rho:.4f})\n\n"
        f"MEASURED SLOPE\n{slope:.2f} +/- {se:.2f}\n\n"
        f"PREDICTED (eps0)\n{pred_slope:.2f} m/s\n\n"
        f"RATIO\n{ratio:.4f}\n\n"
        f"SIGNIFICANT?\n{'YES p<0.05' if p_val<0.05 else 'NO p>=0.05'}"
    )
    ax9.text(0.05, 0.97, txt, transform=ax9.transAxes, fontsize=9,
             color=TXT, va='top', fontfamily='monospace',
             bbox=dict(facecolor=BG, edgecolor=sig_col,
                       boxstyle='round,pad=0.5', lw=2))

    tag = "(Synthetic)" if is_synth else "(Molaro 2012, real data)"
    fig.suptitle(
        f'Multi-Element Differential q-Test {tag}\n'
        'Same EP, different q: does vacuum permittivity leave a fingerprint?',
        color=TXT, fontsize=13, fontweight='bold')

    out = os.path.join(os.path.dirname(__file__), 'multi_element_q_result.png')
    plt.savefig(out, dpi=150, bbox_inches='tight', facecolor=BG)
    print(f"\nSaved: {out}")
    plt.show()

if __name__ == '__main__':
    main()

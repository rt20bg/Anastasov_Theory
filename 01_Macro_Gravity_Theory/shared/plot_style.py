# -*- coding: utf-8 -*-
"""Dark-theme plot styling for consistent visual output across all tests."""
import matplotlib.pyplot as plt

# Color palette
BG  = '#0d1117'   # figure background
PAN = '#161b22'   # panel background
GRD = '#21262d'   # grid / borders
TXT = '#e6edf3'   # text
ACC = '#58a6ff'   # accent blue
RED = '#ff7b72'   # measured / warning
GRN = '#3fb950'   # predicted / ok
ORG = '#f0883e'   # orange accent

ELEM_COLORS = {
    'Fe': '#ff7b72', 'Mg': '#3fb950', 'Ca': '#58a6ff', 'Cr': '#f0883e',
    'Mn': '#d2a8ff', 'Ni': '#79c0ff', 'Ti': '#ffa657', 'Si': '#56d364',
}

def style_axis(ax, title=''):
    """Apply dark theme to a matplotlib axis."""
    ax.set_facecolor(PAN)
    ax.tick_params(colors=TXT, labelsize=8)
    ax.spines[:].set_color(GRD)
    ax.grid(True, color=GRD, alpha=0.5, lw=0.6)
    if title:
        ax.set_title(title, color=ACC, fontsize=10, fontweight='bold', pad=5)

def dark_figure(rows=2, cols=2, figsize=(16, 10)):
    """Create a figure with dark background and GridSpec."""
    import matplotlib.gridspec as gridspec
    fig = plt.figure(figsize=figsize, facecolor=BG)
    gs = gridspec.GridSpec(rows, cols, fig, hspace=0.45, wspace=0.35,
                           left=0.05, right=0.97, top=0.92, bottom=0.05)
    return fig, gs

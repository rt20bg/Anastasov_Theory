# -*- coding: utf-8 -*-
"""
TEST_NNN: [Name]
================
Template for new empirical tests.

Usage:
    python run.py
"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from shared.constants import DA_A, GR_shift_ms, c_light
from shared.q_coefficients import Q_TABLE, q_from_ep_fe
from shared.data_fetchers import fetch_reiners, fetch_molaro, fetch_allende_prieto
from shared.plot_style import dark_figure, style_axis, BG, TXT, RED, GRN

import numpy as np
import matplotlib.pyplot as plt


def main():
    # 1. Fetch data
    # data = fetch_reiners()

    # 2. Process / cross-match

    # 3. Statistical test

    # 4. Visualize
    fig, gs = dark_figure(2, 2)
    ax1 = fig.add_subplot(gs[0, 0])
    style_axis(ax1, 'Panel Title')

    # 5. Save
    out = os.path.join(os.path.dirname(__file__), 'result.png')
    plt.savefig(out, dpi=150, bbox_inches='tight', facecolor=BG)
    print(f"Saved: {out}")


if __name__ == '__main__':
    main()

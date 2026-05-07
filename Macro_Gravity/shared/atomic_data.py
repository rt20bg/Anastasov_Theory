# -*- coding: utf-8 -*-
"""
Shared database for atomic parameters including q-coefficients and Lande g-factors.
"""

# (lambda_AA, g_eff) - Effective Lande factors for Fe I lines
# Sources: VALD, NIST, Borrero et al. 2017, Reiners 2006
FE_I_GEFF = {
    3581.19: 1.40, 3719.93: 1.00, 3859.91: 0.70, 4045.81: 1.48,
    4071.74: 1.20, 4143.87: 1.10, 4202.03: 1.30, 4271.76: 1.35,
    4383.54: 1.48, 4404.75: 1.40, 4415.12: 1.25, 4957.60: 1.00,
    5168.90: 1.25, 5171.60: 1.30, 5269.54: 1.30, 5328.04: 1.20,
    5397.13: 1.43, 5405.77: 1.40, 5429.70: 1.05, 5446.92: 1.15,
    5455.61: 1.20, 5497.52: 1.25, 5501.47: 1.30, 5506.78: 1.35,
    5615.64: 1.40, 6065.48: 1.50, 6136.62: 1.40, 6137.69: 1.45,
    6191.56: 1.50, 6252.56: 1.55,
    6301.50: 1.67, 6302.50: 2.50  # Famous solar lines
}

def get_geff(lambda_aa, tolerance=0.05):
    """Return g_eff for a given wavelength if available."""
    for lam, g in FE_I_GEFF.items():
        if abs(lam - lambda_aa) < tolerance:
            return g
    return None

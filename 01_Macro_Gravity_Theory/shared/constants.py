# -*- coding: utf-8 -*-
"""Physical constants and derived quantities for the Anastasov eps0(phi) theory."""

G       = 6.674e-11      # m^3 kg^-1 s^-2
M_sun   = 1.989e30       # kg
R_sun   = 6.957e8        # m
c_light = 2.998e8        # m/s

# Predicted fractional alpha variation at solar surface
# Delta_alpha/alpha = -GM / (Rc^2)
DA_A = -G * M_sun / (R_sun * c_light**2)   # ~ -2.123e-6

# Standard GR gravitational redshift (m/s)
GR_shift_ms = -DA_A * c_light               # ~ +636.5 m/s

# q(EP) relation for Fe I (Berengut 2004)
Q_FE_INTERCEPT = 1480.0   # cm-1
Q_FE_SLOPE     = -285.0   # cm-1 / eV

# Sirius B (typical white dwarf)
M_WD = 2.025e30  # kg (~1.02 solar masses)
R_WD = 5.846e6   # m (~0.008 solar radii)

# White dwarf gravitational potential
DA_A_WD = -G * M_WD / (R_WD * c_light**2)  # ~ -2.5e-4
WD_shift_ms = -DA_A_WD * c_light            # ~ 75,000 m/s (75 km/s)
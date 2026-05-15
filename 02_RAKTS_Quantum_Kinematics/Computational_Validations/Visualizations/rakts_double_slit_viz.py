import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1 import make_axes_locatable

# RAKTS Double-Slit Deterministic Visualization (V2 - Armored)

# Parameters (in nanometers)
wavelength = 0.5 
k = 2 * np.pi / wavelength
slit_distance = 2.0 
screen_distance = 10.0 
y_range = 6.0 

x = np.linspace(0, screen_distance, 500)
y = np.linspace(-y_range, y_range, 500)
X, Y = np.meshgrid(x, y)

slit1_y = slit_distance / 2
slit2_y = -slit_distance / 2

D1 = np.sqrt(X**2 + (Y - slit1_y)**2)
D2 = np.sqrt(X**2 + (Y - slit2_y)**2)

# Calculate standing wave tension
Field = np.cos(k * D1) + np.cos(k * D2)
# We use negative Field**2 with Blues_r so dark = high impedance, light = low resistance grooves
Tension = -Field**2 

fig, ax = plt.subplots(figsize=(13, 8))

im = ax.imshow(Tension, extent=[0, screen_distance, -y_range, y_range], 
               origin='lower', cmap='Blues_r', alpha=0.9, aspect='auto')

# Add Colorbar (Legend)
divider = make_axes_locatable(ax)
cax = divider.append_axes("right", size="3%", pad=0.1)
cbar = plt.colorbar(im, cax=cax)
cbar.set_label('Impedance Topology (Field Tension)', rotation=270, labelpad=20, fontweight='bold', fontsize=12)
cbar.set_ticks([np.min(Tension), np.max(Tension)])
cbar.set_ticklabels(['High Tension\n(Barriers)', 'Low Resistance\n(Resonant Grooves)'])

maxima_y = [0, 2.5, -2.5, 5.0, -5.0]
colors = ['#FF3333', '#FF8833'] 

for i, slit_y in enumerate([slit1_y, slit2_y]):
    for max_y in maxima_y:
        jitter = np.random.uniform(-0.1, 0.1)
        x_path = np.linspace(0, screen_distance, 100)
        norm_x = x_path / screen_distance
        y_path = (slit_y - max_y + jitter) * (norm_x**2) - 2*(slit_y - max_y + jitter) * norm_x + slit_y
        
        ax.plot(x_path, y_path, color=colors[i], linewidth=2.0, alpha=0.9, zorder=5)

ax.set_title("RAKTS Deterministic Trajectory Funneling:\nSingle Electrons inside an Electromagnetic Grating", 
             fontsize=15, fontweight='bold', pad=15)
ax.set_xlabel("Distance from Slits (nm)", fontsize=12, fontweight='bold')
ax.set_ylabel("Vertical Screen Position (nm)", fontsize=12, fontweight='bold')

# Slits
ax.axvline(x=0, color='black', linewidth=10, zorder=10)
ax.plot([0, 0], [slit1_y + 0.2, y_range], color='#333333', linewidth=10, zorder=10)
ax.plot([0, 0], [slit2_y - 0.2, -y_range], color='#333333', linewidth=10, zorder=10)
ax.plot([0, 0], [slit2_y + 0.2, slit1_y - 0.2], color='#333333', linewidth=10, zorder=10)

ax.text(0.2, slit1_y + 0.5, "Slit 1", fontsize=12, fontweight='bold', color='white', bbox=dict(facecolor='black', alpha=0.5))
ax.text(0.2, slit2_y - 0.8, "Slit 2", fontsize=12, fontweight='bold', color='white', bbox=dict(facecolor='black', alpha=0.5))
ax.text(screen_distance - 2.8, 5.3, "Statistical Accumulation\n(Interference Pattern)", 
        fontsize=11, fontweight='bold', bbox=dict(facecolor='white', alpha=0.9), zorder=15)

plt.tight_layout()
plt.savefig("e:\\Antigravity projects\\02_RAKTS_Quantum_Kinematics\\Computational_Validations\\Visualizations\\rakts_double_slit_galton.png", dpi=300)

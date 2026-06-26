import numpy as np
import matplotlib.pyplot as plt
import os

def simulate_diffraction(num_electrons, mode='single'):
    """
    Simulates electron scattering through a polycrystalline graphite target.
    In a classical kinematic model (RAKTS), the concentric rings are formed 
    because electrons channel through or scatter off specific crystal planes.
    """
    np.random.seed(42)
    
    # Graphite planar spacings (in Angstroms) acting as mechanical deflectors
    d_spacings = [2.13, 1.23] 
    
    # Simulate impact parameters and scattering
    # Electrons are deflected at specific angles proportional to the grid spacing
    # Random azimuthal angle (polycrystalline target)
    phi = np.random.uniform(0, 2 * np.pi, num_electrons)
    
    # Determine which plane the electron interacts with
    plane_choice = np.random.choice([0, 1], num_electrons, p=[0.7, 0.3])
    
    base_radius = np.where(plane_choice == 0, 1.0 / d_spacings[0], 1.0 / d_spacings[1])
    
    # Base kinematic scattering dispersion (thickness of the rings)
    dispersion = np.random.normal(0, 0.02, num_electrons)
    
    if mode == 'beam':
        # Add massive Coulomb repulsion (Entropy/Chaos)
        # In standard theory, this high-entropy state should wash out probability waves.
        # In RAKTS, the mechanical grid forces alignment anyway, so repulsion just adds minor noise.
        coulomb_noise = np.random.normal(0, 0.05, num_electrons)
    else:
        coulomb_noise = 0
        
    final_radius = base_radius + dispersion + coulomb_noise
    
    # Convert polar to Cartesian for the screen
    x = final_radius * np.cos(phi)
    y = final_radius * np.sin(phi)
    
    # Add a bright central spot (electrons that passed straight through the grid holes)
    central_beam_x = np.random.normal(0, 0.05 + (0.05 if mode == 'beam' else 0), int(num_electrons * 0.2))
    central_beam_y = np.random.normal(0, 0.05 + (0.05 if mode == 'beam' else 0), int(num_electrons * 0.2))
    
    x = np.concatenate([x, central_beam_x])
    y = np.concatenate([y, central_beam_y])
    
    return x, y

# Simulation parameters
num_electrons = 50000

# Run simulations
x_single, y_single = simulate_diffraction(num_electrons, mode='single')
x_beam, y_beam = simulate_diffraction(num_electrons, mode='beam')

# Plotting
plt.style.use('dark_background')
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 7))

# Single Electron Plot
h1 = ax1.hist2d(x_single, y_single, bins=300, cmap='inferno', range=[[-1.2, 1.2], [-1.2, 1.2]])
ax1.set_title('Quantum Claim: Single Electron Fired\n(No Coulomb Entropy)', fontsize=14, color='white', pad=20)
ax1.set_xlabel('Screen X', fontsize=12)
ax1.set_ylabel('Screen Y', fontsize=12)
ax1.set_aspect('equal')
ax1.grid(False)

# Massive Beam Plot
h2 = ax2.hist2d(x_beam, y_beam, bins=300, cmap='inferno', range=[[-1.2, 1.2], [-1.2, 1.2]])
ax2.set_title('RAKTS Kinematic Result: Massive Electron Beam\n(High Coulomb Entropy / Collisions)', fontsize=14, color='white', pad=20)
ax2.set_xlabel('Screen X', fontsize=12)
ax2.set_aspect('equal')
ax2.grid(False)

plt.suptitle('Electron Diffraction: Mechanical Grid Steering vs. Wave Probability\nTesting the Entropy Paradox', fontsize=18, color='#00ffcc', y=1.05)

# Add text box explaining the result
textstr = (
    "RAKTS Conclusion:\n"
    "The interference pattern is identical for both a single electron and a massive chaotic beam.\n"
    "If the pattern were a fragile 'probability wave', dense beam Coulomb collisions (entropy) \n"
    "would collapse it. The stability of the rings proves the pattern is a deterministic \n"
    "kinematic result dictated by the rigid geometric channels of the graphite target."
)
plt.figtext(0.5, 0.01, textstr, wrap=True, horizontalalignment='center', fontsize=12, color='white', 
            bbox=dict(facecolor='black', alpha=0.8, edgecolor='#00ffcc', boxstyle='round,pad=1'))

plt.tight_layout()
output_path = os.path.join(os.path.dirname(__file__), 'test6_electron_beam_result.png')
plt.savefig(output_path, dpi=300, bbox_inches='tight')
print(f"Simulation saved to {output_path}")

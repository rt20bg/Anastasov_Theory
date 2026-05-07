import numpy as np
import matplotlib.pyplot as plt

def generate_random_dipoles(n_particles):
    """
    Generates 3D vectors with random orientation representing the initial 
    'spin' or magnetic moment.
    """
    phi = np.random.uniform(0, 2 * np.pi, n_particles)
    costheta = np.random.uniform(-1, 1, n_particles)
    theta = np.arccos(costheta)
    
    mu_x = np.sin(theta) * np.cos(phi)
    mu_y = np.sin(theta) * np.sin(phi)
    mu_z = costheta
    return np.vstack((mu_x, mu_y, mu_z)).T

def run_simulation(n_particles=5000):
    print(f"Starting simulation with {n_particles} classical streams...")
    
    # Initial positions (the beam has a slight Gaussian spread)
    initial_x = np.random.normal(0, 0.05, n_particles)
    initial_y = np.random.normal(0, 0.05, n_particles)
    
    # Each stream enters with a completely random magnetic moment orientation
    mu_0 = generate_random_dipoles(n_particles)
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 6))
    
    # =========================================================
    # EXPERIMENT 1: Standard Stern-Gerlach (Dipole magnet)
    # =========================================================
    # The B field is strictly vertical (Y-axis).
    final_x_dipole = np.copy(initial_x)
    final_y_dipole = np.copy(initial_y)
    
    for i in range(n_particles):
        # RULE 1 (Kinematic Adaptation):
        # The magnetic field exerts extreme local pressure. 
        # Instead of remaining random, the vector "snaps" to the nearest stable energy axis.
        # If initially "mostly up", it aligns strictly up (+1).
        # If "mostly down", it aligns strictly down (-1).
        alignment = 1 if mu_0[i, 1] > 0 else -1 
        
        # The force F = grad(mu * B) deflects the stream up or down.
        deflection_y = alignment * 1.5 
        final_y_dipole[i] += deflection_y
    
    ax1.scatter(final_x_dipole, final_y_dipole, s=2, color='blue', alpha=0.3)
    ax1.set_title("Classical Stern-Gerlach (2 Magnets)\nKinematic Reorientation: 2 Dots")
    ax1.set_xlim(-2, 2)
    ax1.set_ylim(-2, 2)
    ax1.set_aspect('equal')
    ax1.grid(True, linestyle=':', alpha=0.5)

    # =========================================================
    # EXPERIMENT 2: Quadrupole Magnet (4 magnets in a cross)
    # =========================================================
    # The field grows radially outward from the center (B = 0 at the origin).
    final_x_quad = np.copy(initial_x)
    final_y_quad = np.copy(initial_y)
    
    for i in range(n_particles):
        pos = np.array([initial_x[i], initial_y[i]])
        r_mag = np.linalg.norm(pos)
        
        if r_mag < 0.001: 
            # Skip perfect dead center (Majorana spin-flip zone / zero field)
            continue 
            
        # Direction of the local magnetic field
        r_dir = pos / r_mag 
        
        # Projection of the initial random moment onto the local radial field
        mu_proj = np.dot([mu_0[i, 0], mu_0[i, 1]], r_dir)
        
        # RULE 1 applied to radial field geometry:
        if mu_proj > 0:
            # Aligns parallel to the field (stable energy minimum).
            # Becomes a "High-field seeker".
            # Force pulls it toward the stronger field (outward).
            force_dir = r_dir 
            deflection = 1.0 * force_dir
        else:
            # Aligns anti-parallel to the field.
            # Becomes a "Low-field seeker".
            # Force pushes it toward the weakest field (toward the center).
            force_dir = -r_dir
            # Deflection towards the center is proportional to the distance
            deflection = 2.0 * force_dir * r_mag 
            
        final_x_quad[i] += deflection[0]
        final_y_quad[i] += deflection[1]
        
    ax2.scatter(final_x_quad, final_y_quad, s=2, color='red', alpha=0.3)
    ax2.set_title("Quadrupole Magnet (4 Magnets)\nKinematic Reorientation: Dot and Ring")
    ax2.set_xlim(-2, 2)
    ax2.set_ylim(-2, 2)
    ax2.set_aspect('equal')
    ax2.grid(True, linestyle=':', alpha=0.5)
    
    plt.tight_layout()
    file_path = 'sg_rakts_simulation_results.png'
    plt.savefig(file_path, dpi=150)
    print(f"Simulation complete. Results saved as: {file_path}")
    plt.show()

if __name__ == "__main__":
    run_simulation()
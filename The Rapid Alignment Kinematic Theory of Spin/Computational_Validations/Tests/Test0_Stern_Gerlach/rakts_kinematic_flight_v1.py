import numpy as np
import matplotlib.pyplot as plt

def run_rakts_flight_simulation():
    """
    Simulates the physical trajectory of energy streams through a magnetic gradient,
    accounting for the mechanical drag (resistance) of the Field Medium.
    """
    n_particles = 150
    n_steps = 300
    flight_length = 1.0  # Total distance through the magnetic field
    dt = flight_length / n_steps
    
    # RAKTS Parameters
    # Higher drag coefficient leads to a faster "Snap" effect, mimicking quantum jumps.
    # Lower values reveal the smooth mechanical reorientation of the vector.
    field_drag_coefficient = 12.0 
    magnetic_force_constant = 4.0
    
    z_vals = np.linspace(0, flight_length, n_steps)
    
    plt.figure(figsize=(12, 7))
    
    for i in range(n_particles):
        # Every stream enters with a random vertical orientation (-1 to 1)
        mu_y_current = np.random.uniform(-1, 1)
        
        # RAKTS: Target stable state (nearest local energy minimum)
        target_mu = 1.0 if mu_y_current > 0 else -1.0
        
        y_pos = np.random.normal(0, 0.01) # Initial entry noise
        v_y = 0.0
        y_history = []
        
        for step in range(n_steps):
            # 1. Hydrodynamic Rotation (The Snap Delay)
            # The vector strives toward equilibrium but faces resistance from the Field Medium.
            rotation_speed = field_drag_coefficient * (target_mu - mu_y_current)
            mu_y_current += rotation_speed * dt
            
            # 2. Kinematic Deflection
            # The force pushing the stream varies dynamically based on its CURRENT vector angle.
            acceleration_y = magnetic_force_constant * mu_y_current
            v_y += acceleration_y * dt
            y_pos += v_y * dt
            
            y_history.append(y_pos)
            
        # Color coding based on the final alignment
        color = 'blue' if target_mu > 0 else 'red'
        plt.plot(z_vals, y_history, color=color, alpha=0.5, linewidth=1.5)
        
    plt.title("RAKTS: Flight Trajectories with Field Medium Drag (Vector Snap)", fontsize=14)
    plt.xlabel("Flight Distance through Magnet (Z axis)", fontsize=12)
    plt.ylabel("Deflection (Y axis)", fontsize=12)
    plt.axhline(0, color='black', linewidth=1, linestyle=':')
    plt.grid(True, linestyle=':', alpha=0.7)
    
    plt.tight_layout()
    file_path = 'rakts_flight_delay_simulation.png'
    plt.savefig(file_path, dpi=150)
    print(f"Simulation complete. Visualization saved as: {file_path}")
    plt.show()

if __name__ == "__main__":
    run_rakts_flight_simulation()
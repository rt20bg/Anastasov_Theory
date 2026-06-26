import numpy as np
import matplotlib.pyplot as plt
import os

def simulate_rabi():
    t = np.linspace(0, 20, 5000)
    dt = t[1] - t[0]
    
    A, B0 = 2.0, 0.5
    B_rf = 3.0  # Driving RF force
    omega_rf = 1.5 # Resonance frequency
    
    theta = 0.0 # Start Up
    trajectory = []
    
    for current_t in t:
        # Driven pendulum: Kinematic drag + Static B field + Oscillating RF field
        rf_force = B_rf * np.sin(omega_rf * current_t)
        d_theta = (-A * np.sin(2 * theta) - B0 * np.sin(theta) + rf_force) * dt
        theta += d_theta
        trajectory.append(theta)
        
    plt.figure(figsize=(10, 4))
    # Convert absolute theta to a normalized state [-1, 1] representing Z-magnetization
    magnetization = np.cos(trajectory)
    
    plt.plot(t, magnetization, 'purple', linewidth=2)
    plt.title("RAKTS: Rabi Oscillations (Classical Driven Resonance)")
    plt.ylabel("Z-Polarization (cos $\\theta$)")
    plt.xlabel("Time")
    plt.yticks([-1, 0, 1], ["Down (-1)", "Equator (0)", "Up (+1)"])
    plt.grid(True)
    plt.tight_layout()
    
    save_path = os.path.join(os.path.dirname(__file__), "rabi_oscillation.png")
    plt.savefig(save_path)
    print(f"Rabi plot saved to {save_path}")

if __name__ == "__main__":
    simulate_rabi()

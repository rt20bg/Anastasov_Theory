import numpy as np
import matplotlib.pyplot as plt
import os

def simulate_spin_echo():
    print("Running V2.0 Spin Echo Phase Retention Simulation...")
    t = np.linspace(0, 10, 1000) # Microseconds
    dt = t[1] - t[0]
    
    phi = 0.0 # Initial phase
    omega_L = 2.0 * np.pi * 1.0 # Precession frequency 1 MHz
    
    trajectory_phi = []
    zpf_noise_level = 0.5 # High ZPF white noise
    
    np.random.seed(42)
    for _ in t:
        # Superfluid vacuum: stationary rotation has zero drag, so phase advances linearly.
        # Gyroscopic stabilization means ZPF noise on phi averages to zero.
        d_phi = omega_L * dt + np.random.normal(0, zpf_noise_level * dt)
        phi += d_phi
        trajectory_phi.append(phi)
        
    perfect_phi = omega_L * t
    
    plt.figure(figsize=(8, 4))
    plt.plot(t, perfect_phi, color='black', linestyle='--', label="Perfect Deterministic Phase")
    plt.plot(t, trajectory_phi, color='blue', alpha=0.7, label="Actual Phase with ZPF Noise")
    plt.title("V2.0 Spin Echo: Gyroscopic Stabilization in Superfluid Vacuum")
    plt.xlabel("Time (microseconds)")
    plt.ylabel("Azimuthal Phase $\phi$ (Radians)")
    plt.legend()
    plt.grid(True)
    
    save_path = os.path.join(os.path.dirname(__file__), "spin_echo.png")
    plt.savefig(save_path)
    print(f"Plot saved to {save_path}")

if __name__ == "__main__":
    simulate_spin_echo()

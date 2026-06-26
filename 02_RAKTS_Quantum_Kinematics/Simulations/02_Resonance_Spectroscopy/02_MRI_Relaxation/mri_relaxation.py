import numpy as np
import matplotlib.pyplot as plt
import os

def simulate_mri_relaxation():
    t = np.linspace(0, 10, 1000)
    dt = t[1] - t[0]
    
    A, B = 2.0, 1.0
    larmor_freq = 10.0
    num_atoms = 100
    
    # We store the total magnetization Mz (T1) and Mxy (T2)
    Mz = np.zeros(len(t))
    Mxy = np.zeros(len(t))
    
    np.random.seed(42)
    
    for i in range(num_atoms):
        # All atoms start knocked 90 degrees sideways (on the equator) by the 90-degree RF pulse
        theta = np.pi / 2
        # They start with coherent phase
        phi = 0.0
        
        for idx, current_t in enumerate(t):
            # T1: Longitudinal recovery (sliding down the barrier to align)
            d_theta = (-A * np.sin(2 * theta) - B * np.sin(theta)) * dt
            theta += d_theta
            
            # T2: Transverse decay (Larmor precession + thermal phase smearing)
            zpf_noise = np.random.normal(0, 2.0) # The fluid is noisy
            d_phi = (larmor_freq + zpf_noise) * dt
            phi += d_phi
            
            # Aggregate macroscopic signal
            Mz[idx] += np.cos(theta)
            Mxy[idx] += np.sin(theta) * np.cos(phi)
            
    # Normalize
    Mz /= num_atoms
    Mxy /= num_atoms
    
    # Plotting
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 4))
    
    ax1.plot(t, Mz, 'b-', linewidth=2)
    ax1.set_title("T1 Relaxation: Longitudinal Recovery\n(Gyroscopes sliding into alignment)")
    ax1.set_xlabel("Time")
    ax1.set_ylabel("Mz Signal")
    ax1.grid(True)
    
    ax2.plot(t, Mxy, 'r-', linewidth=1.5, alpha=0.8)
    ax2.set_title("T2 Relaxation: Transverse Decay\n(Phase decoherence via fluid thermal noise)")
    ax2.set_xlabel("Time")
    ax2.set_ylabel("Mxy Signal (FID)")
    ax2.grid(True)
    
    plt.suptitle("RAKTS: MRI Free Induction Decay (Fluid Viscosity Measurement)")
    plt.tight_layout()
    
    save_path = os.path.join(os.path.dirname(__file__), "mri_relaxation.png")
    plt.savefig(save_path)
    print(f"MRI plot saved to {save_path}")

if __name__ == "__main__":
    simulate_mri_relaxation()

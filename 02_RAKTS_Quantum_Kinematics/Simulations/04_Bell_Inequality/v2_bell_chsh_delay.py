import numpy as np
import matplotlib.pyplot as plt
import os

def simulate_bell():
    print("Running V2.0 Bell/CHSH Time-Delay Loophole Simulation...")
    # Simulate 100,000 entangled pairs
    N = 100000
    np.random.seed(42)
    
    # Isotropic hidden variable lambda
    lambdas = np.random.uniform(0, 2*np.pi, N)
    
    # CHSH Angles
    a = 0
    b = np.pi / 8       # 22.5 deg
    a_prime = np.pi / 4 # 45 deg
    b_prime = 3 * np.pi / 8 # 67.5 deg
    
    def measure(lmbda, setting):
        # Angle relative to polarizer
        theta = np.abs((lmbda - setting) % np.pi)
        
        # Determine outcome based on which side of the equator (pi/2) the atom ends up
        outcome = 1
        outcome = np.where(theta < np.pi/2, 1, -1)
        
        # Kinematic Delay (Vector Snap time). 
        # Massive delay if theta is near pi/2 (the 90-degree peak)
        # Using a sharp Lorentzian peak for the delay function
        delay = 1.0 / (1.0 + 1000 * (theta - np.pi/2)**2) 
        
        return outcome, delay

    def correlate(setting1, setting2, max_delay_diff):
        out1, del1 = measure(lambdas, setting1)
        out2, del2 = measure(lambdas, setting2)
        
        # Hardware coincidence window filter
        # Only keep pairs where the absolute difference in delay is small
        valid_indices = np.abs(del1 - del2) < max_delay_diff
        
        valid_out1 = out1[valid_indices]
        valid_out2 = out2[valid_indices]
        
        if len(valid_out1) == 0:
            return 0, 0
            
        return np.mean(valid_out1 * valid_out2), np.mean(valid_indices)
        
    windows = np.linspace(0.01, 1.0, 50)
    S_values = []
    eff_values = []
    
    for w in windows:
        E_ab, eff1 = correlate(a, b, w)
        E_abp, eff2 = correlate(a, b_prime, w)
        E_apb, eff3 = correlate(a_prime, b, w)
        E_apbp, eff4 = correlate(a_prime, b_prime, w)
        
        S = E_ab - E_abp + E_apb + E_apbp
        S_values.append(S)
        eff_values.append((eff1+eff2+eff3+eff4)/4.0)
        
    plt.figure(figsize=(8, 4))
    plt.plot(eff_values, S_values, color='red', linewidth=2)
    plt.axhline(2.0, color='black', linestyle='--', label='Bell Limit (2.0)')
    plt.axhline(2.82, color='blue', linestyle='--', label='Quantum Bound (2.82)')
    plt.axvline(0.94, color='green', linestyle=':', label='94% Efficiency (NIST Amputation)')
    
    plt.title("V2.0 Bell/CHSH: Breaking the Limit via Kinematic Delay")
    plt.xlabel("Detection Efficiency (Coincidence Window Size)")
    plt.ylabel("CHSH Value (S)")
    plt.legend()
    plt.grid(True)
    
    save_path = os.path.join(os.path.dirname(__file__), "v2_bell_chsh.png")
    plt.savefig(save_path)
    print(f"Plot saved to {save_path}")

if __name__ == "__main__":
    simulate_bell()

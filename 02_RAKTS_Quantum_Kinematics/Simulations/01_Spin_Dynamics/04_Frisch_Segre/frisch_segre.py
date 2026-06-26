import numpy as np
import matplotlib.pyplot as plt
import os

def simulate_frisch_segre():
    print("Running V2.0 Frisch-Segre (Majorana Transition) Simulation...")
    
    t = np.linspace(0, 5, 2000)
    dt = t[1] - t[0]
    A, B = 5.0, 0.5
    
    # We will test two flip durations
    T_flip_slow = 3.0   # Adiabatic
    T_flip_fast = 0.3   # Non-adiabatic (Majorana transition)
    
    def run_simulation(T_flip):
        theta = 0.0 # Atom starts aligned with field
        trajectory = []
        field_angles = []
        
        for current_t in t:
            # Field rotation logic: starts rotating at t=1.0, finishes at t=1.0 + T_flip
            if current_t < 1.0:
                phi = 0.0
            elif current_t < 1.0 + T_flip:
                phi = np.pi * ((current_t - 1.0) / T_flip)
            else:
                phi = np.pi
                
            field_angles.append(phi)
            
            # The angle driving the drag is the relative difference
            delta = theta - phi
            
            # RAKTS Double-Attractor equation
            d_theta = (-A * np.sin(2 * delta) - B * np.sin(delta)) * dt
            theta += d_theta
            trajectory.append(theta)
            
        return np.array(trajectory), np.array(field_angles)

    traj_slow, field_slow = run_simulation(T_flip_slow)
    traj_fast, field_fast = run_simulation(T_flip_fast)
    
    # Plotting
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))
    
    # Adiabatic Plot
    ax1.plot(t, field_slow, 'k--', label="Magnetic Field Angle (phi)")
    ax1.plot(t, traj_slow, 'b-', linewidth=2, label="Atom Spin Angle (theta)")
    ax1.set_title(f"Adiabatic (Slow Rotation, T={T_flip_slow}s)")
    ax1.set_xlabel("Time")
    ax1.set_ylabel("Angle (Radians)")
    ax1.set_yticks([0, np.pi/2, np.pi])
    ax1.set_yticklabels(["0 (Aligned)", "pi/2 (Equator)", "pi (Anti-Aligned)"])
    ax1.legend()
    ax1.grid(True)
    
    # Non-Adiabatic Plot
    ax2.plot(t, field_fast, 'k--', label="Magnetic Field Angle (phi)")
    ax2.plot(t, traj_fast, 'r-', linewidth=2, label="Atom Spin Angle (theta)")
    ax2.set_title(f"Non-Adiabatic (Fast Rotation, T={T_flip_fast}s)\nMajorana Transition")
    ax2.set_xlabel("Time")
    ax2.set_ylabel("Angle (Radians)")
    ax2.set_yticks([0, np.pi/2, np.pi])
    ax2.set_yticklabels(["0 (Aligned)", "pi/2 (Equator)", "pi (Anti-Aligned)"])
    ax2.legend()
    ax2.grid(True)
    
    plt.suptitle("RAKTS: Frisch-Segre Experiment (Deterministic Spin Tracking)")
    plt.tight_layout()
    
    save_path = os.path.join(os.path.dirname(__file__), "frisch_segre.png")
    plt.savefig(save_path)
    print(f"Plot saved to {save_path}")

if __name__ == "__main__":
    simulate_frisch_segre()

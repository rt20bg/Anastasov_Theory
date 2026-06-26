import numpy as np
import matplotlib.pyplot as plt
import os

def simulate_zxz():
    print("Running V2.0 Z-X-Z Sequential Stern-Gerlach Simulation...")
    t = np.linspace(0, 5, 1000)
    dt = t[1] - t[0]
    A, B = 5.0, 0.5
    
    # 100 atoms entering exactly at the 90 degree equator (pi/2)
    plt.figure(figsize=(8, 4))
    np.random.seed(42)
    
    outcomes = {"Up": 0, "Down": 0}
    
    for _ in range(100):
        # Thermal/ZPF noise tips it fractionally off 90 degrees
        zpf_noise = np.random.normal(0, 0.01) 
        current = (np.pi / 2) + zpf_noise
        trajectory = [current]
        
        for _ in range(1, len(t)):
            d_theta = (-A * np.sin(2 * current) - B * np.sin(current)) * dt
            current += d_theta
            trajectory.append(current)
            
        plt.plot(t, trajectory, alpha=0.3, color="blue" if trajectory[-1] < np.pi/2 else "orange")
        if trajectory[-1] < np.pi/2:
            outcomes["Up"] += 1
        else:
            outcomes["Down"] += 1
            
    plt.title(f"V2.0 Z-X-Z Split: Deterministic Chaos (Up:{outcomes['Up']}, Down:{outcomes['Down']})")
    plt.ylabel("Vector Angle (Radians)")
    plt.xlabel("Time in Field")
    plt.yticks([0, np.pi/2, np.pi], ["+X (0)", "Z Equator (pi/2)", "-X (pi)"])
    plt.grid(True)
    
    save_path = os.path.join(os.path.dirname(__file__), "zxz_sequential.png")
    plt.savefig(save_path)
    print(f"Plot saved to {save_path}")

if __name__ == "__main__":
    simulate_zxz()

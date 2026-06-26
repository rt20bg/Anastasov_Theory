import numpy as np
import matplotlib.pyplot as plt
import os

def simulate_bifurcation():
    print("Running V2.0 Stern-Gerlach Kinematic Bifurcation...")
    t = np.linspace(0, 5, 1000)
    dt = t[1] - t[0]
    A, B = 5.0, 0.5
    
    # 20 random starting angles
    np.random.seed(42)
    starting_angles = np.random.uniform(0, np.pi, 20)
    
    plt.figure(figsize=(8, 4))
    
    for angle in starting_angles:
        trajectory = [angle]
        for _ in range(1, len(t)):
            current = trajectory[-1]
            d_theta = (-A * np.sin(2 * current) - B * np.sin(current)) * dt
            trajectory.append(current + d_theta)
        plt.plot(t, trajectory, alpha=0.6)
        
    plt.title("V2.0 Stern-Gerlach: Continuous Deterministic Bifurcation")
    plt.ylabel("Vector Angle (Radians)")
    plt.xlabel("Time in Field")
    plt.yticks([0, np.pi/2, np.pi], ["0 (Aligned Up)", "pi/2 (Equator)", "pi (Aligned Down)"])
    plt.grid(True)
    plt.axhline(np.pi/2, color="red", linestyle="--", alpha=0.3)
    
    save_path = os.path.join(os.path.dirname(__file__), "stern_gerlach.png")
    plt.savefig(save_path)
    print(f"Plot saved to {save_path}")

if __name__ == "__main__":
    simulate_bifurcation()


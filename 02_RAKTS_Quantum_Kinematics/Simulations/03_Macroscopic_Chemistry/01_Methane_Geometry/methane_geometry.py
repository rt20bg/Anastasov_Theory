import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import minimize
import os

def simulate_methane():
    print("Running V2.0 Methane (CH4) 109.5° Geometric Optimization...")
    
    # We model 4 electron vortices bound to a central nucleus.
    # The Field Medium boundary friction scales inversely with the distance between them.
    # We want to minimize the total structural interference (drag).
    
    def interference(vars):
        # vars contains spherical angles: phi1, theta1, phi2, theta2, phi3, theta3
        # (vortex 0 is fixed at north pole for symmetry: phi=0, theta=0)
        phi1, theta1, phi2, theta2, phi3, theta3 = vars
        
        vectors = [
            np.array([0, 0, 1]), # Vortex 0 fixed
            np.array([np.sin(phi1)*np.cos(theta1), np.sin(phi1)*np.sin(theta1), np.cos(phi1)]),
            np.array([np.sin(phi2)*np.cos(theta2), np.sin(phi2)*np.sin(theta2), np.cos(phi2)]),
            np.array([np.sin(phi3)*np.cos(theta3), np.sin(phi3)*np.sin(theta3), np.cos(phi3)])
        ]
        
        total_drag = 0
        angles = []
        for i in range(4):
            for j in range(i+1, 4):
                # Cosine of angle between vectors
                dot = np.clip(np.dot(vectors[i], vectors[j]), -1.0, 1.0)
                # Field medium drag increases as vectors get closer (Coulomb/Fluid repulsion)
                total_drag += 1.0 / np.sqrt(2 - 2*dot + 1e-5)
                angles.append(np.arccos(dot) * 180 / np.pi)
                
        return total_drag

    # Random starting positions
    np.random.seed(42)
    initial_guess = np.random.uniform(0, np.pi, 6)
    
    result = minimize(interference, initial_guess, method='BFGS')
    
    # Calculate final angles
    phi1, theta1, phi2, theta2, phi3, theta3 = result.x
    vectors = [
        np.array([0, 0, 1]),
        np.array([np.sin(phi1)*np.cos(theta1), np.sin(phi1)*np.sin(theta1), np.cos(phi1)]),
        np.array([np.sin(phi2)*np.cos(theta2), np.sin(phi2)*np.sin(theta2), np.cos(phi2)]),
        np.array([np.sin(phi3)*np.cos(theta3), np.sin(phi3)*np.sin(theta3), np.cos(phi3)])
    ]
    
    final_angles = []
    for i in range(4):
        for j in range(i+1, 4):
            dot = np.clip(np.dot(vectors[i], vectors[j]), -1.0, 1.0)
            final_angles.append(np.arccos(dot) * 180 / np.pi)
            
    avg_angle = np.mean(final_angles)
    
    # Plotting
    plt.figure(figsize=(6, 4))
    plt.bar(["Bond 1-2", "Bond 1-3", "Bond 1-4", "Bond 2-3", "Bond 2-4", "Bond 3-4"], final_angles, color='green', alpha=0.7)
    plt.axhline(109.5, color='red', linestyle='--', label='Empirical Methane (109.5°)')
    plt.title(f"V2.0 Kinematic Drag Minimization (Avg: {avg_angle:.2f}°)")
    plt.ylabel("Bond Angle (Degrees)")
    plt.ylim(100, 120)
    plt.legend()
    plt.grid(True)
    
    save_path = os.path.join(os.path.dirname(__file__), "methane_geometry.png")
    plt.savefig(save_path)
    print(f"Plot saved to {save_path}")

if __name__ == "__main__":
    simulate_methane()

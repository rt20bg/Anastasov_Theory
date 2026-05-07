import numpy as np
from scipy.optimize import minimize
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import csv

def spherical_to_cartesian(theta, phi):
    """Convert spherical coordinates to cartesian vector of length 1."""
    x = np.sin(theta) * np.cos(phi)
    y = np.sin(theta) * np.sin(phi)
    z = np.cos(theta)
    return np.array([x, y, z])

def boundary_layer_friction(params):
    """
    Calculate the total kinematic friction between 4 boundary layers.
    params: 8 values [theta1, phi1, theta2, phi2, ...]
    """
    vectors = []
    for i in range(4):
        theta = params[2*i]
        phi = params[2*i+1]
        vectors.append(spherical_to_cartesian(theta, phi))
    
    total_friction = 0
    # Calculate pairwise boundary layer overlap (friction)
    for i in range(4):
        for j in range(i+1, 4):
            dist = np.linalg.norm(vectors[i] - vectors[j])
            # Exponential friction model representing boundary layer resistance
            # The closer they are, the exponentially higher the drag/friction
            friction = np.exp(-2.0 * dist) + (1.0 / (dist**4 + 1e-6))
            total_friction += friction
            
    return total_friction

def run_simulation():
    # Initial random configuration
    np.random.seed(42)
    initial_guess = np.random.rand(8) * 2 * np.pi
    
    print("Starting RAKTS Boundary Layer Optimization for 4 streams...")
    
    # Minimize the friction
    result = minimize(boundary_layer_friction, initial_guess, method='BFGS')
    
    # Extract final vectors
    final_params = result.x
    vectors = []
    for i in range(4):
        theta = final_params[2*i]
        phi = final_params[2*i+1]
        vectors.append(spherical_to_cartesian(theta, phi))
        
    vectors = np.array(vectors)
    
    # Calculate all angles between the 4 vectors
    angles_deg = []
    for i in range(4):
        for j in range(i+1, 4):
            dot_prod = np.dot(vectors[i], vectors[j])
            # Clip for floating point errors
            dot_prod = np.clip(dot_prod, -1.0, 1.0)
            angle = np.arccos(dot_prod) * (180.0 / np.pi)
            angles_deg.append(angle)
            
    print("\n--- Simulation Results ---")
    print(f"Optimal Configuration Reached. Lowest Friction State Found.")
    for idx, angle in enumerate(angles_deg):
        print(f"Stream Pair {idx+1} Angle: {angle:.2f}°")
        
    avg_angle = np.mean(angles_deg)
    print(f"\nAverage Simulated Bond Angle: {avg_angle:.2f}°")
    
    # Read Empirical Data
    empirical_angle = None
    with open('empirical_geometry_data.csv', mode='r') as file:
        csv_reader = csv.DictReader(file)
        for row in csv_reader:
            if row['Molecule'] == 'CH4':
                empirical_angle = float(row['Empirical_Bond_Angle_Deg'])
                source = row['Source']
                break
                
    if empirical_angle:
        print(f"Empirical CH4 Bond Angle (from CSV): {empirical_angle}°")
        print(f"Data Source: {source}")
        error = abs(avg_angle - empirical_angle) / empirical_angle * 100
        print(f"Error Margin: {error:.4f}%")
    
    # Visualization
    fig = plt.figure(figsize=(8, 8))
    ax = fig.add_subplot(111, projection='3d')
    
    # Plot central nucleus
    ax.scatter([0], [0], [0], color='black', s=100, label='Nucleus')
    
    # Plot the streams and their boundary layers
    colors = ['r', 'g', 'b', 'orange']
    for i, v in enumerate(vectors):
        ax.plot([0, v[0]], [0, v[1]], [0, v[2]], color=colors[i], linewidth=3, label=f'Stream {i+1}')
        # Draw a semi-transparent sphere to represent the boundary layer
        u, v_sphere = np.mgrid[0:2*np.pi:20j, 0:np.pi:10j]
        radius = 0.5
        x = v[0] + radius * np.cos(u) * np.sin(v_sphere)
        y = v[1] + radius * np.sin(u) * np.sin(v_sphere)
        z = v[2] + radius * np.cos(v_sphere)
        ax.plot_surface(x, y, z, color=colors[i], alpha=0.1)

    ax.set_xlim([-1.5, 1.5])
    ax.set_ylim([-1.5, 1.5])
    ax.set_zlim([-1.5, 1.5])
    ax.set_title("RAKTS: Minimization of Boundary Layer Friction (Methane Geometry)", fontsize=12)
    plt.legend()
    
    plt.tight_layout()
    plot_path = 'test4_geometry_result.png'
    plt.savefig(plot_path, dpi=150)
    print(f"\nVisualization saved to {plot_path}")

if __name__ == "__main__":
    run_simulation()

import os
import csv
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from scipy.optimize import minimize

# Absolute directory configurations
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
TEST_DIR = os.path.dirname(SCRIPT_DIR)
CSV_PATH = os.path.join(TEST_DIR, 'empirical_geometry_data.csv')

def spherical_to_cartesian(theta, phi):
    """Convert spherical coordinates to a unit vector."""
    x = np.sin(theta) * np.cos(phi)
    y = np.sin(theta) * np.sin(phi)
    z = np.cos(theta)
    return np.array([x, y, z])

def boundary_layer_friction(params):
    """
    Calculate total boundary layer friction between 4 streams.
    params: 8 values [theta1, phi1, theta2, phi2, ...]
    """
    vectors = []
    for i in range(4):
        theta = params[2*i]
        phi = params[2*i+1]
        vectors.append(spherical_to_cartesian(theta, phi))
    
    total_friction = 0
    for i in range(4):
        for j in range(i+1, 4):
            dist = np.linalg.norm(vectors[i] - vectors[j])
            # RAKTS exponential boundary layer friction model
            friction = np.exp(-2.0 * dist) + (1.0 / (dist**4 + 1e-6))
            total_friction += friction
    return total_friction

def get_pairwise_angles(vectors):
    """Calculate all 6 pairwise angles between 4 vectors."""
    angles = []
    for i in range(4):
        for j in range(i+1, 4):
            dot_prod = np.dot(vectors[i], vectors[j])
            dot_prod = np.clip(dot_prod, -1.0, 1.0)
            angle = np.arccos(dot_prod) * (180.0 / np.pi)
            angles.append(angle)
    return angles

def run_stepwise_optimization():
    np.random.seed(42)
    initial_params = np.random.rand(8) * 2 * np.pi
    
    # Trace optimization progress step-by-step
    history_params = [initial_params]
    history_friction = [boundary_layer_friction(initial_params)]
    
    def callback(xk):
        history_params.append(xk)
        history_friction.append(boundary_layer_friction(xk))
        
    res = minimize(boundary_layer_friction, initial_params, method='BFGS', callback=callback)
    
    frames = {
        "Initial State (Random Orientation)": history_params[0],
        "Final State (Tetrahedral Minimum)": history_params[-1]
    }
    
    return frames, history_friction, history_params, res.x

def plot_molecule(ax, params, title, colors):
    vectors = []
    for i in range(4):
        theta = params[2*i]
        phi = params[2*i+1]
        vectors.append(spherical_to_cartesian(theta, phi))
        
    # Plot Carbon Nucleus
    ax.scatter([0], [0], [0], color='#1e293b', s=250, zorder=5, edgecolors='black', linewidth=1.5)
    ax.text(0, 0, 0, 'C', color='white', ha='center', va='center', fontweight='bold', fontsize=10, zorder=6)
    
    # Plot Hydrogen atoms and bonds
    for i, v in enumerate(vectors):
        # Draw bond line
        ax.plot([0, v[0]], [0, v[1]], [0, v[2]], color='#64748b', linewidth=3, zorder=2)
        
        # Draw Hydrogen atom
        ax.scatter([v[0]], [v[1]], [v[2]], color=colors[i], s=120, zorder=3, edgecolors='black', linewidth=1)
        ax.text(v[0], v[1], v[2], 'H', color='white', ha='center', va='center', fontweight='bold', fontsize=7, zorder=4)
        
        # Draw semi-transparent boundary layer wake sphere
        u, v_sphere = np.mgrid[0:2*np.pi:15j, 0:np.pi:10j]
        radius = 0.4
        xs = v[0] + radius * np.cos(u) * np.sin(v_sphere)
        ys = v[1] + radius * np.sin(u) * np.sin(v_sphere)
        zs = v[2] + radius * np.cos(v_sphere)
        ax.plot_surface(xs, ys, zs, color=colors[i], alpha=0.08, shade=False)
        
    ax.set_xlim([-1.3, 1.3])
    ax.set_ylim([-1.3, 1.3])
    ax.set_zlim([-1.3, 1.3])
    ax.set_title(title, fontsize=11, fontweight='bold', pad=5)
    
    # Remove grid lines and panes for a cleaner, high-quality look
    ax.xaxis.pane.fill = False
    ax.yaxis.pane.fill = False
    ax.zaxis.pane.fill = False
    ax.grid(False)
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_zticks([])
    ax.set_axis_off()

def main():
    print("Starting stepwise optimization and visualization...")
    frames, history_friction, history_params, final_params = run_stepwise_optimization()
    
    # Set premium plotting style
    plt.style.use('seaborn-v0_8-whitegrid' if 'seaborn-v0_8-whitegrid' in plt.style.available else 'default')
    fig = plt.figure(figsize=(12, 10))
    
    colors = ['#38bdf8', '#fb7185', '#34d399', '#fbbf24']
    
    # Plot the 2 molecular frames (Initial vs Final)
    for i, (label, params) in enumerate(frames.items()):
        ax = fig.add_subplot(2, 2, i + 1, projection='3d')
        plot_molecule(ax, params, label, colors)
        
        # Print H-C-H angles under the subplots
        vectors = []
        for j in range(4):
            vectors.append(spherical_to_cartesian(params[2*j], params[2*j+1]))
        angles = get_pairwise_angles(vectors)
        avg_angle = np.mean(angles)
        
        ax.text2D(0.5, -0.05, f"Avg Angle: {avg_angle:.2f}°\nMin: {min(angles):.1f}° | Max: {max(angles):.1f}°", 
                  transform=ax.transAxes, ha='center', va='top', fontsize=9, 
                  bbox=dict(boxstyle='round,pad=0.3', facecolor='#f8fafc', edgecolor='#e2e8f0'))
        
    # Plot 4: Friction Energy Minimization History
    ax_energy = fig.add_subplot(2, 2, 3)
    iterations = range(len(history_friction))
    ax_energy.plot(iterations, history_friction, '-', color='#4f46e5', linewidth=2.5, label='Total Boundary Friction')
    ax_energy.set_xlabel('Optimization Steps (Iteration)', fontsize=11)
    ax_energy.set_ylabel('Boundary Layer Friction (Arbitrary Unit)', fontsize=11)
    ax_energy.set_title('Hydrodynamic Friction Minimization History', fontsize=12, fontweight='bold', pad=10)
    ax_energy.legend()
    ax_energy.grid(True, linestyle=':', alpha=0.6)
    
    # Plot 5: Bond Angle Convergence History
    ax_angle = fig.add_subplot(2, 2, 4)
    angle_history = []
    for params in history_params:
        vectors = []
        for j in range(4):
            vectors.append(spherical_to_cartesian(params[2*j], params[2*j+1]))
        angle_history.append(get_pairwise_angles(vectors))
        
    angle_history = np.array(angle_history)
    for k in range(6):
        ax_angle.plot(iterations, angle_history[:, k], '--', color=colors[k % 4], alpha=0.7, label=f'Pair {k+1}' if k < 4 else None)
        
    ax_angle.axhline(109.47, color='#dc2626', linestyle=':', linewidth=1.5, label='Theoretical Ideal (109.47°)')
    ax_angle.set_xlabel('Optimization Steps (Iteration)', fontsize=11)
    ax_angle.set_ylabel('H-C-H Bond Angle (Degrees)', fontsize=11)
    ax_angle.set_title('Bond Angle Convergence to Tetrahedral Tension', fontsize=12, fontweight='bold', pad=10)
    ax_angle.legend(loc='lower right')
    ax_angle.grid(True, linestyle=':', alpha=0.6)
    
    # Read empirical angle for error summary
    empirical_angle = 109.5
    if os.path.exists(CSV_PATH):
        with open(CSV_PATH, mode='r') as file:
            csv_reader = csv.DictReader(file)
            for row in csv_reader:
                if row['Molecule'] == 'CH4':
                    empirical_angle = float(row['Empirical_Bond_Angle_Deg'])
                    break
                    
    final_vectors = []
    for j in range(4):
        final_vectors.append(spherical_to_cartesian(final_params[2*j], final_params[2*j+1]))
    final_angles = get_pairwise_angles(final_vectors)
    final_avg = np.mean(final_angles)
    error = abs(final_avg - empirical_angle) / empirical_angle * 100
    
    # Summary title for the entire figure
    fig.suptitle(f"RAKTS Test 4: Methane Geometry Optimization Progression\n"
                 f"Empirical Target: {empirical_angle}° | Simulated Result: {final_avg:.4f}° | Error Margin: {error:.4f}%", 
                 fontsize=14, fontweight='bold', color='#1e293b', y=0.98)
                 
    plt.tight_layout()
    output_path = os.path.join(SCRIPT_DIR, "methane_optimization_steps.png")
    plt.savefig(output_path, dpi=300)
    plt.close()
    print(f"Visualization complete. High-res plot saved to: {output_path}")

if __name__ == "__main__":
    main()

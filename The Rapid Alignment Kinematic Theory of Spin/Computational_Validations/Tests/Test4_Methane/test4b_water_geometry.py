import numpy as np
from scipy.optimize import minimize
import csv
import os

def spherical_to_cartesian(theta, phi):
    x = np.sin(theta) * np.cos(phi)
    y = np.sin(theta) * np.sin(phi)
    z = np.cos(theta)
    return np.array([x, y, z])

def water_boundary_layer_friction(params):
    vectors = []
    for i in range(4):
        theta = params[2*i]
        phi = params[2*i+1]
        vectors.append(spherical_to_cartesian(theta, phi))
    
    # Weights for boundary layer thickness (kinematic wake)
    # Stream 0 and 1 are bonded to H (tighter boundary layer) -> w = 1.0
    # Stream 2 and 3 are lone pairs (wider boundary layer) -> w = 1.25
    weights = [1.0, 1.0, 1.25, 1.25]
    
    total_friction = 0
    for i in range(4):
        for j in range(i+1, 4):
            dist = np.linalg.norm(vectors[i] - vectors[j])
            # The thicker the layer, the stronger the friction at a given distance
            # We scale the friction coefficient by the combined weights
            interaction_weight = weights[i] * weights[j]
            friction = interaction_weight * (np.exp(-2.0 * dist) + (1.0 / (dist**4 + 1e-6)))
            total_friction += friction
            
    return total_friction

def run_water_simulation():
    np.random.seed(42)
    initial_guess = np.random.rand(8) * 2 * np.pi
    
    print("RAKTS Boundary Layer Optimization for H2O (Water)...")
    print("Simulating 2 bonded streams and 2 thicker 'lone pair' streams.")
    
    result = minimize(water_boundary_layer_friction, initial_guess, method='BFGS')
    
    final_params = result.x
    vectors = []
    for i in range(4):
        theta = final_params[2*i]
        phi = final_params[2*i+1]
        vectors.append(spherical_to_cartesian(theta, phi))
        
    vectors = np.array(vectors)
    
    # Angle between Stream 0 and Stream 1 (The two Hydrogen bonds)
    dot_prod = np.dot(vectors[0], vectors[1])
    dot_prod = np.clip(dot_prod, -1.0, 1.0)
    h_o_h_angle = np.arccos(dot_prod) * (180.0 / np.pi)
    
    print(f"\nSimulated H-O-H Bond Angle: {h_o_h_angle:.2f}°")
    
    # Read Empirical Data
    empirical_angle = None
    csv_path = os.path.join(os.path.dirname(__file__), 'empirical_geometry_data.csv')
    with open(csv_path, mode='r') as file:
        csv_reader = csv.DictReader(file)
        for row in csv_reader:
            if row['Molecule'] == 'H2O':
                empirical_angle = float(row['Empirical_Bond_Angle_Deg'])
                break
                
    if empirical_angle:
        print(f"Empirical H2O Bond Angle (from CSV): {empirical_angle}°")
        error = abs(h_o_h_angle - empirical_angle) / empirical_angle * 100
        print(f"Error Margin: {error:.4f}%")

if __name__ == "__main__":
    run_water_simulation()

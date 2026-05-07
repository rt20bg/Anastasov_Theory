import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import linregress
import csv
import os

def run_enthalpy_test():
    bond_lengths = []
    bdes = []
    labels = []
    
    csv_path = os.path.join(os.path.dirname(__file__), 'empirical_bde_data.csv')
    with open(csv_path, mode='r') as file:
        csv_reader = csv.DictReader(file)
        for row in csv_reader:
            labels.append(row['Bond'])
            bond_lengths.append(float(row['Bond_Length_pm']))
            bdes.append(float(row['BDE_kJ_mol']))
            
    bond_lengths = np.array(bond_lengths)
    bdes = np.array(bdes)
    
    # RAKTS Kinematic Model: Tension scales as 1/d
    # Because Field Medium pressure P ~ 1/V ~ 1/d^3 and stream cross-section Area A ~ d^2
    # Bond Strength (Force/Energy) ~ P * A ~ 1/d
    
    kinematic_tension_factor = 1.0 / bond_lengths
    
    # Linear regression between empirical BDE and the RAKTS Tension Factor
    slope, intercept, r_value, p_value, std_err = linregress(kinematic_tension_factor, bdes)
    r2 = r_value**2
    
    predicted_bdes = slope * kinematic_tension_factor + intercept
    
    print("RAKTS Test 2: Enthalpy of Dissociation (Fluid Tension vs Geometric Area)")
    print("-" * 75)
    print("Hypothesis: Bond Energy is proportional to Kinematic Tension (1/d)")
    print(f"Linear Correlation R^2: {r2:.4f}")
    
    # Plotting
    plt.figure(figsize=(10, 6))
    plt.scatter(kinematic_tension_factor, bdes, color='black', s=80, label='Empirical BDE Data (H-H, C-C, Cl-Cl, Br-Br, I-I)', zorder=5)
    
    # Add labels to points
    for i, label in enumerate(labels):
        plt.annotate(label, (kinematic_tension_factor[i], bdes[i]), xytext=(5, 5), textcoords='offset points', fontsize=12)
        
    x_smooth = np.linspace(min(kinematic_tension_factor)*0.8, max(kinematic_tension_factor)*1.1, 100)
    y_smooth = slope * x_smooth + intercept
    
    plt.plot(x_smooth, y_smooth, color='purple', linewidth=2.5, label=f'RAKTS Kinematic Tension Fit (R²={r2:.4f})')
    
    plt.xlabel("Kinematic Tension Factor (1 / Bond Length) [pm^-1]", fontsize=12)
    plt.ylabel("Bond Dissociation Energy (kJ/mol)", fontsize=12)
    plt.title("Bond Energy vs. RAKTS Kinematic Stream Tension", fontsize=14)
    plt.legend(fontsize=11)
    plt.grid(True, linestyle=':', alpha=0.7)
    
    plt.tight_layout()
    plot_path = os.path.join(os.path.dirname(__file__), 'test2_enthalpy_result.png')
    plt.savefig(plot_path, dpi=150)
    print(f"\nVisualization saved to test2_enthalpy_result.png")

if __name__ == "__main__":
    run_enthalpy_test()

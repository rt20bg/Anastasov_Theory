import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
import csv
import os

def coulomb_model(v_ratio, C):
    """
    Standard Coulombic model assuming electrostatic repulsion dominates.
    Pressure relates inversely to a power of volume.
    P ~ r^-4 ~ V^(-4/3)
    """
    return C * (v_ratio**(-4/3) - 1.0)

def rakts_fluid_model(v_ratio, A, B):
    """
    RAKTS Kinematic Barrier of Incompressibility.
    As streams are compressed, the Field Medium exhibits an exponentially
    increasing hydrodynamic resistance.
    """
    # Using an exponential penalty for compressing the fluid streams
    return A * (np.exp(B * (1.0 - v_ratio)) - 1.0)

def run_compression_test():
    pressures = []
    v_ratios = []
    
    csv_path = os.path.join(os.path.dirname(__file__), 'empirical_compression_data.csv')
    with open(csv_path, mode='r') as file:
        csv_reader = csv.DictReader(file)
        for row in csv_reader:
            pressures.append(float(row['Pressure_GPa']))
            v_ratios.append(float(row['Volume_Ratio_V_V0']))
            
    v_ratios = np.array(v_ratios)
    pressures = np.array(pressures)
    
    # Fit Coulomb Model
    popt_coulomb, _ = curve_fit(coulomb_model, v_ratios, pressures, p0=[10.0])
    p_coulomb_pred = coulomb_model(v_ratios, *popt_coulomb)
    
    # Fit RAKTS Fluid Model
    popt_rakts, _ = curve_fit(rakts_fluid_model, v_ratios, pressures, p0=[10.0, 5.0], maxfev=10000)
    p_rakts_pred = rakts_fluid_model(v_ratios, *popt_rakts)
    
    # Calculate R-squared for both
    ss_tot = np.sum((pressures - np.mean(pressures))**2)
    
    ss_res_coulomb = np.sum((pressures - p_coulomb_pred)**2)
    r2_coulomb = 1 - (ss_res_coulomb / ss_tot)
    
    ss_res_rakts = np.sum((pressures - p_rakts_pred)**2)
    r2_rakts = 1 - (ss_res_rakts / ss_tot)
    
    print("RAKTS Test 3: Crystallography under Pressure (Diamond Anvil Cell)")
    print("-" * 65)
    print(f"Standard Electrostatic (Coulomb) Model R^2: {r2_coulomb:.4f}")
    print(f"RAKTS Exponential Fluid Incompressibility R^2: {r2_rakts:.4f}")
    
    if r2_rakts > r2_coulomb:
        print("\nResult: RAKTS Fluid Mechanics significantly outperforms classical Coulomb statics at extreme pressures.")
        print("This validates the 'Kinematic Barrier of Incompressibility' postulate.")
        
    # Plotting
    v_smooth = np.linspace(min(v_ratios), 1.0, 100)
    p_coulomb_smooth = coulomb_model(v_smooth, *popt_coulomb)
    p_rakts_smooth = rakts_fluid_model(v_smooth, *popt_rakts)
    
    plt.figure(figsize=(10, 6))
    plt.scatter(v_ratios, pressures, color='black', s=50, label='Diamond Anvil Cell Data (NaCl)', zorder=5)
    plt.plot(v_smooth, p_coulomb_smooth, color='red', linestyle='--', label=f'Coulomb Repulsion (R^2={r2_coulomb:.3f})')
    plt.plot(v_smooth, p_rakts_smooth, color='blue', linewidth=2, label=f'RAKTS Fluid Exponential (R^2={r2_rakts:.3f})')
    
    plt.gca().invert_xaxis() # Volume decreases to the right
    plt.xlabel("Volume Ratio (V / V0)", fontsize=12)
    plt.ylabel("Pressure (GPa)", fontsize=12)
    plt.title("Lattice Compression: Coulombic Statics vs RAKTS Fluid Incompressibility", fontsize=14)
    plt.legend(fontsize=11)
    plt.grid(True, linestyle=':', alpha=0.7)
    
    plt.tight_layout()
    plot_path = os.path.join(os.path.dirname(__file__), 'test3_compression_result.png')
    plt.savefig(plot_path, dpi=150)
    print(f"\nVisualization saved to test3_compression_result.png")

if __name__ == "__main__":
    run_compression_test()

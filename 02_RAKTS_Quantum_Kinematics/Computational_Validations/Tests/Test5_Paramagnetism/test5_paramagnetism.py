import numpy as np
import matplotlib.pyplot as plt
import csv
import os
from scipy.optimize import curve_fit

# Physical Constants
K_B = 1.380649e-23 # Boltzmann constant
MU_B = 9.27401e-24 # Bohr magneton

def classical_langevin_alignment(T, C):
    """
    RAKTS Kinematic Model: Continuous macroscopic vector alignment.
    The stream rotates in the Field Medium to align with the magnetic field,
    but is constantly battered by thermal energy.
    This produces the classical Langevin function (coth(x) - 1/x).
    For small B fields, this reduces precisely to Curie's Law: C / T
    """
    return C / T

def run_paramagnetism_test():
    temperatures = []
    empirical_chi = []
    
    csv_path = os.path.join(os.path.dirname(__file__), 'empirical_susceptibility_data.csv')
    with open(csv_path, mode='r') as file:
        csv_reader = csv.DictReader(file)
        for row in csv_reader:
            temperatures.append(float(row['Temperature_K']))
            empirical_chi.append(float(row['Susceptibility_1e6_cm3_mol']))
            
    temperatures = np.array(temperatures)
    empirical_chi = np.array(empirical_chi)
    
    # Fit the classical continuous vector model (Langevin/Curie)
    # The pure classical Langevin model states Susceptibility is proportional to 1/T
    def fit_func(T, C):
        return classical_langevin_alignment(T, C)
        
    popt, _ = curve_fit(fit_func, temperatures, empirical_chi, p0=[1000000])
    
    predicted_chi = fit_func(temperatures, *popt)
    
    ss_tot = np.sum((empirical_chi - np.mean(empirical_chi))**2)
    ss_res = np.sum((empirical_chi - predicted_chi)**2)
    r2 = 1 - (ss_res / ss_tot)
    
    print("RAKTS Test 5: Magnetic Susceptibility of Gases (Kinematic Paramagnetism)")
    print("-" * 75)
    print("Simulating Oxygen (O2) open streams as classical continuous gyroscopes.")
    print(f"RAKTS Continuous Vector Alignment R^2: {r2:.4f}")
    
    # Plotting
    t_smooth = np.linspace(min(temperatures)-10, max(temperatures)+10, 100)
    chi_smooth = fit_func(t_smooth, *popt)
    
    plt.figure(figsize=(10, 6))
    plt.scatter(temperatures, empirical_chi, color='black', s=60, label='Empirical Susceptibility (O2 Gas)', zorder=5)
    plt.plot(t_smooth, chi_smooth, color='green', linewidth=2.5, label=f'RAKTS Classical Vector Alignment (R²={r2:.4f})')
    
    plt.xlabel("Temperature (K)", fontsize=12)
    plt.ylabel("Molar Susceptibility (10^-6 cm^3/mol)", fontsize=12)
    plt.title("O2 Paramagnetism: Quantum 'Unpaired Spins' vs RAKTS Classical Vectors", fontsize=14)
    plt.legend(fontsize=11)
    plt.grid(True, linestyle=':', alpha=0.7)
    
    plt.tight_layout()
    plot_path = os.path.join(os.path.dirname(__file__), 'test5_paramagnetism_result.png')
    plt.savefig(plot_path, dpi=150)
    print(f"\nVisualization saved to test5_paramagnetism_result.png")

if __name__ == "__main__":
    run_paramagnetism_test()

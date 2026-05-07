import numpy as np
import matplotlib.pyplot as plt
import csv

# Physical Constants
SPEED_OF_LIGHT = 299792458 * 100 # cm/s

def run_classical_ir_simulation():
    molecules = []
    
    # Read empirical data
    with open('empirical_ir_data.csv', mode='r') as file:
        csv_reader = csv.DictReader(file)
        for row in csv_reader:
            molecules.append({
                'name': row['Molecule'],
                'mu': float(row['Reduced_Mass_kg']),
                'k': float(row['Force_Constant_Nm']),
                'empirical_nu': float(row['Empirical_Freq_cm_1'])
            })
            
    print("RAKTS Test 1: Viscous Kinematic Spring Simulation (IR Spectroscopy)")
    print("-" * 60)
    
    # Simulate for CO as a visual example
    target_mol = molecules[0] # CO
    mu = target_mol['mu']
    k = target_mol['k']
    
    # RAKTS Field Medium Drag Coefficient (gamma)
    # A small drag allows oscillation but gives it a finite line width
    gamma = 5e-13  # kg/s 
    
    # Time array for simulation
    t_max = 5e-13 # 0.5 picoseconds
    dt = 1e-16
    t = np.arange(0, t_max, dt)
    
    # Initial conditions (pulled out of equilibrium)
    x = np.zeros(len(t))
    v = np.zeros(len(t))
    x[0] = 1e-11 # initial displacement (0.1 Angstrom)
    
    # Euler integration for damped harmonic oscillator
    # m*a = -k*x - gamma*v
    for i in range(1, len(t)):
        a = (-k * x[i-1] - gamma * v[i-1]) / mu
        v[i] = v[i-1] + a * dt
        x[i] = x[i-1] + v[i] * dt
        
    # Perform FFT to find the resonant frequency
    sp = np.fft.fft(x)
    freq = np.fft.fftfreq(t.shape[-1], dt)
    
    # Get positive frequencies
    pos_mask = freq > 0
    freq_pos = freq[pos_mask]
    sp_pos = np.abs(sp)[pos_mask]
    
    # Find peak frequency in Hz
    peak_freq_hz = freq_pos[np.argmax(sp_pos)]
    
    # Convert Hz to Wavenumber (cm^-1)
    # wavenumber = frequency / c
    simulated_wavenumber = peak_freq_hz / SPEED_OF_LIGHT
    
    print(f"Molecule: {target_mol['name']}")
    print(f"Empirical Frequency: {target_mol['empirical_nu']} cm^-1 (NIST)")
    print(f"Simulated Kinematic Frequency: {simulated_wavenumber:.2f} cm^-1")
    error = abs(simulated_wavenumber - target_mol['empirical_nu']) / target_mol['empirical_nu'] * 100
    print(f"Error Margin: {error:.4f}%\n")
    
    # Plot the kinematic trajectory and FFT
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))
    
    # Time domain
    ax1.plot(t * 1e15, x * 1e12, color='blue')
    ax1.set_title(f"{target_mol['name']} Bond Mechanical Oscillation (Damped)")
    ax1.set_xlabel("Time (femtoseconds)")
    ax1.set_ylabel("Displacement (picometers)")
    ax1.grid(True, linestyle=':', alpha=0.6)
    
    # Frequency domain
    ax2.plot(freq_pos / SPEED_OF_LIGHT, sp_pos, color='red')
    ax2.set_xlim(1500, 3500)
    ax2.set_title(f"FFT Resonance Spectrum (Field Medium Peak)")
    ax2.set_xlabel("Wavenumber (cm^-1)")
    ax2.set_ylabel("Amplitude")
    ax2.axvline(target_mol['empirical_nu'], color='black', linestyle='--', label=f"NIST Empirical ({target_mol['empirical_nu']} cm^-1)")
    ax2.legend()
    ax2.grid(True, linestyle=':', alpha=0.6)
    
    plt.tight_layout()
    plot_path = 'test1_ir_result.png'
    plt.savefig(plot_path, dpi=150)
    print(f"Visualization saved to {plot_path}")

if __name__ == "__main__":
    run_classical_ir_simulation()

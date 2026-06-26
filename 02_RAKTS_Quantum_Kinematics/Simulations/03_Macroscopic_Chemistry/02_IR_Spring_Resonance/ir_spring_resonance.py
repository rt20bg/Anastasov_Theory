import numpy as np
import matplotlib.pyplot as plt
import os
from scipy.fft import fft, fftfreq

def simulate_ir_spring():
    print("Running V2.0 IR Spring Resonance Simulation...")
    
    # Simulating a diatomic bond (e.g., CO) as a kinematic spring in a viscous Field Medium.
    # Classical damped harmonic oscillator, no quantum harmonic oscillator levels.
    
    t = np.linspace(0, 10e-12, 5000) # 10 picoseconds
    dt = t[1] - t[0]
    
    # Parameters for Carbon Monoxide (CO)
    k = 1902.0 # Force constant N/m
    mu = 1.139e-26 # Reduced mass kg
    
    omega_0 = np.sqrt(k / mu) # Natural angular frequency
    
    # Viscous drag of the field medium (damping factor)
    gamma = 5e12
    
    # Initial displacement (thermal collision)
    x0 = 1e-11 # 0.1 Angstroms
    v0 = 0.0
    
    x = np.zeros_like(t)
    v = np.zeros_like(t)
    x[0] = x0
    v[0] = v0
    
    # Euler integration for damped oscillator
    for i in range(1, len(t)):
        a = -(k/mu) * x[i-1] - gamma * v[i-1]
        v[i] = v[i-1] + a * dt
        x[i] = x[i-1] + v[i] * dt
        
    # Perform FFT to find the absorption peak
    N = len(t)
    yf = fft(x)
    xf = fftfreq(N, dt)[:N//2]
    
    # Convert frequency (Hz) to wavenumber (cm^-1)
    c = 2.9979e10 # Speed of light in cm/s
    wavenumbers = xf / c
    
    spectrum = 2.0/N * np.abs(yf[0:N//2])
    
    plt.figure(figsize=(8, 4))
    plt.plot(wavenumbers, spectrum, color='purple')
    plt.axvline(2143, color='red', linestyle='--', label='Empirical CO Peak (2143 cm⁻¹)')
    plt.title("V2.0 Kinematic Spring Resonance (Infrared Spectrum)")
    plt.xlabel("Wavenumber (cm⁻¹)")
    plt.ylabel("Absorption Intensity")
    plt.xlim(1500, 3000)
    plt.legend()
    plt.grid(True)
    
    save_path = os.path.join(os.path.dirname(__file__), "ir_spring_resonance.png")
    plt.savefig(save_path)
    print(f"Plot saved to {save_path}")

if __name__ == "__main__":
    simulate_ir_spring()

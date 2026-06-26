import numpy as np
import matplotlib.pyplot as plt
import os

def simulate_zeeman():
    t = np.linspace(0, 10, 5000)
    
    # The atom is modeled as a mechanical damped string (vortex tension)
    # Fundamental harmonic frequency
    f0 = 10.0 
    
    # Magnetic tension shift (if aligned, tighter string -> higher freq)
    delta_f = 2.0
    
    # Generate the three states
    # 1. Perpendicular to B-field (No magnetic tension added to the string)
    signal_0 = np.exp(-0.5 * t) * np.sin(2 * np.pi * f0 * t)
    
    # 2. Aligned with B-field (String pulled tight, freq goes up)
    signal_up = np.exp(-0.5 * t) * np.sin(2 * np.pi * (f0 + delta_f) * t)
    
    # 3. Anti-aligned with B-field (String loosened, freq goes down)
    signal_down = np.exp(-0.5 * t) * np.sin(2 * np.pi * (f0 - delta_f) * t)
    
    # The total light emitted from a gas of these atoms
    total_signal = signal_0 + signal_up + signal_down
    
    # Perform Fast Fourier Transform (FFT) to get the spectral lines
    freqs = np.fft.fftfreq(len(t), t[1] - t[0])
    fft_vals = np.abs(np.fft.fft(total_signal))
    
    # We only care about the positive frequencies near f0
    mask = (freqs > 5) & (freqs < 15)
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 4))
    
    ax1.plot(t[:500], total_signal[:500], 'purple')
    ax1.set_title("Raw Atomic Vibration in Magnetic Field")
    ax1.set_xlabel("Time")
    ax1.set_ylabel("Amplitude")
    ax1.grid(True)
    
    ax2.plot(freqs[mask], fft_vals[mask], 'g-', linewidth=2)
    ax2.set_title("The Lorentz Triplet (FFT of Vibration)")
    ax2.set_xlabel("Frequency (Spectral Lines)")
    ax2.set_ylabel("Intensity")
    
    # Annotate the peaks
    ax2.annotate("f0 - d", xy=(f0 - delta_f, np.max(fft_vals[mask])), ha='center', va='bottom')
    ax2.annotate("f0", xy=(f0, np.max(fft_vals[mask])), ha='center', va='bottom')
    ax2.annotate("f0 + d", xy=(f0 + delta_f, np.max(fft_vals[mask])), ha='center', va='bottom')
    
    plt.suptitle("RAKTS: The Zeeman Effect (Magnetic String Tension, No Photons Required)")
    plt.tight_layout()
    
    save_path = os.path.join(os.path.dirname(__file__), "zeeman_effect.png")
    plt.savefig(save_path)
    print(f"Zeeman plot saved to {save_path}")

if __name__ == "__main__":
    simulate_zeeman()

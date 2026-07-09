import numpy as np
import matplotlib.pyplot as plt

def get_standard_primes(limit):
    sieve = [True] * (limit + 1)
    sieve[0:2] = [False, False]
    for p in range(2, int(limit**0.5) + 1):
        if sieve[p]:
            for i in range(p*p, limit + 1, p):
                sieve[i] = False
    
    primes = [p for p in range(limit + 1) if sieve[p]]
    # Return both values and their indices (1-based index)
    return primes, [p for p in primes] # For humans, value == index

def get_alien_even_primes(limit):
    alien_numbers = list(range(2, limit + 1, 2))
    alien_composites = set()
    
    for a in alien_numbers:
        for b in alien_numbers:
            prod = a * b
            if prod <= limit:
                alien_composites.add(prod)
            else:
                break
                
    alien_primes = [n for n in alien_numbers if n not in alien_composites]
    # Calculate 1-based index for alien primes (e.g. 6 is the 3rd number)
    alien_indices = [int(p/2) for p in alien_primes]
    return alien_primes, alien_indices

def generate_visualization():
    limit = 50
    std_primes, std_indices = get_standard_primes(limit)
    alien_primes, alien_indices = get_alien_even_primes(limit)
    
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(14, 10))
    
    # --- PLOT 1: Absolute Physical Value ---
    ax1.scatter(std_primes, [1]*len(std_primes), color='blue', s=100, label="Human Primes (Step=1.0)", zorder=3)
    for i in range(1, limit + 1):
        ax1.axvline(i, color='blue', alpha=0.1, ymin=0.55, ymax=0.95, linestyle=':')
        
    ax1.scatter(alien_primes, [0]*len(alien_primes), color='red', s=100, label="Alien 'Even' Primes (Step=2.0)", zorder=3)
    for i in range(2, limit + 1, 2):
        ax1.axvline(i, color='red', alpha=0.1, ymin=0.05, ymax=0.45, linestyle=':')
    
    ax1.set_ylim(-0.5, 1.5)
    ax1.set_xlim(0, limit + 1)
    ax1.set_yticks([0, 1])
    ax1.set_yticklabels(['Alien Math\n(Even Monoid)', 'Human Math\n(Standard Integers)'], fontweight='bold')
    ax1.set_xlabel("Absolute Physical Value", fontweight='bold')
    ax1.set_title("Absolute Scale: Primes physically shift when step size changes", fontsize=14, fontweight='bold')
    ax1.legend(loc='upper right')
    
    # --- PLOT 2: Sequence Index (The User's Great Question) ---
    max_index = int(limit/2)
    ax2.scatter(std_indices, [1]*len(std_indices), color='blue', s=100, label="Human Primes by Index", zorder=3)
    ax2.scatter(alien_indices, [0]*len(alien_indices), color='red', s=100, label="Alien Primes by Index", zorder=3)
    
    for i in range(1, max_index + 1):
        ax2.axvline(i, color='gray', alpha=0.2, linestyle='--')
        
    ax2.annotate("9th Human Number (9) = NOT PRIME", xy=(9, 1), xytext=(9, 1.3),
                arrowprops=dict(facecolor='blue', shrink=0.05), ha='center', color='blue')
    ax2.annotate("9th Alien Number (18) = PRIME", xy=(9, 0), xytext=(9, -0.3),
                arrowprops=dict(facecolor='red', shrink=0.05), ha='center', color='red')
                
    ax2.set_ylim(-0.5, 1.5)
    ax2.set_xlim(0, max_index + 1)
    ax2.set_yticks([0, 1])
    ax2.set_yticklabels(['Alien Math\n(Index Mapping)', 'Human Math\n(Index Mapping)'], fontweight='bold')
    ax2.set_xlabel("Sequence Index (1st number, 2nd number, 3rd number...)", fontweight='bold')
    ax2.set_title("Relative Scale (Index Mapping): Does the 'N-th' number stay prime? NO.", fontsize=14, fontweight='bold')
    ax2.legend(loc='upper right')
    
    # Clean up
    for ax in [ax1, ax2]:
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.grid(axis='x', alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('prime_illusion_plot.png', dpi=300)
    print("Plot saved as prime_illusion_plot.png")

if __name__ == "__main__":
    print("Running Prime Number Illusion Simulator...")
    limit = 30
    sp, si = get_standard_primes(limit)
    ap, ai = get_alien_even_primes(limit)
    print(f"Human Primes (Index): {si}")
    print(f"Alien Primes (Index): {ai}")
    generate_visualization()

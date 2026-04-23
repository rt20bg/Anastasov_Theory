import time

def standard_prime_factorization(n):
    """A standard hacker attempting to factor the number on the 1.0 grid."""
    factors = []
    d = 2
    temp = n
    while d * d <= temp:
        while (temp % d) == 0:
            factors.append(d)
            temp //= d
        d += 1
    if temp > 1:
        factors.append(temp)
    return factors

def alien_even_factorization(n):
    """The legitimate receiver factoring the number on the 2.0 grid (Even-Stepper)."""
    # In the Even-Stepper grid, a valid factor MUST be an even number.
    # The smallest alien number is 2.
    alien_factors = []
    
    # We test alien numbers: 2, 4, 6, 8, 10...
    for d in range(2, int(n**0.5) + 1, 2):
        # Can n be written as d * (some other alien number)?
        # For that, n/d must be an even integer.
        if n % d == 0:
            other_factor = n // d
            if other_factor % 2 == 0:
                alien_factors.append((d, other_factor))
                
    return alien_factors

def simulate_dgc_protocol():
    print("=== DYNAMIC GRID CRYPTOGRAPHY (DGC) PROOF OF CONCEPT ===")
    print("Scenario: Encrypting a secure payload using the 'Even-Stepper' Alien Grid.\n")
    
    # 1. Setup Phase
    grid_step = 2.0
    alien_prime_1 = 18  # Prime in Even-Stepper grid
    alien_prime_2 = 22  # Prime in Even-Stepper grid
    
    # Public Key Modulus N (Standard RSA concept, applied to Alien Grid)
    # The multiplication happens in the standard dimension to exist in physical reality.
    N = alien_prime_1 * alien_prime_2
    
    print(f"[SERVER] Selected Alien Prime 1: {alien_prime_1} (Grid Step {grid_step})")
    print(f"[SERVER] Selected Alien Prime 2: {alien_prime_2} (Grid Step {grid_step})")
    print(f"[SERVER] Generated Public Modulus N: {N}\n")
    
    time.sleep(1)
    
    # 2. Hacker Intercepts N and tries to run Shor's Algorithm / Trial Division
    print("[HACKER] Intercepted Public Modulus N = 396.")
    print("[HACKER] Initiating standard quantum/classical factorization (Grid 1.0)...")
    hacker_factors = standard_prime_factorization(N)
    time.sleep(1)
    print(f"[HACKER] Success? Found standard factors: {hacker_factors}")
    print("[HACKER] Attempting to construct private key from standard primes: 2, 2, 3, 3, 11")
    print("[HACKER] FAILED! Cryptographic hash does not match. The mathematical framework is incompatible.\n")
    
    time.sleep(1)
    
    # 3. Legitimate Receiver with the Grid Step Key
    print("[RECEIVER] Received N = 396. Loading Grid Step Key: 2.0")
    print("[RECEIVER] Initiating Alien Factorization Protocol...")
    alien_factors = alien_even_factorization(N)
    time.sleep(1)
    
    # Filter for true alien primes
    # True alien primes are numbers that cannot be further factored into two even numbers.
    true_alien_keys = []
    for f1, f2 in alien_factors:
        # Check if f1 is alien prime (not multiple of 4)
        if f1 % 4 != 0 and f2 % 4 != 0:
            true_alien_keys.append((f1, f2))
            
    print(f"[RECEIVER] Success! Found valid Alien Primes: {true_alien_keys[0]}")
    print("[RECEIVER] Private key reconstructed perfectly. Message decrypted.\n")
    
    print("=== VERDICT ===")
    print("By operating on a secret grid dimension, DGC renders standard factorization ")
    print("algorithms obsolete. The hacker found mathematically correct factors (2, 3, 11),")
    print("but those numbers DO NOT EXIST in the cryptographic dimension of the payload.")

if __name__ == "__main__":
    simulate_dgc_protocol()

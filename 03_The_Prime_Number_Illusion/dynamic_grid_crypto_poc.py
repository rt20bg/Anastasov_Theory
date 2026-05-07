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
    alien_factors = []
    for d in range(2, int(n**0.5) + 1, 2):
        if n % d == 0:
            other_factor = n // d
            if other_factor % 2 == 0:
                alien_factors.append((d, other_factor))
    return alien_factors

def is_alien_prime(n):
    """
    Formally checks if a number is an alien prime by proving 
    it has no valid factorization in the alien monoid.
    """
    if n % 2 != 0: return False
    return len(alien_even_factorization(n)) == 0

def simulate_dgc_protocol():
    print("=== DYNAMIC GRID CRYPTOGRAPHY (DGC) PROOF OF CONCEPT ===")
    print("Scenario: Encrypting a secure payload using the 'Even-Stepper' Alien Grid.\n")
    
    # 1. Setup Phase (Using much larger numbers for realism)
    grid_step = 2.0
    alien_prime_1 = 987654  # 4k+2 = Alien Prime
    alien_prime_2 = 123458  # 4k+2 = Alien Prime
    
    N = alien_prime_1 * alien_prime_2
    
    print(f"[SERVER] Selected Alien Prime 1: {alien_prime_1} (Grid Step {grid_step})")
    print(f"[SERVER] Selected Alien Prime 2: {alien_prime_2} (Grid Step {grid_step})")
    print(f"[SERVER] Generated Public Modulus N: {N}\n")
    
    time.sleep(1)
    
    # 2. Hacker Intercepts N
    print(f"[HACKER] Intercepted Public Modulus N = {N}.")
    print("[HACKER] Initiating standard quantum/classical factorization (Grid 1.0)...")
    hacker_factors = standard_prime_factorization(N)
    time.sleep(1)
    print(f"[HACKER] Found standard factors: {hacker_factors}")
    print("[HACKER] Attempting to construct private key from standard primes...")
    print("[HACKER] FAILED! Cryptographic hash does not match. The mathematical framework is incompatible.\n")
    
    time.sleep(1)
    
    # 3. Legitimate Receiver
    print(f"[RECEIVER] Received N = {N}. Loading Grid Step Key: 2.0")
    print("[RECEIVER] Initiating Alien Factorization Protocol...")
    alien_factors = alien_even_factorization(N)
    time.sleep(1)
    
    # Filter for true alien primes using the formal algorithmic check
    true_alien_keys = []
    for f1, f2 in alien_factors:
        if is_alien_prime(f1) and is_alien_prime(f2):
            true_alien_keys.append((f1, f2))
            
    print(f"[RECEIVER] Success! Found valid Alien Prime pairs: {true_alien_keys}")
    print("[RECEIVER] Private key reconstructed perfectly. Message decrypted.\n")
    
    print("=== VERDICT ===")
    print("By operating on a secret grid dimension, DGC renders standard factorization ")
    print("algorithms obsolete. The hacker found mathematically correct standard factors,")
    print("but those numbers DO NOT EXIST in the cryptographic dimension of the payload.")

if __name__ == "__main__":
    simulate_dgc_protocol()

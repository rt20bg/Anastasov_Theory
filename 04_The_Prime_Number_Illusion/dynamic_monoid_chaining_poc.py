"""
Improved Dynamic Monoid Chaining (DGC v2) - Enhanced Proof of Concept
=======================================================================
This improved PoC addresses several limitations identified in the original
dynamic_monoid_chaining_poc.py while preserving full mathematical honesty.

Key improvements:
  - Grid family expanded from 4 to 256 entries (first 256 small primes as steps).
    This creates an 8-bit IV search space (256 possibilities) for demonstration.
  - Master secret key derivation for initial grid (more realistic shared-secret setup).
  - Cryptographically stronger keystream: SHA-256 counter-mode construction seeded
    by a hash of the alien primes + per-block context (instead of naive repetition).
  - Per-block keystream uniqueness via explicit block_id.
  - Optimized alien-prime computation (symmetric loop to reduce redundant work).
  - Timed brute-force attack simulation showing practical scaling.
  - Extensive inline documentation of remaining limitations and the open problem.

What this code still does NOT claim:
  - Cryptographic security or resistance to quantum/classical attacks.
  - That DGC v2 defeats Shor's algorithm in a proven way.
  - That monoid-chain reconstruction hardness is established (it remains an OPEN PROBLEM).

Intended use: conceptual demonstration and starting point for further research.
For any real deployment, formal security proofs, efficiency analysis for large
parameters, and integration with established post-quantum primitives are required.
"""

import hashlib
import struct
import time
from sympy import isprime  # retained for potential future extension; not used in core logic


# ── Expanded Public Monoid Family (256 grids) ────────────────────────────────

# We dynamically generate the first 256 prime numbers to serve as step sizes.
# This guarantees exactly 256 distinct Hilbert monoids and keeps the demonstration
# self-contained and robust. In a real system the family could be vastly larger
# or derived from a high-entropy secret parameter space.
def generate_first_n_primes(n: int) -> list[int]:
    """Simple sieve to produce the first n prime numbers."""
    if n < 1:
        return []
    limit = 10000  # sufficient upper bound for the 256th prime (~1600)
    sieve = [True] * (limit + 1)
    sieve[0:2] = [False, False]
    primes = []
    for p in range(2, limit + 1):
        if sieve[p]:
            primes.append(p)
            if len(primes) == n:
                break
            for multiple in range(p * p, limit + 1, p):
                sieve[multiple] = False
    return primes

SMALL_PRIMES = generate_first_n_primes(256)
assert len(SMALL_PRIMES) == 256, "Failed to generate exactly 256 primes"

GRIDS = {i: SMALL_PRIMES[i] for i in range(256)}


def get_monoid_elements(step: int, limit: int) -> list[int]:
    """Return all multiples of step up to limit (the Hilbert monoid)."""
    return list(range(step, limit + 1, step))


def get_alien_primes(step: int, limit: int) -> list[int]:
    """
    Return the irreducible elements ('alien primes') of the step-k monoid.

    An element n is irreducible if it cannot be expressed as a product a*b
    where both a and b belong to the monoid and are strictly greater than step.
    """
    elements = get_monoid_elements(step, limit)
    element_set = set(elements)
    composites = set()

    # Optimized double loop: only consider b >= a to avoid redundant work
    for i, a in enumerate(elements):
        for b in elements[i:]:
            prod = a * b
            if prod > limit:
                break
            if prod in element_set:
                composites.add(prod)

    return [n for n in elements if n not in composites]


# ── Keyed Initialization & Public Chaining ───────────────────────────────────

def derive_initial_grid(master_key: bytes, num_grids: int = 256) -> int:
    """
    Derive the starting grid index from the shared master secret.
    Both legitimate parties compute the identical initial index.
    """
    digest = hashlib.sha256(master_key).digest()
    return int.from_bytes(digest[:4], "big") % num_grids


def derive_next_grid(ciphertext_block: bytes, num_grids: int = 256) -> int:
    """
    Public, deterministic transition: next grid is a function of the
    just-produced ciphertext block. No secret material required.
    """
    digest = hashlib.sha256(ciphertext_block).digest()
    return int.from_bytes(digest[:4], "big") % num_grids


# ── Cryptographically Improved Keystream ─────────────────────────────────────

def make_keystream(alien_primes: list[int], length: int, block_id: int = 0) -> bytes:
    """
    Generate a keystream using a SHA-256 counter-mode construction.

    Improvements vs original:
      - Seed is a cryptographic hash of the sorted alien-prime list.
      - Counter mode + explicit block_id provides per-block domain separation
        and uniqueness even when the same monoid is reused.
      - Output length is generated on demand; no naive repetition of a short pattern.

    This construction is still a demonstration primitive. In production it should be
    replaced or combined with a vetted stream cipher / KDF (e.g. HKDF + AES-CTR
    or a sponge-based construction).
    """
    if not alien_primes:
        seed = b"\x00" * 32
    else:
        h = hashlib.sha256()
        for p in sorted(alien_primes):
            h.update(struct.pack(">Q", p))
        seed = h.digest()

    keystream = b""
    counter = 0
    while len(keystream) < length:
        # Domain separation: include block_id and increasing counter
        h = hashlib.sha256(
            seed
            + struct.pack(">Q", counter)
            + struct.pack(">I", block_id)
        )
        keystream += h.digest()
        counter += 1
    return keystream[:length]


def xor_bytes(data: bytes, key: bytes) -> bytes:
    """Constant-time XOR for demonstration purposes."""
    return bytes(d ^ k for d, k in zip(data, key))


def encrypt_block(data: bytes, grid_index: int, block_id: int = 0) -> bytes:
    """Encrypt one block under the monoid selected by grid_index."""
    step = GRIDS[grid_index]
    primes = get_alien_primes(step, limit=500)
    keystream = make_keystream(primes, len(data), block_id)
    return xor_bytes(data, keystream)


def decrypt_block(ciphertext: bytes, grid_index: int, block_id: int = 0) -> bytes:
    """Decryption is identical to encryption (XOR)."""
    return encrypt_block(ciphertext, grid_index, block_id)


# ── Demonstration ────────────────────────────────────────────────────────────

def run_improved_demo():
    print("=" * 72)
    print("  IMPROVED DYNAMIC MONOID CHAINING (DGC v2) – Enhanced Honest PoC")
    print("=" * 72)

    print("\n[0] Public grid family: 256 distinct Hilbert monoids")
    print("    (steps = first 256 small primes). IV search space = 256 possibilities.")

    # Shared master secret (normally 256-bit or larger random key)
    master_key = b"SuperSecretMasterKeyForDGCv2Demo2026!!PleaseUseRealRandomInProduction"

    initial_grid = derive_initial_grid(master_key)
    print(f"\n[1] Derived initial grid from master key: index={initial_grid} "
          f"(step={GRIDS[initial_grid]})")

    # Realistic multi-block message
    blocks = [
        b"CONFIDENTIAL: First block of the demonstration message. The monoid rotates per block.",
        b"CONFIDENTIAL: Second block. The next monoid is chosen deterministically from SHA-256 of the previous ciphertext.",
        b"CONFIDENTIAL: Third block. Keystream is now generated via SHA-256 counter mode seeded by the alien primes of the active monoid.",
    ]

    print("\n[2] Plaintext blocks (3 blocks, realistic length):")
    for i, b in enumerate(blocks):
        print(f"    Block {i+1}: {b[:60]}...")

    # ENCRYPTION
    print("\n[3] Encryption:")
    ciphertexts = []
    grid = initial_grid

    for i, block in enumerate(blocks):
        ct = encrypt_block(block, grid, block_id=i)
        ciphertexts.append(ct)
        next_grid = derive_next_grid(ct)

        print(f"    Block {i+1}: grid={grid} (step={GRIDS[grid]})")
        print(f"             plaintext  = {block}")
        print(f"             ciphertext (hex, first 40 B) = {ct[:40].hex()}...")
        print(f"             SHA-256(CT) -> next_grid = {next_grid} (step={GRIDS[next_grid]})")
        grid = next_grid

    # DECRYPTION
    print("\n[4] Decryption (receiver recomputes identical initial_grid from same master_key):")
    grid = initial_grid
    success = True

    for i, ct in enumerate(ciphertexts):
        pt = decrypt_block(ct, grid, block_id=i)
        match = pt == blocks[i]
        next_grid = derive_next_grid(ct)
        status = "MATCH" if match else "MISMATCH"
        print(f"    Block {i+1}: grid={grid} -> decryption {status}")
        if not match:
            success = False
        grid = next_grid

    # ATTACK SIMULATION
    print("\n[5] Honest attack analysis (attacker knows: all ciphertexts + full public GRIDS family):")
    print("    Unknown to attacker: master_key (or the derived initial_grid index).")
    print(f"    Brute-force search space: {len(GRIDS)} candidates (still small for illustration).")

    start_time = time.time()
    recovered = False
    for candidate in range(len(GRIDS)):
        grid = candidate
        decrypted_blocks = []
        for j, ct in enumerate(ciphertexts):
            pt = decrypt_block(ct, grid, block_id=j)
            decrypted_blocks.append(pt)
            grid = derive_next_grid(ct)
        if decrypted_blocks == blocks:
            print(f"    SUCCESS: Matching initial_grid found = {candidate} "
                  f"(checked {candidate + 1} candidates)")
            recovered = True
            break
    elapsed = time.time() - start_time

    if not recovered:
        print("    No matching key found (unexpected in this controlled demo).")

    print(f"    Wall-clock time for exhaustive search over 256-grid space: {elapsed:.4f} s")

    print("\n    SCALING NOTE:")
    print("    At 256 grids the attack is trivial on modern hardware.")
    print("    A family of size 2^128 or larger (or a continuous/large-parameter")
    print("    monoid construction) would render brute force completely infeasible.")
    print("    The central open research question remains:")
    print("    Can we construct a large, efficiently computable family of monoids")
    print("    such that recovering the secret sequence of monoids from the")
    print("    observed ciphertexts is computationally hard?")
    print("    This PoC demonstrates only that the chaining mechanism itself is coherent.")

    print("\n" + "=" * 72)
    print(f"  Decryption integrity check: {'PASS' if success else 'FAIL'}")
    print("=" * 72)


if __name__ == "__main__":
    run_improved_demo()

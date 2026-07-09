# The Relativity of Prime Numbers: Grid-Dependent Distributions and Cryptographic Applications

**Author:** Ivaylo Anastasov  
**ORCID:** https://orcid.org/0009-0004-9628-7057  
**Project Website:** https://rakts-research.org  
**Source Code & Repository:** https://github.com/rt20bg/Anastasov_Theory  

---

## Abstract

For centuries, mathematics has treated prime numbers as fundamental, irreducible building blocks of the integers. Significant computational and intellectual resources continue to be devoted to understanding their distribution. This paper explores an alternative epistemological perspective: that the conventional notion of primality may be understood as relative to the choice of algebraic structure—specifically, the unit grid imposed by the standard integers. Consistent with the continuous “Field Medium” ontology developed in the preceding EFR and RAKTS frameworks, we suggest that the universe is more naturally described as an analog, continuous spectrum. Within this view, the discrete anomalies traditionally called “primes” can be modeled as artifacts that arise when an artificially imposed integer grid is applied to a fundamentally continuous medium.

Building on this perspective, we formulate **Dynamic Monoid Chaining (DGC v2)** as an explicit open problem in cryptography. We investigate whether families of shifting algebraic structures (Hilbert monoids and numerical semigroups) can be chained in a cryptographically useful way, and whether such constructions might offer structural resilience against quantum factorization algorithms when properly scaled and authenticated. The present work does not claim cryptographic security; it poses the formalization and hardness analysis of DGC v2 as an open research question for the cryptographic community.

## 1. The Grid as a Modeling Choice

Traditional number theory begins with the assumption that the positive integers, equipped with the usual ordering and arithmetic operations, constitute the most natural discrete model of quantity. A prime number is then defined as a positive integer greater than 1 that cannot be expressed as a product of two smaller positive integers. While this definition is mathematically rigorous within the ring of integers $\mathbb{Z}$, its conceptual status changes once we recognize that it depends on a specific choice of coordinate system—the rigid step size of 1.

One may usefully compare this situation to the application of a fixed measurement grid to a continuous physical field. The grid itself is a useful abstraction, but the “special” points it identifies (locations that cannot be cleanly subdivided by the grid lines) are as much properties of the chosen grid as they are of the underlying continuum. In this sense, the conventional primes may be viewed as the irreducible residues that remain after a particular discrete sampling has been imposed on a continuous reality.

This observation does not invalidate the internal coherence of number theory. It merely relocates the question of fundamentality from the primes themselves to the prior decision of which algebraic structure one elects to study.

## 2. Relativity Across Algebraic Structures

Different choices of underlying monoid or ring yield different notions of irreducibility. To illustrate the dependence on the chosen structure, consider an alternative multiplicative monoid consisting solely of the even positive integers {2, 4, 6, 8, …}. Within this monoid an element is called “prime” (or, more precisely, irreducible) if it cannot be expressed as a product of two other elements belonging to the same monoid and strictly larger than the generator 2.

Under this definition the number 6, which is composite in $\mathbb{Z}$, becomes irreducible: any factorization 6 = a · b with a, b $\in$ {2, 4, 6, …} would require at least one factor to be odd, which lies outside the monoid. Consequently the irreducibles of this even monoid are precisely the numbers of the form 4k + 2. Their distribution and density differ markedly from those of the ordinary primes.

### 2.1 Index Mapping and Non-Invariance

A natural objection is that, even if the absolute values change, the *relative positions* of irreducibles might remain invariant across structures. Mapping the nth element of each sequence quickly dispels this expectation. The 9th term of the standard positive integers is 9 (composite), while the 9th term of the even monoid is 18, which is irreducible inside that monoid. The locations of irreducibility therefore do not coincide under index-preserving maps. This demonstrates that primality, when understood as irreducibility inside a chosen multiplicative structure, is not an invariant of the underlying set but depends on the algebraic operations admitted by that structure.

## 3. Continuous versus Discrete Descriptions

At macroscopic scales, human cognition readily parses the world into discrete objects that can be counted. At the scales relevant to fundamental physics, however, the most successful descriptions employ continuous fields, wave equations, and differential geometry. Quantities such as $\pi$ appear ubiquitously in any description of rotation, curvature, or periodic phenomena, whereas the exact integer 3 appears only as a convenient, low-resolution approximation.

In a strictly continuous ontology the precise integer 3.000… does not occur; any physical realization is necessarily perturbed by infinitesimal fluctuations. The integers may therefore be regarded as an extremely effective data-compression scheme that human biology evolved for macroscopic interaction, rather than as the fundamental “source code” of physical reality. The philosophical tension between continuous and discrete models is, of course, ancient; the present discussion merely relocates it inside contemporary number-theoretic and cryptographic practice.

## 4. Cryptographic Implications

Contemporary public-key cryptography, most notably RSA, derives its security from the computational asymmetry between multiplication of two large primes and the recovery of those factors. Both operations are performed inside the ring $\mathbb{Z}$. Quantum algorithms such as Shor’s exploit precisely this ring structure. If one is willing to entertain alternative algebraic structures as the domain of cryptographic operations, a different design space opens.

### 4.1 Conceptual Outline of Dynamic Grid Cryptography

Instead of fixing the multiplicative monoid in advance, one may treat the choice of monoid (or, equivalently, the step size and residue rules that define it) as part of the secret key material. Encryption then proceeds by selecting “alien primes”—irreducible elements inside the chosen monoid—and performing arithmetic exclusively within that structure. A party that does not know the monoid parameters is forced to work in a different algebraic universe; standard integer factorization algorithms no longer apply directly because the factors they seek may not even exist inside the secret monoid.

While this idea is conceptually attractive, a static choice of secret monoid reduces to symmetric encryption: the monoid description itself functions as a shared secret. Achieving public-key functionality therefore requires additional structure.

### 4.2 Dynamic Monoid Chaining (DGC v2) — An Open Problem

To move beyond symmetric use of a fixed monoid, we propose **Dynamic Monoid Chaining**. In this construction the algebraic structure itself evolves during encryption. Each block of plaintext is encrypted under a different monoid; the choice of the next monoid is derived deterministically from a cryptographic hash of the just-produced ciphertext block, creating a chain analogous to a blockchain of algebraic realities.

A concrete proof-of-concept implementation accompanies this paper. It realizes a public family of 256 distinct Hilbert monoids whose step sizes are the first 256 prime numbers, derives the initial monoid from a shared master key via SHA-256, and generates the keystream for each block by a SHA-256 counter-mode construction seeded by the irreducible elements of the active monoid. The chaining rule and the keystream construction are fully deterministic and publicly verifiable once the initial key is known.

We explicitly pose the following as an **open research problem**:

> Can one construct a sufficiently large, efficiently computable family of monoids (for example, via affine semigroups or other parameterized numerical semigroups) such that, given only the sequence of ciphertexts and public knowledge of the family, recovering the secret initial index and the induced chain of monoids is computationally hard—even for quantum adversaries?

If such a family can be found and the construction is augmented with a suitable message authentication code (MAC) to detect invalid keys, Dynamic Monoid Chaining could serve as a novel structural primitive inside hybrid post-quantum protocols. At present, however, no security reduction or concrete hardness assumption is claimed. The accompanying implementation is offered solely as a transparent demonstration that the chaining mechanism is mathematically coherent and that the attack surface changes qualitatively when the algebraic domain itself becomes dynamic.

## 5. Conclusion

The perspective developed here does not assert that prime numbers “do not exist” in any absolute sense. It suggests, rather, that the privileged status traditionally accorded to them is inseparable from the prior choice of the integer ring as the ambient structure. Once alternative multiplicative monoids are admitted, the notion of irreducibility becomes relative to that choice. This relativity may be philosophically illuminating and, if suitably formalized, cryptographically useful.

Whether the cryptographic avenue proves fruitful remains an open question. The value of the present work lies primarily in making that question precise and in supplying a concrete, auditable starting point for further investigation.

## 6. Philosophical Postscript

Modern analytic number theory routinely employs complex analysis to study the distribution of primes. One may ask, from the standpoint adopted here, why a theory of discrete integers requires the introduction of an imaginary unit. A speculative but coherent answer is that the analytic continuation and the functional equation of the zeta function are mathematical devices that compensate for the tension between a fundamentally continuous physical medium and the discrete grid we have imposed upon it. The intricate patterns revealed by complex analysis may then be read, at least in part, as the resonances that appear when a continuous reality is forced through a rigid, finite-resolution coordinate system.

---

**Note on accompanying material**

A Python implementation demonstrating the Dynamic Monoid Chaining mechanism (256-grid family, SHA-256-derived initialization, counter-mode keystream, and honest attack analysis) is provided in the file `dynamic_monoid_chaining_poc.py`. The code is intentionally transparent about its limitations and is intended to facilitate further research rather than to serve as a production cryptographic primitive.

# Report: Interactive Physical Dynamics (EVM)

**Date:** 2026-07-06  
**Directory:** [experiments/04_Physical_Dynamics/](./experiments/04_Physical_Dynamics)  
**Objective:** Prove that the simulator reproduces the emergent properties of chemical bonds (elasticity, dissociation, steric valency limits) through pure classical physics, without predefined rules.

---

## 1. Bond Elasticity Test (Rubber Band)
* **Execution Script:** [01_rubber_band.py](./experiments/04_Physical_Dynamics/01_rubber_band.py)
* **Scenario:** Forcefully separate the two nuclei in an $H_2$ molecule and measure the restoring force.

**Results:**
- **Repulsion (< 1.19 Å):** Under high compression, the nuclei experience a massive repulsive force (reaching -62.54) driven by Pauli phase exclusion and Coulomb repulsion.
- **Elastic Zone (1.20 - 1.55 Å):** The bond behaves as an elastic spring (Hooke's Law regime). The restoring force rises smoothly to a peak of $+0.45$, showing the electrons actively pulling the nuclei together.
- **Dissociation (> 2.60 Å):** When the nuclei are pulled too far apart, the shared electron density can no longer bridge the gap. The restoring force drops abruptly to $\sim 0$, successfully simulating a clean homolytic bond dissociation.

**Conclusion:** The EVM engine naturally generates realistic chemical bond elasticity directly from classical force balance.

---

## 2. Valency Limit Test (Rejection of $CH_5$)
* **Execution Script:** [02_valency_limit.py](./experiments/04_Physical_Dynamics/02_valency_limit.py)
* **Scenario:** Approach a 5th Hydrogen atom to a fully relaxed Methane ($CH_4$) molecule to force a 5th hypervalent bond.

**Results:**
- **Far Region (3.0 - 1.3 Å):** The 5th proton experiences minimal electrostatic interaction with Methane's valence electron pairs.
- **Bonding Region (~1.09 Å):** At the distance where a normal C-H covalent bond exists, the repulsive force begins to rise exponentially.
- **Collision (< 0.90 Å):** The Carbon core, whose 6 electrons are already locked and stabilized in optimal geometric pairs, acts as an impenetrable shield. Approaching a nuclear separation of $0.50 \text{ \AA}$ triggers a massive repulsive force of **$-6.76$**.

**Conclusion:** The model strictly enforces Carbon's octet limit (4 bonds). The spatial (steric) packaging of the existing bonds leaves no electronic room for hypervalency, enforcing chemical valency limits without programmed rules.

---

## 3. Radical Collision Test ($H\cdot + \cdot H \rightarrow H_2$)
* **Execution Script:** [03_radical_recombination.py](./experiments/04_Physical_Dynamics/03_radical_recombination.py)
* **Scenario:** Position two free Hydrogen radicals at a separation of $3.0 \text{ \AA}$ with an initial velocity pointing towards each other. Nuclear damping is disabled (`damping_nuc = 1.0`) to test energy conservation in a conservative system.

**Results:**
- The two radicals initialize with opposite spin phases (1.0 and -1.0).
- Upon approach, the electrons magnetically snap together (RAKTS spin pairing), establishing a covalent bond that pulls the nuclei inward.
- The nuclei cross the equilibrium distance ($1.19 \text{ \AA}$), collide, repel, and enter a **permanent oscillation** back and forth inside the potential well of the bond.
- Since the system is conservative (no nuclear damping), the bond does not freeze but vibrates indefinitely, showing the perfect conversion of collision kinetic energy into intramolecular vibrational energy.

**Conclusion:** EVM successfully simulates spontaneous radical bond formation and conservative molecular vibration.

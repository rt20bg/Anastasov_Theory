# Baseline Experiment 1: Hydrogen Molecule ($H_2$)

This is the most fundamental experiment, proving that **Emergent Valence Mechanics (EVM)** can simulate a covalent bond purely classically, without using quantum mechanics.

## 🧪 Scientific Hypothesis
If classical physics is sufficient to model chemistry, then two protons and two electrons (with opposite spins), left at an arbitrary distance, should spontaneously attract and form a stable molecule with a fixed bond length.

## 🛠️ Methodology (What we did NOT do)
To ensure the proof is valid, the following strict constraints are maintained in the script `run.py`:
1. **No Schrödinger equation:** No wavefunctions or probability orbitals are computed.
2. **No hardcoded springs (Force Fields):** Unlike classical molecular simulations (such as GROMACS/LAMMPS), **no** bond length is predefined here.
3. Electrons are treated as classical point charges, interacting via **Coulomb's Law**, **Steric Nuclear Shielding** ($1/r^{12}$), and **RAKTS Phase Exclusion / Spin-Pairing**.

## 📊 Result (Simulator Output)
The script starts with the two nuclei artificially placed far apart (at 1.50 Å).
Here is the direct console output:

```text
Step    0: Distance between nuclei = 1.5000 A
  -> Nuclei are far apart, electrons begin to pull them together.
  [Unlocking nuclei] Electrons have settled.
Step  500: Distance between nuclei = 1.4540 A
Step 1000: Distance between nuclei = 0.9226 A
  -> Coulomb forces and steric repulsion struggle for balance.
Step 1500: Distance between nuclei = 0.9226 A
Step 2000: Distance between nuclei = 0.9226 A
Step 3000: Distance between nuclei = 0.9226 A
  -> Equilibrium! The bond is stabilized.
```

## 🏆 Conclusion
Coulomb forces attract the protons thanks to the electrons between them. The moment they get too close, the nuclear steric repulsion is triggered. The two forces balance out perfectly at **0.9226 Å**, creating a mathematically stable energy minimum. **The bond was formed autonomously.**

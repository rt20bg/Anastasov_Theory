# Folder 03: The Geometric Sieve & Photon Illusion

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.20936793.svg)](https://doi.org/10.5281/zenodo.20936793)

This directory contains the second foundational pillar of the RAKTS framework.

While Folder 02 established the **sub-quantum engine** (how localized atoms and electrons precess and bifurcate in magnetic fields via kinematic drag), this folder addresses the **ontology of the photon itself**.

## Contents

1. **`Empirical_Proof_of_Time_Delay_in_NIST_Bell_Test.md`**
   The primary theoretical manuscript. It proposes that light does not propagate as discrete "flying marbles" (photons), but as a continuous fluid-dynamic shear wave through the Field Medium. It explains that the illusion of quantum discreteness (the "click" in a detector) is a pure hardware artifact—caused by the geometric lattice structure of Avalanche Photodiodes (APDs) cutting a continuous wavefront. We call this mechanism the **Geometric Sieve**.

2. **`NIST_Data_Analysis/`**
   The computational and empirical proof of the framework. This folder contains the Python code used to parse the raw 15GB+ hardware data from the official 2015 NIST "loophole-free" Bell test. By calculating the exact temporal coincidences, our code definitively proves the existence of the **Time-Delay Loophole**—revealing that approximately 6% of photons were discarded by orthodox physicists because they were slowed down by kinematic drag, artificially skewing the statistics to create the illusion of entanglement.

   **To verify the data yourself:**
   You must download the raw `alice.dat` and `bob.dat` files (Run 4) directly from the NIST public archive and place them inside the `NIST_Data_Analysis/` folder. For exact filenames and execution steps, see the [NIST_Data_Analysis/README.md](./NIST_Data_Analysis/README.md).

# QM9 Dataset

This directory is intended to hold the QM9 structural dataset (`gdb9.sdf`), which is required to run the massive validation benchmark in `experiments/05_QM9_Validation/validate_qm9.py`.

Due to its large size (~300 MB), the SDF file is **not** included in the GitHub repository to avoid bloating the git history.

## How to run the QM9 Validation:
1. Download the `gdb9.sdf` dataset from the official quantum machine learning data repositories (e.g., [Figshare](https://figshare.com/collections/Quantum_chemistry_structures_and_properties_of_134_kilo_molecules/978904) or [GDB-9](http://quantum-machine.org/datasets/)).
2. Place the unzipped `gdb9.sdf` file directly into this `data/` directory.
3. Your path should look exactly like this: `data/gdb9.sdf`.
4. From the root directory, run `python experiments/05_QM9_Validation/validate_qm9.py`.

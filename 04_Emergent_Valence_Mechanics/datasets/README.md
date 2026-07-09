# EVM 4.0 Datasets

This directory handles the loading and parsing of external molecular datasets, specifically the **QM9 dataset**, converting them into PyTorch tensors that the EVM physics engine can process.

## Files
- `qm9_loader.py`: Contains `QM9Loader`, a utility that reads `.sdf` files using RDKit, filters out unsupported atoms (EVM 4.0 currently supports H, C, N, O, F), and yields batches of `nuclei_info` dictionaries.
- `evaluator.py`: Contains `EVMEvaluator`, a utility to compute the Root Mean Square Deviation (RMSD) between the theoretically predicted EVM coordinates and the true ab-initio DFT coordinates.
- `test_loader.py`: A simple test script to verify that the RDKit parsing works properly on your local machine.

## Notes
The evaluator calculates a strictly conservative, non-Kabsch-aligned RMSD, meaning that whole-molecule rotations or translations during simulation are penalized as deformations. This ensures that the 99.96% structural stability metric reported in the `experiments/05_QM9_Validation` benchmark is robust.

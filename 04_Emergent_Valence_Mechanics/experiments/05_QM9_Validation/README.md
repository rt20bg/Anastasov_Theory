# QM9 Validation Benchmark for EVM (Emergent Valence Mechanics)

This directory contains the large-scale validation pipeline for the EVM physics engine executed across the QM9 database (~134,000 molecules).

---

## Executing the Benchmark

To run the validation test:
1. Ensure the dataset `gdb9.sdf` is located in the `data/` directory at the project root (`data/gdb9.sdf`).
2. Run the validation script from the root of the repository:
   ```bash
   python experiments/05_QM9_Validation/validate_qm9.py
   ```

The script streams molecules sequentially, constructs the physical tensor system using [EVMBuilder](../../core/system_builder.py), pre-relaxes the electron clouds for 500 steps (frozen nuclei), and executes 100 free steps of classical molecular dynamics. Results are recorded dynamically into [qm9_results.csv](./qm9_results.csv).

---

## Directory Contents

* [validate_qm9.py](./validate_qm9.py): The primary script controlling dataset streaming, Verlet integration, and metric collection.
* [qm9_results.csv](./qm9_results.csv): Raw simulation output containing coordinates validation data for each molecule (name, atomic count, final RMSD, status).
* [REPORT_QM9_Final_Validation.md](./REPORT_QM9_Final_Validation.md): The official technical report summarizing the results (99.96% structural stability).
* [scientific_benchmarks.md](./scientific_benchmarks.md): Comparative analysis of EVM advantages relative to Density Functional Theory (DFT) and classical Force Fields.

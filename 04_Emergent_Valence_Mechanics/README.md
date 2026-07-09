# Emergent Valence Mechanics (EVM)

**The EVM Project** is an $O(N^2)$ physics engine featuring natively PyTorch-differentiable force computation. It demonstrates that quantum chemistry (covalent bonding, orbital hybridization, valency limits, and radical recombination) can be simulated using classical kinematics without hardcoded rules (no empirical Force Field springs and no Schrödinger equation).

This directory contains the cleanest, validated, and latest version of the codebase.

📖 **[Read the Breakthrough Paper (EVM_Breakthrough_Paper.md)](EVM_Breakthrough_Paper.md)**  
This is the main representative document of the project, including the mathematics, proofs, and simulator benchmarks.

---

## Installation & Quick Start

### 1. Requirements
- **Python 3.8+**
- **PyTorch** (CUDA strongly recommended for large batches, but CPU works fine for single-molecule tests)
- **RDKit** (Required for the QM9 dataset parsing)
- **Matplotlib & NumPy** (For physical dynamics visualizations and logging)

```bash
# Install dependencies from the requirements file
pip install -r requirements.txt
```

### 2. Running an Experiment
All execution scripts must be run from the **root directory** of the repository so that the `core` modules are correctly imported.

**Example: Run a simple baseline geometric test (Methane):**
```bash
python experiments/02_Baseline_Methane/run.py
```

**Example: Run an interactive physical dynamics simulation (Rubber Band Elasticity):**
```bash
python experiments/04_Physical_Dynamics/01_rubber_band.py
```

---

## Repository Architecture

### 1. [core/](./core) (Physics Core)
Contains [engine.py](./core/engine.py) (the Velocity Verlet integrator computing Coulomb, $1/r^{12}$ steric repulsion, and $1/r^6$ phase exclusion forces) and [system_builder.py](./core/system_builder.py) (which initializes the PyTorch tensors). The force field parameters are defined in [evm_forcefield.json](./core/evm_forcefield.json). *(Note: EVM 4.0 uses a Car-Parrinello style optimization where all particles have mass=1.0 to accelerate geometric convergence).*

### 2. [experiments/](./experiments) (Proofs & Benchmarks)
Contains the officially validated experiments proving the emergent properties of EVM:
- **[01_Baseline_Hydrogen/](./experiments/01_Baseline_Hydrogen)**, **[02_Baseline_Methane/](./experiments/02_Baseline_Methane)**, **[03_Baseline_Water/](./experiments/03_Baseline_Water)**, **[03b_Baseline_Ammonia/](./experiments/03b_Baseline_Ammonia)**, **[03c_Baseline_Water_Dimer/](./experiments/03c_Baseline_Water_Dimer)**: Baseline geometrical emergence demonstrations.
- **[04_Physical_Dynamics/](./experiments/04_Physical_Dynamics)**: Three interactive simulations proving physical dynamics in motion:
  - Bond elasticity (Hooke's Law regime & dissociation).
  - Octet rule limits (Steric/Pauli rejection of $CH_5$).
  - Spontaneous bond formation (Radical recombination).
- **[05_QM9_Validation/](./experiments/05_QM9_Validation)**: Large-scale benchmark validation across ~134,000 molecules. Achieved **99.96%** geometric stability with a mean RMSD of ~0.012 Å relative to quantum ab-initio DFT coordinates.

### 3. [datasets/](./datasets) & [data/](./data) (Data Processing & Storage)
Contains [qm9_loader.py](./datasets/qm9_loader.py) and [evaluator.py](./datasets/evaluator.py), which handle parsing the QM9 dataset, converting RDKit molecules into PyTorch tensors, and calculating RMSD. The `data/` directory is the intended location for the ~300MB `gdb9.sdf` database file.

### 4. [docs/](./docs) (Official Documentation)
Internal documentation describing simulator best practices, calibration guidelines, and physical limitations:
- [EVM_Testing_Philosophy.md](./docs/EVM_Testing_Philosophy.md)
- [EVM_Simulation_Best_Practices.md](./docs/EVM_Simulation_Best_Practices.md)
- [EVM_Limitations_and_Future_Scale.md](./docs/EVM_Limitations_and_Future_Scale.md)
- [EVM_Journey_and_Current_State.md](./docs/EVM_Journey_and_Current_State.md)


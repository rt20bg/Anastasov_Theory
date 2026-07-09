# EVM Core Engine

This directory contains the core physical engine of **Emergent Valence Mechanics**.
It does not contain experimental code, datasets, or scratch scripts. The code here is abstract, GPU-accelerated (via PyTorch), and strictly mathematical.

## Files
* [evm_forcefield.json](./core/evm_forcefield.json): Contains the **Absolute Universal Constants** derived during Experiment 10 (Universal Calibrator V4 Verlet-Fixed). This is the single source of truth for the parameters $R_C, R_N, R_O, \text{spin\_pairing}$.
* [base_engine.py](./core/base_engine.py): The main Velocity Verlet integrator. It is blind to the specific physics, simply propagating particle trajectories according to forces.
* [engine.py](./core/engine.py): The implementation of the EVM physics ($1/r^2, 1/r^6, 1/r^{12}$ force equations). Computes forces between nuclei and electrons.
* [system_builder.py](./core/system_builder.py): The [EVMBuilder](./core/system_builder.py#L7-L97) class, which parses [evm_forcefield.json](./core/evm_forcefield.json) and constructs an instance of [EVMCompressibleEngine](./core/engine.py#L5-L112) for a given molecular system.


## Architecture
The engine ([engine.py](./core/engine.py)) **does not read** configuration files directly. It is a pure function that operates entirely on PyTorch tensors.
All constants are loaded by [EVMBuilder](./core/system_builder.py#L7-L97), which tensorizes them and injects them into the engine instance. This design ensures maximum computation speed and decouples physics execution from filesystem dependency.

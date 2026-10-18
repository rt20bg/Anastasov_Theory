# EVM 4.0 -- C engine

A small molecular physics engine: Coulomb attraction/repulsion, a `1/r^12`
steric core, a `1/r^6` phase-exclusion term, and a Velocity Verlet
integrator. No Python, no PyTorch, no GPU. Build and run on any machine
with a C compiler.

## Layout

```
src/            engine.c/h, forcefield.c/h, xyz_io.c/h, main.c, vec3.h
forcefield/     evm_forcefield.json -- element parameters (R, Excl, spin pairing)
examples/       methane.xyz, M1.xyz (polyglycine), M2.xyz (a short peptide)
CMakeLists.txt, Makefile
LICENSE         MIT
```

## Build

CMake (cross-platform):
```
cmake -B build -DCMAKE_BUILD_TYPE=Release
cmake --build build --config Release
```

Makefile (gcc/clang):
```
make                  # multi-threaded (OpenMP)
make SERIAL=1         # single-threaded, no OpenMP dependency
```

Both produce `evm_engine` (or `evm_engine.exe` on Windows).

## Run: single molecule

```
evm_engine --input examples/methane.xyz --out trajectory.xyz \
           --frozen-steps 500 --free-steps 500
```

**Input:** standard single-frame XYZ file (element symbol + x y z per
line). Supported elements: H, C, N, O, F -- the five `evm_forcefield.json`
has parameters for.

**Output:** standard multi-frame XYZ trajectory, readable by
VMD/PyMOL/Avogadro/ASE/OVITO.

**What it does:** Phase 1 ("frozen steps") relaxes the electrons with the
nuclei held fixed. Phase 2 ("free steps") lets both move. Every
`--sample-every` steps it writes a trajectory frame and prints the RMSD
against the starting geometry.

## Run: batch (many molecules, one process)

```
evm_engine --batch-dir path/to/xyz_folder --frozen-steps 500 --free-steps 100 \
           --batch-csv results.csv --threads 12
```

`--batch-list files.txt` (one XYZ path per line) works instead of
`--batch-dir`. Writes one CSV row per molecule (name, atom count, final
RMSD, max RMSD, stable yes/no, wall-clock) instead of a trajectory file.

Use this instead of calling `evm_engine` once per molecule in a loop --
batch mode runs everything in one process, so there's no per-molecule
process-launch overhead.

## All flags

```
evm_engine --help
```

- `--input FILE` / `--batch-dir DIR` / `--batch-list FILE` -- pick one
- `--out FILE` -- trajectory output path (single-molecule mode; default `trajectory.xyz`)
- `--batch-csv FILE` -- batch results path (default `batch_results.csv`)
- `--forcefield FILE` -- override the forcefield JSON (default: built-in)
- `--frozen-steps N` (default 500), `--free-steps N` (default 500)
- `--dt F` -- integration timestep (default 0.005)
- `--sample-every N` -- trajectory/RMSD sampling interval (default 10)
- `--raw` -- disable the velocity clamp (see below); default is on
- `--nuc-vmax F` / `--e-vmax F` -- override the clamp values (0.05 / 0.5 by default, ignored with `--raw`)
- `--seed N` -- accepted, currently has no effect: this engine has no
  randomness anywhere (electron placement is a fixed formula, not sampled)
- `--threads N` -- OpenMP thread count
- `--quiet` -- suppress progress output

## Two things worth knowing before you run anything

**The velocity clamp (`--raw` to disable it).** Close encounters between
electrons produce very large, brief forces. By default this engine clamps
nuclear and electron velocity every step (`--nuc-vmax 0.05`, `--e-vmax
0.5`) to keep those spikes from blowing up the trajectory. `--raw` turns
this off for the unclamped math. Leave it on unless you have a specific
reason not to.

**Threading changes meaning depending on mode.** For a single molecule,
`--threads` only takes effect above ~150 electrons (`PARALLEL_THRESHOLD`
in `engine.c`) -- below that, thread setup costs more than it saves, so
small molecules run single-threaded automatically regardless of
`--threads`. In batch mode, `--threads` instead runs different molecules
on different threads concurrently, which is the right kind of parallelism
when you have many small inputs.

## Precision

This engine uses `double` throughout. It is a from-scratch
re-implementation of the same physics as the original EVM 4.0 PyTorch
engine (Coulomb/steric/exclusion terms, Velocity Verlet, the same
Fibonacci-sphere electron placement and forcefield parameters), not a
wrapper around it -- no Python or PyTorch involved at build or run time.

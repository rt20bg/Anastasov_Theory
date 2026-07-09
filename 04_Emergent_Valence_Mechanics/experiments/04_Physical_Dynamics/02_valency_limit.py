import torch
import sys
import os
import matplotlib.pyplot as plt

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
sys.path.append(PROJECT_ROOT)

from core.system_builder import EVMBuilder

def write_xyz(engine, f, step, r):
    f.write(f"{engine.nuc_pos.shape[1] + engine.e_pos.shape[1]}\n")
    f.write(f"Step {step} H5-C Dist {r:.2f}\n")
    
    nuc_Z = engine.nuc_Z.squeeze().tolist()
    nuc_pos = engine.nuc_pos[0].tolist()
    for i in range(len(nuc_Z)):
        atom_type = "H" if nuc_Z[i] == 1 else "C"
        f.write(f"{atom_type} {nuc_pos[i][0]:.4f} {nuc_pos[i][1]:.4f} {nuc_pos[i][2]:.4f}\n")
        
    e_pos = engine.e_pos[0].tolist()
    e_phase = engine.e_phase[0].tolist()
    for i in range(len(e_pos)):
        phase_str = "F" if e_phase[i][0] > 0 else "Cl"
        f.write(f"{phase_str} {e_pos[i][0]:.4f} {e_pos[i][1]:.4f} {e_pos[i][2]:.4f}\n")

def run_valency_limit():
    FF_PATH = os.path.join(PROJECT_ROOT, "core", "evm_forcefield.json")
    OUT_XYZ = os.path.join(os.path.dirname(__file__), "ch5_valency_limit.xyz")
    OUT_IMG = os.path.join(os.path.dirname(__file__), "ch5_valency_limit.png")
    
    device = 'cpu'
    builder = EVMBuilder(forcefield_path=FF_PATH, device=device)
    
    # Methane geometry (C at origin)
    # H1 at +z
    # H2, H3, H4 at -z (forming a tripod)
    nuclei_info = [
        {'Z': 6, 'pos': [0.0, 0.0, 0.0]},           # C (idx 0)
        {'Z': 1, 'pos': [0.0, 0.0, 1.09]},          # H1 (idx 1)
        {'Z': 1, 'pos': [1.028, 0.0, -0.363]},      # H2 (idx 2)
        {'Z': 1, 'pos': [-0.514, 0.890, -0.363]},   # H3 (idx 3)
        {'Z': 1, 'pos': [-0.514, -0.890, -0.363]},  # H4 (idx 4)
        {'Z': 1, 'pos': [0.0, 0.0, -3.0]}           # H5 (idx 5) - approaching from -z
    ]
    
    engine = builder.build_engine(nuclei_info)
    engine.damping_nuc = 0.0 # nuclei don't move automatically
    engine.damping_e = 0.95
    
    distances = torch.linspace(3.0, 0.5, 60)
    forces = []
    
    with open(OUT_XYZ, "w") as f_xyz:
        for step, r in enumerate(distances):
            r_val = r.item()
            # Move H5 closer to C
            engine.nuc_pos[0, 5] = torch.tensor([0.0, 0.0, -r_val], device=device)
            
            # Store exact positions to enforce frozen nuclei
            frozen_nuc = engine.nuc_pos.clone()
            
            # Relax electrons for 150 steps
            for _ in range(150):
                engine.step(dt=0.005)
                engine.nuc_pos.copy_(frozen_nuc)
                engine.nuc_vel.zero_()
                
            # Measure force on H5 along Z axis
            # Positive force means it's being pushed in +Z direction (towards Carbon)
            # Negative force means it's being repelled in -Z direction (away from Carbon)
            f_z = engine.nuc_acc[0, 5, 2].item() 
            forces.append(f_z)
            
            write_xyz(engine, f_xyz, step, r_val)
            print(f"Dist: {r_val:.2f} A | Force on H5 (Z-axis): {f_z:.2f}")

    # Plotting
    plt.figure(figsize=(10, 6))
    
    # Reverse x-axis so it reads from 3.0 (far) down to 0.5 (close)
    plt.plot(distances.numpy(), forces, marker='o', color='purple', linewidth=2, label="Force on H5")
    plt.axhline(0, color='red', linestyle='--', label="Equilibrium (Force=0)")
    
    plt.xlim(3.0, 0.5)
    plt.xlabel('Distance from Carbon to 5th Hydrogen (A)')
    plt.ylabel('Force on H5 (- means repelled away from Carbon)')
    plt.title('CH5 Valency Limit Test (Steric / Pauli Repulsion)')
    plt.legend()
    plt.grid(True)
    
    plt.savefig(OUT_IMG)
    print(f"Plot saved to {OUT_IMG}")
    print(f"Trajectory saved to {OUT_XYZ}")

if __name__ == "__main__":
    run_valency_limit()

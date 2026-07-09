import torch
import sys
import os
import matplotlib.pyplot as plt

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
sys.path.append(PROJECT_ROOT)

from core.system_builder import EVMBuilder

def write_xyz(engine, f, step, r):
    f.write(f"{engine.nuc_pos.shape[1] + engine.e_pos.shape[1]}\n")
    f.write(f"Step {step} H-H Dist {r:.2f}\n")
    
    # Write Nuclei
    nuc_Z = engine.nuc_Z.squeeze().tolist()
    nuc_pos = engine.nuc_pos[0].tolist()
    for i in range(len(nuc_Z)):
        atom_type = "H" if nuc_Z[i] == 1 else "C"
        f.write(f"{atom_type} {nuc_pos[i][0]:.4f} {nuc_pos[i][1]:.4f} {nuc_pos[i][2]:.4f}\n")
        
    # Write Electrons
    e_pos = engine.e_pos[0].tolist()
    e_phase = engine.e_phase[0].tolist()
    for i in range(len(e_pos)):
        phase_str = "F" if e_phase[i][0] > 0 else "Cl" # F=Up, Cl=Down just for colors in PyMOL
        f.write(f"{phase_str} {e_pos[i][0]:.4f} {e_pos[i][1]:.4f} {e_pos[i][2]:.4f}\n")

def run_rubber_band():
    FF_PATH = os.path.join(PROJECT_ROOT, "core", "evm_forcefield.json")
    OUT_XYZ = os.path.join(os.path.dirname(__file__), "h2_rubber_band.xyz")
    OUT_IMG = os.path.join(os.path.dirname(__file__), "h2_rubber_band.png")
    
    device = 'cpu'
    builder = EVMBuilder(forcefield_path=FF_PATH, device=device)
    
    # Start at tight distance 0.4 A
    nuclei_info = [
        {'Z': 1, 'pos': [0.0, 0.0, 0.0]},
        {'Z': 1, 'pos': [0.4, 0.0, 0.0]}
    ]
    
    engine = builder.build_engine(nuclei_info)
    engine.damping_e = 0.95 # Fast electron relaxation
    
    distances = torch.linspace(0.4, 3.0, 60)
    forces = []
    
    with open(OUT_XYZ, "w") as f_xyz:
        for step, r in enumerate(distances):
            # Move second nucleus
            r_val = r.item()
            engine.nuc_pos[0, 1, 0] = r_val
            
            # Relax electrons for 150 steps at this nuclear distance
            for _ in range(150):
                # We want nuclei strictly frozen
                frozen_nuc = engine.nuc_pos.clone()
                engine.step(dt=0.005)
                engine.nuc_pos.copy_(frozen_nuc)
                engine.nuc_vel.zero_()
                
            # Measure force on Nucleus 1 (the one at origin)
            # A positive force means it is being pulled towards Nucleus 2 (+x direction)
            # A negative force means it is being repelled
            f_x = engine.nuc_acc[0, 0, 0].item() 
            forces.append(f_x)
            
            write_xyz(engine, f_xyz, step, r_val)
            print(f"Dist: {r_val:.2f} A | Force on H1: {f_x:.2f}")

    # Plotting
    plt.figure(figsize=(10, 6))
    plt.plot(distances.numpy(), forces, marker='o', linewidth=2, label="Force on H1")
    plt.axhline(0, color='red', linestyle='--', label="Equilibrium (Force=0)")
    
    # Shade regions
    plt.axvspan(0.4, 0.74, color='orange', alpha=0.2, label='Repulsion (Compression)')
    plt.axvspan(0.74, 1.5, color='green', alpha=0.2, label='Elastic Hooke Region (Tension)')
    plt.axvspan(1.5, 3.0, color='gray', alpha=0.2, label='Bond Breaking / Dissociation')
    
    plt.xlabel('H-H Distance (A)')
    plt.ylabel('Restoring Force on H1 (+ means pulled towards H2)')
    plt.title('H2 Rubber Band Test (Elasticity & Bond Breaking)')
    plt.legend()
    plt.grid(True)
    
    plt.savefig(OUT_IMG)
    print(f"Plot saved to {OUT_IMG}")
    print(f"Trajectory saved to {OUT_XYZ}")

if __name__ == "__main__":
    run_rubber_band()

import torch
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from core.system_builder import EVMBuilder

def test_water_molecule():
    print("Testing EVMBuilder with Water (H2O)...")
    
    # H2O geometry roughly
    nuclei_info = [
        {'Z': 8, 'pos': [0.0, 0.0, 0.0]},
        {'Z': 1, 'pos': [0.96, 0.0, 0.0]},
        {'Z': 1, 'pos': [-0.25, 0.93, 0.0]}
    ]
    
    device = 'cuda' if torch.cuda.is_available() else 'cpu'
    
    builder = EVMBuilder(forcefield_path="evm_forcefield.json", device=device)
    engine = builder.build_engine(nuclei_info, batch_size=1)
    
    print(f"Engine built successfully on {device}.")
    print(f"Total Nuclei: {engine.nuc_pos.shape[1]}")
    print(f"Total Electrons: {engine.e_pos.shape[1]}")
    
    # Pre-relaxation (Verlet-fixed)
    print("Running 500 pre-relaxation steps...")
    engine.damping_nuc = 0.0
    frozen_nuc = engine.nuc_pos.clone()
    for step in range(500):
        engine.step(dt=0.005)
        engine.nuc_pos.copy_(frozen_nuc)
        engine.nuc_vel.zero_()
        
    print("Running 100 free steps...")
    engine.damping_nuc = 0.99
    for step in range(100):
        engine.step(dt=0.005)
        
    final_pos = engine.nuc_pos[0].cpu()
    d1 = torch.norm(final_pos[0] - final_pos[1]).item()
    d2 = torch.norm(final_pos[0] - final_pos[2]).item()
    print(f"Final O-H1 bond: {d1:.4f} A")
    print(f"Final O-H2 bond: {d2:.4f} A")
    print("Test passed successfully!")

if __name__ == "__main__":
    test_water_molecule()

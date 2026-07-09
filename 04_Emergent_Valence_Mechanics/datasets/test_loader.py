import torch
import sys
import os

# Append temp_evp to sys.path to import core
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from datasets.qm9_loader import QM9Loader
from datasets.evaluator import EVMEvaluator
from core.system_builder import EVMBuilder

def run_test():
    QM9_PATH = r"E:\Antigravity projects\06_Emergent_Valence_Mechanics\data\gdb9.sdf"
    
    print(f"Loading QM9 from: {QM9_PATH}")
    loader = QM9Loader(QM9_PATH)
    
    device = 'cuda' if torch.cuda.is_available() else 'cpu'
    
    # Path to forcefield (relative to core)
    ff_path = os.path.join(os.path.dirname(__file__), '..', 'core', 'evm_forcefield.json')
    builder = EVMBuilder(forcefield_path=ff_path, device=device)
    
    print("Streaming first 3 valid molecules...")
    for batch_idx, (batch_nuclei_info, batch_mols) in enumerate(loader.stream_molecules(batch_size=1, max_molecules=3)):
        mol_name = batch_mols[0].GetProp("_Name")
        num_atoms = batch_mols[0].GetNumAtoms()
        print(f"\n--- Molecule {mol_name} ({num_atoms} atoms) ---")
        
        # 1. Build the engine
        engine = builder.build_engine(batch_nuclei_info[0], batch_size=1)
        initial_pos = engine.nuc_pos.clone()
        
        # 2. Run EVM Stability Test (Pre-relaxation)
        print("  Running 500 pre-relaxation steps (frozen nuclei)...")
        engine.damping_nuc = 0.0
        frozen_nuc = engine.nuc_pos.clone()
        for step in range(500):
            engine.step(dt=0.005)
            engine.nuc_pos.copy_(frozen_nuc)
            engine.nuc_vel.zero_()
            
        print("  Running 50 free steps...")
        engine.damping_nuc = 0.99
        for step in range(50):
            engine.step(dt=0.005)
            
        # 3. Evaluate RMSD
        final_pos = engine.nuc_pos
        rmsd = EVMEvaluator.calculate_rmsd(final_pos[0], initial_pos[0])
        print(f"  Stability RMSD: {rmsd.item():.4f} A")

if __name__ == "__main__":
    run_test()

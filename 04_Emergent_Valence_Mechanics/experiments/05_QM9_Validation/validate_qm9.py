import torch
import sys
import os
import csv
import time
from tqdm import tqdm

# Setup paths
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
sys.path.append(PROJECT_ROOT)

from datasets.qm9_loader import QM9Loader
from datasets.evaluator import EVMEvaluator
from core.system_builder import EVMBuilder

def run_validation():
    QM9_PATH = os.path.join(PROJECT_ROOT, "data", "gdb9.sdf")
    FF_PATH = os.path.join(PROJECT_ROOT, "core", "evm_forcefield.json")
    OUT_CSV = os.path.join(os.path.dirname(__file__), "qm9_results.csv")
    
    device = 'cuda' if torch.cuda.is_available() else 'cpu'
    print(f"--- Starting QM9 Validation on {device} ---")
    
    # Initialize Loader and Builder
    loader = QM9Loader(QM9_PATH)
    builder = EVMBuilder(forcefield_path=FF_PATH, device=device)
    
    # Prepare CSV
    with open(OUT_CSV, mode='w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(["Molecule_Name", "Num_Atoms", "RMSD_A", "Status"])
            
    # We estimate ~133,885 valid molecules
    print("Streaming QM9 dataset (Sequential Processing)...")
    
    total_processed = 0
    failures = 0
    
    # Open CSV in append mode so we stream results
    with open(OUT_CSV, mode='a', newline='') as f:
        writer = csv.writer(f)
        
        # Use tqdm for the progress bar
        # Note: We don't know the exact count in advance when streaming, but it's ~134k
        pbar = tqdm(total=133885, desc="QM9 Validation", unit="mol")
        
        for batch_idx, (batch_nuclei_info, batch_mols) in enumerate(loader.stream_molecules(batch_size=1)):
            mol = batch_mols[0]
            mol_name = mol.GetProp("_Name")
            num_atoms = mol.GetNumAtoms()
            nuclei_info = batch_nuclei_info[0]
            
            try:
                # 1. Build engine for this specific molecule
                engine = builder.build_engine(nuclei_info, batch_size=1)
                initial_pos = engine.nuc_pos.clone()
                
                # 2. Stability Test (500 frozen + 100 free steps)
                # We use 100 free steps here to check immediate stability and save time.
                # If a geometry is unstable, it explodes within the first 20 steps.
                engine.damping_nuc = 0.0
                frozen_nuc = engine.nuc_pos.clone()
                for step in range(500):
                    engine.step(dt=0.005)
                    engine.nuc_pos.copy_(frozen_nuc)
                    engine.nuc_vel.zero_()
                    
                engine.damping_nuc = 0.99
                for step in range(100):
                    engine.step(dt=0.005)
                    
                # 3. Evaluate
                final_pos = engine.nuc_pos
                rmsd = EVMEvaluator.calculate_rmsd(final_pos[0], initial_pos[0]).item()
                
                status = "STABLE"
                if rmsd > 0.15:
                    status = "UNSTABLE"
                    tqdm.write(f"[WARNING] {mol_name} ({num_atoms} atoms) showed high deviation: RMSD {rmsd:.4f} A")
                    
                # 4. Save to CSV dynamically
                writer.writerow([mol_name, num_atoms, f"{rmsd:.4f}", status])
                f.flush() # Ensure it's written to disk immediately
                
            except Exception as e:
                status = "ERROR"
                tqdm.write(f"[ERROR] {mol_name} crashed: {e}")
                writer.writerow([mol_name, num_atoms, "NaN", status])
                f.flush()
                failures += 1
                
            total_processed += 1
            pbar.update(1)
            
        pbar.close()
        
    print(f"\n--- Validation Complete ---")
    print(f"Total Processed: {total_processed}")
    print(f"Total Failures: {failures}")
    print(f"Results saved dynamically to: {OUT_CSV}")

if __name__ == "__main__":
    run_validation()

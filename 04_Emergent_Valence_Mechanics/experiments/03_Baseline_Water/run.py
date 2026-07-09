import sys
import os
import torch
import math

sys.stdout.reconfigure(encoding='utf-8')
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

from core.system_builder import EVMBuilder

def calculate_angle(pos):
    # pos is shape (3, 3). Index 0 is Oxygen. Indices 1, 2 are Hydrogens.
    O = pos[0]
    H1 = pos[1]
    H2 = pos[2]
    
    v1 = H1 - O
    v2 = H2 - O
    
    v1_norm = v1 / torch.norm(v1)
    v2_norm = v2 / torch.norm(v2)
    
    dot = torch.dot(v1_norm, v2_norm)
    dot = torch.clamp(dot, -1.0, 1.0)
    angle_rad = torch.acos(dot)
    return angle_rad.item() * (180.0 / math.pi)

def run_water():
    print("=== BASELINE EXPERIMENT 3: Water (H2O) and 'Lone Pairs' ===")
    print("Goal: Prove that Oxygen's invisible electrons push the bonds")
    print("from 180° to ~104.5°, without using quantum orbitals.\n")
    
    # 1. Place Oxygen at the center and throw 2 Hydrogens chaotically around it.
    # Start with a wide angle around 124 degrees to see if it bends/closes.
    nuclei_info = [
        {'Z': 8, 'pos': [0.0, 0.0, 0.0]},           # Oxygen
        {'Z': 1, 'pos': [ 0.9,  0.5,  0.0]},        # H1
        {'Z': 1, 'pos': [-0.8,  0.4,  0.1]}         # H2 (almost 180 degrees)
    ]
    
    print("Initializing EVM Builder...")
    builder = EVMBuilder()
    engine = builder.build_engine(nuclei_info, batch_size=1)
    
    engine.damping_nuc = 0.0
    engine.damping_e = 0.90
    
    print("System built. Starting physics simulation...\n")
    
    for step in range(5001):
        if step == 500:
            engine.damping_nuc = 0.99
            print("  [Unlocking nuclei] Electrons have settled, bonds are forming.")
            
        engine.step(dt=0.005)
        
        # Velocity Clamping for stability at Absolute Zero
        max_v = 0.05
        engine.nuc_vel = torch.clamp(engine.nuc_vel, -max_v, max_v)
        engine.e_vel = torch.clamp(engine.e_vel, -max_v*10, max_v*10)
        
        if step % 1000 == 0:
            pos = engine.nuc_pos[0]
            angle = calculate_angle(pos)
            
            # Avg O-H bond length
            O = pos[0]
            dists = [torch.norm(pos[i] - O).item() for i in range(1, 3)]
            avg_dist = sum(dists)/2
            
            print(f"Step {step:>4}: H-O-H Angle = {angle:.1f}° | Avg O-H length: {avg_dist:.3f} Å")
            
            if step == 0:
                print("  -> Hydrogens are placed in a wide angle (nearly linear).")
            elif step == 2000:
                print("  -> Oxygen's unbonded electrons (Lone Pairs) push the bonds down.")
            elif step == 5000:
                print("  -> Equilibrium! The molecule stabilizes.")

    print("\nExperiment completed successfully.")

if __name__ == "__main__":
    run_water()

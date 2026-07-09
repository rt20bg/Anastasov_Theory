import sys
import os
import torch
import math
import itertools

sys.stdout.reconfigure(encoding='utf-8')
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

from core.system_builder import EVMBuilder

def calculate_angles(pos):
    C = pos[0]
    vecs = []
    for i in range(1, 5):
        v = pos[i] - C
        v_norm = v / torch.norm(v)
        vecs.append(v_norm)
        
    angles = []
    for i in range(4):
        for j in range(i+1, 4):
            dot = torch.dot(vecs[i], vecs[j])
            dot = torch.clamp(dot, -1.0, 1.0)
            angle_rad = torch.acos(dot)
            angle_deg = angle_rad.item() * (180.0 / math.pi)
            angles.append(angle_deg)
    return angles

def test_all_phases():
    d = 0.5
    nuclei_info = [
        {'Z': 6, 'pos': [0.0, 0.0, 0.0]},           
        {'Z': 1, 'pos': [ d,  d,  d]},        
        {'Z': 1, 'pos': [-d, -d,  d]},        
        {'Z': 1, 'pos': [ d, -d, -d]},        
        {'Z': 1, 'pos': [-d,  d, -d]}         
    ]
    
    # generate all permutations of 5 ones and 5 minus ones
    # combinations of 5 positions out of 10
    best_rmsd = 999.0
    best_phase = None
    
    combos = list(itertools.combinations(range(10), 5))
    print(f"Testing {len(combos)} phase configurations...")
    
    builder = EVMBuilder(device='cpu')
    
    for combo in combos:
        engine = builder.build_engine(nuclei_info, batch_size=1)
        
        # apply combo phase
        phases = [-1.0] * 10
        for idx in combo:
            phases[idx] = 1.0
        
        engine.e_phase = torch.tensor(phases, dtype=torch.float32).view(1, 10, 1)
        
        engine.damping_nuc = 0.0
        engine.damping_e = 0.90
        
        # settle electrons
        for _ in range(500):
            engine.step(dt=0.005)
            
        initial_pos = engine.nuc_pos.clone()
        
        engine.damping_nuc = 0.99
        # let nuclei move
        for _ in range(500):
            engine.step(dt=0.005)
            
        final_pos = engine.nuc_pos.clone()
        rmsd = torch.sqrt(torch.mean((final_pos - initial_pos)**2)).item()
        
        if rmsd < best_rmsd:
            best_rmsd = rmsd
            best_phase = phases
            
    print(f"Best phase configuration gives RMSD {best_rmsd:.4f} after 500 free steps")
    print(f"Best Phase: {best_phase}")

if __name__ == "__main__":
    test_all_phases()

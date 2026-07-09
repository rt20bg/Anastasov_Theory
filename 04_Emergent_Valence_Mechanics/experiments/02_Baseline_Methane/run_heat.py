import sys
import os
import torch
import math

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

def run_methane():
    # Start near a tetrahedral geometry to avoid the CH2.H2 local minimum at 0 K
    d = 0.5
    nuclei_info = [
        {'Z': 6, 'pos': [0.0, 0.0, 0.0]},           
        {'Z': 1, 'pos': [ d,  d,  d]},        
        {'Z': 1, 'pos': [-d, -d,  d]},        
        {'Z': 1, 'pos': [ d, -d, -d]},        
        {'Z': 1, 'pos': [-d,  d, -d]}         
    ]
    
    builder = EVMBuilder(device='cpu')
    engine = builder.build_engine(nuclei_info, batch_size=1)
    
    engine.damping_nuc = 0.0
    engine.damping_e = 0.90
    
    for step in range(5001):
        if step == 500:
            engine.damping_nuc = 0.99
            
        engine.step(dt=0.005)
        
        max_v = 0.05
        engine.nuc_vel = torch.clamp(engine.nuc_vel, -max_v, max_v)
        engine.e_vel = torch.clamp(engine.e_vel, -max_v*10, max_v*10)
        
        if step % 1000 == 0 or step == 5000:
            pos = engine.nuc_pos[0]
            angles = calculate_angles(pos)
            min_angle = min(angles)
            max_angle = max(angles)
            C = pos[0]
            dists = [torch.norm(pos[i] - C).item() for i in range(1, 5)]
            avg_dist = sum(dists)/4
            print(f"Step {step:>4}: Angles -> from {min_angle:.1f}° to {max_angle:.1f}° | Avg C-H bond length: {avg_dist:.3f} Å")

if __name__ == "__main__":
    run_methane()

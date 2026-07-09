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
    
    # Phase setup
    optimal_phases = [1.0, 1.0, -1.0, 1.0, -1.0, -1.0, 1.0, 1.0, -1.0, -1.0]
    engine.e_phase = torch.tensor(optimal_phases, dtype=torch.float32, device=engine.device).view(1, 10, 1)
    
    engine.damping_nuc = 0.0
    engine.damping_e = 0.90
    
    for step in range(5001):
        if step == 500:
            engine.damping_nuc = 0.99
            
        # DYNAMIC PHASE ANNEALING (Proxy for EVM 5.0 Vector Snap)
        # Every 100 steps, let's try to randomly swap two opposite spins
        # if it lowers the potential energy. But we don't have a get_energy() function exposed!
        # Actually, if we just scramble the phases randomly, it's a bad idea.
        
        engine.step(dt=0.005)
        
        max_v = 0.05
        engine.nuc_vel = torch.clamp(engine.nuc_vel, -max_v, max_v)
        engine.e_vel = torch.clamp(engine.e_vel, -max_v*10, max_v*10)
        
        if step % 1000 == 0 or step == 5000:
            pos = engine.nuc_pos[0]
            angles = calculate_angles(pos)
            min_angle = min(angles)
            max_angle = max(angles)
            print(f"Step {step:>4}: Angles -> from {min_angle:.1f}° to {max_angle:.1f}°")

if __name__ == "__main__":
    run_methane()

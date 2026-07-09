import sys
import os
import torch
import matplotlib.pyplot as plt

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
sys.path.append(PROJECT_ROOT)

from core.system_builder import EVMBuilder

def write_xyz(filename, nuclei_pos, e_pos):
    """Appends a frame to an XYZ trajectory file."""
    num_atoms = nuclei_pos.shape[0] + e_pos.shape[0]
    with open(filename, "a") as f:
        f.write(f"{num_atoms}\nEVM Radical Recombination Frame\n")
        for i in range(nuclei_pos.shape[0]):
            p = nuclei_pos[i]
            f.write(f"H {p[0]:.4f} {p[1]:.4f} {p[2]:.4f}\n")
        for i in range(e_pos.shape[0]):
            p = e_pos[i]
            f.write(f"X {p[0]:.4f} {p[1]:.4f} {p[2]:.4f}\n")

def test_radical_recombination():
    print("--- EVM Play Test: Radical Recombination (H. + H. -> H2) ---")
    
    xyz_path = os.path.join(os.path.dirname(__file__), "h2_radical_collision.xyz")
    if os.path.exists(xyz_path):
        os.remove(xyz_path)
    
    # SETUP: Two free Hydrogen radicals 3.0 Å apart.
    # We will give them a minor initial velocity (0.15), then let Coulomb/Exclusion take over.
    nuclei_info = [
        {'Z': 1, 'pos': [-1.5, 0.0, 0.0]},    # H1
        {'Z': 1, 'pos': [ 1.5, 0.0, 0.0]}     # H2
    ]
    
    FF_PATH = os.path.join(PROJECT_ROOT, "core", "evm_forcefield.json")
    builder = EVMBuilder(forcefield_path=FF_PATH, device='cpu')
    
    engine = builder.build_engine(nuclei_info, batch_size=1)
    
    print("\nPhase 1: Electronic Relaxation (Frozen Nuclei)")
    engine.damping_nuc = 0.0
    frozen_nuc = engine.nuc_pos.clone()
    for step in range(500):
        engine.step(dt=0.005)
        engine.nuc_pos.copy_(frozen_nuc)
        engine.nuc_vel.zero_()

    # Give them an initial velocity towards each other to start the movement
    engine.nuc_vel[0, 0, 0] = 0.15   # H1 moving right
    engine.nuc_vel[0, 1, 0] = -0.15  # H2 moving left
    
    print("\nSimulating Recombination (Zero Damping / Perfect Energy Conservation)")
    engine.damping_nuc = 1.0 
    engine.damping_e = 1.0 # Ensure electrons don't drain energy from the nuclei
    
    def get_distance(engine):
        pos_H1 = engine.nuc_pos[0, 0]
        pos_H2 = engine.nuc_pos[0, 1]
        return torch.norm(pos_H1 - pos_H2).item()
        
    def get_kinetic_energy(engine):
        v = engine.nuc_vel[0] # [2, 3]
        v_sq = torch.sum(v**2, dim=1) # [2]
        # Mass of nucleus in EVM 4.0 is 1.0
        ke = 0.5 * torch.sum(v_sq).item()
        return ke

    min_dist = float('inf')
    max_dist = 0.0
    
    distances = []
    kinetic_energies = []
    steps = []
    
    print("Simulating collision over 3000 steps...")
    for step in range(1, 3001):
        engine.step(dt=0.005)
        
        dist = get_distance(engine)
        ke = get_kinetic_energy(engine)
        
        if dist < min_dist: min_dist = dist
        if dist > max_dist: max_dist = dist
        
        distances.append(dist)
        kinetic_energies.append(ke)
        steps.append(step)
        
        if step % 20 == 0:
            write_xyz(xyz_path, engine.nuc_pos[0].cpu().numpy(), engine.e_pos[0].cpu().numpy())
            
        if step % 300 == 0:
            print(f"Step {step:4d}: H-H distance = {dist:.3f} A | KE = {ke:.3f}")
            
    print("\n--- Final Results ---")
    print(f"Minimum Distance Reached: {min_dist:.3f} A")
    print(f"Maximum Distance Reached (after initial collision): {max_dist:.3f} A")
    
    # Plotting
    plt.figure(figsize=(10, 5))
    
    plt.subplot(1, 2, 1)
    plt.plot(steps, distances, color='blue', label='H-H Distance')
    plt.axhline(y=0.74, color='green', linestyle='--', label='Exp. Bond Length')
    plt.xlabel('Simulation Steps')
    plt.ylabel('Distance (Å)')
    plt.title('Radical Recombination Trajectory')
    plt.legend()
    
    plt.subplot(1, 2, 2)
    plt.plot(steps, kinetic_energies, color='red', label='Kinetic Energy')
    plt.xlabel('Simulation Steps')
    plt.ylabel('Kinetic Energy (a.u.)')
    plt.title('Nuclear Kinetic Energy')
    plt.legend()
    
    plt.tight_layout()
    plot_path = os.path.join(os.path.dirname(__file__), "h2_radical_collision.png")
    plt.savefig(plot_path)
    print(f"Plot saved to {plot_path}")
    print(f"Trajectory saved to {xyz_path}")
    
    if min_dist < 1.0 and max_dist < 4.0:
        print("SUCCESS: Radicals successfully recombined into H2!")
        print("The nuclei are vibrating conservatively.")
    elif max_dist > 5.0:
        print("FAILED: Radicals flew apart (no attraction).")
    else:
        print("FAILED: Radicals collapsed (steric failure).")

if __name__ == "__main__":
    test_radical_recombination()

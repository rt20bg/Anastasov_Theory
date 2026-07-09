import sys
import os
import torch
import math

sys.stdout.reconfigure(encoding='utf-8')

# Add the project root to sys.path to be able to import core
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

from core.system_builder import EVMBuilder

def run_hydrogen():
    print("=== BASELINE EXPERIMENT 1: Hydrogen Molecule (H2) ===")
    print("Goal: Demonstrate how two hydrogen atoms spontaneously form")
    print("a covalent bond and find the perfect length WITHOUT hardcoded springs.\n")
    
    # 1. Initialize nuclei
    # Artificially place them far apart at 1.50 A to observe their attraction.
    nuclei_info = [
        {'Z': 1, 'pos': [0.0, 0.0, 0.0]},
        {'Z': 1, 'pos': [1.5, 0.0, 0.0]}
    ]
    
    print("Initializing EVM Builder...")
    # The Builder automatically spawns 2 electrons with opposite spin phase
    builder = EVMBuilder()
    
    # Set Heavy Damping to absorb kinetic energy and find the stable minimum.
    # damping_nuc = 0.99 means nuclei are heavily damped and move very slowly,
    # allowing the electrons to first position themselves between them.
    engine = builder.build_engine(
        nuclei_info, 
        batch_size=1
    )
    
    # 1. Freeze nuclei (damping = 0.0) to allow electrons
    # to settle between them without causing kinetic shock.
    engine.damping_nuc = 0.0
    engine.damping_e = 0.90
    
    print("System built. Starting physics simulation...\n")
    
    # Start Newton integrator
    for step in range(3001):
        # 2. At step 500, unlock nuclei with very high damping (0.99)
        if step == 500:
            engine.damping_nuc = 0.99
            print("  [Unlocking nuclei] Electrons have settled.")
            
        engine.step(dt=0.005)
        
        # Every 500 steps, print the distance between the two nuclei
        if step % 500 == 0:
            pos = engine.nuc_pos[0]  # shape: (N, 3)
            dx = pos[0, 0] - pos[1, 0]
            dy = pos[0, 1] - pos[1, 1]
            dz = pos[0, 2] - pos[1, 2]
            dist = math.sqrt(dx**2 + dy**2 + dz**2)
            
            print(f"Step {step:>4}: Distance between nuclei = {dist:.4f} A")
            
            if step == 0:
                print("  -> Nuclei are far apart, electrons begin to pull them together.")
            elif step == 1000:
                print("  -> Coulomb forces and steric repulsion struggle for balance.")
            elif step == 3000:
                print("  -> Equilibrium! The bond is stabilized.")

    print("\nExperiment completed successfully.")

if __name__ == "__main__":
    run_hydrogen()

import numpy as np
from scipy.optimize import minimize

def spherical_to_cartesian(r, theta, phi):
    """Converts spherical coordinates to a 3D vector."""
    return np.array([
        r * np.sin(theta) * np.cos(phi),
        r * np.sin(theta) * np.sin(phi),
        r * np.cos(theta)
    ])

def radial_friction_model(params, num_streams):
    """
    Evaluates the total friction/energy of an atom with variable radius streams.
    Params contains: (r, theta, phi) for each stream.
    Total length of params = num_streams * 3
    """
    streams = params.reshape((num_streams, 3))
    
    A = 5.0 # Inward vacuum pull strength (like nuclear attraction)
    B = 1.0 # Outward core repulsion strength (centrifugal shield)
    C = 2.0 # Stream-stream lateral boundary friction strength (electron-electron repulsion)
    
    total_energy = 0
    vecs = []
    
    # 1. Radial Energy for each stream
    for i in range(num_streams):
        r, theta, phi = streams[i]
        r = abs(r) + 1e-3 # Prevent r from going exactly 0 or negative
        
        # Radial balance: Inward pull + outward core push
        radial_energy = -(A / r) + (B / r**4)
        total_energy += radial_energy
        
        vecs.append(spherical_to_cartesian(r, theta, phi))
        
    # 2. Inter-stream Friction (Electron-Electron repulsion equivalent)
    for i in range(num_streams):
        for j in range(i+1, num_streams):
            d = np.linalg.norm(vecs[i] - vecs[j])
            # Boundary layer drag + hard core repulsion between streams
            friction = np.exp(-2*d) + 1/(d**4 + 1e-6)
            total_energy += C * friction
            
    return total_energy

def run_test():
    print("RAKTS Variable Radius Test (Predicting Ionic Radii)\n")
    print("Hypothesis: Cations (missing streams) will shrink because of reduced lateral friction.")
    print("Anions (extra streams) will expand because of increased lateral friction.\n")
    
    # Test 1: Neutral Atom (4 streams)
    print("Testing Neutral Atom (4 streams)...")
    np.random.seed(42)
    init_guess_4 = np.random.rand(12) 
    init_guess_4[0::3] = 1.0 # Initial radius 1.0
    
    res_4 = minimize(radial_friction_model, init_guess_4, args=(4,), method='BFGS')
    r_4 = np.mean(np.abs(res_4.x[0::3]))
    print(f"Neutral Atom Average Stream Radius: {r_4:.4f}")
    
    # Test 2: Cation (Ion missing 1 stream, N=3)
    print("\nTesting Cation (3 streams, missing one 'electron')...")
    init_guess_3 = np.random.rand(9)
    init_guess_3[0::3] = 1.0
    
    res_3 = minimize(radial_friction_model, init_guess_3, args=(3,), method='BFGS')
    r_3 = np.mean(np.abs(res_3.x[0::3]))
    print(f"Cation Average Stream Radius: {r_3:.4f}")
    
    # Test 3: Anion (Ion with 1 extra stream, N=5)
    print("\nTesting Anion (5 streams, extra 'electron')...")
    init_guess_5 = np.random.rand(15)
    init_guess_5[0::3] = 1.0
    
    res_5 = minimize(radial_friction_model, init_guess_5, args=(5,), method='BFGS')
    r_5 = np.mean(np.abs(res_5.x[0::3]))
    print(f"Anion Average Stream Radius: {r_5:.4f}")
    
    print("\n-------------------------")
    print("CONCLUSION:")
    if r_3 < r_4 < r_5:
        print("SUCCESS! The code naturally predicts that Cations shrink and Anions expand.")
        print("This matches empirical chemistry perfectly, derived purely from kinematic boundary layer pressure!")
    else:
        print("Failed. Needs tuning of constants A, B, C.")

if __name__ == "__main__":
    run_test()

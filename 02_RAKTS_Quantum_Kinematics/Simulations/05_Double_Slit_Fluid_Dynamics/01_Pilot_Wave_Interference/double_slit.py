import numpy as np
import matplotlib.pyplot as plt
import os

def simulate_double_slit():
    # Simulation Parameters
    wavelength = 1.0
    k = 2 * np.pi / wavelength
    slit_dist = 4.0
    
    # 2D Grid for plotting the background Field Medium interference pattern
    Y, X = np.mgrid[0.1:20:200j, -10:10:200j]
    
    # Distance to the two slits (located at y=0, x = -slit_dist/2 and x = +slit_dist/2)
    r1 = np.sqrt((X - slit_dist/2)**2 + Y**2)
    r2 = np.sqrt((X + slit_dist/2)**2 + Y**2)
    
    # The Pilot Wave Interference Intensity (Constructive & Destructive)
    Intensity = (np.cos(k * r1) + np.cos(k * r2))**2
    
    plt.figure(figsize=(10, 8))
    # Plot the fluid wave intensity as a background heatmap
    plt.pcolormesh(X, Y, Intensity, cmap='Blues', shading='auto', alpha=0.5)
    
    # Simulate Particle Trajectories
    # Particles are guided by the gradient of the intensity field
    dt = 0.05
    C = 0.5 # Coupling constant (how strongly the fluid wave pushes the particle)
    vy = 1.0 # Constant forward velocity
    
    # Define a helper function to calculate the gradient numerically
    def get_gradient_x(x, y):
        # Prevent division by zero near the origin
        if y < 0.5: return 0
        r1_right = np.sqrt((x + 0.01 - slit_dist/2)**2 + y**2)
        r2_right = np.sqrt((x + 0.01 + slit_dist/2)**2 + y**2)
        I_right = (np.cos(k * r1_right) + np.cos(k * r2_right))**2
        
        r1_left = np.sqrt((x - 0.01 - slit_dist/2)**2 + y**2)
        r2_left = np.sqrt((x - 0.01 + slit_dist/2)**2 + y**2)
        I_left = (np.cos(k * r1_left) + np.cos(k * r2_left))**2
        
        return (I_right - I_left) / 0.02

    np.random.seed(42)
    
    # Simulate 50 particles going through Left Slit, 50 through Right Slit
    for slit_pos in [-slit_dist/2, slit_dist/2]:
        for _ in range(50):
            # Start at the slit with slight thermal noise in X angle
            x = slit_pos + np.random.normal(0, 0.1)
            y = 0.1
            traj_x, traj_y = [x], [y]
            
            while y < 20:
                # The particle "surfs" the wave. It climbs the intensity gradients.
                grad_x = get_gradient_x(x, y)
                # Damping to prevent them from shooting off infinitely
                x += C * grad_x * dt
                y += vy * dt
                
                traj_x.append(x)
                traj_y.append(y)
                
            color = 'red' if slit_pos < 0 else 'orange'
            plt.plot(traj_x, traj_y, color=color, alpha=0.6, linewidth=1.5)

    # Draw the slits
    plt.plot([-10, -slit_dist/2 - 0.5], [0, 0], 'k-', lw=5)
    plt.plot([-slit_dist/2 + 0.5, slit_dist/2 - 0.5], [0, 0], 'k-', lw=5)
    plt.plot([slit_dist/2 + 0.5, 10], [0, 0], 'k-', lw=5)

    plt.title("RAKTS: The Double Slit Fluid Illusion\nClassical particles (lines) surf the continuous Field Medium interference pattern (blue)")
    plt.xlabel("Screen Position (X)")
    plt.ylabel("Distance from Slits (Y)")
    plt.xlim(-10, 10)
    plt.ylim(0, 20)
    
    save_path = os.path.join(os.path.dirname(__file__), "double_slit.png")
    plt.savefig(save_path)
    print(f"Double Slit plot saved to {save_path}")

if __name__ == "__main__":
    simulate_double_slit()

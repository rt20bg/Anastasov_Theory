import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import solve_ivp
import os

# Ensure the output directory exists
os.makedirs("02_RAKTS_Quantum_Kinematics/Computational_Validations/Tests/Test9_Frisch_Segre", exist_ok=True)

def llg_equation(t, s, B_func, alpha):
    """
    Classical Landau-Lifshitz-Gilbert (LLG) type equation of motion 
    with hydrodynamic Field Medium damping.
    ds/dt = s x B - alpha * s x (s x B)
    """
    B = B_func(t)
    s_cross_B = np.cross(s, B)
    damping = -alpha * np.cross(s, s_cross_B)
    return s_cross_B + damping

def simulate_transit(flight_time, alpha, B0=1.0):
    """
    Simulates the transit of a spin vortex through a rotating magnetic field.
    The field rotates from +z to -z over the course of the flight_time.
    """
    # Define rotating field: B(t) rotates in the x-z plane
    def B_field(t):
        theta = (t / flight_time) * np.pi
        return np.array([B0 * np.sin(theta), 0.0, B0 * np.cos(theta)])
    
    # Initial state: fully aligned with the initial field B(0) = [0, 0, B0] (parallel to +z)
    s0 = np.array([0.0, 0.0, 1.0])
    
    # Solve ODE
    t_span = (0.0, flight_time)
    sol = solve_ivp(llg_equation, t_span, s0, args=(B_field, alpha), rtol=1e-8, atol=1e-8)
    
    # Final state
    s_final = sol.y[:, -1]
    s_final /= np.linalg.norm(s_final) # Normalize
    
    # Final field direction is along -z
    B_final = B_field(flight_time)
    B_final_dir = B_final / np.linalg.norm(B_final)
    
    # Projection onto the final field direction (1 = adiabatic tracking, -1 = spin flip)
    projection = np.dot(s_final, B_final_dir)
    return projection

# Parameters
alpha = 0.5  # Hydrodynamic drag/viscosity coefficient of the Field Medium
flight_times = np.logspace(-1.5, 2.0, 50)  # Logarithmic range of flight times (Delta t_flight)
projections = []

# Run simulations
for ft in flight_times:
    proj = simulate_transit(ft, alpha)
    projections.append(proj)

# Plotting the Frisch-Segre Adiabatic to Non-Adiabatic Transition
plt.figure(figsize=(9, 5.5))
plt.style.use('seaborn-v0_8-whitegrid' if 'seaborn-v0_8-whitegrid' in plt.style.available else 'default')

# Custom premium styling
plt.rcParams['font.family'] = 'DejaVu Sans'
plt.plot(flight_times, projections, '-', color='#1f77b4', linewidth=2.5, label='RAKTS Classical Damping Model')

# Theoretical thresholds
plt.axvline(x=1.0/alpha, color='#d62728', linestyle='--', linewidth=1.5, 
            label=r'Critical Limit: $\Delta t_{flight} \approx \tau_{drag}$')

# Shaded regions
plt.axvspan(0.03, 1.0/alpha, color='#d62728', alpha=0.1, label='Non-Adiabatic Regime (Spin Flip)')
plt.axvspan(1.0/alpha, 100, color='#2ca02c', alpha=0.1, label='Adiabatic Tracking (Continuous Alignment)')

# Labels and configuration
plt.xscale('log')
plt.xlabel(r'Flight Time Through Transition Zone $\Delta t_{flight}$ (arbitrary units)', fontsize=12)
plt.ylabel('Final Alignment Projection (Spin State)', fontsize=12)
plt.title('Frisch-Segrè 1933 Experiment: Adiabatic vs. Non-Adiabatic Transition\nClassical Hydrodynamic Alignment Lag (RAKTS)', fontsize=13, fontweight='bold', pad=15)
plt.ylim(-1.05, 1.05)
plt.yticks([-1, 0, 1], ['-1 (Spin Flip / Unaligned)', '0 (Smear)', '+1 (Tracked / Aligned)'])
plt.legend(loc='lower right', frameon=True, facecolor='white', edgecolor='#e0e0e0', framealpha=0.9)
plt.tight_layout()

# Save the plot
output_dir = "02_RAKTS_Quantum_Kinematics/Computational_Validations/Tests/Test9_Frisch_Segre"
if not os.path.exists(output_dir):
    os.makedirs(output_dir)
output_path = os.path.join(output_dir, "frisch_segre_transition.png")
plt.savefig(output_path, dpi=300)
plt.close()

print(f"Simulation completed successfully. Plot saved to: {output_path}")

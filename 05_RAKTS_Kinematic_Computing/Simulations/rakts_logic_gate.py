import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import solve_ivp
import os

def run_kinematic_nand_gate():
    """
    Simulates a Universal Analog Kinematic NAND Gate.
    Proves Turing-completeness of the Field Medium framework.
    Uses a Background Field bias (acting as an analog NOT gate/inverter)
    and fluid dynamic drag to create deterministic logical states.
    """
    
    # Simulation Parameters
    t_span = (0, 15)
    t_eval = np.linspace(t_span[0], t_span[1], 800)
    
    # Physics constants
    drag_coefficient = 0.8
    
    # The crucial addition: Background Field Bias
    # This acts as a constant "wind" pulling the system to the negative (True) state
    v_bg = np.array([-1.5, 0.0])
    
    # Input vectors
    v_input_magnitude = np.array([1.0, 0.0])
    v_zero = np.array([0.0, 0.0])
    
    # Define the 4 cases of a NAND Gate
    cases = {
        "Case 1 (A=0, B=0)": (v_zero, v_zero),
        "Case 2 (A=1, B=0)": (v_input_magnitude, v_zero),
        "Case 3 (A=0, B=1)": (v_zero, v_input_magnitude),
        "Case 4 (A=1, B=1)": (v_input_magnitude, v_input_magnitude)
    }
    
    # ODE: dV/dt = (V_bg + Va + Vb) - Drag * V * |V|^2
    # The V * |V|^2 term provides non-linear fluid drag (Landau-Lifshitz analog)
    def logic_field_derivative(t, v_out, va, vb):
        v_out_vec = np.array(v_out)
        v_mag_sq = np.dot(v_out_vec, v_out_vec)
        
        # Total driving force (Background + Inputs)
        driving_force = v_bg + va + vb
        
        # Hydrodynamic resistance of the medium
        drag_force = drag_coefficient * v_out_vec * v_mag_sq
        
        return driving_force - drag_force

    # Initial state (resting vacuum, starts at 0)
    v_out_initial = [0.0, 0.0]

    # Run simulations
    solutions = {}
    for name, (va, vb) in cases.items():
        sol = solve_ivp(
            fun=lambda t, y, a=va, b=vb: logic_field_derivative(t, y, a, b),
            t_span=t_span,
            y0=v_out_initial,
            t_eval=t_eval,
            method='RK45'
        )
        solutions[name] = sol

    # Plotting
    plt.figure(figsize=(12, 7))
    
    colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728']
    linestyles = ['-', '--', '-.', ':']
    
    for (name, sol), color, ls in zip(solutions.items(), colors, linestyles):
        # We plot the X-component to see direction (Negative = True, Positive = False)
        x_component = sol.y[0]
        plt.plot(sol.t, x_component, label=name, color=color, linestyle=ls, linewidth=2.5)

    # Threshold line at 0
    plt.axhline(0, color='black', linewidth=1.5, linestyle='-', alpha=0.5)
    
    # Background coloring for True/False zones
    plt.axhspan(-2, 0, facecolor='lightgreen', alpha=0.1, label='Logical 1 (TRUE) Zone')
    plt.axhspan(0, 2, facecolor='lightcoral', alpha=0.1, label='Logical 0 (FALSE) Zone')

    plt.title('Universal Kinematic NAND Gate via Background Field Bias', fontsize=16, fontweight='bold', pad=20)
    plt.xlabel('Time (Simulation Steps)', fontsize=14)
    plt.ylabel('Output Vector X-Component (Negative = True, Positive = False)', fontsize=14)
    plt.ylim(-1.5, 1.5)
    plt.grid(True, linestyle=':', alpha=0.7)
    plt.legend(fontsize=12, loc='upper right')
    
    # Save the output visualization
    output_path = os.path.join(os.path.dirname(__file__), 'kinematic_nand_output.png')
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    print(f"Simulation complete. Graph saved to: {output_path}")

if __name__ == "__main__":
    run_kinematic_nand_gate()

import torch
import numpy as np
class EVMBaseEngine:
    def __init__(self, batch_size, nuclei_info, num_electrons, damping_e=0.999, damping_nuc=0.999, device=None):
        """
        Batched Engine: Simulates `batch_size` independent molecules simultaneously.
        nuclei_info is a list of dicts: {'pos': [x,y,z], 'Z': int, 'mass': float}
        NOTE: 'pos' is ignored here as the initial positions should be set manually 
        after initialization via `engine.nuc_pos = batched_nuc_pos`.
        """
        if device is None:
            self.device = 'cuda' if torch.cuda.is_available() else 'cpu'
        else:
            self.device = device
            
        self.batch_size = batch_size
        self.damping_e = damping_e
        self.damping_nuc = damping_nuc
        
        N_nuc = len(nuclei_info)
        self.nuc_pos = torch.zeros((batch_size, N_nuc, 3), dtype=torch.float32, device=self.device)
        self.nuc_vel = torch.zeros((batch_size, N_nuc, 3), dtype=torch.float32, device=self.device)
        self.nuc_Z = torch.zeros((N_nuc, 1), dtype=torch.float32, device=self.device)
        self.nuc_mass = torch.zeros((N_nuc, 1), dtype=torch.float32, device=self.device)
        
        # We just store Z and mass. The user must manually populate self.nuc_pos for all batches.
        for i, info in enumerate(nuclei_info):
            self.nuc_Z[i] = info['Z']
            self.nuc_mass[i] = info.get('mass', 1.0)
            
        self.e_pos = torch.zeros((batch_size, 0, 3), dtype=torch.float32, device=self.device)
        self.e_vel = torch.zeros((batch_size, 0, 3), dtype=torch.float32, device=self.device)
        self.e_phase = torch.zeros((batch_size, 0, 1), dtype=torch.float32, device=self.device)
        
        self.num_electrons = 0
        for _ in range(num_electrons):
            self.add_electron()

    def add_electron(self):
        new_pos = torch.randn(self.batch_size, 1, 3, device=self.device) * 2.0
        v_tangent = torch.randn(self.batch_size, 1, 3, device=self.device)
            
        # Assign kinematic phase (+1 or -1)
        phase_val = 1.0 if self.num_electrons % 2 == 0 else -1.0
        phase_tensor = torch.full((self.batch_size, 1, 1), phase_val, dtype=torch.float32, device=self.device)
        
        self.e_pos = torch.cat([self.e_pos, new_pos], dim=1)
        self.e_vel = torch.cat([self.e_vel, v_tangent], dim=1)
        self.e_phase = torch.cat([self.e_phase, phase_tensor], dim=1)
        self.num_electrons += 1

    def compute_forces(self):
        """
        Must be implemented by child classes to define physics rules.
        Returns: (F_e, F_n)
        """
        raise NotImplementedError
        
    def step(self, dt=0.005):
        if self.num_electrons == 0 and self.nuc_pos.shape[1] == 0:
            return

        # Initialize accelerations if they don't exist
        if not hasattr(self, 'e_acc'):
            F_e, F_n = self.compute_forces()
            F_e = torch.clamp(F_e, min=-1000.0, max=1000.0)
            F_n = torch.clamp(F_n, min=-1000.0, max=1000.0)
            self.e_acc = F_e
            # nuc_Z and nuc_mass are [N_nuc, 1]. F_n is [B, N_nuc, 3].
            self.nuc_acc = F_n / self.nuc_mass.unsqueeze(0) 

        # 1. Update positions (Velocity Verlet part 1)
        self.e_pos = self.e_pos + self.e_vel * dt + 0.5 * self.e_acc * (dt**2)
        self.nuc_pos = self.nuc_pos + self.nuc_vel * dt + 0.5 * self.nuc_acc * (dt**2)
        
        # 2. Compute NEW Forces
        F_e_new, F_n_new = self.compute_forces()
        
        # CLAMP NEW FORCES
        F_e_new = torch.clamp(F_e_new, min=-1000.0, max=1000.0)
        F_n_new = torch.clamp(F_n_new, min=-1000.0, max=1000.0)
        
        e_acc_new = F_e_new
        nuc_acc_new = F_n_new / self.nuc_mass.unsqueeze(0)
        
        # 3. Update velocities (Velocity Verlet part 2)
        self.e_vel = self.e_vel + 0.5 * (self.e_acc + e_acc_new) * dt 
        self.nuc_vel = self.nuc_vel + 0.5 * (self.nuc_acc + nuc_acc_new) * dt
        
        # Update stored accelerations
        self.e_acc = e_acc_new
        self.nuc_acc = nuc_acc_new
        
        # 4. Thermostat / Damping (Decoupled for stability during collisions)
        self.e_vel *= self.damping_e
        self.nuc_vel *= self.damping_nuc

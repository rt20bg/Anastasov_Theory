import torch
import numpy as np
import json
import os
from core.engine import EVMCompressibleEngine

class EVMBuilder:
    def __init__(self, forcefield_path="evm_forcefield.json", device='cpu'):
        self.device = device
        self.ff = self._load_forcefield(forcefield_path)
        
    def _load_forcefield(self, path):
        if not os.path.isabs(path):
            path = os.path.join(os.path.dirname(__file__), path)
        with open(path, 'r') as f:
            return json.load(f)
            
    def build_engine(self, nuclei_info, batch_size=1):
        """
        Builds the EVM engine for a specific molecule using the loaded forcefield.
        nuclei_info: list of dicts [{'Z': 6, 'pos': [x,y,z]}, ...]
        """
        # Calculate total electrons
        num_electrons = sum(info['Z'] for info in nuclei_info)
        
        # Build global parameter tensors for the engine
        global_R = torch.zeros(batch_size, 10, dtype=torch.float32, device=self.device)
        global_excl = torch.zeros(batch_size, 10, dtype=torch.float32, device=self.device)
        
        # Populate from forcefield
        for z_str, params in self.ff["elements"].items():
            Z = int(z_str)
            global_R[:, Z] = params["R"]
            global_excl[:, Z] = params["Excl"]
            
        spin_pairing_tensor = torch.tensor([self.ff["spin_pairing"]] * batch_size, dtype=torch.float32, device=self.device)
        
        # Build electron mapping
        e_idx_list = []
        for info in nuclei_info:
            Z = info['Z']
            e_idx_list.extend([Z] * Z)
        e_idx_tensor = torch.tensor(e_idx_list, dtype=torch.long, device=self.device)
        
        # Add 'idx' and 'mass' to nuclei_info if missing (required by base_engine)
        for i, info in enumerate(nuclei_info):
            if 'idx' not in info:
                info['idx'] = info['Z']
            if 'mass' not in info:
                # EVM 4.0 uses a Car-Parrinello style optimization where nuclei and electron masses are equal (1.0).
                # This accelerates gradient descent to static equilibrium. True dynamic masses are reserved for EVM 5.0.
                info['mass'] = 1.0
        
        U_0 = self.ff.get("U_0", 10.0)
        nn_steric = self.ff.get("nn_steric", 0.001)
        
        # Instantiate Engine
        engine = EVMCompressibleEngine(
            batch_size=batch_size,
            nuclei_info=nuclei_info,
            num_electrons=num_electrons,
            e_idx_tensor=e_idx_tensor,
            global_excl=global_excl,
            global_R=global_R,
            damping_e=0.8,
            damping_nuc=0.99,
            spin_pairing_tensor=spin_pairing_tensor,
            U_0=U_0,
            nn_steric=nn_steric,
            device=self.device
        )
        
        # Setup initial positions (Engine expects batched tensors)
        nuc_pos = torch.tensor([info['pos'] for info in nuclei_info], dtype=torch.float32, device=self.device)
        engine.nuc_pos = nuc_pos.unsqueeze(0).expand(batch_size, -1, -1).clone()
        
        # Electron Initializer (Spawn electrons around nuclei)
        e_pos_single = []
        e_phases_single = []
        e_idx_global = 0
        
        for info in nuclei_info:
            Z = info['Z']
            pos = info['pos']
            for i in range(Z):
                phi = np.arccos(1 - 2*(i+0.5)/Z)
                theta = np.pi * (1 + 5**0.5) * i
                x = pos[0] + 0.3 * np.sin(phi) * np.cos(theta)
                y = pos[1] + 0.3 * np.sin(phi) * np.sin(theta)
                z = pos[2] + 0.3 * np.cos(phi)
                e_pos_single.append([x, y, z])
                
                # EVM 4.0 STATIC PHASE INITIALIZATION:
                # We use a global alternating index (e_idx_global) instead of a local atom-based index (i).
                # This ensures the entire system has a perfectly balanced number of +1 and -1 phases, 
                # allowing spontaneous bond formation. Since EVM 4.0 lacks dynamic spin-flipping (Larmor Precession), 
                # this global parity acts as a proxy for the system finding its lowest magnetic energy state.
                e_phases_single.append(1.0 if e_idx_global % 2 == 0 else -1.0)
                e_idx_global += 1
                
        e_pos_tensor = torch.tensor(e_pos_single, dtype=torch.float32, device=self.device)
        engine.e_pos = e_pos_tensor.unsqueeze(0).expand(batch_size, -1, -1).clone()
        
        e_phases_tensor = torch.tensor(e_phases_single, dtype=torch.float32, device=self.device).unsqueeze(1)
        engine.e_phase = e_phases_tensor.unsqueeze(0).expand(batch_size, -1, -1).clone()
        
        engine.e_vel.zero_()
        engine.nuc_vel.zero_()
        
        return engine

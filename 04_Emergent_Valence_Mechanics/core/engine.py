import torch
import torch.nn as nn
from core.base_engine import EVMBaseEngine

class EVMCompressibleEngine(EVMBaseEngine, nn.Module):
    """
    Batched EVM 3.1: Compressible Electron Clouds.
    Simulates `batch_size` independent molecules simultaneously.
    """
    def __init__(self, batch_size, nuclei_info, num_electrons, e_idx_tensor, global_excl, global_R, damping_e=0.8, damping_nuc=0.8, spin_pairing_tensor=None, U_0=10.0, nn_steric=0.001, device='cpu'):
        super().__init__(batch_size, nuclei_info, num_electrons, damping_e, damping_nuc, device)
        self.exclusion_params = global_excl
        self.R_params = global_R
        self.e_idx_tensor = e_idx_tensor
        self.spin_pairing = spin_pairing_tensor # [B]
        self.U_0 = U_0
        self.nn_steric = nn_steric
        
        self.e_element_idx = e_idx_tensor
        
    def compute_forces(self):
        B = self.batch_size
        N_e = self.num_electrons
        N_nuc = len(self.nuc_pos[0])
        
        F_e = torch.zeros_like(self.e_pos) # [B, N_e, 3]
        F_n = torch.zeros_like(self.nuc_pos) # [B, N_nuc, 3]
        
        curr_excls = torch.abs(self.exclusion_params) # [10] or [B, 10]
        curr_Rs = torch.abs(self.R_params) # [10] or [B, 10]
        
        # Map element parameters to each electron
        if curr_excls.dim() == 2:
            # Batched params: [B, 10]
            e_excl = curr_excls[:, self.e_element_idx] # [B, N_e]
            e_R = curr_Rs[:, self.e_element_idx] # [B, N_e]
        else:
            # Single params: [10] -> [1, N_e] broadcasted
            e_excl = curr_excls[self.e_element_idx].unsqueeze(0).expand(B, -1) # [B, N_e]
            e_R = curr_Rs[self.e_element_idx].unsqueeze(0).expand(B, -1) # [B, N_e]
        
        # --- Precompute Electron-Nucleus differences for compressibility and forces ---
        if N_e > 0 and N_nuc > 0:
            diff_en = self.e_pos.unsqueeze(2) - self.nuc_pos.unsqueeze(1) # [B, N_e, N_nuc, 3]
            dist_sq_en = torch.sum(diff_en**2, dim=3) + 1e-6 # [B, N_e, N_nuc]
            dist_en = torch.sqrt(dist_sq_en)
            
            # nuc_Z is [N_nuc, 1]. Transpose to [1, N_nuc], then unsqueeze for [1, 1, N_nuc]
            Z_matrix_en = self.nuc_Z.T.unsqueeze(0) 
            
            # Compressibility: U_coulomb = sum_nuc (Z / r) -> [B, N_e]
            U_coulomb = torch.sum(Z_matrix_en / dist_en, dim=2) 
            compression_factor = torch.exp(-U_coulomb / self.U_0) # [B, N_e]
        else:
            compression_factor = torch.ones(B, N_e, dtype=torch.float32, device=self.device)
            
        # Effective exclusion based on compression
        e_excl_eff = e_excl * compression_factor # [B, N_e]
        
        # Pairwise exclusion matrix [B, N_e, N_e]
        excl_pair = (e_excl_eff.unsqueeze(2) + e_excl_eff.unsqueeze(1)) / 2.0 
        
        # a. e-e repulsion
        if N_e > 1:
            diff_ee = self.e_pos.unsqueeze(2) - self.e_pos.unsqueeze(1) # [B, N_e, N_e, 3]
            dist_sq_ee = torch.sum(diff_ee**2, dim=3) + 1e-6 # [B, N_e, N_e]
            dist_ee = torch.sqrt(dist_sq_ee)
            
            phase_match = (self.e_phase.unsqueeze(2) == self.e_phase.unsqueeze(1)).squeeze(3).float()
            phase_mismatch = 1.0 - phase_match
            
            # Spin Pairing: Opposite spins magnetically attract, reducing their net Coulomb repulsion
            sp = self.spin_pairing.unsqueeze(1).unsqueeze(2) # [B, 1, 1]
            f_coulomb_mag = (1.0 - sp * phase_mismatch) / dist_sq_ee
            
            f_exclusion_mag = phase_match * excl_pair / (dist_sq_ee ** 3)
            
            f_ee_total = (f_coulomb_mag + f_exclusion_mag).unsqueeze(3) * (diff_ee / dist_ee.unsqueeze(3))
            # Zero out self-interaction
            f_ee_total.diagonal(dim1=1, dim2=2).fill_(0)
            F_e += torch.sum(f_ee_total, dim=2)
            
        # b. n-n repulsion
        if N_nuc > 1:
            diff_nn = self.nuc_pos.unsqueeze(2) - self.nuc_pos.unsqueeze(1) # [B, N_nuc, N_nuc, 3]
            dist_sq_nn = torch.sum(diff_nn**2, dim=3) # [B, N_nuc, N_nuc]
            
            # Z is [N_nuc, 1]. Z * Z^T -> [N_nuc, N_nuc] -> [1, N_nuc, N_nuc]
            Z_matrix = (self.nuc_Z @ self.nuc_Z.T).unsqueeze(0)
            
            f_coulomb_nn = Z_matrix / (dist_sq_nn + 1e-6)
            f_steric_nn = self.nn_steric / ((dist_sq_nn + 1e-6)**6)
            
            f_nn_mag = f_coulomb_nn + f_steric_nn
            
            f_nn_total = f_nn_mag.unsqueeze(3) * (diff_nn / (torch.sqrt(dist_sq_nn).unsqueeze(3) + 1e-6))
            f_nn_total.diagonal(dim1=1, dim2=2).fill_(0)
            F_n += torch.sum(f_nn_total, dim=2)
            
        # c. e-n attraction & steric
        if N_e > 0 and N_nuc > 0:
            f_en_mag = -Z_matrix_en / dist_sq_en # [B, N_e, N_nuc]
            
            e_R_matrix = e_R.unsqueeze(2).expand(-1, -1, N_nuc) # [B, N_e, N_nuc]
            f_en_steric = 12 * (e_R_matrix**12) / (dist_sq_en**6.5)
            
            f_en_total = (f_en_mag + f_en_steric).unsqueeze(3) * (diff_en / dist_en.unsqueeze(3)) # [B, N_e, N_nuc, 3]
            
            F_e += torch.sum(f_en_total, dim=2)
            F_n -= torch.sum(f_en_total, dim=1)
            
        return F_e, F_n

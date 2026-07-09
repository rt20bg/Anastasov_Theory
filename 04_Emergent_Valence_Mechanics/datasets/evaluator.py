import torch

class EVMEvaluator:
    @staticmethod
    def calculate_rmsd(pos_pred, pos_true):
        """
        Calculates the Root Mean Square Deviation (RMSD) between predicted and true coordinates.
        Both should be PyTorch tensors of shape [N, 3] or [B, N, 3].
        Returns a single float or a tensor of shape [B].
        """
        # Note: This calculates raw coordinate RMSD without Kabsch (Procrustes) alignment.
        # This makes the metric strictly conservative, as any whole-molecule translation or rotation 
        # during the simulation will be penalized as deformation.
        diff = pos_pred - pos_true
        sq_dist = torch.sum(diff ** 2, dim=-1) # [N] or [B, N]
        mean_sq_dist = torch.mean(sq_dist, dim=-1) # Scalar or [B]
        rmsd = torch.sqrt(mean_sq_dist)
        return rmsd

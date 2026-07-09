import os
from rdkit import Chem

SUPPORTED_ATOMS = {1, 6, 7, 8, 9} # H, C, N, O, F

class QM9Loader:
    def __init__(self, sdf_path):
        if not os.path.exists(sdf_path):
            raise FileNotFoundError(f"Cannot find QM9 SDF at {sdf_path}")
        self.sdf_path = sdf_path
        
    def stream_molecules(self, batch_size=1, max_molecules=None):
        """
        Streams molecules from the SDF file.
        Yields batches of molecules ready to be fed to EVMBuilder.
        Returns a tuple: (batch_nuclei_info, batch_mols)
        Where batch_nuclei_info is a list of nuclei_info lists, one for each molecule.
        """
        supplier = Chem.SDMolSupplier(self.sdf_path, removeHs=False, sanitize=True)
        
        batch_nuclei_info = []
        batch_mols = []
        count = 0
        
        for mol in supplier:
            if mol is None:
                continue
                
            # Filter out any theoretically unsupported atoms (QM9 contains H, C, N, O, F, which are all natively supported by EVM 4.0)
            supported = True
            for atom in mol.GetAtoms():
                if atom.GetAtomicNum() not in SUPPORTED_ATOMS:
                    supported = False
                    break
                    
            if not supported:
                continue
                
            # Extract true DFT geometry
            conf = mol.GetConformer()
            nuclei_info = []
            for i, atom in enumerate(mol.GetAtoms()):
                pos = conf.GetAtomPosition(i)
                nuclei_info.append({
                    'Z': atom.GetAtomicNum(),
                    'pos': [pos.x, pos.y, pos.z]
                })
                
            batch_nuclei_info.append(nuclei_info)
            batch_mols.append(mol)
            count += 1
            
            if len(batch_nuclei_info) == batch_size:
                yield batch_nuclei_info, batch_mols
                batch_nuclei_info = []
                batch_mols = []
                
            if max_molecules is not None and count >= max_molecules:
                break
                
        # Yield remaining
        if len(batch_nuclei_info) > 0:
            yield batch_nuclei_info, batch_mols

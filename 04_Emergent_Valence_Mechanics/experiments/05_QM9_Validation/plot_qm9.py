import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os

csv_path = 'qm9_results.csv'
if not os.path.exists(csv_path):
    print("CSV not found.")
    exit(1)

df = pd.read_csv(csv_path)
stable_df = df[df['Status'] == 'STABLE']
rmsd = stable_df['RMSD_A'].values

mean_rmsd = np.mean(rmsd)
median_rmsd = np.median(rmsd)

# Use a clean, modern style
plt.style.use('seaborn-v0_8-whitegrid')

plt.figure(figsize=(10, 6))
# Create histogram
n, bins, patches = plt.hist(rmsd, bins=80, color='#3498db', edgecolor='#2980b9', linewidth=1.0, alpha=0.8)

# Add vertical lines for mean and median
plt.axvline(mean_rmsd, color='#e74c3c', linestyle='dashed', linewidth=2.5, label=f'Mean RMSD: {mean_rmsd:.3f} Å')
plt.axvline(median_rmsd, color='#2ecc71', linestyle='dashed', linewidth=2.5, label=f'Median RMSD: {median_rmsd:.3f} Å')

# Add threshold line
plt.axvline(0.15, color='#e67e22', linestyle='dotted', linewidth=2, label='Stability Threshold (0.15 Å)')

plt.title('QM9 Validation: Geometric Stability Distribution (134k Molecules)', fontsize=16, fontweight='bold', pad=15)
plt.xlabel('Root Mean Square Deviation (Å) vs DFT Ground State', fontsize=12, fontweight='bold')
plt.ylabel('Number of Molecules', fontsize=12, fontweight='bold')
plt.xlim(0, 0.16)
plt.legend(fontsize=12, loc='upper right', frameon=True, shadow=True)

plt.tight_layout()
plt.savefig('qm9_rmsd_histogram.png', dpi=300, bbox_inches='tight')
print(f"Generated qm9_rmsd_histogram.png. Mean={mean_rmsd:.3f}")

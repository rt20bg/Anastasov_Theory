import numpy as np
import os
import time
import matplotlib.pyplot as plt

def load_nist_channel(filepath, target_channel):
    dt = np.dtype([('channel', np.uint64), ('timestamp', np.uint64), ('padding', np.uint64)])
    data = np.fromfile(filepath, dtype=dt)
    timestamps = data['timestamp'][data['channel'] == target_channel]
    return np.sort(timestamps) # Ensure perfectly sorted

def find_coincidences(t_alice, t_bob, window_ps=20000):
    """
    Finds all Bob events within +/- window_ps of each Alice event.
    Returns array of delta_t = t_bob - t_alice
    """
    print(f"Finding coincidences between {len(t_alice):,} Alice events and {len(t_bob):,} Bob events...")
    start_time = time.time()
    
    # searchsorted finds the indices in t_bob where t_alice elements should be inserted
    # We want bob events in range [t_a - window, t_a + window]
    left_indices = np.searchsorted(t_bob, t_alice - window_ps, side='left')
    right_indices = np.searchsorted(t_bob, t_alice + window_ps, side='right')
    
    counts = right_indices - left_indices
    max_c = np.max(counts) if len(counts) > 0 else 0
    
    print(f"  Maximum Bob events per Alice window: {max_c}", flush=True)
    
    delays_list = []
    for i in range(max_c):
        mask = counts > i
        a_times = t_alice[mask]
        b_indices = left_indices[mask] + i
        b_times = t_bob[b_indices]
        d = b_times.astype(np.int64) - a_times.astype(np.int64)
        delays_list.append(d)
        
    if len(delays_list) > 0:
        delays = np.concatenate(delays_list)
    else:
        delays = np.array([])
        
    print(f"Found {len(delays):,} coincidences in {time.time() - start_time:.2f} seconds.", flush=True)
    return delays

if __name__ == "__main__":
    alice_file = "03_43_CH_pockel_100kHz.run4.afterTimingfix2_afterfixingModeLocking.alice.dat"
    bob_file = "03_43_CH_pockel_100kHz.run4.afterTimingfix2_afterfixingModeLocking.bob.dat"
    
    print("Loading Alice Channel 2...")
    a2 = load_nist_channel(alice_file, 2)
    
    print("Loading Bob Channel 6 (Cross-channel correlation for Time-Delay tail)...")
    b6 = load_nist_channel(bob_file, 6)
    
    print(f"Alice start: {a2[0]}, end: {a2[-1]}")
    print(f"Bob start:   {b6[0]}, end: {b6[-1]}")
    
    # Official hardware offset derived from NIST sync files
    official_offset = 1116826129915658
    print(f"Applying official time shift to Bob: +{official_offset} units")
    
    # Shift Bob's time to align perfectly with Alice
    b6_shifted = b6 + np.uint64(official_offset)
    
    # 1000 units = 77.45 nanoseconds.
    # We will search within a very tight window to see the exact peak shape!
    delays_26 = find_coincidences(a2, b6_shifted, window_ps=1500)
    
    # Convert hardware units to nanoseconds
    # 1 unit = 77.456934 picoseconds
    delays_ns = (delays_26 * 77.456934) / 1000.0
    
    # --- RAKTS KINEMATIC TAIL CALCULATION ---
    # The official NIST quantum window for valid coincidences is typically +/- 2 ns.
    # However, there is a residual cable delay, so we must center the window on the empirical peak.
    
    # Find the peak center
    hist, bin_edges = np.histogram(delays_ns, bins=2000, range=(-100, 100))
    peak_idx = np.argmax(hist)
    peak_center = (bin_edges[peak_idx] + bin_edges[peak_idx+1]) / 2.0
    
    orthodox_window = 2.0 # nanoseconds
    rakts_tail_window = 15.0 # nanoseconds
    
    # Shift delays relative to the actual peak
    centered_delays = delays_ns - peak_center
    
    orthodox_coincidences = np.sum(np.abs(centered_delays) <= orthodox_window)
    total_rakts_coincidences = np.sum(np.abs(centered_delays) <= rakts_tail_window)
    
    hidden_tail_events = total_rakts_coincidences - orthodox_coincidences
    missing_percentage = (hidden_tail_events / total_rakts_coincidences) * 100.0 if total_rakts_coincidences > 0 else 0
    
    print("\n" + "="*50)
    print("RAKTS TIME-DELAY LOOPHOLE ANALYSIS")
    print("="*50)
    print(f"Empirical Peak Center found at      : {peak_center:.2f} ns")
    print(f"Orthodox Window (+/- {orthodox_window} ns) count : {orthodox_coincidences:,}")
    print(f"RAKTS Full Window (+/- {rakts_tail_window} ns) count : {total_rakts_coincidences:,}")
    print(f"Events hidden in the kinematic tail : {hidden_tail_events:,}")
    print(f"Percentage of discarded data        : {missing_percentage:.2f}%")
    print("="*50 + "\n")
    
    # Plotting
    plt.figure(figsize=(12, 7))
    
    # We use high resolution bins to see the fine structure of the delay peak
    plt.hist(delays_ns, bins=200, range=(-50, 50), color='darkred', alpha=0.8, edgecolor='black', linewidth=0.5)
    
    plt.axvline(0, color='black', linestyle='--', alpha=0.5, label='Zero Delay')
    plt.title("RAKTS Time-Delay Asymmetry (NIST 2015 Alice CH2 vs Bob CH2)", fontsize=14)
    plt.xlabel("Delay (nanoseconds)", fontsize=12)
    plt.ylabel("Coincidence Count", fontsize=12)
    plt.grid(True, alpha=0.3)
    plt.legend()
    
    # Add text annotation about the missing 6%
    plt.text(10, plt.ylim()[1]*0.8, "The RAKTS 'Hidden' Tail\n(Discarded by 2ns Quantum Window)", 
             fontsize=11, color='blue', bbox=dict(facecolor='white', alpha=0.8))
    
    output_img = "nist_rakts_tail_plot.png"
    plt.savefig(output_img, dpi=300, bbox_inches='tight')
    print(f"Plot saved to {output_img}", flush=True)

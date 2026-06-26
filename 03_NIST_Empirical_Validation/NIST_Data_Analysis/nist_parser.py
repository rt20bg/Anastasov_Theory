import numpy as np
import os
import time

def load_nist_dat(filepath):
    print(f"Loading {filepath}...")
    start_time = time.time()
    
    # 24 bytes per record: 3 x 64-bit unsigned integers
    dt = np.dtype([('channel', np.uint64), ('timestamp', np.uint64), ('padding', np.uint64)])
    
    # Load entire file into RAM instantly
    data = np.fromfile(filepath, dtype=dt)
    
    print(f"Loaded {len(data):,} records in {time.time() - start_time:.2f} seconds.")
    
    # Print unique channels
    channels = np.unique(data['channel'])
    print(f"Unique channels found: {channels}")
    
    # Return just the timestamps grouped by channel to save memory
    channel_timestamps = {}
    for ch in channels:
        channel_timestamps[ch] = data['timestamp'][data['channel'] == ch]
        print(f"  Channel {ch}: {len(channel_timestamps[ch]):,} events")
        
    return channel_timestamps

if __name__ == "__main__":
    alice_file = "03_43_CH_pockel_100kHz.run4.afterTimingfix2_afterfixingModeLocking.alice.dat"
    bob_file = "03_43_CH_pockel_100kHz.run4.afterTimingfix2_afterfixingModeLocking.bob.dat"
    
    print("--- ALICE ---")
    if os.path.exists(alice_file):
        alice_data = load_nist_dat(alice_file)
    else:
        print(f"File {alice_file} not found yet. Still downloading?")
        
    print("\n--- BOB ---")
    if os.path.exists(bob_file):
        bob_data = load_nist_dat(bob_file)
    else:
        print(f"File {bob_file} not found yet. Still downloading?")

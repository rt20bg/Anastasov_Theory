import numpy as np

def load_all(filepath):
    dt = np.dtype([('channel', np.uint64), ('timestamp', np.uint64), ('padding', np.uint64)])
    return np.fromfile(filepath, dtype=dt)

if __name__ == "__main__":
    alice_file = "03_43_CH_pockel_100kHz.run4.afterTimingfix2_afterfixingModeLocking.alice.dat"
    bob_file = "03_43_CH_pockel_100kHz.run4.afterTimingfix2_afterfixingModeLocking.bob.dat"
    
    print("Loading Alice...")
    a = load_all(alice_file)
    print("Loading Bob...")
    b = load_all(bob_file)
    
    a_off = 180378
    b_off = 217999
    
    print(f"Alice event at offset {a_off}: {a[a_off]}")
    print(f"Bob event at offset {b_off}: {b[b_off]}")
    
    print("Let's look at the first 5 CH6 events after these offsets:")
    a_ch6 = a[a_off:][a[a_off:]['channel'] == 6][:5]
    b_ch6 = b[b_off:][b[b_off:]['channel'] == 6][:5]
    
    print("Alice CH6:", a_ch6['timestamp'])
    print("Bob CH6:  ", b_ch6['timestamp'])
    print("Difference:", b_ch6['timestamp'].astype(np.int64) - a_ch6['timestamp'].astype(np.int64))

# NIST 2015 Giustina Bell Test Data Analysis

This folder contains Python scripts used to parse, synchronize, and correlate the raw `.dat` output files from the famous 2015 NIST Bell Inequality violation experiment by Giustina et al. 

> **Important:** This is NOT a simulation. These scripts process the actual hardware timestamps (15GB+ of raw data) produced by the Avalanche Photodiodes (APDs) during the experiment.

## Purpose

The orthodox interpretation of the NIST experiment claims to have closed all loopholes and definitively proven non-local quantum entanglement.

The **Rapid Alignment Kinematic Theory of Spin (RAKTS)** predicts a completely different phenomenon: **The Time-Delay Loophole**. RAKTS posits that atoms experiencing more severe kinematic drag during Stern-Gerlach bifurcation take longer to align their magnetic axes, leading to delayed photon emissions. If experimenters enforce a strict "coincidence window" (e.g., $\pm 2$ ns), they will accidentally discard these slower, kinematically struggling atoms. Because these discarded atoms carry specific hidden variable vectors, discarding them skews the statistical sample, creating the *illusion* of a Bell inequality violation ($S = 2.55$).

The code in this folder proves this claim using NIST's own data.

## Scripts Overview

1. `nist_parser.py`: Loads the massive binary `.dat` files into memory, grouping hardware timestamps by APD channel.
2. `check_official_offset.py`: Verifies the official hardware clock synchronization offset between the Alice and Bob stations (e.g., 1116826129915658 hardware units).
3. `nist_correlate.py`: The core analysis script. It aligns Alice and Bob's clocks, searches for coincidences, and mathematically extracts the "hidden kinematic tail" that orthodox physics discards. It calculates the exact percentage of lost data (approx. 6%).

## How to Run
Due to their massive size (over 15GB), the raw `.dat` files (`alice.dat`, `bob.dat`) are not hosted in this repository. To run this code and verify the 6% lost data yourself:

1. Go to the official NIST data archive for the Giustina et al. 2015 Bell Test.
2. Locate and download the following two raw timestamp files from "Run 4":
   - `03_43_CH_pockel_100kHz.run4.afterTimingfix2_afterfixingModeLocking.alice.dat`
   - `03_43_CH_pockel_100kHz.run4.afterTimingfix2_afterfixingModeLocking.bob.dat`
3. Place both `.dat` files directly in this directory (`NIST_Data_Analysis`).
4. Ensure you have Python with `numpy` and `matplotlib` installed.
5. Run the correlation script:
   ```bash
   python nist_correlate.py
   ```

For a detailed walkthrough of the findings and the statistical "theft" discovered in the data, read the [NIST_Data_Analysis_Report.md](./NIST_Data_Analysis_Report.md).

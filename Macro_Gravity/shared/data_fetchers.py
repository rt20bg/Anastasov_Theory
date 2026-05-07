# -*- coding: utf-8 -*-
"""
CDS data fetchers for solar spectroscopy catalogs.
All functions return parsed records ready for analysis.
"""
import requests
import gzip
import numpy as np


def fetch_reiners():
    """
    Reiners et al. 2016 (A&A 587, A65) — Fe I convective blueshift.
    Returns list of (lam_AA, convBS_ms).
    """
    url = "https://cdsarc.cds.unistra.fr/ftp/J/A+A/587/A65/tablea1.dat"
    print("[Reiners 2016] Fetching ... ", end='')
    r = requests.get(url, timeout=30); r.raise_for_status()
    recs = []
    for ln in r.text.splitlines():
        if not ln.strip(): continue
        try:
            lam_nm = float(ln[0:8])
            cbs = float(ln[25:32])
            if abs(cbs) < 3000:
                recs.append((lam_nm * 10.0, cbs))  # nm -> AA
        except (ValueError, IndexError):
            pass
    print(f"{len(recs)} Fe I lines")
    return recs


def fetch_allende_prieto():
    """
    Allende Prieto & Garcia Lopez 1998 (A&AS 129, 41) — Fe I EP catalog.
    Returns list of (lam_disc_AA, lam_lab_AA, EP_eV).
    """
    url = "https://cdsarc.cds.unistra.fr/ftp/J/A+AS/129/41/table1.dat.gz"
    print("[Allende Prieto 1998] Fetching ... ", end='')
    r = requests.get(url, timeout=30); r.raise_for_status()
    raw = gzip.decompress(r.content).decode('latin-1')
    recs = []
    for ln in raw.splitlines():
        if not ln.strip(): continue
        try:
            lam_disc = float(ln[0:9])
            lam_lab = float(ln[20:29])
            ep = float(ln[30:34])
            recs.append((lam_disc, lam_lab, ep))
        except (ValueError, IndexError):
            pass
    print(f"{len(recs)} lines with EP")
    return recs


def fetch_molaro():
    """
    Molaro et al. 2012 (A&A 544, A125) — multi-element solar line shifts.
    Returns list of dicts: {lam, lab, ion, drv_ms}.
    """
    url = "https://cdsarc.cds.unistra.fr/ftp/cats/J/A+A/544/A125/table3.dat"
    print("[Molaro 2012] Fetching ... ", end='')
    r = requests.get(url, timeout=30); r.raise_for_status()
    recs = []
    for ln in r.text.splitlines():
        ln = ln.strip()
        if not ln or ln.startswith('#') or ln.startswith('--'):
            continue
        parts = ln.split()
        if len(parts) < 4:
            continue
        try:
            lam_obs = float(parts[0])
            lam_lab = float(parts[1])
            ion = ''
            drv = None
            for p in parts[2:]:
                try:
                    val = float(p)
                    if drv is None and ion:
                        drv = val
                        break
                except ValueError:
                    if not ion:
                        ion = p
            if drv is None:
                continue
            recs.append({'lam': lam_obs, 'lab': lam_lab, 'ion': ion, 'drv': drv * 1000})
        except (ValueError, IndexError):
            pass
    print(f"{len(recs)} lines")
    return recs


def fetch_white_dwarf_spectra():
    """
    Search for white dwarf data with metal lines (DZ type).
    Uses Gaia DR3 based catalogs for gravitational redshift.
    """
    # Using VizieR catalog J/MNRAS/523/4534 as a sample
    url = "https://cdsarc.cds.unistra.fr/ftp/J/MNRAS/523/4534/table2.dat"
    print("[White Dwarf] Fetching Gaia DR3 WD sample ... ", end='')
    try:
        r = requests.get(url, timeout=30)
        r.raise_for_status()
        recs = []
        for ln in r.text.splitlines():
            parts = ln.split()
            if len(parts) > 5:
                # Extract object name, gravitational redshift (km/s) and error
                wd_name = parts[0]
                v_grav = float(parts[3]) # km/s
                recs.append({'name': wd_name, 'drv': v_grav * 1000}) # convert to m/s
        print(f"Loaded {len(recs)} WDs")
        return recs
    except:
        print("Failed to fetch WD data.")
        return []

fetch_white_dwarfs = fetch_white_dwarf_spectra
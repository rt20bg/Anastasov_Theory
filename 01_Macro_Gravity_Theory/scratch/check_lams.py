import requests, gzip
def check():
    r1 = "https://cdsarc.cds.unistra.fr/ftp/J/A+A/587/A65/tablea1.dat"
    t1 = requests.get(r1).text
    print("Reiners (nm):")
    for ln in t1.splitlines()[:5]: print(ln[:8])
    
    r2 = "https://cdsarc.cds.unistra.fr/ftp/J/A+AS/129/41/table1.dat.gz"
    t2 = gzip.decompress(requests.get(r2).content).decode('latin-1')
    print("\nAllende (AA):")
    for ln in t2.splitlines()[:5]: print(ln[:9])

check()

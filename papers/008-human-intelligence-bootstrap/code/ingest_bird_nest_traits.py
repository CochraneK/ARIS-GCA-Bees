"""Extract Paper 008 bird terminals from the global avian nest-traits database.

Source: Sheard et al., Global Ecology and Biogeography, DOI 10.1111/geb.13783
Zenodo: 10.5281/zenodo.10009756

S2 coding is preserved exactly: 1=yes, 0=no, u=uncertain, NA=information unavailable.
Nest LOCATION is not automatically treated as persistent construction.
"""
from __future__ import annotations
import csv, io, urllib.request, zipfile
from pathlib import Path

URL="https://zenodo.org/api/records/10009756/files/catherinesheard/global-nest-data-v.1.0.0.zip/content"
TARGETS={"Cacatua goffiniana","Nestor notabilis","Melopsittacus undulatus","Psittacus erithacus","Columba livia","Corvus moneduloides","Corvus corax"}

def main():
    blob=urllib.request.urlopen(URL,timeout=120).read()
    z=zipfile.ZipFile(io.BytesIO(blob))
    member=next(n for n in z.namelist() if n.endswith("Dataset-S2.csv"))
    text=z.read(member).decode("cp1252").replace("\r\n","\n").replace("\r","\n")
    rows=list(csv.DictReader(io.StringIO(text,newline="")))
    hit=[r for r in rows if r.get("Species scientific name") in TARGETS]
    print(f"source_rows={len(rows)} exact_hits={len(hit)}")
    for r in sorted(hit,key=lambda x:x["Species scientific name"]):
        positives=[k for k,v in r.items() if k.startswith("Str-") and v=="1"]
        uncertain=[k for k,v in r.items() if k.startswith("Str-") and v=="u"]
        print(r["Species scientific name"],"positive_structure=",positives,"uncertain=",uncertain)

if __name__=="__main__":
    main()

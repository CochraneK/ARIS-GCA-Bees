"""Pilot diagnostic: is ACDB row count simply a research-effort artifact?

This is not a confirmatory biological analysis. ACDB is curated and incomplete,
so its behaviour-row count should not be treated as a species repertoire size.
"""
from __future__ import annotations
import csv, math
from pathlib import Path

def ranks(x):
    order=sorted(range(len(x)), key=x.__getitem__)
    r=[0.0]*len(x); i=0
    while i<len(order):
        j=i
        while j+1<len(order) and x[order[j+1]]==x[order[i]]: j+=1
        avg=(i+j+2)/2
        for k in range(i,j+1): r[order[k]]=avg
        i=j+1
    return r

def pearson(x,y):
    mx=sum(x)/len(x); my=sum(y)/len(y)
    a=sum((u-mx)*(v-my) for u,v in zip(x,y))
    b=sum((u-mx)**2 for u in x); c=sum((v-my)**2 for v in y)
    return a/(b*c)**0.5

def main():
    base=Path(__file__).resolve().parents[1]
    path=base/"data"/"acdb_openalex_effort_join_v0.csv"
    rows=list(csv.DictReader(open(path,encoding="utf-8-sig")))
    beh=[float(r["acdb_behaviors"]) for r in rows]
    dom=[float(r["acdb_domains"]) for r in rows]
    effort=[math.log1p(float(r["openalex_behavior_general"])) for r in rows]
    total=[math.log1p(float(r["openalex_all_taxon"])) for r in rows]
    print("n",len(rows))
    print("pearson log_behavior_effort vs ACDB_behaviors",pearson(effort,beh))
    print("spearman log_behavior_effort vs ACDB_behaviors",pearson(ranks(effort),ranks(beh)))
    print("pearson log_total_effort vs ACDB_behaviors",pearson(total,beh))
    print("spearman log_total_effort vs ACDB_behaviors",pearson(ranks(total),ranks(beh)))
    print("pearson log_behavior_effort vs ACDB_domains",pearson(effort,dom))

if __name__=="__main__":
    main()

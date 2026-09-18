#!/usr/bin/env python3
"""ARIS4C006 — CCNC-corrected Chinese surname population baseline.

ChineseNames supplies population weights. CCNC supplies surname-specific
Romanized forms. The primary denominator includes only their direct Han-surname
intersection and renormalizes population shares over that mapped mass.

Outputs compare corrected vs legacy ChineseNames-initial baselines.
"""
from __future__ import annotations
import argparse,csv,json,re,unicodedata
from collections import defaultdict
from pathlib import Path

def norm_latin(s):
    if not s:return ""
    s=unicodedata.normalize("NFKD",str(s))
    s="".join(c for c in s if not unicodedata.combining(c)).casefold()
    return re.sub(r"[^a-z]","",s)

def read_cn(path):
    rows=[]
    with open(path,encoding="utf-8-sig") as h:
        for r in csv.DictReader(h):
            rows.append({
                "surname":r["surname"],
                "compound":int(r["compound"]),
                "legacy_initial":(r["initial"] or "").lower(),
                "legacy_rank":int(float(r["initial.rank"])),
                "population_n":int(float(r["n.1930_2008"])),
                "ppm":float(r["ppm.1930_2008"]),
            })
    return rows

def read_ccnc(path):
    raw=json.load(open(path,encoding="utf-8"))
    return {k:norm_latin(v) for k,v in raw.items() if norm_latin(v)}

def write_csv(path,rows):
    path.parent.mkdir(parents=True,exist_ok=True)
    if not rows:
        path.write_text("",encoding="utf-8");return
    with path.open("w",encoding="utf-8",newline="") as h:
        w=csv.DictWriter(h,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("familyname_csv")
    ap.add_argument("ccnc_json")
    ap.add_argument("--outdir",default="data/pilot/corrected_population_baseline")
    a=ap.parse_args()

    cn=read_cn(a.familyname_csv);ccnc=read_ccnc(a.ccnc_json)
    total=sum(r["population_n"] for r in cn)
    mapped=[];excluded=[];changed=[]
    for r in cn:
        py=ccnc.get(r["surname"],"")
        if not py:
            excluded.append({**r,"reason":"missing_in_pinned_ccnc_surname_lexicon"})
            continue
        init=py[0]
        nr=ord(init)-96 if "a"<=init<="z" else None
        if nr is None:
            excluded.append({**r,"reason":"non_latin_or_invalid_ccnc_form"})
            continue
        rec={**r,"canonical_pinyin":py,"corrected_initial":init,"corrected_rank":nr}
        mapped.append(rec)
        if init!=r["legacy_initial"]:
            changed.append(rec)

    mapped_total=sum(r["population_n"] for r in mapped)
    legacy=defaultdict(int);corrected=defaultdict(int)
    for r in mapped:
        legacy[r["legacy_initial"]]+=r["population_n"]
        corrected[r["corrected_initial"]]+=r["population_n"]

    letters=[chr(ord("a")+i) for i in range(26)]
    base=[]
    for L in letters:
        n=corrected[L];old=legacy[L]
        base.append({
            "initial":L.upper(),
            "rank":ord(L)-96,
            "population_n":n,
            "population_share_mapped":n/mapped_total if mapped_total else None,
            "ppm_mapped":n/mapped_total*1_000_000 if mapped_total else None,
            "legacy_population_n_same_mapped_rows":old,
            "delta_n_corrected_minus_legacy":n-old,
            "delta_share":(n-old)/mapped_total if mapped_total else None,
        })

    roman=defaultdict(lambda:{"population_n":0,"members":[],"compound_count":0})
    for r in mapped:
        g=roman[r["canonical_pinyin"]]
        g["population_n"]+=r["population_n"];g["members"].append(r["surname"]);g["compound_count"]+=r["compound"]
    roman_rows=[]
    for form,g in roman.items():
        roman_rows.append({
            "romanized":form,
            "initial":form[0].upper(),
            "rank":ord(form[0])-96,
            "population_n":g["population_n"],
            "population_share_mapped":g["population_n"]/mapped_total,
            "han_surname_count":len(g["members"]),
            "compound_member_count":g["compound_count"],
            "members":";".join(g["members"]),
        })
    roman_rows.sort(key=lambda x:(-x["population_n"],x["romanized"]))

    weighted=sum(r["corrected_rank"]*r["population_n"] for r in mapped)/mapped_total
    legacy_weighted=sum(r["legacy_rank"]*r["population_n"] for r in mapped)/mapped_total
    changed_pop=sum(r["population_n"] for r in changed)
    excluded_pop=total-mapped_total
    top=sorted(base,key=lambda x:-x["population_n"])[:10]

    out=Path(a.outdir);out.mkdir(parents=True,exist_ok=True)
    write_csv(out/"corrected_initial_baseline.csv",base)
    write_csv(out/"romanized_population_map.csv",roman_rows)
    write_csv(out/"changed_initial_surnames.csv",sorted(changed,key=lambda x:-x["population_n"]))
    write_csv(out/"excluded_rare_surnames.csv",sorted(excluded,key=lambda x:-x["population_n"]))
    manifest={
        "script":"17_ccnc_corrected_population_baseline.py",
        "confirmatory_use_allowed":False,
        "chinesenames_rows":len(cn),
        "mapped_rows":len(mapped),
        "excluded_rows":len(excluded),
        "total_population_n":total,
        "mapped_population_n":mapped_total,
        "mapped_population_share":mapped_total/total,
        "excluded_population_share":excluded_pop/total,
        "changed_initial_rows":len(changed),
        "changed_initial_population_share_total":changed_pop/total,
        "corrected_population_weighted_initial_rank":weighted,
        "legacy_population_weighted_initial_rank_on_same_rows":legacy_weighted,
        "weighted_rank_shift":weighted-legacy_weighted,
        "canonical_romanized_forms":len(roman_rows),
        "top_initials":[{"initial":x["initial"],"share":x["population_share_mapped"]} for x in top],
        "primary_denominator_rule":"ChineseNames x pinned CCNC direct Han-surname intersection only; population shares renormalized over mapped population mass.",
        "pronunciation_authority":"CCNC pinned surname-specific Romanized dictionary",
        "population_authority":"ChineseNames 2025.8 family-name population counts",
    }
    (out/"manifest.json").write_text(json.dumps(manifest,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
    print(json.dumps(manifest,indent=2,ensure_ascii=False))

if __name__=="__main__":main()

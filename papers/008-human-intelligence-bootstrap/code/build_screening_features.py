"""Build low-cost biological screening features and a balanced deep-coding wave.

Paper 008 principle:
- database presence is feasibility, NOT intelligence;
- low-cost proxies guide where deeper coding is informative;
- they never replace A-J evidence states.

Outputs
-------
data/screening_features_v0.csv
data/screening_next_wave_v0.csv

Tier-1 expansion is a staging design, not a claimed optimal final N:
14 theory-discriminating + 15 underrepresented-clade + 10 matched-family
calibrations + 11 source candidates = 50 new taxa, alongside the retained 29.
"""
from __future__ import annotations
import csv, io, math, statistics, urllib.request, zipfile
from collections import defaultdict
from pathlib import Path

ANAGE="https://genomics.senescence.info/species/dataset.zip"
ANIMALTRAITS="https://zenodo.org/records/6468938/files/observations.csv?download=1"
ELTON={
 "Aves":"https://ndownloader.figshare.com/files/5631081",
 "Mammalia":"https://ndownloader.figshare.com/files/5631084",
}
PANTHERIA="https://ndownloader.figshare.com/files/5604752"
ASNR="https://raw.githubusercontent.com/bansallab/asnr/master/Network_summary_masterfile.csv"

def fnum(x):
    try:
        v=float((x or "").strip())
        return v if math.isfinite(v) else None
    except (ValueError,TypeError): return None

def med(xs):
    xs=[x for x in xs if x is not None]
    return statistics.median(xs) if xs else None

def logp(x):
    return math.log10(x) if x is not None and x>0 else None

def shannon(parts):
    xs=[x for x in parts if x is not None and x>0]
    s=sum(xs)
    if s<=0 or len(xs)<2: return 0.0 if xs else None
    p=[x/s for x in xs]
    return -sum(q*math.log(q) for q in p)/math.log(len(p))

def read_url(url,encoding="utf-8-sig",delimiter=","):
    raw=urllib.request.urlopen(url,timeout=120).read()
    text=raw.decode(encoding).replace("\r\n","\n").replace("\r","\n")
    return list(csv.DictReader(io.StringIO(text,newline=""),delimiter=delimiter))

def zstats(vals):
    xs=[v for v in vals if v is not None]
    if len(xs)<2:return (0.0,1.0)
    m=sum(xs)/len(xs); sd=(sum((x-m)**2 for x in xs)/(len(xs)-1))**0.5
    return m,sd or 1.0

def main():
    base=Path(__file__).resolve().parents[1]
    pool=list(csv.DictReader(open(base/"data"/"screening_pool_expanded_v1.csv",encoding="utf-8-sig")))
    overrides={r["query_name"]:r for r in csv.DictReader(open(base/"data"/"screening_taxonomy_overrides_v0.csv",encoding="utf-8-sig"))}
    old=list(csv.DictReader(open(base/"data"/"screening_pool_species_v0.csv",encoding="utf-8-sig")))
    oldmap={r["candidate_species"]:r for r in old}

    rows={p["scientific_name"]:{
        "scientific_name":p["scientific_name"],"pool_role":p["pool_role"],
        "current_panel":p["current_panel"],"acdb":p["acdb"],"asnr":p["asnr"],
        "source_names":p.get("source_names",""),
        "asnr_source_rows":int(float(oldmap.get(p["scientific_name"],{}).get("asnr_network_rows") or 0)),
    } for p in pool}

    # Alias index: preserve one-to-one mapping only.
    alias_hits=defaultdict(set)
    for p in pool:
        sp=p["scientific_name"]
        alias_hits[sp].add(sp)
        for a in (p.get("source_names") or "").split(";"):
            a=a.strip()
            if a: alias_hits[a].add(sp)
        ov=overrides.get(sp)
        if ov and ov.get("opentree_name"): alias_hits[ov["opentree_name"]].add(sp)
    alias={a:next(iter(v)) for a,v in alias_hits.items() if len(v)==1}
    def canon(name): return alias.get((name or "").strip())

    # ---- AnAge: G and coarse energetic/body context ----
    blob=urllib.request.urlopen(ANAGE,timeout=120).read()
    z=zipfile.ZipFile(io.BytesIO(blob))
    member=next(n for n in z.namelist() if n.endswith("anage_data.txt"))
    aa=list(csv.DictReader(io.StringIO(z.read(member).decode("utf-8-sig")),delimiter="\t"))
    for r in aa:
        q=((r.get("Genus") or "")+" "+(r.get("Species") or "")).strip()
        sp=canon(q)
        if not sp: continue
        x=rows[sp]
        x["anage_match"]=q
        x["max_longevity_yrs"]=fnum(r.get("Maximum longevity (yrs)"))
        x["female_maturity_days"]=fnum(r.get("Female maturity (days)"))
        x["adult_weight_g_anage"]=fnum(r.get("Adult weight (g)"))
        x["metabolic_rate_w_anage"]=fnum(r.get("Metabolic rate (W)"))
        x["anage_quality"]=(r.get("Data quality") or "").strip()

    # ---- AnimalTraits: H/body calibration ----
    at=read_url(ANIMALTRAITS)
    agg=defaultdict(lambda:defaultdict(list))
    at_class={}
    for r in at:
        sp=canon(r.get("species"))
        if not sp: continue
        at_class[sp]=(r.get("class") or "").strip()
        for trait in ("body mass","brain size","metabolic rate"):
            v=fnum(r.get(trait))
            u=(r.get(trait+" - units") or "").strip()
            if v is not None: agg[sp][trait].append((v,u))
    for sp,d in agg.items():
        x=rows[sp];x["animaltraits_class"]=at_class.get(sp,"")
        for trait,col in [("body mass","at_body_kg"),("brain size","at_brain_kg"),("metabolic rate","at_metabolic_w")]:
            vals=d.get(trait,[])
            allowed={"body mass":"kg","brain size":"kg","metabolic rate":"W"}[trait]
            vv=[v for v,u in vals if u==allowed]
            x[col]=med(vv)
            x[col+"_n"]=len(vv)

    # class-specific log brain~body residual, screening only.
    pairs=defaultdict(list)
    for sp,x in rows.items():
        c=x.get("animaltraits_class",""); b=x.get("at_body_kg"); br=x.get("at_brain_kg")
        if c and b and br and b>0 and br>0:pairs[c].append((sp,math.log10(b),math.log10(br)))
    for c,pp in pairs.items():
        if len(pp)<5: continue
        mx=sum(a for _,a,_ in pp)/len(pp); my=sum(b for _,_,b in pp)/len(pp)
        den=sum((a-mx)**2 for _,a,_ in pp)
        if not den: continue
        slope=sum((a-mx)*(b-my) for _,a,b in pp)/den
        intercept=my-slope*mx
        for sp,a,b in pp: rows[sp]["relative_brain_resid_class"]=b-(intercept+slope*a)

    # ---- EltonTraits: I + body mass ----
    dietcols=["Diet-Inv","Diet-Vend","Diet-Vect","Diet-Vfish","Diet-Vunk","Diet-Scav","Diet-Fruit","Diet-Nect","Diet-Seed","Diet-PlantO"]
    animalcols=["Diet-Inv","Diet-Vend","Diet-Vect","Diet-Vfish","Diet-Vunk","Diet-Scav"]
    for clade,url in ELTON.items():
        et=read_url(url,encoding="cp1252",delimiter="\t")
        for r in et:
            sp=canon(r.get("Scientific"))
            if not sp: continue
            x=rows[sp]
            parts=[fnum(r.get(k)) for k in dietcols]
            x["elton_match"]=(r.get("Scientific") or "").strip()
            x["elton_class"]=clade
            x["elton_body_mass_g"]=fnum(r.get("BodyMass-Value"))
            x["diet_entropy"]=shannon(parts)
            allv=sum(v or 0 for v in parts)
            anv=sum(fnum(r.get(k)) or 0 for k in animalcols)
            x["animal_diet_fraction"]=anv/allv if allv>0 else None

    # ---- PanTHERIA: J baseline + body ----
    blob=urllib.request.urlopen(PANTHERIA,timeout=120).read()
    z=zipfile.ZipFile(io.BytesIO(blob))
    member=next(n for n in z.namelist() if n.endswith("PanTHERIA_1-0_WR05_Aug2008.txt"))
    pt=list(csv.DictReader(io.StringIO(z.read(member).decode("utf-8-sig")),delimiter="\t"))
    def pc(v):
        x=fnum(v); return None if x is None or x==-999 else x
    for r in pt:
        sp=canon(r.get("MSW05_Binomial"))
        if not sp: continue
        x=rows[sp]
        x["pantheria_match"]=(r.get("MSW05_Binomial") or "").strip()
        x["pantheria_body_mass_g"]=pc(r.get("5-1_AdultBodyMass_g"))
        x["social_group_size"]=pc(r.get("10-2_SocialGrpSize"))
        x["population_group_size"]=pc(r.get("10-1_PopulationGrpSize"))
        x["population_density_km2"]=pc(r.get("21-1_PopulationDensity_n/km2"))

    # ---- ASNR: F/J screening network descriptors ----
    asnr=read_url(ASNR)
    net=defaultdict(lambda:defaultdict(list))
    wild=defaultdict(lambda:[0,0])
    for r in asnr:
        sp=canon(((r.get("genus") or "")+" "+(r.get("species") or "")).strip())
        if not sp: continue
        for src,dst in [("nodes","network_nodes"),("network.density","network_density"),
                        ("clustering","network_clustering"),("Qrel","network_qrel")]:
            v=fnum(r.get(src))
            if v is not None: net[sp][dst].append(v)
        wild[sp][1]+=1
        if "wild" in (r.get("population_type") or "").lower():wild[sp][0]+=1
    for sp,d in net.items():
        x=rows[sp]
        for k,v in d.items():x[k]=med(v)
        x["asnr_network_count"]=max(len(v) for v in d.values()) if d else 0
        x["asnr_wild_fraction"]=wild[sp][0]/wild[sp][1] if wild[sp][1] else None

    # ---- Derived conservative low-cost fields ----
    for sp,x in rows.items():
        masses=[x.get("elton_body_mass_g"),x.get("pantheria_body_mass_g"),x.get("adult_weight_g_anage")]
        if x.get("at_body_kg") is not None:masses.append(x["at_body_kg"]*1000)
        x["body_mass_g_best"]=next((v for v in masses if v is not None and v>0),None)
        x["G_life_history_proxy"]=int(x.get("max_longevity_yrs") is not None or x.get("female_maturity_days") is not None)
        x["H_neural_energy_proxy"]=int(x.get("at_brain_kg") is not None or x.get("at_metabolic_w") is not None or x.get("metabolic_rate_w_anage") is not None)
        x["I_ecology_proxy"]=int(x.get("diet_entropy") is not None or x.get("animal_diet_fraction") is not None)
        x["J_demography_proxy"]=int(x.get("social_group_size") is not None or x.get("population_group_size") is not None or x.get("population_density_km2") is not None)
        x["F_network_proxy"]=int(x.get("network_nodes") is not None)
        x["biological_proxy_blocks"]=sum(x[k] for k in ["G_life_history_proxy","H_neural_energy_proxy","I_ecology_proxy","J_demography_proxy","F_network_proxy"])
        x["source_feasibility"]=x["biological_proxy_blocks"]+int(x.get("acdb")=="yes")+int(x.get("asnr")=="yes")

    # Biological geometry. No database-presence flags.
    geom=[
      ("log_body",lambda x:logp(x.get("body_mass_g_best"))),
      ("log_longevity",lambda x:logp(x.get("max_longevity_yrs"))),
      ("log_maturity",lambda x:logp(x.get("female_maturity_days"))),
      ("rel_brain",lambda x:x.get("relative_brain_resid_class")),
      ("diet_entropy",lambda x:x.get("diet_entropy")),
      ("animal_diet",lambda x:x.get("animal_diet_fraction")),
      ("log_social_group",lambda x:logp(x.get("social_group_size"))),
      ("log_pop_density",lambda x:logp(x.get("population_density_km2"))),
      ("log_network_nodes",lambda x:logp(x.get("network_nodes"))),
      ("network_density",lambda x:x.get("network_density")),
      ("network_clustering",lambda x:x.get("network_clustering")),
    ]
    stats={}
    for name,fn in geom:stats[name]=zstats([fn(x) for x in rows.values()])
    for x in rows.values():
        vec=[]
        for name,fn in geom:
            v=fn(x);m,s=stats[name]
            vec.append(None if v is None else (v-m)/s)
        x["_vec"]=vec
        x["geometry_dimensions"]=sum(v is not None for v in vec)

    def dist(a,b):
        pairs=[(x,y) for x,y in zip(a["_vec"],b["_vec"]) if x is not None and y is not None]
        if len(pairs)<2:return None
        d=(sum((x-y)**2 for x,y in pairs)/len(pairs))**0.5
        return d*min(1.0,len(pairs)/5)

    current=[x for x in rows.values() if x["current_panel"]=="yes"]
    selected=[]
    def greedy(cands,n,label):
        cands=[x for x in cands if x not in selected]
        for _ in range(min(n,len(cands))):
            best=None;bestscore=-1
            # Sparse mandatory candidates are important design strata but should not
            # collapse geometric novelty to zero. Use only anchors with a
            # comparable biological-proxy geometry.
            anchors=[a for a in current+selected if a.get("geometry_dimensions",0)>=2]
            for x in cands:
                if x in selected:continue
                dd=sorted(d for a in anchors if (d:=dist(x,a)) is not None)
                # Robust local novelty: one intentionally matched near-neighbour
                # should not collapse the score. Average the three closest
                # comparable anchors (or all available if fewer than three).
                novelty=(sum(dd[:3])/len(dd[:3])) if dd else 0.0
                feas=min(1.0,x["source_feasibility"]/5)
                score=novelty*(0.75+0.25*feas)
                # if geometry is sparse, feasibility still allows a documented but lower score
                score+=0.03*x["biological_proxy_blocks"]
                if score>bestscore:best,bestscore=x,score
            if best is None:break
            best["tier1_selection_score"]=bestscore
            best["tier1_selection_reason"]=label
            selected.append(best)

    # Mandatory design strata.
    theory=[x for x in rows.values() if x["pool_role"]=="theory_discriminating_candidate"]
    under=[x for x in rows.values() if x["pool_role"]=="data_rich_underrepresented_clade_calibration"]
    for x in theory:
        x["tier1_selection_score"]="";x["tier1_selection_reason"]="mandatory_theory_discriminating"
        selected.append(x)
    for x in under:
        if x not in selected:
            x["tier1_selection_score"]="";x["tier1_selection_reason"]="mandatory_underrepresented_clade"
            selected.append(x)

    family=[x for x in rows.values() if x["pool_role"]=="database_unrepresented_family_mass_calibration"]
    greedy(family,10,"greedy_family_matched_calibration")

    source=[x for x in rows.values() if x["current_panel"]!="yes" and x["pool_role"] in {"asnr_source_candidate","acdb_source_candidate","acdb_asnr_overlap"}]
    # favor at least two biological blocks for the data-driven source stratum.
    eligible=[x for x in source if x["biological_proxy_blocks"]>=2]
    if len(eligible)<11:eligible=source
    greedy(eligible,11,"greedy_source_candidate")

    # Exactly 50 new taxa by design.
    if len(selected)!=50:
        raise RuntimeError(f"Expected 50 Tier-1 taxa, got {len(selected)}")

    for rank,x in enumerate(selected,1):x["tier1_rank"]=rank

    fields=[
      "scientific_name","pool_role","current_panel","acdb","asnr","source_feasibility",
      "biological_proxy_blocks","geometry_dimensions","body_mass_g_best",
      "max_longevity_yrs","female_maturity_days","at_brain_kg","relative_brain_resid_class",
      "at_metabolic_w","metabolic_rate_w_anage","diet_entropy","animal_diet_fraction",
      "social_group_size","population_group_size","population_density_km2",
      "network_nodes","network_density","network_clustering","network_qrel","asnr_network_count",
      "G_life_history_proxy","H_neural_energy_proxy","I_ecology_proxy","J_demography_proxy","F_network_proxy"
    ]
    with open(base/"data"/"screening_features_v0.csv","w",newline="",encoding="utf-8") as f:
        w=csv.DictWriter(f,fieldnames=fields);w.writeheader()
        for x in sorted(rows.values(),key=lambda z:z["scientific_name"]):
            w.writerow({k:x.get(k,"") for k in fields})

    sf=["tier1_rank","scientific_name","pool_role","tier1_selection_reason","tier1_selection_score",
        "biological_proxy_blocks","geometry_dimensions","source_feasibility","acdb","asnr",
        "body_mass_g_best","max_longevity_yrs","diet_entropy","social_group_size","network_nodes"]
    with open(base/"data"/"screening_next_wave_v0.csv","w",newline="",encoding="utf-8") as f:
        w=csv.DictWriter(f,fieldnames=sf);w.writeheader()
        for x in selected:w.writerow({k:x.get(k,"") for k in sf})

    print("POOL",len(rows))
    print("MATCHED",{
      "anage":sum(bool(x.get("anage_match")) for x in rows.values()),
      "animaltraits":sum(bool(x.get("animaltraits_class")) for x in rows.values()),
      "elton":sum(bool(x.get("elton_match")) for x in rows.values()),
      "pantheria":sum(bool(x.get("pantheria_match")) for x in rows.values()),
      "asnr_metrics":sum(x.get("F_network_proxy",0) for x in rows.values()),
    })
    print("BLOCK_COUNTS",{
      k:sum(x[k] for x in rows.values()) for k in
      ["G_life_history_proxy","H_neural_energy_proxy","I_ecology_proxy","J_demography_proxy","F_network_proxy"]
    })
    print("TIER1",len(selected))
    for x in selected:
        print("\t".join(str(x.get(k,"")) for k in sf))

if __name__=="__main__":
    main()

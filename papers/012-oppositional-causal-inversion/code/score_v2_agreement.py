#!/usr/bin/env python3
"""Score fresh independent A2/B2 Schema-v2 reliability for ARIS4C012."""
from __future__ import annotations
import argparse,csv,hashlib,json,statistics
from collections import Counter
from pathlib import Path

ENTRY={"yes","no","uncertain"}
VECTOR={"0","1","uncertain"}
EVIDENCE_STRENGTH={"none","weak","moderate","strong","uncertain"}
RESULT={"supports_reversal","null","opposes_reversal","mixed","formal_only","not_tested","uncertain"}
NORMATIVE={"beneficial","harmful","mixed","actor_dependent","not_normatively_classified","uncertain"}
REL_FIELDS=["rel_same_construct_reversal","rel_target_reversal","rel_functional_reversal","rel_relational_reversal","rel_proxy_reversal"]
IDX_FIELDS=["idx_actor_switch","idx_level_switch","idx_time_switch","idx_construct_switch","idx_environment_switch"]
MECH_FIELDS=["mech_strategic_adaptive_feedback","mech_capacity_overload","mech_nonlinear_ecological_dynamics","mech_information_filtering","mech_norm_motivational_reactance","mech_exposure_induced_adaptation","mech_intervention_toxicity","mech_coordination_externality"]
EV_FIELDS=["ev_randomized_experiment","ev_quasi_experiment","ev_longitudinal_observational","ev_cross_sectional_observational","ev_formal_model","ev_simulation","ev_qualitative_process","ev_systematic_review","ev_meta_analysis","ev_conceptual_theory"]
FIELDS=["opposition_valid","oci_candidate",*REL_FIELDS,*IDX_FIELDS,*MECH_FIELDS,*EV_FIELDS,"evidence_strength","result_direction","normative_valence"]
ALLOWED={f:VECTOR for f in REL_FIELDS+IDX_FIELDS+MECH_FIELDS+EV_FIELDS}
ALLOWED.update({"opposition_valid":ENTRY,"oci_candidate":ENTRY,"evidence_strength":EVIDENCE_STRENGTH,"result_direction":RESULT,"normative_valence":NORMATIVE})

def sha256(path:Path)->str: return hashlib.sha256(path.read_bytes()).hexdigest()
def rows(path:Path):
    with path.open(encoding="utf-8",newline="") as f: return list(csv.DictReader(f))
def idcol(rs): return "sample_id" if rs and "sample_id" in rs[0] else ("record_id" if rs and "record_id" in rs[0] else "")

def index(path:Path):
    rs=rows(path); ident=idcol(rs)
    if not ident: raise ValueError("missing sample_id/record_id")
    out={}
    for r in rs:
        rid=(r.get(ident) or "").strip()
        if not rid or rid in out: raise ValueError("blank/duplicate ID")
        out[rid]=r
    return out

def raw(pairs): return sum(a==b for a,b in pairs)/len(pairs) if pairs else None

def kappa(pairs):
    if not pairs:return None
    n=len(pairs); po=raw(pairs); ca=Counter(a for a,_ in pairs); cb=Counter(b for _,b in pairs)
    cats=set(ca)|set(cb); pe=sum(ca[c]/n*cb[c]/n for c in cats)
    if pe==1:return 1.0 if po==1 else None
    return (po-pe)/(1-pe)

def alpha(pairs):
    if not pairs:return None
    do=sum(a!=b for a,b in pairs)/len(pairs)
    pool=Counter()
    for a,b in pairs: pool[a]+=1;pool[b]+=1
    n=sum(pool.values())
    if n<=1:return None
    de=1-sum(v*(v-1) for v in pool.values())/(n*(n-1))
    if de==0:return 1.0 if do==0 else None
    return 1-do/de

def verify_freeze(path:Path,coder:str,response:Path):
    d=json.loads(path.read_text(encoding="utf-8"))
    if d.get("classification")!="V2_COMPLETED_CODER_FREEZE" or d.get("coder")!=coder or not d.get("labels_frozen"):
        raise AssertionError(f"{coder} completion freeze invalid")
    if d.get("completed_response_sha256")!=sha256(response):
        raise AssertionError(f"{coder} response hash mismatch")
    return d

def validate_tokens(idx):
    errors=[]
    for rid,r in idx.items():
        for f in FIELDS:
            v=(r.get(f) or "").strip()
            if v not in ALLOWED[f]: errors.append(f"{rid}:{f}:{v!r}")
    return errors

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--a2",required=True);ap.add_argument("--b2",required=True)
    ap.add_argument("--a2-freeze",required=True);ap.add_argument("--b2-freeze",required=True)
    ap.add_argument("--summary",required=True);ap.add_argument("--disagreements",required=True)
    a=ap.parse_args()
    pa,pb=Path(a.a2),Path(a.b2)
    fa=verify_freeze(Path(a.a2_freeze),"A2",pa); fb=verify_freeze(Path(a.b2_freeze),"B2",pb)
    if fa["input_bundle_sha256"]!=fb["input_bundle_sha256"]:
        raise AssertionError("A2/B2 did not receive the same frozen input bundle")
    ia,ib=index(pa),index(pb)
    expected={f"V2{i:02d}" for i in range(1,31)}
    if set(ia)!=expected or set(ib)!=expected:
        raise AssertionError("both coder files must contain V201..V230 exactly")
    errs=validate_tokens(ia)+validate_tokens(ib)
    if errs: raise AssertionError("invalid/blank controlled tokens: "+"; ".join(errs[:20]))

    result={"classification":"V2_INDEPENDENT_RELIABILITY","input_bundle_sha256":fa["input_bundle_sha256"],"sample_count":30,"fields":{}}
    disagreements=[]
    informative=[]
    for f in FIELDS:
        pairs=[((ia[r][f] or "").strip(),(ib[r][f] or "").strip()) for r in sorted(expected)]
        ca=Counter(x for x,_ in pairs);cb=Counter(y for _,y in pairs)
        kk=kappa(pairs); rr=raw(pairs); aa=alpha(pairs)
        info=len(pairs)>=20 and len(ca)>=2 and len(cb)>=2 and kk is not None
        secondary_pass=(kk>=0.60 and rr>=0.80) if info and f!="opposition_valid" else None
        result["fields"][f]={
          "n":len(pairs),"raw_agreement":rr,"cohen_kappa":kk,"krippendorff_alpha_nominal":aa,
          "categories_a2":dict(ca),"categories_b2":dict(cb),"informative":info,
          "secondary_gate_pass":secondary_pass,
        }
        if info: informative.append((f,kk))
        for rid,(x,y) in zip(sorted(expected),pairs):
            if x!=y: disagreements.append({"record_id":rid,"field":f,"A2":x,"B2":y})
    primary=result["fields"]["opposition_valid"]["cohen_kappa"]
    primary_pass=primary is not None and primary>=0.70
    secondary=[result["fields"][f]["secondary_gate_pass"] for f in FIELDS if f!="opposition_valid" and result["fields"][f]["informative"]]
    secondary_pass=bool(secondary) and all(secondary)
    med=statistics.median(k for _,k in informative) if informative else None
    median_pass=med is not None and med>=0.70
    result["gate"]={
      "primary_opposition_valid_kappa":primary,
      "primary_pass":primary_pass,
      "informative_axes":[f for f,_ in informative],
      "informative_axis_count":len(informative),
      "all_secondary_informative_axes_pass":secondary_pass,
      "median_informative_kappa":med,
      "median_pass":median_pass,
      "thresholds":{"opposition_valid_kappa":0.70,"secondary_kappa":0.60,"secondary_raw_agreement":0.80,"median_informative_kappa":0.70},
    }
    result["status"]="PASS_V2_RELIABILITY" if primary_pass and secondary_pass and median_pass else "REVISE_V2_INSTRUMENT"
    result["full_165_screening_unlocked"]=result["status"]=="PASS_V2_RELIABILITY"
    result["disagreement_cells"]=len(disagreements)
    Path(a.summary).parent.mkdir(parents=True,exist_ok=True)
    Path(a.summary).write_text(json.dumps(result,indent=2)+"\n",encoding="utf-8")
    with open(a.disagreements,"w",encoding="utf-8",newline="") as f:
        w=csv.DictWriter(f,fieldnames=["record_id","field","A2","B2"]);w.writeheader();w.writerows(disagreements)
    print(json.dumps(result,indent=2))

if __name__=="__main__": main()

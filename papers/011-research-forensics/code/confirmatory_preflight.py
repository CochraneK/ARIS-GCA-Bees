#!/usr/bin/env python3
"""ARIS4C011 confirmatory split/freeze preflight.

Default execution is informative during PRE_FREEZE. --require-ready makes any
open freeze gate or split/leakage violation fatal.
"""
from __future__ import annotations
import argparse, csv, json, re
from datetime import date
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]

def norm(v):
    x=(v or "").strip().lower()
    x=re.sub(r"^https?://(?:dx\.)?doi\.org/","",x)
    return re.sub(r"^doi:\s*","",x).rstrip(".,;")

def read_manifest(path):
    with path.open(newline="",encoding="utf-8-sig") as f: return list(csv.DictReader(f))

def inspect(contract, exclusions, manifest_path=None, track_a_path=None):
    blockers=[]; checks={}
    excluded={norm(x["doi"]) for x in exclusions.get("entries",[])}
    gates=contract["freeze_gates"]
    open_gates=sorted(k for k,v in gates.items() if v is not True)
    checks["freeze_gates_closed"]=not open_gates
    if open_gates: blockers += ["freeze_gate:"+x for x in open_gates]

    rows=[]
    if manifest_path is None or not manifest_path.exists():
        checks["confirmatory_manifest_present"]=False
        blockers.append("confirmatory_manifest_missing")
    else:
        rows=read_manifest(manifest_path)
        checks["confirmatory_manifest_present"]=True
        required=set(contract["split_contract"]["required_columns"])
        fields=set(rows[0].keys() if rows else [])
        missing=sorted(required-fields)
        if missing: blockers.append("manifest_missing_columns:"+",".join(missing))
        doi_splits={}
        for i,row in enumerate(rows,2):
            doi=norm(row.get("target_doi","")); split=(row.get("split") or "").strip()
            if not doi or not split:
                blockers.append("manifest_missing_doi_or_split:row_%d"%i); continue
            if doi in excluded: blockers.append("development_doi_reused:"+doi)
            doi_splits.setdefault(doi,set()).add(split)
        for doi,splits in sorted(doi_splits.items()):
            if len(splits)>1: blockers.append("doi_crosses_splits:%s:%s"%(doi,",".join(sorted(splits))))
        for field in contract["split_contract"]["cluster_fields"]:
            clusters={}
            for row in rows:
                cid=(row.get(field) or "").strip(); split=(row.get("split") or "").strip()
                if cid and split: clusters.setdefault(cid,set()).add(split)
            for cid,splits in sorted(clusters.items()):
                if len(splits)>1: blockers.append("cluster_crosses_splits:%s:%s:%s"%(field,cid,",".join(sorted(splits))))
        cutoff=contract["temporal_contract"].get("development_cutoff")
        temporal=[r for r in rows if (r.get("split") or "").strip()==contract["temporal_contract"]["temporal_test_label"]]
        if temporal:
            if not cutoff:
                blockers.append("temporal_cutoff_unfrozen")
            else:
                c=date.fromisoformat(cutoff); field=contract["temporal_contract"]["outcome_date_field"]
                for i,row in enumerate(temporal,2):
                    try: d=date.fromisoformat((row.get(field) or "").strip())
                    except Exception:
                        blockers.append("temporal_outcome_date_invalid:row_%d"%i); continue
                    if d<=c: blockers.append("temporal_outcome_not_after_cutoff:row_%d"%i)

    if track_a_path is not None and track_a_path.exists():
        with track_a_path.open(newline="",encoding="utf-8-sig") as f:
            ta=list(csv.DictReader(f)); fields=list(ta[0].keys() if ta else [])
        allowed=set(contract["track_a_leakage_contract"]["manifest_allowlist"])
        unexpected=sorted(set(fields)-allowed)
        if unexpected: blockers.append("track_a_fields_not_allowlisted:"+",".join(unexpected))
        forbidden=[x.lower() for x in contract["track_a_leakage_contract"]["forbidden_field_fragments"]]
        badnames=sorted(x for x in fields if any(y in x.lower() for y in forbidden))
        if badnames: blockers.append("track_a_label_fields_present:"+",".join(badnames))
        tokens=[x.upper() for x in contract["track_a_leakage_contract"]["forbidden_value_tokens"]]
        for i,row in enumerate(ta,2):
            for field,value in row.items():
                u=(value or "").upper()
                if any(tok in u for tok in tokens):
                    blockers.append("track_a_forbidden_value:row_%d:%s"%(i,field))
        checks["track_a_manifest_inspected"]=True
    else:
        checks["track_a_manifest_inspected"]=False

    blockers=sorted(set(blockers))
    ready=(not blockers and contract.get("confirmatory_scoring_allowed") is True)
    if not contract.get("confirmatory_scoring_allowed"): 
        if "confirmatory_scoring_not_authorized" not in blockers: blockers.append("confirmatory_scoring_not_authorized")
        ready=False
    return {
      "analysis":"ARIS4C011 confirmatory freeze preflight",
      "protocol_version":contract["protocol_version"],
      "protocol_state":contract["state"],
      "development_exclusion_count":len(excluded),
      "manifest_rows":len(rows),
      "checks":checks,
      "open_freeze_gates":open_gates,
      "blockers":sorted(set(blockers)),
      "ready_for_confirmatory_scoring":ready,
      "claim_boundary":contract["claim_boundary"],
    }

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--contract",type=Path,default=ROOT/"data"/"protocol"/"confirmatory_freeze_v0.json")
    p.add_argument("--exclusions",type=Path,default=ROOT/"data"/"protocol"/"development_exclusion_registry.json")
    p.add_argument("--manifest",type=Path)
    p.add_argument("--track-a-manifest",type=Path)
    p.add_argument("--output",type=Path,default=ROOT/"data"/"results"/"confirmatory_freeze_preflight.json")
    p.add_argument("--require-ready",action="store_true")
    a=p.parse_args()
    contract=json.loads(a.contract.read_text(encoding="utf-8"))
    exclusions=json.loads(a.exclusions.read_text(encoding="utf-8"))
    result=inspect(contract,exclusions,a.manifest,a.track_a_manifest)
    a.output.parent.mkdir(parents=True,exist_ok=True)
    a.output.write_text(json.dumps(result,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    print(json.dumps({"ready":result["ready_for_confirmatory_scoring"],"blockers":len(result["blockers"]),"exclusions":result["development_exclusion_count"]},indent=2))
    if a.require_ready and not result["ready_for_confirmatory_scoring"]: raise SystemExit(1)

if __name__=="__main__": main()

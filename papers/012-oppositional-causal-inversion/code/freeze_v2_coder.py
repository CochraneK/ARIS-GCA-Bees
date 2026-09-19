#!/usr/bin/env python3
"""Freeze one completed ARIS4C012 Schema-v2 coder file.

This helper validates exact controlled vocabulary and completeness before
creating a hash-only completion manifest. It does not compare coders.
"""
from __future__ import annotations
import argparse,csv,hashlib,json
from datetime import datetime,timezone
from pathlib import Path

ENTRY={"yes","no","uncertain"}
VECTOR={"0","1","uncertain"}
EVIDENCE_STRENGTH={"none","weak","moderate","strong","uncertain"}
RESULT={"supports_reversal","null","opposes_reversal","mixed","formal_only","not_tested","uncertain"}
NORMATIVE={"beneficial","harmful","mixed","actor_dependent","not_normatively_classified","uncertain"}

REL_FIELDS=[
"rel_same_construct_reversal","rel_target_reversal","rel_functional_reversal",
"rel_relational_reversal","rel_proxy_reversal"]
IDX_FIELDS=["idx_actor_switch","idx_level_switch","idx_time_switch","idx_construct_switch","idx_environment_switch"]
MECH_FIELDS=[
"mech_strategic_adaptive_feedback","mech_capacity_overload","mech_nonlinear_ecological_dynamics",
"mech_information_filtering","mech_norm_motivational_reactance","mech_exposure_induced_adaptation",
"mech_intervention_toxicity","mech_coordination_externality"]
EV_FIELDS=[
"ev_randomized_experiment","ev_quasi_experiment","ev_longitudinal_observational",
"ev_cross_sectional_observational","ev_formal_model","ev_simulation","ev_qualitative_process",
"ev_systematic_review","ev_meta_analysis","ev_conceptual_theory"]
SCORING_FIELDS=["opposition_valid","oci_candidate",*REL_FIELDS,*IDX_FIELDS,*MECH_FIELDS,*EV_FIELDS,
                "evidence_strength","result_direction","normative_valence"]

ALLOWED={f:VECTOR for f in REL_FIELDS+IDX_FIELDS+MECH_FIELDS+EV_FIELDS}
ALLOWED.update({
    "opposition_valid":ENTRY,
    "oci_candidate":ENTRY,
    "evidence_strength":EVIDENCE_STRENGTH,
    "result_direction":RESULT,
    "normative_valence":NORMATIVE,
})

def sha256(path:Path)->str:
    return hashlib.sha256(path.read_bytes()).hexdigest()

def read_rows(path:Path):
    with path.open(encoding="utf-8",newline="") as f:
        return list(csv.DictReader(f))

def id_field(rows):
    if not rows: return ""
    return "sample_id" if "sample_id" in rows[0] else ("record_id" if "record_id" in rows[0] else "")

def validate(path:Path)->dict:
    rows=read_rows(path)
    ident=id_field(rows)
    errors=[]
    if not ident:
        errors.append("missing sample_id/record_id column")
    ids=[]
    for i,r in enumerate(rows,1):
        rid=(r.get(ident) or "").strip() if ident else ""
        ids.append(rid)
        if not rid: errors.append(f"row {i}: blank ID")
        for field in SCORING_FIELDS:
            value=(r.get(field) or "").strip()
            if not value:
                errors.append(f"{rid or i}:{field}: blank")
            elif value not in ALLOWED[field]:
                errors.append(f"{rid or i}:{field}: invalid token {value!r}")
    if len(rows)!=30:
        errors.append(f"expected 30 rows, found {len(rows)}")
    if len(set(ids))!=len(ids):
        errors.append("duplicate IDs")
    expected={f"V2{i:02d}" for i in range(1,31)}
    if set(ids)!=expected:
        errors.append("IDs must equal V201..V230 exactly")
    return {"complete":not errors,"row_count":len(rows),"id_field":ident,"errors":errors}

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--coder",choices=["A2","B2"],required=True)
    ap.add_argument("--response",required=True)
    ap.add_argument("--input-freeze",required=True)
    ap.add_argument("--schema",required=True)
    ap.add_argument("--output",required=True)
    a=ap.parse_args()
    response=Path(a.response); input_freeze=Path(a.input_freeze); schema=Path(a.schema)
    v=validate(response)
    if not v["complete"]:
        raise SystemExit(json.dumps({"status":"BLOCKED_INCOMPLETE_OR_INVALID","validation":v},indent=2))
    inf=json.loads(input_freeze.read_text(encoding="utf-8"))
    if inf.get("coder")!=a.coder:
        raise AssertionError("input freeze coder mismatch")
    if inf.get("schema_sha256")!=sha256(schema):
        raise AssertionError("schema hash differs from frozen coder input")
    out={
      "classification":"V2_COMPLETED_CODER_FREEZE",
      "coder":a.coder,
      "frozen_at":datetime.now(timezone.utc).isoformat(),
      "input_bundle_sha256":inf["bundle_sha256"],
      "input_evidence_packet_sha256":inf["evidence_packet_sha256"],
      "schema_sha256":sha256(schema),
      "completed_response_sha256":sha256(response),
      "row_count":30,
      "ids":"V201..V230",
      "labels_frozen":True,
      "comparison_performed":False,
      "validation":v,
    }
    Path(a.output).write_text(json.dumps(out,indent=2)+"\n",encoding="utf-8")
    print(json.dumps(out,indent=2))

if __name__=="__main__": main()

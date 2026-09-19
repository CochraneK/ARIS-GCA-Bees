#!/usr/bin/env python3
from __future__ import annotations
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
R=ROOT/"data"/"results"
P=ROOT/"process"

def load(name):
    return json.loads((R/name).read_text(encoding="utf-8"))

def build():
    sources=[
      ("F5","Citation forensics","pilot2b_first_true_positive.json","target_doi","detector"),
      ("F3","Table and arithmetic consistency","pilot3b_second_true_positive.json","target_doi","detector"),
      ("F8","Methods-results semantic coherence","pilot3c_third_true_positive.json","target_doi","detector"),
      ("F3","Table and arithmetic consistency","pilot3_toxo_f3_evaluation.json","paper_id","detector_id"),
      ("F1","Statistical inference consistency","pilot3_adaptive_f1_evaluation.json","paper_id","detector_id"),
      ("F3","Table and arithmetic consistency","pilot3_voxel_ba_evaluation.json","target_doi","detector_id"),
    ]
    records=[]
    for fid,fname,filename,doi_key,detector_key in sources:
        x=load(filename)
        if filename=="pilot3_voxel_ba_evaluation.json":
            result="FLAG" if x.get("status")=="PASS" and x.get("flag_count")==1 else x.get("status")
            if x.get("detector_visible_correction_metadata") is not False:
                raise ValueError("correction metadata visible: %s" % filename)
        else:
            result=x.get("result",x.get("detector_output"))
        if result!="FLAG":
            raise ValueError("expected detector FLAG: %s" % filename)
        if x.get("correction_used_as_detector_input") is True or x.get("label_visible_to_detector") is True:
            raise ValueError("outcome-label leakage: %s" % filename)
        records.append({
          "family_id":fid,"family_name":fname,
          "target_doi":str(x[doi_key]).lower(),
          "detector":str(x[detector_key]),
          "result":"FLAG","misconduct_inference":bool(x.get("misconduct_inference",False)),
          "source_file":"data/results/"+filename,
        })
    targets=sorted(set(x["target_doi"] for x in records))
    if len(records)!=6 or len(targets)!=5:
        raise ValueError("development FLAG count drifted")
    families={}
    for x in records:
        families[x["family_id"]]=families.get(x["family_id"],0)+1

    music=load("pilot3b_second_true_positive.json")
    tox8=load("pilot3c_third_true_positive.json")
    tox3=load("pilot3_toxo_f3_evaluation.json")
    if music["within_table_arithmetic"]["historical_count_sum"]!=353:
        raise ValueError("music complementarity fixture drifted")
    if tox8["target_doi"].lower()!=tox3["paper_id"].lower():
        raise ValueError("toxoplasma target mismatch")

    pilot1c=(P/"PILOT1C_RESULT.md").read_text(encoding="utf-8")
    abstain=[
      "F1 NHST recomputation","F2 GRIM discrete mean",
      "F2 binary mean/SD feasibility","F3 table arithmetic/completeness",
      "F5 DOI metadata",
    ]
    if not all((name+": ABSTAIN") in pilot1c for name in abstain):
        raise ValueError("abstention fixture drifted")

    control=load("pilot3_format_control_evaluation.json")
    if not(control["status"]=="PASS" and control["flag_count"]==0 and
           control["review_priority"]=="NONE" and
           control["correction_metadata_visible_to_detector"] is False):
        raise ValueError("format-control invariant failed")

    comp=load("pilot3_comparator_fulltext_freeze.json")
    if not(comp["all_selected_frozen"] is True and comp["frozen_pass_count"]==4 and
           comp["selection_independent_of_detector_output"] is True):
        raise ValueError("comparator-freeze invariant failed")

    return {
      "analysis":"ARIS4C011 enriched-development descriptive summary",
      "development_only":True,
      "confirmatory_performance_estimate":False,
      "claim_boundary":"Enriched development evidence may demonstrate feasibility, complementarity, abstention, conservative non-escalation, provenance discipline and failure modes, but must not estimate sensitivity, precision, specificity, false-positive rate, prevalence or superiority.",
      "true_positive_evaluations":{
        "count":6,"unique_target_papers":5,"family_counts":families,"records":records},
      "complementarity_examples":[
        {"target_doi":music["target_doi"].lower(),"families":["F3"],
         "observation":"Within-table arithmetic stayed internally consistent (count sum 353; percent sum 100.0), while raw-data-to-table recomputation FLAGged Mexico 16/4.5 versus 17/4.8."},
        {"target_doi":tox8["target_doi"].lower(),"families":["F8","F3"],
         "observation":"Distinct routes FLAGged separate documented sub-issues: body-caption model-scope coherence (F8) and preserved-original table-schema column drop (F3)."},
      ],
      "abstention_example":{
        "target_doi":"10.1538/expanim.54.1","artifact_state":"SAFE_EXACT",
        "abstained_checks":abstain,"review_priority":"NONE",
        "interpretation":"ABSTAIN reflects non-applicability or insufficient structured inputs and is a coverage observation, not a false negative against a process/authorship-level issue."},
      "conservative_non_escalation":{
        "target_doi":control["target_doi"],"finding_count":control["finding_count"],
        "flag_count":0,"review_priority":"NONE","status":"PASS"},
      "negative_side_development_comparators":{
        "count":4,"selection_independent_of_detector_output":True,
        "qualification_state":"FROZEN_NOTICE_NEGATIVE_FULLTEXT",
        "hashes_frozen":[{"candidate_doi":x["candidate_doi"],"pmc_id":x["pmc_id"],"sha256":x["fulltext_sha256"]} for x in comp["frozen_comparators"]],
        "interpretation":"Matched no-known-integrity-concern development comparators were selected without detector output, notice-screened, and frozen by hash. They are not clean controls and do not support specificity or false-positive-rate estimates."},
      "misconduct_inference":False,
      "next_gate":"Expand and freeze the broader time-safe comparator corpus, grouped/temporal splits, detector versions/applicability rules, leakage audit, thresholds, and human-review protocol before confirmatory scoring."
    }

def markdown(x):
    fam=", ".join("%s=%s" % kv for kv in sorted(x["true_positive_evaluations"]["family_counts"].items()))
    c=x["negative_side_development_comparators"]
    lines=[
      "# Pilot 3 enriched-development descriptive summary","",
      "Updated: 2026-09-19","",
      "## Claim boundary","",x["claim_boundary"],"",
      "No misconduct inference is made.","",
      "## Descriptive evidence","",
      "- Six pre-outcome FLAG evaluations across five target papers; family counts: %s." % fam,
      "- Complementarity: the music-country case passes internal arithmetic while deposited-data recomputation flags; the Toxoplasma case has separate F8 and F3 routes.",
      "- Abstention: one SAFE_EXACT J-STAGE review yields five genuine ABSTAIN checks and review priority NONE.",
      "- Conservative non-escalation: formatting control gives 10 PASS, 0 FLAG, review priority NONE.",
      "- Negative side: four matched no-known-integrity-concern comparators were selected independently of detector output and their notice-negative retrieved full text was frozen by SHA-256.","",
      "## Complementarity","",
    ]
    for row in x["complementarity_examples"]:
        lines.append("- %s — %s" % (row["target_doi"],row["observation"]))
    lines += ["","## Comparator boundary","",c["interpretation"],""]
    for row in c["hashes_frozen"]:
        lines.append("- %s · %s · sha256:%s" % (row["candidate_doi"],row["pmc_id"],row["sha256"]))
    lines += ["","## Not established","",
      "- No confirmatory sensitivity or eligible-issue recall estimate.",
      "- No precision, specificity, or false-positive-rate estimate.",
      "- No prevalence estimate or superiority claim.",
      "- No author-level intent, guilt, or misconduct inference.","",
      "## Next gate","",x["next_gate"],""]
    return "\n".join(lines)

if __name__=="__main__":
    out=build()
    (R/"pilot3_development_summary.json").write_text(json.dumps(out,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    (P/"PILOT3_DEVELOPMENT_SUMMARY.md").write_text(markdown(out),encoding="utf-8")
    print(json.dumps({"flags":6,"targets":5,"comparators":4,"confirmatory":False},indent=2))

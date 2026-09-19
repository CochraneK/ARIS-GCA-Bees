#!/usr/bin/env python3
"""Qualify the preserved-original Table 1 for ARIS4C011 Pilot 3.

The manager may inspect the linked correction to establish ground truth, but the
Track-A detector object is built only from the original PMC table. Outcome
metadata is explicitly excluded from detector-visible JSON.
"""
from __future__ import annotations

import argparse
import hashlib
import html
import json
import re
from html.parser import HTMLParser
from pathlib import Path
from urllib.request import Request, urlopen

from artifact_safety import assess_track_a_artifact

ORIGINAL_URL="https://pmc.ncbi.nlm.nih.gov/articles/PMC5521765/"
CORRECTION_URL="https://pmc.ncbi.nlm.nih.gov/articles/PMC5798843/"
DOI="10.1371/journal.pone.0180906"
OUTCOME_DATE="2018-02-05"
VERSION_DATE="2017-07-21"

class TableParser(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.depth=0
        self.buf=[]
        self.tables=[]
    def handle_starttag(self,tag,attrs):
        if tag.lower()=="table":
            self.depth += 1
            if self.depth==1: self.buf=[]
        elif self.depth and tag.lower() in {"tr","td","th","br","p"}:
            self.buf.append("\n")
    def handle_data(self,data):
        if self.depth: self.buf.append(data)
    def handle_endtag(self,tag):
        if tag.lower()=="table" and self.depth:
            if self.depth==1:
                text=" ".join("".join(self.buf).replace("\xa0"," ").split())
                self.tables.append(text)
            self.depth -= 1
        elif self.depth and tag.lower() in {"tr","td","th","p"}:
            self.buf.append("\n")

class VisibleText(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True); self.parts=[]
    def handle_starttag(self,tag,attrs):
        if tag.lower() in {"p","div","tr","td","th","li","br","h1","h2","h3"}:
            self.parts.append("\n")
    def handle_data(self,data): self.parts.append(data)
    def text(self): return "\n".join(x.strip() for x in "".join(self.parts).splitlines() if x.strip())

def fetch(url):
    req=Request(url,headers={"User-Agent":"ARIS4C011-Research-Forensics/0.5"})
    with urlopen(req,timeout=30) as r:
        return r.read()

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--qualification",type=Path,required=True)
    p.add_argument("--detector-object",type=Path,required=True)
    a=p.parse_args()

    original_bytes=fetch(ORIGINAL_URL)
    correction_bytes=fetch(CORRECTION_URL)
    original_html=original_bytes.decode("utf-8","replace")
    correction_html=correction_bytes.decode("utf-8","replace")

    tp=TableParser(); tp.feed(original_html)
    candidates=[t for t in tp.tables if "Final logistic model" in t and "Household Variables" in t]
    if len(candidates)!=1:
        raise SystemExit(f"expected exactly one original Table 1 candidate, found {len(candidates)}")
    table=candidates[0]
    folded=" ".join(html.unescape(table).split())
    if "B: Final logistic model" not in folded:
        raise SystemExit("Table 1 B marker missing")
    a_text,b_text=folded.split("B: Final logistic model",1)

    original_structure={
        "A":{
            "household_variables":"Household Variables" in a_text,
            "yes_total":"Yes/ total (%)" in a_text,
            "or":" OR " in f" {a_text} ",
            "ci95":"95% CI" in a_text,
            "p_value":"p-value" in a_text,
        },
        "B":{
            "adjusted_or":"Adjusted-OR" in b_text,
            "ci95":"95% CI" in b_text.split("p<0.05",1)[0],
            "p_value":"p-value" in b_text.split("p<0.05",1)[0],
        },
    }
    a_cols=sum(original_structure["A"].values())
    b_cols=sum(original_structure["B"].values())

    vp=VisibleText(); vp.feed(correction_html)
    correction_text=" ".join(vp.text().split())
    correction_confirms=(
        "two columns missing from Table 1B" in correction_text
        or "two columns missing from Table 1B." in correction_text
    )

    # The original PMC record is treated as a preserved-original object only
    # because the live original still displays the known pre-correction schema
    # while the correction is a separate linked record.
    defect_state_preserved=(
        original_structure["B"]["adjusted_or"]
        and original_structure["B"]["p_value"]
        and not original_structure["B"]["ci95"]
        and b_cols < a_cols
    )
    q=assess_track_a_artifact(
        artifact_version_date=VERSION_DATE,
        outcome_date=OUTCOME_DATE,
        immutable_or_historical_snapshot=bool(defect_state_preserved and correction_confirms),
        historical_equivalence="preserved_original_published_version",
        provenance_source="PubMed Central original article record PMC5521765; correction stored separately as PMC5798843",
        title="Table 1 from original article",
        filename_or_path="PMC5521765#Table1",
        leading_text=folded[:6000],
        current_metadata_has_update_relation=True,
    )

    safe=(q.status=="SAFE_EXACT" and defect_state_preserved and correction_confirms)
    qualification={
        "target_doi":DOI,
        "original_url":ORIGINAL_URL,
        "correction_url_manager_only":CORRECTION_URL,
        "artifact_version_date":VERSION_DATE,
        "outcome_date":OUTCOME_DATE,
        "original_html_sha256":hashlib.sha256(original_bytes).hexdigest(),
        "correction_html_sha256":hashlib.sha256(correction_bytes).hexdigest(),
        "original_structure":original_structure,
        "original_A_detected_columns_n":a_cols,
        "original_B_detected_columns_n":b_cols,
        "defect_state_preserved":defect_state_preserved,
        "correction_confirms_two_missing_columns":correction_confirms,
        "generic_artifact_qualification":q.to_dict(),
        "qualification":"SAFE_EXACT" if safe else "BLOCKED",
        "track_a_eligible":safe,
        "manager_used_outcome_metadata":True,
        "detector_may_see_outcome_metadata":False,
    }

    detector_object={
        "track":"A_CONTENT_ONLY",
        "paper_id":"10.1371/journal.pone.0180906",
        "object_role":"table",
        "object_label":"Table 1",
        "source":"PMC5521765 preserved original article",
        "artifact_version_date":VERSION_DATE,
        "safe_exact":safe,
        "section_A_observed_headers":[
            name for name,ok in {
                "Household Variables":original_structure["A"]["household_variables"],
                "Yes/ total (%)":original_structure["A"]["yes_total"],
                "OR":original_structure["A"]["or"],
                "95% CI":original_structure["A"]["ci95"],
                "p-value":original_structure["A"]["p_value"],
            }.items() if ok
        ],
        "section_B_observed_headers":[
            name for name,ok in {
                "Adjusted-OR":original_structure["B"]["adjusted_or"],
                "95% CI":original_structure["B"]["ci95"],
                "p-value":original_structure["B"]["p_value"],
            }.items() if ok
        ],
        "outcome_or_correction_metadata_included":False,
    }

    a.qualification.parent.mkdir(parents=True,exist_ok=True)
    a.qualification.write_text(json.dumps(qualification,indent=2)+"\n",encoding="utf-8")
    a.detector_object.write_text(json.dumps(detector_object,indent=2)+"\n",encoding="utf-8")
    print(json.dumps({
        "qualification":qualification["qualification"],
        "track_a_eligible":safe,
        "A_columns":a_cols,
        "B_columns":b_cols,
        "defect_state_preserved":defect_state_preserved,
        "correction_confirms":correction_confirms,
        "detector_outcome_metadata":detector_object["outcome_or_correction_metadata_included"],
    },indent=2))

if __name__=="__main__":
    main()

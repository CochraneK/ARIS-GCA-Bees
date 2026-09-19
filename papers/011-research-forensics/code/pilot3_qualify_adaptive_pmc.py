#!/usr/bin/env python3
"""Freeze the preserved-original significance sentence for ARIS4C011 Pilot 3.

Manager-side correction evidence is used only to qualify provenance/ground
truth. The detector-visible object contains only the original sentence.
"""
from __future__ import annotations
import argparse,hashlib,json,re
from html.parser import HTMLParser
from pathlib import Path
from urllib.request import Request,urlopen

from artifact_safety import assess_track_a_artifact

ORIGINAL="https://pmc.ncbi.nlm.nih.gov/articles/PMC5538738/"
CORRECTION="https://pmc.ncbi.nlm.nih.gov/articles/PMC5912759/"
DOI="10.1371/journal.pone.0180395"
VERSION_DATE="2017-08-01"
OUTCOME_DATE="2018-04-23"

class Text(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True); self.parts=[]
    def handle_starttag(self,tag,attrs):
        if tag.lower() in {"p","div","section","h1","h2","h3","h4","li","br"}:
            self.parts.append("\n")
    def handle_data(self,data): self.parts.append(data)
    def text(self): return "\n".join(" ".join(x.split()) for x in "".join(self.parts).splitlines() if " ".join(x.split()))

def fetch(url):
    req=Request(url,headers={"User-Agent":"ARIS4C011-Research-Forensics/0.6"})
    with urlopen(req,timeout=30) as r: return r.read()

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--qualification",type=Path,required=True)
    p.add_argument("--detector-object",type=Path,required=True)
    a=p.parse_args()

    ob=fetch(ORIGINAL); cb=fetch(CORRECTION)
    op=Text(); op.feed(ob.decode("utf-8","replace")); original=op.text()
    cp=Text(); cp.feed(cb.decode("utf-8","replace")); correction=cp.text()

    # Exact original target sentence. Flexible whitespace but no correction text.
    m=re.search(
        r"There were significant increases in the amount of imitation by people with dementia\s*\(p\s*>\s*\.05\)\s*in Intervention sessions\.",
        original,
        flags=re.I,
    )
    if not m:
        raise SystemExit("original preserved p>.05 significance sentence not found")
    sentence=" ".join(m.group(0).split())

    manager_confirms=bool(re.search(
        r"correct sentence should read:\s*Therefore, two-tailed results were accepted",
        correction,re.I,
    )) and bool(re.search(
        r"correct sentence should read:\s*There were significant increases in the amount of imitation by people with dementia\s*\(p\s*<\s*\.05\)\s*in Intervention sessions",
        correction,re.I,
    ))

    defect_preserved=("significant increases" in sentence.lower() and bool(re.search(r"p\s*>\s*\.05",sentence,re.I)))
    q=assess_track_a_artifact(
        artifact_version_date=VERSION_DATE,
        outcome_date=OUTCOME_DATE,
        immutable_or_historical_snapshot=bool(defect_preserved and manager_confirms),
        historical_equivalence="preserved_original_published_version",
        provenance_source="PubMed Central original article PMC5538738; correction preserved separately as PMC5912759",
        title="Original Results subsection: Imitation",
        filename_or_path="PMC5538738#Imitation",
        leading_text=sentence,
        current_metadata_has_update_relation=True,
    )
    safe=(q.status=="SAFE_EXACT" and defect_preserved and manager_confirms)

    qualification={
        "target_doi":DOI,
        "artifact_role":"body_text",
        "artifact_version_date":VERSION_DATE,
        "outcome_date":OUTCOME_DATE,
        "original_url":ORIGINAL,
        "correction_url_manager_only":CORRECTION,
        "original_html_sha256":hashlib.sha256(ob).hexdigest(),
        "correction_html_sha256":hashlib.sha256(cb).hexdigest(),
        "defect_state_preserved":defect_preserved,
        "manager_correction_confirms_direction_fix":manager_confirms,
        "generic_artifact_qualification":q.to_dict(),
        "qualification":"SAFE_EXACT" if safe else "BLOCKED",
        "track_a_eligible":safe,
        "detector_may_see_outcome_metadata":False,
    }
    detector={
        "track":"A_CONTENT_ONLY",
        "paper_id":DOI,
        "object_role":"body_text",
        "object_label":"Results > Communicative behaviours > Imitation",
        "source":"PMC5538738 preserved original article",
        "artifact_version_date":VERSION_DATE,
        "safe_exact":safe,
        "text":sentence,
        "outcome_or_correction_metadata_included":False,
    }
    a.qualification.parent.mkdir(parents=True,exist_ok=True)
    a.qualification.write_text(json.dumps(qualification,indent=2)+"\n",encoding="utf-8")
    a.detector_object.write_text(json.dumps(detector,indent=2)+"\n",encoding="utf-8")
    print(json.dumps({
        "qualification":qualification["qualification"],
        "defect_state_preserved":defect_preserved,
        "manager_confirms":manager_confirms,
        "detector_text":sentence,
        "detector_outcome_metadata":False,
    },indent=2))
if __name__=="__main__": main()

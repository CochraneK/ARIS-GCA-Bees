#!/usr/bin/env python3
"""Acquire manager-side public notice evidence availability for ARIS4C011.

This layer is label-side only. It enriches the frozen unadjudicated packet with
Crossref / PubMed / PMC provenance and evidence-availability metadata, but it
does not run detectors, assign issue labels, or copy notice full text into Git.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import time
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from pathlib import Path
from typing import Any

USER_AGENT="ARIS4C011-confirmatory-notice-evidence/0.2 (https://github.com/CochraneK/ARIS4C)"

def request_bytes(url:str,attempts:int=4)->bytes:
    req=urllib.request.Request(url,headers={"User-Agent":USER_AGENT,"Accept":"*/*"})
    last=None
    for i in range(attempts):
        try:
            with urllib.request.urlopen(req,timeout=45) as r:
                return r.read()
        except Exception as exc:
            last=exc
            if i+1>=attempts:
                raise
            time.sleep(1.25*(i+1))
    raise RuntimeError(last)

def get_json(url:str)->dict[str,Any]:
    return json.loads(request_bytes(url).decode("utf-8"))

def first_text(v:Any)->str:
    if isinstance(v,list):
        return str(v[0]) if v else ""
    return str(v or "")

def crossref_notice(doi:str)->dict[str,Any]:
    url="https://api.crossref.org/works/"+urllib.parse.quote(doi,safe="")
    msg=(get_json(url).get("message") or {})
    return {
        "title":first_text(msg.get("title")).strip(),
        "type":str(msg.get("type") or ""),
        "publisher":str(msg.get("publisher") or ""),
        "abstract_present":bool(msg.get("abstract")),
        "link_count":len(msg.get("link") or []),
        "url":str(msg.get("URL") or ("https://doi.org/"+doi)),
    }

def pubmed_ids(doi:str)->list[str]:
    params=urllib.parse.urlencode({
        "db":"pubmed","term":f'"{doi}"[AID]',"retmode":"json","retmax":"5",
        "tool":"aris4c011",
    })
    x=get_json("https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?"+params)
    return [str(v) for v in ((x.get("esearchresult") or {}).get("idlist") or [])]

def pubmed_record(pmid:str)->dict[str,Any]:
    params=urllib.parse.urlencode({"db":"pubmed","id":pmid,"retmode":"xml","tool":"aris4c011"})
    raw=request_bytes("https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?"+params)
    root=ET.fromstring(raw)
    title=" ".join("".join((root.find(".//ArticleTitle") or ET.Element("x")).itertext()).split())
    pubs=sorted({(n.text or "").strip() for n in root.findall(".//PublicationType") if (n.text or "").strip()})
    rels=[]
    for n in root.findall(".//CommentsCorrections"):
        rels.append({
            "ref_type":str(n.attrib.get("RefType") or ""),
            "ref_source":(n.findtext("RefSource") or "").strip(),
            "linked_pmid":(n.findtext("PMID") or "").strip(),
        })
    ids=root.findall(".//PubmedData/ArticleIdList/ArticleId")
    pmcids=sorted({(n.text or "").strip() for n in ids if n.attrib.get("IdType")=="pmc" and (n.text or "").strip()})
    return {
        "pmid":pmid,
        "title":title,
        "publication_types":pubs,
        "comments_corrections":rels,
        "pmc_id":pmcids[0] if len(pmcids)==1 else "",
        "pmc_id_count":len(pmcids),
    }

def pmc_probe(pmcid:str)->dict[str,Any]:
    params=urllib.parse.urlencode({"db":"pmc","id":pmcid,"retmode":"xml","tool":"aris4c011"})
    url="https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?"+params
    raw=request_bytes(url)
    root=ET.fromstring(raw)
    body=root.find(".//body")
    body_text=" ".join("".join(body.itertext()).split()) if body is not None else ""
    return {
        "pmc_id":pmcid,
        "jats_available":bool(body_text),
        "jats_sha256":hashlib.sha256(raw).hexdigest(),
        "body_char_count":len(body_text),
        "source_url":url,
    }

def acquire(rows:list[dict])->dict[str,Any]:
    results=[]
    for row in rows:
        doi=(row.get("notice_or_source_doi") or "").strip().lower()
        rec={
            "feasibility_id":row["feasibility_id"],
            "target_doi":row["target_doi"],
            "notice_or_source_doi":doi,
            "update_type":row["update_type"],
            "outcome_date":row["outcome_date"],
            "crossref":None,
            "pubmed_exact_doi_pmids":[],
            "pubmed":None,
            "pmc":None,
            "manager_evidence_route":"PUBLISHER_DOI",
            "acquisition_errors":[],
            "issue_adjudication_state":"UNASSESSED",
            "detector_output_used":False,
        }
        try:
            rec["crossref"]=crossref_notice(doi)
        except Exception as exc:
            rec["acquisition_errors"].append("crossref:"+type(exc).__name__)
        time.sleep(0.12)
        try:
            ids=pubmed_ids(doi)
            rec["pubmed_exact_doi_pmids"]=ids
            if len(ids)==1:
                rec["pubmed"]=pubmed_record(ids[0])
                rec["manager_evidence_route"]="PUBMED"
                pmcid=rec["pubmed"].get("pmc_id","")
                if pmcid:
                    rec["pmc"]=pmc_probe(pmcid)
                    if rec["pmc"].get("jats_available"):
                        rec["manager_evidence_route"]="PMC_JATS"
        except Exception as exc:
            rec["acquisition_errors"].append("pubmed_pmc:"+type(exc).__name__)
        time.sleep(0.20)
        results.append(rec)
    routes={}
    for r in results:
        routes[r["manager_evidence_route"]]=routes.get(r["manager_evidence_route"],0)+1
    return {
        "analysis":"ARIS4C011 manager-side notice evidence availability v0",
        "state":"MANAGER_EVIDENCE_ACQUIRED_UNADJUDICATED",
        "row_count":len(results),
        "detector_output_used":False,
        "full_notice_text_committed":False,
        "claim_boundary":"Evidence acquisition only. No issue family, artifact role, detector performance, or confirmatory eligibility is inferred here.",
        "route_counts":routes,
        "rows_with_any_acquisition_error":sum(bool(r["acquisition_errors"]) for r in results),
        "rows":results,
    }

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--input",type=Path,required=True)
    p.add_argument("--output",type=Path,required=True)
    a=p.parse_args()
    with a.input.open(newline="",encoding="utf-8") as f:
        rows=list(csv.DictReader(f))
    out=acquire(rows)
    a.output.parent.mkdir(parents=True,exist_ok=True)
    a.output.write_text(json.dumps(out,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    print(json.dumps({
        "row_count":out["row_count"],
        "route_counts":out["route_counts"],
        "rows_with_any_acquisition_error":out["rows_with_any_acquisition_error"],
        "detector_output_used":False,
    },indent=2))
    if out["row_count"]!=len(rows):
        raise SystemExit("row-count mismatch")

if __name__=="__main__":
    main()

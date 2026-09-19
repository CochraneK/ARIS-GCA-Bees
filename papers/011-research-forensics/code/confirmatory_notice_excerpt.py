#!/usr/bin/env python3
"""Create short manager-only notice excerpts for adjudication.

Excerpts are capped at 80 whitespace-delimited words per source. Full notice
text is never committed. This file is label-side provenance and must never be
used as Track-A detector input.
"""
from __future__ import annotations
import argparse,json,re,time,urllib.parse,urllib.request
import xml.etree.ElementTree as ET
from pathlib import Path

UA="ARIS4C011-confirmatory-notice-excerpt/0.1 (https://github.com/CochraneK/ARIS4C)"
MAX_WORDS=80

def request(url,attempts=4):
    req=urllib.request.Request(url,headers={"User-Agent":UA,"Accept":"*/*"})
    last=None
    for i in range(attempts):
        try:
            with urllib.request.urlopen(req,timeout=45) as r: return r.read()
        except Exception as exc:
            last=exc
            if i+1>=attempts: raise
            time.sleep(1.25*(i+1))
    raise RuntimeError(last)

def compact(text):
    return " ".join((text or "").split())

def cap(text,max_words=MAX_WORDS):
    words=compact(text).split()
    return " ".join(words[:max_words]),len(words)>max_words,len(words)

def pubmed_abstract(pmid):
    q=urllib.parse.urlencode({"db":"pubmed","id":pmid,"retmode":"xml","tool":"aris4c011"})
    root=ET.fromstring(request("https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?"+q))
    parts=[]
    for n in root.findall(".//Abstract/AbstractText"):
        label=(n.attrib.get("Label") or "").strip()
        text=compact("".join(n.itertext()))
        if text: parts.append((label+": " if label else "")+text)
    return compact(" ".join(parts))

def pmc_body(pmcid):
    q=urllib.parse.urlencode({"db":"pmc","id":pmcid,"retmode":"xml","tool":"aris4c011"})
    root=ET.fromstring(request("https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?"+q))
    body=root.find(".//body")
    return compact("".join(body.itertext())) if body is not None else ""

def build(evidence):
    rows=[]
    for src in evidence.get("rows",[]):
        route=src.get("manager_evidence_route")
        text=""; kind="NONE"; source_url="https://doi.org/"+src["notice_or_source_doi"]; error=""
        try:
            if route=="PMC_JATS" and src.get("pmc",{}).get("pmc_id"):
                pmcid=src["pmc"]["pmc_id"]
                text=pmc_body(pmcid); kind="PMC_JATS"
                source_url=f"https://pmc.ncbi.nlm.nih.gov/articles/{pmcid}/"
            elif route=="PUBMED" and src.get("pubmed",{}).get("pmid"):
                pmid=src["pubmed"]["pmid"]
                text=pubmed_abstract(pmid); kind="PUBMED_ABSTRACT" if text else "PUBMED_METADATA_ONLY"
                source_url=f"https://pubmed.ncbi.nlm.nih.gov/{pmid}/"
        except Exception as exc:
            error=type(exc).__name__
        excerpt,truncated,total=cap(text)
        rows.append({
            "feasibility_id":src["feasibility_id"],
            "target_doi":src["target_doi"],
            "notice_or_source_doi":src["notice_or_source_doi"],
            "update_type":src["update_type"],
            "source_kind":kind,
            "source_url":source_url,
            "excerpt":excerpt,
            "excerpt_word_count":len(excerpt.split()),
            "source_word_count":total,
            "excerpt_truncated":truncated,
            "acquisition_error":error,
            "manager_only":True,
            "track_a_input_allowed":False,
        })
        time.sleep(0.15)
    return {
        "analysis":"ARIS4C011 manager-only short notice excerpts v0",
        "state":"MANAGER_EXCERPTS_NOT_TRACK_A_INPUT",
        "max_excerpt_words":MAX_WORDS,
        "row_count":len(rows),
        "rows_with_nonempty_excerpt":sum(bool(x["excerpt"]) for x in rows),
        "rows_with_error":sum(bool(x["acquisition_error"]) for x in rows),
        "full_notice_text_committed":False,
        "rows":rows,
    }

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--input",type=Path,required=True)
    p.add_argument("--output",type=Path,required=True)
    a=p.parse_args()
    e=json.loads(a.input.read_text(encoding="utf-8"))
    out=build(e)
    a.output.parent.mkdir(parents=True,exist_ok=True)
    a.output.write_text(json.dumps(out,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    print(json.dumps({
      "rows":out["row_count"],"nonempty":out["rows_with_nonempty_excerpt"],
      "errors":out["rows_with_error"],"max_excerpt_words":MAX_WORDS
    },indent=2))
    if any(x["excerpt_word_count"]>MAX_WORDS for x in out["rows"]): raise SystemExit(1)

if __name__=="__main__": main()

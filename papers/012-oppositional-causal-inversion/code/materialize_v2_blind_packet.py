#!/usr/bin/env python3
"""Materialize and freeze the ARIS4C012 Schema-v2 blind validation packet.

Scientific invariants:
- consume only the frozen fresh-sample manifest;
- never expose retrieval stratum/query/draw metadata to coders;
- never expose Pilot-0 labels, disagreement diagnoses, or adjudication;
- give A2 and B2 byte-identical evidence and response forms;
- preserve provenance for every evidence excerpt;
- never overwrite an existing freeze unless the caller explicitly removes it first.

Evidence is metadata/abstract level only. Abstracts are normalized and capped at
180 words. Missing abstracts remain explicit BIBLIOGRAPHIC_ONLY cases rather
than being silently inferred from titles.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import html
import json
import re
import time
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

USER_AGENT = "ARIS4C012/2.0 research-metadata-materializer (+https://github.com/CochraneK/ARIS4C)"
MAX_EVIDENCE_WORDS = 180
FORBIDDEN_MANIFEST_FIELDS = {
    "stratum","query_index","query","provider","provider_id","cited_by_count",
    "dedupe_key","draw_score","selection_rank","source_rank",
}
FORBIDDEN_CODING_FIELDS = {
    "opposition_valid","oci_candidate","primary_mechanism","actor_switch",
    "level_switch","time_switch","construct_switch","environment_switch",
    "feedback","nonlinearity","selection_filtering","power_asymmetry",
    "evidence_tier","causal_claim_strength","result_support",
}

def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()

def sha256_file(path: Path) -> str:
    return sha256_bytes(path.read_bytes())

def read_csv(path: Path) -> list[dict[str,str]]:
    with path.open(encoding="utf-8",newline="") as f:
        return list(csv.DictReader(f))

def clean_text(value: str | None) -> str:
    s = html.unescape(value or "")
    s = re.sub(r"<[^>]+>", " ", s)
    s = re.sub(r"\\s+", " ", s).strip()
    return s

def cap_words(text: str, limit: int = MAX_EVIDENCE_WORDS) -> tuple[str,bool,int]:
    words = text.split()
    truncated = len(words) > limit
    kept = words[:limit]
    return " ".join(kept), truncated, len(kept)

def reconstruct_openalex_abstract(inv) -> str:
    if not isinstance(inv, dict) or not inv:
        return ""
    positions = []
    for word, locs in inv.items():
        if not isinstance(locs, list):
            continue
        for pos in locs:
            if isinstance(pos, int):
                positions.append((pos, word))
    positions.sort()
    return clean_text(" ".join(word for _, word in positions))

def request_json(url: str, timeout: int = 30, retries: int = 3):
    last = None
    for attempt in range(retries):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT, "Accept":"application/json"})
            with urllib.request.urlopen(req, timeout=timeout) as r:
                return json.loads(r.read().decode("utf-8"))
        except Exception as exc:
            last = exc
            if attempt + 1 < retries:
                time.sleep(0.8 * (attempt + 1))
    raise RuntimeError(f"request failed: {url} ({type(last).__name__})") from last

def fetch_openalex(doi: str) -> tuple[str,str,str]:
    if not doi:
        return "","",""
    url = "https://api.openalex.org/works/https://doi.org/" + doi
    try:
        d = request_json(url)
    except Exception:
        return "","",""
    abstract = reconstruct_openalex_abstract(d.get("abstract_inverted_index"))
    landing = ""
    pl = d.get("primary_location") or {}
    if isinstance(pl, dict):
        landing = pl.get("landing_page_url") or ""
    return abstract, url, landing

def fetch_crossref(doi: str) -> tuple[str,str,str]:
    if not doi:
        return "","",""
    url = "https://api.crossref.org/works/" + urllib.parse.quote(doi, safe="")
    try:
        d = request_json(url)
    except Exception:
        return "","",""
    msg = d.get("message") or {}
    abstract = clean_text(msg.get("abstract") or "")
    landing = msg.get("URL") or ""
    return abstract, url, landing

def fetch_semantic_scholar(doi: str) -> tuple[str,str,str]:
    if not doi:
        return "","",""
    ident = urllib.parse.quote("DOI:" + doi, safe="")
    url = "https://api.semanticscholar.org/graph/v1/paper/" + ident + "?fields=title,abstract,year,venue,externalIds,url"
    try:
        d = request_json(url)
    except Exception:
        return "","",""
    return clean_text(d.get("abstract") or ""), url, d.get("url") or ""

def evidence_for(row: dict[str,str]) -> dict:
    doi = (row.get("doi") or "").strip().lower()
    title = clean_text(row.get("title"))
    evidence = ""
    source = ""
    source_url = ""
    landing = row.get("landing_url") or ""

    for name, fn in (
        ("openalex", fetch_openalex),
        ("crossref", fetch_crossref),
        ("semantic_scholar", fetch_semantic_scholar),
    ):
        text, api_url, source_landing = fn(doi)
        if text:
            evidence, source, source_url = text, name, api_url
            if source_landing:
                landing = source_landing
            break

    evidence, truncated, word_count = cap_words(evidence)
    state = "ABSTRACT_EXCERPT" if evidence else "BIBLIOGRAPHIC_ONLY"
    return {
        "sample_id": row["sample_id"],
        "title": title,
        "year": row.get("year") or "",
        "doi": doi,
        "type": row.get("type") or "",
        "venue": clean_text(row.get("venue_or_topic")),
        "evidence_text": evidence,
        "evidence_state": state,
        "evidence_source": source,
        "evidence_source_url": source_url,
        "landing_url": landing,
        "evidence_word_count": word_count,
        "evidence_truncated": truncated,
    }

def assert_blind_record(record: dict) -> None:
    leaked = FORBIDDEN_MANIFEST_FIELDS.intersection(record)
    if leaked:
        raise AssertionError(f"retrieval metadata leaked into blind packet: {sorted(leaked)}")
    leaked = FORBIDDEN_CODING_FIELDS.intersection(record)
    if leaked:
        raise AssertionError(f"prior coding fields leaked into blind packet: {sorted(leaked)}")

def canonical_jsonl(records: list[dict]) -> bytes:
    lines=[]
    for r in sorted(records,key=lambda x:x["sample_id"]):
        assert_blind_record(r)
        lines.append(json.dumps(r,ensure_ascii=False,sort_keys=True,separators=(",",":")))
    return ("\\n".join(lines)+"\\n").encode("utf-8")

def build_response_csv(template_path: Path, records: list[dict]) -> bytes:
    with template_path.open(encoding="utf-8",newline="") as f:
        reader=csv.DictReader(f)
        fields=reader.fieldnames or []
    if "sample_id" not in fields or "title" not in fields:
        raise AssertionError("v2 coding template must contain sample_id and title")
    import io
    buf=io.StringIO(newline="")
    w=csv.DictWriter(buf,fieldnames=fields,lineterminator="\\n")
    w.writeheader()
    for r in sorted(records,key=lambda x:x["sample_id"]):
        row={k:"" for k in fields}
        row["sample_id"]=r["sample_id"]
        row["title"]=r["title"]
        w.writerow(row)
    return buf.getvalue().encode("utf-8")

def main() -> None:
    ap=argparse.ArgumentParser()
    ap.add_argument("--sample",required=True)
    ap.add_argument("--schema",required=True)
    ap.add_argument("--template",required=True)
    ap.add_argument("--out-dir",required=True)
    ap.add_argument("--freeze-dir",required=True)
    ap.add_argument("--sleep",type=float,default=0.15)
    args=ap.parse_args()

    sample_path=Path(args.sample)
    schema_path=Path(args.schema)
    template_path=Path(args.template)
    out_dir=Path(args.out_dir)
    freeze_dir=Path(args.freeze_dir)
    common_freeze=freeze_dir/"V2_BLIND_PACKET_FREEZE.json"
    if common_freeze.exists():
        print(f"Freeze already exists: {common_freeze}; refusing to overwrite.")
        return

    rows=read_csv(sample_path)
    if len(rows)!=30 or len({r["sample_id"] for r in rows})!=30:
        raise AssertionError("frozen sample must contain exactly 30 unique sample IDs")

    records=[]
    for i,row in enumerate(rows):
        records.append(evidence_for(row))
        if args.sleep and i+1 < len(rows):
            time.sleep(args.sleep)

    out_dir.mkdir(parents=True,exist_ok=True)
    freeze_dir.mkdir(parents=True,exist_ok=True)

    packet_bytes=canonical_jsonl(records)
    packet_path=out_dir/"common_evidence_packet.jsonl"
    packet_path.write_bytes(packet_bytes)

    response_bytes=build_response_csv(template_path,records)
    a2_path=out_dir/"A2_response.csv"
    b2_path=out_dir/"B2_response.csv"
    a2_path.write_bytes(response_bytes)
    b2_path.write_bytes(response_bytes)

    packet_sha=sha256_bytes(packet_bytes)
    schema_sha=sha256_file(schema_path)
    response_sha=sha256_bytes(response_bytes)
    bundle_material=(packet_sha+"\\n"+schema_sha+"\\n"+response_sha+"\\n").encode()
    bundle_sha=sha256_bytes(bundle_material)

    counts={}
    sources={}
    for r in records:
        counts[r["evidence_state"]]=counts.get(r["evidence_state"],0)+1
        src=r["evidence_source"] or "none"
        sources[src]=sources.get(src,0)+1

    retrieved=datetime.now(timezone.utc).isoformat()
    report={
        "classification":"V2_BLIND_EVIDENCE_MATERIALIZATION",
        "retrieved_at":retrieved,
        "sample_count":len(records),
        "evidence_state_counts":counts,
        "evidence_source_counts":sources,
        "abstract_excerpt_count":counts.get("ABSTRACT_EXCERPT",0),
        "bibliographic_only_count":counts.get("BIBLIOGRAPHIC_ONLY",0),
        "max_evidence_words":MAX_EVIDENCE_WORDS,
        "blind_fields_excluded":sorted(FORBIDDEN_MANIFEST_FIELDS | FORBIDDEN_CODING_FIELDS),
        "ready_for_independent_coding":counts.get("BIBLIOGRAPHIC_ONLY",0)==0,
        "note":"If bibliographic_only_count > 0, do not start A2/B2. First apply a pre-coding evidence-availability amendment or acquire equivalent blinded evidence without inspecting labels.",
    }
    report_path=out_dir/"materialization_report.json"
    report_path.write_text(json.dumps(report,ensure_ascii=False,indent=2)+"\\n",encoding="utf-8")

    common={
        "classification":"V2_BLIND_PACKET_FREEZE",
        "frozen_at":retrieved,
        "sample_manifest":str(sample_path),
        "sample_manifest_sha256":sha256_file(sample_path),
        "schema":str(schema_path),
        "schema_sha256":schema_sha,
        "evidence_packet":str(packet_path),
        "evidence_packet_sha256":packet_sha,
        "response_form_sha256":response_sha,
        "bundle_sha256":bundle_sha,
        "sample_count":30,
        "byte_identical_coder_inputs":True,
        "materialization_report":str(report_path),
        "ready_for_independent_coding":report["ready_for_independent_coding"],
    }
    common_freeze.write_text(json.dumps(common,ensure_ascii=False,indent=2)+"\\n",encoding="utf-8")

    for coder,path in (("A2",a2_path),("B2",b2_path)):
        d={
            "classification":"V2_INDEPENDENT_CODER_INPUT_FREEZE",
            "coder":coder,
            "frozen_at":retrieved,
            "evidence_packet_sha256":packet_sha,
            "schema_sha256":schema_sha,
            "response_form":str(path),
            "response_form_sha256":sha256_file(path),
            "bundle_sha256":bundle_sha,
            "must_remain_blind_to_other_coder":True,
            "must_remain_blind_to_pilot0_labels_and_adjudication":True,
            "ready_for_independent_coding":report["ready_for_independent_coding"],
        }
        (freeze_dir/f"{coder}_INPUT_FREEZE.json").write_text(json.dumps(d,ensure_ascii=False,indent=2)+"\\n",encoding="utf-8")

    assert sha256_file(a2_path)==sha256_file(b2_path)==response_sha
    a2=json.loads((freeze_dir/"A2_INPUT_FREEZE.json").read_text(encoding="utf-8"))
    b2=json.loads((freeze_dir/"B2_INPUT_FREEZE.json").read_text(encoding="utf-8"))
    assert a2["bundle_sha256"]==b2["bundle_sha256"]==bundle_sha
    print(json.dumps(report,ensure_ascii=False,indent=2))

if __name__=="__main__":
    main()

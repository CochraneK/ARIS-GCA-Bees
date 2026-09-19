#!/usr/bin/env python3
"""Build a blinded ARIS4C011 confirmatory-feasibility event frame.

This is NOT the confirmatory benchmark and contains no detector outputs.
It samples Crossref correction/retraction update events in balanced calendar
strata, excludes every DOI exposed during development, resolves target-paper
metadata, and leaves artifact/issue eligibility unassessed.

Purpose: estimate acquisition/adjudication/missingness feasibility before
freezing confirmatory sample size, splits, thresholds, or performance analysis.
"""
from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import json
import re
import time
import urllib.parse
import urllib.request
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_EXCLUSIONS = ROOT / "data" / "protocol" / "development_exclusion_registry.json"
USER_AGENT = "ARIS4C011-confirmatory-feasibility/0.1 (https://github.com/CochraneK/ARIS4C)"
STATUS_RE = re.compile(
    r"\b(RETRACTED|RETRACTION|WITHDRAWN|CORRECTION|CORRIGENDUM|ERRATUM|"
    r"EXPRESSION\s+OF\s+CONCERN)\b",
    re.I,
)


def norm_doi(value: str) -> str:
    x=(value or "").strip().lower()
    x=re.sub(r"^https?://(?:dx\.)?doi\.org/","",x)
    x=re.sub(r"^doi:\s*","",x)
    return x.rstrip(".,;")


def date_parts(obj: dict[str, Any] | None) -> str:
    if not obj:
        return ""
    parts=obj.get("date-parts") or []
    if not parts or not parts[0]:
        return ""
    p=list(parts[0])
    y=int(p[0]); m=int(p[1]) if len(p)>1 else 1; d=int(p[2]) if len(p)>2 else 1
    return f"{y:04d}-{m:02d}-{d:02d}"


def first_text(value: Any) -> str:
    if isinstance(value,list):
        return str(value[0]) if value else ""
    return str(value or "")


def request_json(url: str, attempts: int = 5) -> dict[str, Any]:
    req=urllib.request.Request(url,headers={"User-Agent":USER_AGENT,"Accept":"application/json"})
    last=None
    for attempt in range(attempts):
        try:
            with urllib.request.urlopen(req,timeout=45) as r:
                return json.load(r)
        except Exception as exc:
            last=exc
            if attempt+1>=attempts:
                raise
            time.sleep(1.5*(attempt+1))
    raise RuntimeError(last)


def development_dois(path: Path) -> set[str]:
    x=json.loads(path.read_text(encoding="utf-8"))
    return {norm_doi(e.get("doi","")) for e in x.get("entries",[]) if norm_doi(e.get("doi",""))}


def stable_rank(*parts: str) -> str:
    return hashlib.sha256("\x1f".join(parts).encode()).hexdigest()


def source_work_date(item: dict[str,Any]) -> str:
    for key in ("published-online","published-print","published","issued","created"):
        d=date_parts(item.get(key))
        if d:
            return d
    return ""


def update_events_for_year(update_type: str, year: int, rows: int) -> list[dict[str,Any]]:
    params={
        "filter": ",".join([
            f"update-type:{update_type}",
            f"from-pub-date:{year}-01-01",
            f"until-pub-date:{year}-12-31",
        ]),
        "rows": str(rows),
    }
    url="https://api.crossref.org/v1/works?"+urllib.parse.urlencode(params)
    payload=request_json(url)
    items=((payload.get("message") or {}).get("items") or [])
    out=[]
    for item in items:
        source_doi=norm_doi(item.get("DOI",""))
        for rel in item.get("update-to") or []:
            rel_type=str(rel.get("type") or "").strip().lower()
            if rel_type!=update_type:
                continue
            target=norm_doi(rel.get("DOI",""))
            if not target:
                continue
            outcome=date_parts(rel.get("updated")) or source_work_date(item)
            out.append({
                "target_doi":target,
                "notice_or_source_doi":source_doi,
                "update_type":update_type,
                "outcome_date":outcome,
                "assertion_source":str(rel.get("source") or "").strip().lower(),
                "relation_label":str(rel.get("label") or "").strip(),
                "source_work_title":first_text(item.get("title")).strip(),
                "source_work_date":source_work_date(item),
            })
    return out


def resolve_target(doi: str) -> dict[str,Any]:
    url="https://api.crossref.org/v1/works/"+urllib.parse.quote(doi,safe="")
    msg=(request_json(url).get("message") or {})
    title=first_text(msg.get("title")).strip()
    published=""
    for key in ("published-online","published-print","published","issued","created"):
        published=date_parts(msg.get(key))
        if published:
            break
    return {
        "target_title_current":title,
        "target_title_has_status_marker":bool(STATUS_RE.search(title)),
        "target_published":published,
        "target_year":int(published[:4]) if published[:4].isdigit() else None,
        "target_journal":first_text(msg.get("container-title")).strip(),
        "target_type":str(msg.get("type") or ""),
        "crossref_has_abstract":bool(msg.get("abstract")),
        "crossref_has_fulltext_link":bool(msg.get("link")),
        "crossref_has_updated_by":bool(msg.get("updated-by")),
        "reference_count":msg.get("reference-count"),
        "is_referenced_by_count":msg.get("is-referenced-by-count"),
    }


def build(
    exclusions: Path,
    start_year: int,
    end_year: int,
    per_year_type: int,
    query_rows: int,
) -> dict[str,Any]:
    excluded=development_dois(exclusions)
    selected=[]
    seen=set()

    for year in range(start_year,end_year+1):
        for update_type in ("correction","retraction"):
            events=update_events_for_year(update_type,year,query_rows)
            clean=[]
            for e in events:
                key=(e["target_doi"],e["update_type"],e["outcome_date"])
                if e["target_doi"] in excluded or e["notice_or_source_doi"] in excluded:
                    continue
                if key in seen:
                    continue
                clean.append(e)
            clean.sort(key=lambda e:stable_rank(
                str(year),update_type,e["target_doi"],e["notice_or_source_doi"],e["outcome_date"]
            ))
            chosen=clean[:per_year_type]
            for e in chosen:
                seen.add((e["target_doi"],e["update_type"],e["outcome_date"]))
                selected.append({"calendar_stratum":year,**e})

    resolved=[]
    for i,e in enumerate(selected,1):
        meta=resolve_target(e["target_doi"])
        resolved.append({
            "feasibility_id":f"F{i:03d}",
            **e,
            **meta,
            "issue_adjudication_state":"UNASSESSED",
            "required_artifact_role":"UNASSESSED",
            "artifact_state":"UNASSESSED",
            "confirmatory_eligible":None,
            "detector_output_visible":False,
        })
        time.sleep(0.05)

    counts={}
    for r in resolved:
        k=f'{r["calendar_stratum"]}:{r["update_type"]}'
        counts[k]=counts.get(k,0)+1

    try:
        exclusion_ref=str(exclusions.relative_to(ROOT))
    except ValueError:
        exclusion_ref=exclusions.name

    return {
        "analysis":"ARIS4C011 blinded confirmatory-feasibility frame v0",
        "state":"FEASIBILITY_ONLY_NOT_CONFIRMATORY",
        "generated_utc":dt.datetime.now(dt.timezone.utc).replace(microsecond=0).isoformat(),
        "source":"Crossref REST update-to metadata",
        "development_exclusion_registry":exclusion_ref,
        "development_exclusion_count":len(excluded),
        "calendar_range":[start_year,end_year],
        "update_types":["correction","retraction"],
        "selection_rule":(
            "Within each calendar-year × update-type stratum, exclude any target/source DOI "
            "exposed in development, deduplicate event keys, rank remaining events by SHA-256 "
            "of frozen provenance identifiers, and retain the first N. Detector outputs and "
            "review priority are never used for selection."
        ),
        "per_year_type_target":per_year_type,
        "query_rows_per_stratum":query_rows,
        "candidate_count":len(resolved),
        "counts_by_stratum":counts,
        "allowed_uses":[
            "estimate acquisition workload",
            "estimate issue-adjudication workload",
            "estimate artifact availability/missingness after role qualification",
            "inform confirmatory sample-size planning without detector-effect peeking",
        ],
        "forbidden_uses":[
            "detector performance estimation",
            "threshold tuning",
            "specificity or sensitivity estimation",
            "confirmatory hypothesis testing",
        ],
        "rows":resolved,
    }


def main():
    p=argparse.ArgumentParser()
    p.add_argument("--exclusions",type=Path,default=DEFAULT_EXCLUSIONS)
    p.add_argument("--output",type=Path,required=True)
    p.add_argument("--start-year",type=int,default=2016)
    p.add_argument("--end-year",type=int,default=2025)
    p.add_argument("--per-year-type",type=int,default=4)
    p.add_argument("--query-rows",type=int,default=100)
    a=p.parse_args()
    if a.start_year>a.end_year: raise SystemExit("start year > end year")
    if not (1<=a.per_year_type<=20): raise SystemExit("per-year-type must be 1..20")
    result=build(a.exclusions,a.start_year,a.end_year,a.per_year_type,a.query_rows)
    a.output.parent.mkdir(parents=True,exist_ok=True)
    a.output.write_text(json.dumps(result,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    print(json.dumps({
        "state":result["state"],
        "candidate_count":result["candidate_count"],
        "strata":len(result["counts_by_stratum"]),
        "development_exclusion_count":result["development_exclusion_count"],
    },indent=2))
    expected=(a.end_year-a.start_year+1)*2*a.per_year_type
    if result["candidate_count"]<expected:
        raise SystemExit(f"Frame incomplete: {result['candidate_count']} < target {expected}")


if __name__=="__main__":
    main()

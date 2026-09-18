"""Live archive discovery for ARIS4C011 Pilot 3 priority candidates.

This tool discovers pre-correction CDX captures only. Discovery never upgrades an
artifact to SAFE_EXACT; identity/equivalence/content qualification remains a
separate gate.
"""
from __future__ import annotations
import argparse, csv, json
from pathlib import Path
from wayback_discovery import discover

def read_csv(path: Path):
    with path.open(encoding="utf-8", newline="") as h:
        return list(csv.DictReader(h))

def patterns(doi: str):
    return [
        ("article_html", f"https://journals.plos.org/plosone/article?id={doi}"),
        ("printable_pdf", f"https://journals.plos.org/plosone/article/file?id={doi}&type=printable"),
        ("figure_table_objects", f"https://journals.plos.org/plosone/article/figure?id={doi}*"),
    ]

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--queue",type=Path,required=True)
    ap.add_argument("--output",type=Path,required=True)
    ap.add_argument("--limit",type=int,default=2)
    args=ap.parse_args()
    rows=[r for r in read_csv(args.queue) if r.get("queue_status")=="PRIORITY"][:args.limit]
    out=[]
    for row in rows:
        doi=row["target_doi"]
        event=row["correction_published"]
        for role,url in patterns(doi):
            try:
                records=discover(url,event_date=event,identity_marker=doi,timeout=30)
                captures=[{
                    "timestamp":x.timestamp,
                    "original":x.original,
                    "digest":x.digest,
                    "mimetype":x.mimetype,
                    "statuscode":x.statuscode,
                } for x in records]
                error=""
            except Exception as exc:
                captures=[]
                error=f"{type(exc).__name__}:{exc}"
            out.append({
                "candidate_id":row["candidate_id"],
                "target_doi":doi,
                "correction_published":event,
                "required_role":row["required_role"],
                "query_role":role,
                "query_url":url,
                "capture_n":len(captures),
                "captures":captures,
                "error":error,
                "qualification_status":"DISCOVERY_ONLY",
            })
    summary={
        "candidate_n":len(rows),
        "query_n":len(out),
        "queries_with_capture":sum(x["capture_n"]>0 for x in out),
        "total_unique_capture_digests":len({c["digest"] for x in out for c in x["captures"] if c["digest"]}),
        "safe_exact_claims":0,
        "note":"CDX discovery only; every object still requires identity, version/equivalence and content-role qualification.",
        "queries":out,
    }
    args.output.parent.mkdir(parents=True,exist_ok=True)
    args.output.write_text(json.dumps(summary,indent=2)+"\n",encoding="utf-8")
    print(json.dumps({k:v for k,v in summary.items() if k!="queries"},indent=2))

if __name__=="__main__":
    main()

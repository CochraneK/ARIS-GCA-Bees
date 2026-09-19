#!/usr/bin/env python3
"""Build a conservative DOI denylist from structured ARIS4C011 development artifacts."""

from __future__ import annotations
import argparse, csv, json, re
from pathlib import Path
from typing import Any

DOI_RE = re.compile(r"^10\.\d{4,9}/\S+$", re.I)
KEY_RE = re.compile(r"(doi|paper_id)", re.I)

def norm(value: str) -> str:
    x=(value or "").strip().lower()
    x=re.sub(r"^https?://(?:dx\.)?doi\.org/","",x)
    x=re.sub(r"^doi:\s*","",x)
    return x.rstrip(".,;")

def maybe_add(out: dict[str,dict[str,Any]], key: str, value: Any, source: str) -> None:
    if not KEY_RE.search(str(key)) or not isinstance(value,(str,int,float)):
        return
    doi=norm(str(value))
    if not DOI_RE.match(doi):
        return
    row=out.setdefault(doi,{"doi":doi,"source_files":[],"source_fields":[]})
    if source not in row["source_files"]: row["source_files"].append(source)
    if str(key) not in row["source_fields"]: row["source_fields"].append(str(key))

def walk_json(obj: Any, out: dict[str,dict[str,Any]], source: str, key: str="") -> None:
    if isinstance(obj,dict):
        for k,v in obj.items():
            if isinstance(v,(dict,list)): walk_json(v,out,source,k)
            else: maybe_add(out,k,v,source)
    elif isinstance(obj,list):
        for v in obj: walk_json(v,out,source,key)

def collect(root: Path) -> dict[str,dict[str,Any]]:
    out={}
    candidates=[]
    for base in [root/"data"/"seed",root/"data"/"pilot"]:
        if base.exists():
            candidates += list(base.rglob("*.csv")) + list(base.rglob("*.json"))
    res=root/"data"/"results"
    if res.exists():
        candidates += list(res.glob("pilot*.csv")) + list(res.glob("pilot*.json"))
    for path in sorted(set(candidates)):
        rel=str(path.relative_to(root))
        if path.suffix==".json":
            walk_json(json.loads(path.read_text(encoding="utf-8")),out,rel)
        else:
            with path.open(newline="",encoding="utf-8-sig") as f:
                for row in csv.DictReader(f):
                    for k,v in row.items(): maybe_add(out,k,v,rel)
    for row in out.values():
        row["source_files"].sort(); row["source_fields"].sort()
    return out

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--root",type=Path,default=Path(__file__).resolve().parents[1])
    p.add_argument("--output",type=Path)
    a=p.parse_args()
    outpath=a.output or a.root/"data"/"protocol"/"development_exclusion_registry.json"
    rows=collect(a.root)
    payload={
      "registry_version":"0.1.0",
      "state":"FROZEN_DEVELOPMENT_EXPOSURE_SNAPSHOT",
      "generated_from":"structured seed/pilot artifacts plus data/results/pilot*",
      "exclusion_count":len(rows),
      "policy":"Any DOI exposed during method development, pilot acquisition, comparator discovery/screening, control construction, or development evaluation is excluded from confirmatory performance manifests.",
      "entries":[rows[k] for k in sorted(rows)],
    }
    outpath.parent.mkdir(parents=True,exist_ok=True)
    outpath.write_text(json.dumps(payload,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    print(json.dumps({"exclusion_count":len(rows),"output":str(outpath)},indent=2))

if __name__=="__main__": main()

#!/usr/bin/env python3
"""Create deterministic size-balanced OpenAlex Parquet shard file lists.

Uses only the pinned official manifest. Files are sorted by descending byte
size and greedily assigned to the currently lightest shard. The same manifest,
shard count, and algorithm always produce the same assignment.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path


def sha256(path: Path) -> str:
    h=hashlib.sha256()
    with path.open("rb") as f:
        for b in iter(lambda:f.read(1<<20),b""):
            h.update(b)
    return h.hexdigest()


def main() -> None:
    p=argparse.ArgumentParser()
    p.add_argument("manifest",type=Path)
    p.add_argument("--shards",type=int,default=32)
    p.add_argument("--output-dir",type=Path,required=True)
    args=p.parse_args()
    if args.shards < 1:
        raise SystemExit("--shards must be >=1")

    obj=json.loads(args.manifest.read_text(encoding="utf-8"))
    files=obj.get("files",[])
    if not files:
        raise SystemExit("Manifest has no files")

    normalized=[]
    for x in files:
        url=x.get("url")
        meta=x.get("meta",{})
        size=int(meta.get("content_length",0))
        records=int(meta.get("record_count",0))
        if not url or size < 0 or records < 0:
            raise SystemExit(f"Invalid manifest file entry: {x}")
        normalized.append((url,size,records))

    bins=[{"bytes":0,"records":0,"files":[]} for _ in range(args.shards)]
    for url,size,records in sorted(normalized,key=lambda z:(-z[1],z[0])):
        idx=min(range(args.shards),key=lambda i:(bins[i]["bytes"],i))
        bins[idx]["files"].append(url)
        bins[idx]["bytes"] += size
        bins[idx]["records"] += records

    args.output_dir.mkdir(parents=True,exist_ok=True)
    rows=[]
    for i,b in enumerate(bins):
        path=args.output_dir/f"shard_{i:03d}.txt"
        path.write_text("\n".join(b["files"])+"\n",encoding="utf-8")
        rows.append({
            "shard":i,
            "file_count":len(b["files"]),
            "content_length":b["bytes"],
            "record_count":b["records"],
            "file_list":str(path),
            "file_list_sha256":sha256(path),
        })

    total_bytes=sum(x["content_length"] for x in rows)
    total_records=sum(x["record_count"] for x in rows)
    expected_bytes=int(obj.get("content_length",total_bytes))
    expected_records=int(obj.get("record_count",total_records))
    if total_bytes != expected_bytes:
        raise SystemExit(
            f"Shard byte total {total_bytes} != manifest {expected_bytes}"
        )
    if total_records != expected_records:
        raise SystemExit(
            f"Shard record total {total_records} != manifest {expected_records}"
        )

    audit={
        "status":"PASS",
        "algorithm":"descending-size greedy bin packing; ties by shard index",
        "manifest":str(args.manifest),
        "manifest_sha256":sha256(args.manifest),
        "shards":args.shards,
        "files":len(normalized),
        "content_length":total_bytes,
        "record_count":total_records,
        "min_shard_bytes":min(x["content_length"] for x in rows),
        "max_shard_bytes":max(x["content_length"] for x in rows),
        "assignments":rows,
    }
    (args.output_dir/"SHARD_AUDIT.json").write_text(
        json.dumps(audit,indent=2)+"\n",encoding="utf-8"
    )
    print(json.dumps({
        k:v for k,v in audit.items() if k!="assignments"
    },indent=2))


if __name__=="__main__":
    main()

#!/usr/bin/env python3
"""Probe Harvard Dataverse metadata for the current BUNMD release."""
from __future__ import annotations
import json
import sys
from pathlib import Path

def walk_files(node):
    if isinstance(node, dict):
        if "dataFile" in node and isinstance(node["dataFile"], dict):
            yield node
        for v in node.values():
            yield from walk_files(v)
    elif isinstance(node, list):
        for v in node:
            yield from walk_files(v)

def main():
    src=Path(sys.argv[1])
    out=Path(sys.argv[2])
    obj=json.loads(src.read_text(encoding="utf-8"))
    files=[]
    seen=set()
    for item in walk_files(obj):
        df=item["dataFile"]
        fid=df.get("id")
        if fid in seen:
            continue
        seen.add(fid)
        files.append({
            "id": fid,
            "filename": df.get("filename"),
            "filesize": df.get("filesize"),
            "contentType": df.get("contentType"),
            "description": item.get("description") or df.get("description"),
            "directoryLabel": item.get("directoryLabel"),
            "persistentId": df.get("persistentId"),
            "md5": (df.get("checksum") or {}).get("value"),
        })
    files.sort(key=lambda x: (-(x.get("filesize") or 0), x.get("filename") or ""))
    payload={"status":obj.get("status"),"file_count":len(files),"files":files}
    out.write_text(json.dumps(payload,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
    print(f"BUNMD Dataverse files: {len(files)}")
    for f in files:
        size=f.get("filesize") or 0
        print(f"{f.get('id')}\t{size/1024/1024:.1f} MiB\t{f.get('filename')}\t{f.get('directoryLabel') or ''}")
if __name__=="__main__":
    main()

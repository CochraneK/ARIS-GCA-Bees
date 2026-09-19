#!/usr/bin/env python3
"""Merge manager first-pass adjudication patches into the frozen blank packet."""
from __future__ import annotations
import argparse,csv,json
from pathlib import Path

EDITABLE={
 "issue_family_codes","ground_truth_tier","required_artifact_roles",
 "content_detectability","adjudication_state","adjudication_notes",
}

def merge(rows,patches):
    by_id={r["feasibility_id"]:dict(r) for r in rows}
    seen=set()
    applied=[]
    for patch_file,items in patches:
        for item in items:
            fid=str(item.get("feasibility_id") or "")
            if not fid or fid not in by_id:
                raise ValueError(f"unknown feasibility_id:{fid}")
            if fid in seen:
                raise ValueError(f"duplicate patched feasibility_id:{fid}")
            extra=set(item)-({"feasibility_id"}|EDITABLE)
            if extra:
                raise ValueError(f"noneditable fields in patch {fid}:{sorted(extra)}")
            for k in EDITABLE:
                if k in item:
                    by_id[fid][k]=str(item[k])
            seen.add(fid)
            applied.append({"feasibility_id":fid,"patch_file":patch_file})
    return [by_id[r["feasibility_id"]] for r in rows],applied

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--packet",type=Path,required=True)
    p.add_argument("--patch",type=Path,action="append",default=[])
    p.add_argument("--output",type=Path,required=True)
    p.add_argument("--audit-output",type=Path,required=True)
    a=p.parse_args()
    with a.packet.open(newline="",encoding="utf-8") as f:
        rows=list(csv.DictReader(f))
    patches=[]
    for path in sorted(a.patch,key=lambda x:str(x)):
        x=json.loads(path.read_text(encoding="utf-8"))
        if x.get("state")!="MANAGER_FIRST_PASS_PATCH":
            raise ValueError(f"bad patch state:{path}")
        patches.append((str(path),x.get("records") or []))
    merged,applied=merge(rows,patches)
    a.output.parent.mkdir(parents=True,exist_ok=True)
    with a.output.open("w",newline="",encoding="utf-8") as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0]))
        w.writeheader()
        w.writerows(merged)
    counts={}
    for r in merged:
        s=r.get("adjudication_state","")
        counts[s]=counts.get(s,0)+1
    audit={
        "analysis":"ARIS4C011 manager first-pass patch merge",
        "source_packet_rows":len(rows),
        "patch_files":[p for p,_ in patches],
        "patched_record_count":len(applied),
        "state_counts":counts,
        "source_fields_modified":False,
        "confirmatory_eligibility_inferred":False,
        "applied":applied,
    }
    a.audit_output.write_text(json.dumps(audit,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    print(json.dumps({"patched":len(applied),"state_counts":counts},indent=2))

if __name__=="__main__":
    main()

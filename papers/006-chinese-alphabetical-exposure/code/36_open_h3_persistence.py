#!/usr/bin/env python3
"""ARIS4C006 — post-unlock Persistence5 opener.

Reads an already-passed outcome-blind H3 cohort. Refuses to query e+4/e+5
publication outcomes unless preregistration integrity and external unlock are
both valid and paper status is analysis/manuscript.
"""
from __future__ import annotations
import argparse,csv,json,os,subprocess,sys,time,urllib.parse,urllib.request
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
OA="https://api.openalex.org"
UA="ARIS4C006/0.36 Persistence5 opener"

def get_json(url,retries=5):
    req=urllib.request.Request(url,headers={"User-Agent":UA})
    for i in range(retries):
        try:
            with urllib.request.urlopen(req,timeout=75) as r:return json.loads(r.read().decode("utf-8"))
        except Exception:
            if i+1==retries:return None
            time.sleep(min(8,.8*(2**i)))
    return None

def verify_unlock():
    p=subprocess.run(
      [sys.executable,str(ROOT/"code"/"31_verify_prereg_lock.py"),"--require-unlock"],
      capture_output=True,text=True
    )
    if p.returncode!=0:raise SystemExit("LOCKED/INVALID PREREG STATE:\n"+p.stdout+"\n"+p.stderr)
    return json.loads((ROOT/"process"/"PREREGISTRATION_LOCK.json").read_text(encoding="utf-8"))

def read_csv(path):
    with Path(path).open(encoding="utf-8",newline="") as h:return list(csv.DictReader(h))

def write_csv(path,rows):
    path=Path(path);path.parent.mkdir(parents=True,exist_ok=True)
    with path.open("w",encoding="utf-8",newline="") as h:
        w=csv.DictWriter(h,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)

def persistence_count(aid,e):
    p={
      "filter":",".join([
        f"author.id:{aid}",
        "type:article|conference-paper",
        f"from_publication_date:{e+4}-01-01",
        f"to_publication_date:{e+5}-12-31",
      ]),
      "select":"id",
      "per_page":1,
    }
    if os.getenv("OPENALEX_API_KEY"):p["api_key"]=os.environ["OPENALEX_API_KEY"]
    d=get_json(OA+"/works?"+urllib.parse.urlencode(p,safe=":|"))
    if d is None:return None
    return int((d.get("meta") or {}).get("count") or 0)

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--cohort",required=True)
    ap.add_argument("--structural-manifest",required=True)
    ap.add_argument("--out",required=True)
    ap.add_argument("--manifest",required=True)
    a=ap.parse_args()
    lock=verify_unlock()
    sm=json.loads(Path(a.structural_manifest).read_text(encoding="utf-8"))
    if sm.get("h3_structural_gate_pass") is not True:
        raise SystemExit("H3 structural gate did not pass; outcome opening forbidden")
    if sm.get("persistence_outcome_computed") is not False:
        raise SystemExit("preoutcome manifest is not outcome-blind")

    rows=[r for r in read_csv(a.cohort) if int(r["final_h3_eligible_preoutcome"])==1]
    out=[];fail=0
    for i,r in enumerate(rows,1):
        e=int(r["entry_year"])
        cnt=persistence_count(r["canonical_author_id"],e)
        if cnt is None:
            fail+=1;continue
        q=dict(r)
        q["persistence5"]=int(cnt>=1)
        q["followup_eligible_work_count_e4_e5"]=cnt
        out.append(q)
        if i%100==0:print(f"opened persistence for {i}/{len(rows)} authors",flush=True)

    if not out:raise SystemExit("no persistence outcomes opened")
    write_csv(a.out,out)
    manifest={
      "script":"36_open_h3_persistence.py",
      "prereg_lock_label":lock.get("lock_label"),
      "prereg_lock_sha256":lock.get("combined_sha256"),
      "confirmatory_unlock_verified":True,
      "h3_structural_gate_pass":True,
      "authors_requested":len(rows),
      "authors_with_persistence_outcome":len(out),
      "outcome_query_failures":fail,
      "persistence_outcome_computed":True,
      "effect_or_pvalue_computed":False,
      "endpoint":"1 if >=1 eligible article/conference-paper in e+4 or e+5",
    }
    Path(a.manifest).parent.mkdir(parents=True,exist_ok=True)
    Path(a.manifest).write_text(json.dumps(manifest,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
    print(json.dumps(manifest,indent=2,ensure_ascii=False))

if __name__=="__main__":
    main()

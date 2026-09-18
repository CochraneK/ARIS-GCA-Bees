#!/usr/bin/env python3
"""ARIS4C006 — canonical Hanyu-Pinyin surname-map pilot.

Build a conservative romanized surname map from ChineseNames familyname rows,
using pypinyin 0.55.0 and ChineseNames' supplied initial as an internal check.
Then measure exact-map coverage among Crossref-structured CN-affiliated author
family names in an all-field random sample.

Primary mapping deliberately excludes unreviewed legacy/regional spellings.
"""
from __future__ import annotations
import argparse,csv,itertools,json,os,re,time,unicodedata,urllib.parse,urllib.request
from collections import defaultdict
from pathlib import Path
from pypinyin import lazy_pinyin,pinyin,Style

OA="https://api.openalex.org"
CR="https://api.crossref.org/works/"
UA="ARIS4C006/0.14 canonical-pinyin-surname-map"

def get(url,retries=4):
    req=urllib.request.Request(url,headers={"User-Agent":UA})
    for i in range(retries):
        try:
            with urllib.request.urlopen(req,timeout=60) as r:return json.loads(r.read().decode("utf-8"))
        except Exception:
            if i+1==retries:return None
            time.sleep(.5*(i+1))

def norm_latin(s):
    if not s:return ""
    s=unicodedata.normalize("NFKD",s)
    s="".join(c for c in s if not unicodedata.combining(c)).casefold()
    return re.sub(r"[^a-z]","",s)

def default_py(hanzi):
    return norm_latin("".join(lazy_pinyin(hanzi,style=Style.NORMAL,strict=False)))

def heteronym_candidates(hanzi,cap=200):
    syll=pinyin(hanzi,style=Style.NORMAL,heteronym=True,strict=False)
    options=[]
    for char_opts in syll:
        vals=[]
        for x in char_opts:
            nx=norm_latin(x)
            if nx and nx not in vals:vals.append(nx)
        options.append(vals or [""])
    out=[]
    for combo in itertools.product(*options):
        s="".join(combo)
        if s and s not in out:out.append(s)
        if len(out)>=cap:break
    return out

def build_map(path):
    rows=list(csv.DictReader(open(path,encoding="utf-8-sig")))
    accepted=[];unresolved=[]
    for r in rows:
        han=r["surname"];expected=(r["initial"] or "").lower();pop=int(float(r["n.1930_2008"]))
        d=default_py(han)
        method="default_initial_match";chosen=d
        if not d or d[0]!=expected:
            c=[x for x in heteronym_candidates(han) if x and x[0]==expected]
            if len(c)==1:
                chosen=c[0];method="unique_heteronym_initial_repair"
            else:
                unresolved.append({"surname":han,"compound":r["compound"],"expected_initial":expected,"default_pinyin":d,"matching_candidates":";".join(c),"population_n":pop,"reason":"no_unique_initial_consistent_pinyin"})
                continue
        accepted.append({"surname":han,"compound":int(r["compound"]),"romanized":chosen,"initial":expected,"population_n":pop,"ppm":float(r["ppm.1930_2008"]),"method":method})
    agg={}
    members=defaultdict(list)
    for r in accepted:
        k=r["romanized"];members[k].append(r)
    for k,rr in members.items():
        agg[k]={"romanized":k,"initial":k[0],"population_n":sum(x["population_n"] for x in rr),"chinese_surname_count":len(rr),"compound_member_count":sum(x["compound"] for x in rr),"members":";".join(x["surname"] for x in rr)}
    return rows,accepted,unresolved,list(agg.values())

def field_list():
    d=get(OA+"/fields?per_page=100")
    out=[]
    for x in (d or {}).get("results") or []:
        raw=str(x.get("id") or "").rstrip("/").split("/")[-1]
        m=re.search(r"(\d+)$",raw)
        if m:out.append((int(m.group(1)),x.get("display_name") or raw))
    return sorted(out)

def sample_field(fid,year,target):
    want=min(100,max(target*3,target+30));seed=int(f"{year}{fid:02d}14")
    p={"filter":",".join(["authorships.institutions.country_code:CN",f"primary_topic.field.id:{fid}",f"from_publication_date:{year}-01-01",f"to_publication_date:{year}-12-31"]),"select":"id,doi,authorships","sample":want,"seed":seed,"per_page":want}
    if os.getenv("OPENALEX_API_KEY"):p["api_key"]=os.environ["OPENALEX_API_KEY"]
    d=get(OA+"/works?"+urllib.parse.urlencode(p))
    if not d:return []
    return [w for w in (d.get("results") or []) if len(w.get("authorships") or [])>=2][:target]

def cr(doi_url):
    if not doi_url:return None
    doi=doi_url.removeprefix("https://doi.org/").removeprefix("http://doi.org/")
    d=get(CR+urllib.parse.quote(doi,safe=""))
    return (d or {}).get("message") or None

def is_cn(a):
    return any(i.get("country_code")=="CN" for i in (a.get("institutions") or [])) or "CN" in (a.get("countries") or [])

def write_csv(path,rows,fields=None):
    path.parent.mkdir(parents=True,exist_ok=True)
    if not rows:
        path.write_text("",encoding="utf-8");return
    with path.open("w",encoding="utf-8",newline="") as h:
        w=csv.DictWriter(h,fieldnames=fields or list(rows[0]));w.writeheader();w.writerows(rows)

def main():
    ap=argparse.ArgumentParser();ap.add_argument("familyname_csv");ap.add_argument("--year",type=int,default=2024);ap.add_argument("--per-field",type=int,default=10);ap.add_argument("--outdir",default="data/pilot/pinyin_map");a=ap.parse_args()
    raw,accepted,unresolved,agg=build_map(a.familyname_csv);keys={x["romanized"] for x in agg}
    field_rows=[];total_cn=total_mapped=0
    for fid,fname in field_list():
        cn=mapped=aligned=0
        for w in sample_field(fid,a.year,a.per_field):
            c=cr(w.get("doi"));oa=w.get("authorships") or [];ca=(c or {}).get("author") or []
            if not c or len(oa)!=len(ca):continue
            aligned+=1
            for o,cc in zip(oa,ca):
                if not is_cn(o):continue
                fam=norm_latin(cc.get("family"))
                if not fam:continue
                cn+=1
                if fam in keys:mapped+=1
            time.sleep(.02)
        total_cn+=cn;total_mapped+=mapped
        field_rows.append({"field_id":fid,"field_name":fname,"aligned_works":aligned,"cn_structured_family_rows":cn,"canonical_pinyin_mapped_rows":mapped,"mapping_rate":mapped/cn if cn else None})
        print(json.dumps(field_rows[-1],ensure_ascii=False))
    total_pop=sum(int(float(r["n.1930_2008"])) for r in raw);accepted_pop=sum(r["population_n"] for r in accepted)
    manifest={"script":"14_canonical_pinyin_surname_map.py","pypinyin_version":"0.55.0","confirmatory_use_allowed":False,"familyname_rows":len(raw),"accepted_surname_rows":len(accepted),"unresolved_surname_rows":len(unresolved),"accepted_row_rate":len(accepted)/len(raw),"population_coverage":accepted_pop/total_pop if total_pop else None,"canonical_romanized_forms":len(agg),"compound_rows_total":sum(int(r["compound"]) for r in raw),"compound_rows_accepted":sum(r["compound"] for r in accepted),"sample_year":a.year,"cn_structured_family_rows_sample":total_cn,"canonical_pinyin_mapped_rows_sample":total_mapped,"canonical_mapping_coverage_sample":total_mapped/total_cn if total_cn else None,"primary_rule":"Only direct Han or exact canonical Hanyu-Pinyin matches are confirmatory focal ChineseNames-mappable surname forms; legacy/regional variants require separate reviewed mapping.","privacy":"Only public surname dictionary derivatives and aggregate bibliographic coverage are persisted; sampled person names are not written."}
    out=Path(a.outdir);write_csv(out/"romanization_population_map.csv",sorted(agg,key=lambda x:(-x["population_n"],x["romanized"])));write_csv(out/"unresolved_surnames.csv",unresolved);write_csv(out/"field_mapping_coverage.csv",field_rows);(out/"manifest.json").write_text(json.dumps(manifest,indent=2,ensure_ascii=False)+"\n",encoding="utf-8");print(json.dumps(manifest,indent=2,ensure_ascii=False))
if __name__=="__main__":main()

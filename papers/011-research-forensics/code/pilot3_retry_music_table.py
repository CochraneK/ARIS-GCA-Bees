"""Bounded retry for unresolved PLOS t002/t003 historical table objects."""
from __future__ import annotations
import hashlib,json,time
from pathlib import Path
from urllib.request import Request,urlopen
from urllib.error import URLError,HTTPError
from wayback_discovery import discover
from artifact_safety import assess_track_a_artifact

DOI="10.1371/journal.pone.0293412"
EVENT="2025-01-03"

def fetch(url,retries=4):
    last=None
    for i in range(retries):
        try:
            with urlopen(Request(url,headers={"User-Agent":"ARIS4C011-Research-Forensics/0.3"}),timeout=60) as r:
                return r.read()
        except (URLError,HTTPError,TimeoutError) as e:
            last=e; time.sleep(min(8,2**i))
    raise RuntimeError(str(last))

def probe(tid):
    original=f"https://journals.plos.org/plosone/article/figure?id={DOI}.{tid}"
    try:
        recs=discover(original,event_date=EVENT,identity_marker=f"{DOI}.{tid}",timeout=60)
    except Exception as exc:
        return {"table_id":tid,"qualification":"BLOCKED","reason":[f"cdx:{type(exc).__name__}:{exc}"]}
    if not recs:
        return {"table_id":tid,"qualification":"BLOCKED","reason":["no exact pre-correction capture"]}
    rec=recs[0]
    replay=f"https://web.archive.org/web/{rec.timestamp}id_/{rec.original}"
    try:
        body=fetch(replay)
    except Exception as exc:
        return {"table_id":tid,"capture_timestamp":rec.timestamp,"qualification":"BLOCKED","reason":[f"replay:{type(exc).__name__}:{exc}"]}
    text=body.decode("utf-8","replace"); low=text.lower()
    markers={"mexico":"mexico" in low,"other":"other" in low}
    q=assess_track_a_artifact(
        artifact_version_date=f"{rec.timestamp[:4]}-{rec.timestamp[4:6]}-{rec.timestamp[6:8]}",
        outcome_date=EVENT,
        immutable_or_historical_snapshot=True,
        historical_equivalence="archive_snapshot_of_published_version",
        provenance_source="Internet Archive Wayback CDX + replay",
        filename_or_path=rec.original,
        leading_text=text[:6000],
        current_metadata_has_update_relation=True,
    )
    safe=q.status=="SAFE_EXACT" and all(markers.values())
    return {
        "table_id":tid,"capture_timestamp":rec.timestamp,"cdx_digest":rec.digest,
        "original_url":rec.original,"replay_url":replay,"retrieved_bytes":len(body),
        "retrieved_sha256":hashlib.sha256(body).hexdigest(),"markers":markers,
        "generic_status":q.status,"qualification":"SAFE_EXACT" if safe else "BLOCKED",
        "track_a_eligible":safe,
        "reason":[] if safe else ["target Mexico/Other content markers not both verified"],
    }

def main():
    rows=[probe("t002"),probe("t003")]
    result={"target_doi":DOI,"required_role":"table","bounded_retry":True,
            "rows":rows,"safe_exact_matches":[r["table_id"] for r in rows if r.get("track_a_eligible")]}
    out=Path(__file__).resolve().parents[1]/"data/results/pilot3_music_table_retry.json"
    out.write_text(json.dumps(result,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    print(json.dumps(result,ensure_ascii=False,indent=2))
if __name__=="__main__": main()

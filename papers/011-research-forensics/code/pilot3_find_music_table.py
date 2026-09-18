"""Locate the exact historical PLOS table object carrying the corrected fields.

Scans t001..t006 for pre-correction captures of the target PLOS article and
checks replay content for both 'Mexico' and 'Other'. Discovery and content
identity must agree before any SAFE_EXACT upgrade is considered.
"""
from __future__ import annotations
import hashlib,json,time
from pathlib import Path
from urllib.request import Request,urlopen
from urllib.error import URLError,HTTPError

from wayback_discovery import discover
from artifact_safety import assess_track_a_artifact

DOI="10.1371/journal.pone.0293412"
EVENT="2025-01-03"

def fetch(url,retries=3):
    last=None
    for i in range(retries):
        try:
            with urlopen(Request(url,headers={"User-Agent":"ARIS4C011-Research-Forensics/0.3"}),timeout=30) as r:
                return r.read()
        except (URLError,HTTPError,TimeoutError) as e:
            last=e; time.sleep(2**i)
    raise RuntimeError(str(last))

def main():
    rows=[]
    for n in range(1,7):
        tid=f"t{n:03d}"
        original=f"https://journals.plos.org/plosone/article/figure?id={DOI}.{tid}"
        try:
            recs=discover(original,event_date=EVENT,identity_marker=f"{DOI}.{tid}",timeout=30)
        except Exception as exc:
            rows.append({"table_id":tid,"capture_n":0,"error":f"{type(exc).__name__}:{exc}"})
            continue
        row={"table_id":tid,"original_url":original,"capture_n":len(recs),"error":""}
        if recs:
            rec=recs[0]
            replay=f"https://web.archive.org/web/{rec.timestamp}id_/{rec.original}"
            try:
                body=fetch(replay)
                text=body.decode("utf-8","replace")
                low=text.lower()
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
                row.update({
                    "capture_timestamp":rec.timestamp,
                    "cdx_digest":rec.digest,
                    "replay_url":replay,
                    "retrieved_sha256":hashlib.sha256(body).hexdigest(),
                    "retrieved_bytes":len(body),
                    "markers":markers,
                    "content_target_match":all(markers.values()),
                    "generic_status":q.status,
                    "safe_exact_target":q.status=="SAFE_EXACT" and all(markers.values()),
                })
            except Exception as exc:
                row["replay_error"]=f"{type(exc).__name__}:{exc}"
        rows.append(row)
    matches=[r for r in rows if r.get("safe_exact_target")]
    result={
        "target_doi":DOI,
        "correction_date":EVENT,
        "required_role":"table",
        "tables_scanned":6,
        "safe_exact_target_matches":len(matches),
        "matching_table_ids":[r["table_id"] for r in matches],
        "rows":rows,
    }
    out=Path(__file__).resolve().parents[1]/"data/results/pilot3_music_table_object_scan.json"
    out.write_text(json.dumps(result,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    print(json.dumps(result,ensure_ascii=False,indent=2))

if __name__=="__main__":
    main()

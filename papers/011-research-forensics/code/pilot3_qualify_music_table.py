"""Qualify the exact historical PLOS Table 1 object for ARIS4C011 Pilot 3.

This is intentionally case-specific. It upgrades only if:
- exact t001 publisher object has a pre-correction Wayback capture;
- replay bytes are retrievable;
- target DOI/table identity is visible;
- expected table content markers are present;
- the generic Track-A historical-safety gate returns SAFE_EXACT.
"""
from __future__ import annotations

import argparse, hashlib, json, time, unicodedata
from pathlib import Path
from urllib.request import Request, urlopen
from urllib.error import URLError, HTTPError

from artifact_safety import assess_track_a_artifact
from wayback_discovery import discover


def fetch(url: str, retries: int=3) -> bytes:
    last=None
    for i in range(retries):
        try:
            req=Request(url,headers={"User-Agent":"ARIS4C011-Research-Forensics/0.3"})
            with urlopen(req,timeout=30) as r:
                return r.read()
        except (URLError,HTTPError,TimeoutError) as exc:
            last=exc
            time.sleep(2**i)
    raise RuntimeError(str(last))


def main():
    p=argparse.ArgumentParser()
    p.add_argument("--output",type=Path,required=True)
    a=p.parse_args()

    doi="10.1371/journal.pone.0293412"
    correction_date="2025-01-03"
    original=f"https://journals.plos.org/plosone/article/figure?id={doi}.t001"
    records=discover(
        original,
        event_date=correction_date,
        identity_marker=f"{doi}.t001",
        timeout=30,
    )
    result={
        "target_doi":doi,
        "required_role":"table",
        "object_id":"t001",
        "original_url":original,
        "correction_date":correction_date,
        "discovery_capture_n":len(records),
        "qualification":"BLOCKED",
        "track_a_eligible":False,
        "reason":[],
    }
    if not records:
        result["reason"].append("no exact pre-correction t001 capture discovered")
    else:
        rec=records[0]
        replay=f"https://web.archive.org/web/{rec.timestamp}id_/{rec.original}"
        try:
            body=fetch(replay)
            text=body.decode("utf-8","replace")
            low=text.lower()
            folded="".join(
                ch for ch in unicodedata.normalize("NFKD", low)
                if not unicodedata.combining(ch)
            )
            identity_ok=(doi.lower() in folded or f"journal.pone.0293412.t001" in folded)
            content_markers={
                "table_title":"countries of residence" in folded,
                "survey_1":"survey 1" in folded,
                "mexico":"mexico" in folded,
                "other":"other" in folded,
            }
            content_ok=all(content_markers.values())
            q=assess_track_a_artifact(
                artifact_version_date=f"{rec.timestamp[0:4]}-{rec.timestamp[4:6]}-{rec.timestamp[6:8]}",
                outcome_date=correction_date,
                immutable_or_historical_snapshot=True,
                historical_equivalence="archive_snapshot_of_published_version",
                provenance_source="Internet Archive Wayback CDX + replay",
                title="",
                filename_or_path=rec.original,
                leading_text=text[:6000],
                current_metadata_has_update_relation=True,
            )
            safe=(q.status=="SAFE_EXACT" and identity_ok and content_ok)
            result.update({
                "capture_timestamp":rec.timestamp,
                "capture_digest_cdx":rec.digest,
                "replay_url":replay,
                "retrieved_sha256":hashlib.sha256(body).hexdigest(),
                "retrieved_bytes":len(body),
                "identity_ok":identity_ok,
                "content_markers":content_markers,
                "generic_artifact_qualification":q.to_dict(),
                "qualification":"SAFE_EXACT" if safe else "BLOCKED",
                "track_a_eligible":safe,
            })
            if not identity_ok:
                result["reason"].append("target DOI/table identity not verified in replay content")
            if not content_ok:
                result["reason"].append("expected Table 1 content markers not both present")
            if q.status!="SAFE_EXACT":
                result["reason"].extend(q.reasons)
        except Exception as exc:
            result["reason"].append(f"replay_retrieval_failed:{type(exc).__name__}:{exc}")

    a.output.parent.mkdir(parents=True,exist_ok=True)
    a.output.write_text(json.dumps(result,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    print(json.dumps(result,ensure_ascii=False,indent=2))


if __name__=="__main__":
    main()

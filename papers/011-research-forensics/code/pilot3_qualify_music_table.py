"""Qualify the exact historical PLOS Table 1 object for ARIS4C011 Pilot 3.

Two gates are deliberately separated:
1. artifact provenance/time-safety (SAFE_EXACT / BLOCKED);
2. scientific-content extraction/detection (a later F3 step).

A historical table image can therefore be SAFE_EXACT even before its cells have
been parsed. This avoids confusing "not yet extracted" with "not historical".
"""
from __future__ import annotations

import argparse
import hashlib
import json
import time
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

from artifact_safety import assess_track_a_artifact
from wayback_discovery import discover


DOI="10.1371/journal.pone.0293412"
CORRECTION_DATE="2025-01-03"
WRAPPER_URL=f"https://journals.plos.org/plosone/article/figure?id={DOI}.t001"
WRAPPER_TIMESTAMP="20240520012147"
WRAPPER_DIGEST="JLJFGD45MKV3MXK5F65FHV3MNXYNBD7Y"

IMAGE_CANDIDATES=(
    f"https://journals.plos.org/plosone/article/figure/image?size=inline&id={DOI}.t001",
    f"https://journals.plos.org/plosone/article/figure/image?size=large&id={DOI}.t001",
    f"https://journals.plos.org/plosone/article/figure/image?download&size=original&id={DOI}.t001",
)


def fetch(url: str, retries: int=4, timeout: int=30) -> bytes:
    last=None
    for i in range(retries):
        try:
            req=Request(url,headers={"User-Agent":"ARIS4C011-Research-Forensics/0.4"})
            with urlopen(req,timeout=timeout) as r:
                return r.read()
        except (URLError,HTTPError,TimeoutError) as exc:
            last=exc
            time.sleep(min(2**i,8))
    raise RuntimeError(str(last))


def discover_retry(url: str, retries: int=4):
    last=None
    for i in range(retries):
        try:
            return discover(
                url,
                event_date=CORRECTION_DATE,
                identity_marker=f"{DOI}.t001",
                timeout=30,
            )
        except Exception as exc:
            last=exc
            time.sleep(min(2**i,8))
    return [], f"{type(last).__name__}:{last}"


def image_kind(data: bytes) -> str | None:
    if data.startswith(b"\x89PNG\r\n\x1a\n"):
        return "image/png"
    if data.startswith((b"II*\x00",b"MM\x00*")):
        return "image/tiff"
    if data[:3]==b"\xff\xd8\xff":
        return "image/jpeg"
    return None


def main():
    p=argparse.ArgumentParser()
    p.add_argument("--output",type=Path,required=True)
    args=p.parse_args()

    wrapper_replay=f"https://web.archive.org/web/{WRAPPER_TIMESTAMP}id_/{WRAPPER_URL}"
    result={
        "target_doi":DOI,
        "required_role":"table",
        "object_id":"t001",
        "correction_date":CORRECTION_DATE,
        "qualification":"BLOCKED",
        "track_a_eligible":False,
        "content_extraction_status":"NOT_STARTED",
        "reason":[],
        "wrapper":{
            "url":WRAPPER_URL,
            "timestamp":WRAPPER_TIMESTAMP,
            "cdx_digest":WRAPPER_DIGEST,
            "source_run":35407336466,
        },
        "image_candidate_queries":[],
    }

    try:
        wrapper=fetch(wrapper_replay)
        wq=assess_track_a_artifact(
            artifact_version_date="2024-05-20",
            outcome_date=CORRECTION_DATE,
            immutable_or_historical_snapshot=True,
            historical_equivalence="archive_snapshot_of_published_version",
            provenance_source="Internet Archive Wayback CDX + replay",
            title="",
            filename_or_path=WRAPPER_URL,
            leading_text=wrapper[:6000].decode("utf-8","replace"),
            current_metadata_has_update_relation=True,
        )
        result["wrapper"].update({
            "replay_url":wrapper_replay,
            "retrieved_sha256":hashlib.sha256(wrapper).hexdigest(),
            "retrieved_bytes":len(wrapper),
            "qualification":wq.to_dict(),
        })
        if wq.status!="SAFE_EXACT":
            result["reason"].append("historical table wrapper failed generic time-safety gate")
    except Exception as exc:
        result["reason"].append(f"wrapper_replay_failed:{type(exc).__name__}:{exc}")
        wq=None

    safe_images=[]
    for original in IMAGE_CANDIDATES:
        records,error=discover_retry(original)
        qrow={
            "original_url":original,
            "capture_n":len(records),
            "discovery_error":error if isinstance(error,str) else "",
            "captures":[],
        }
        for rec in records:
            replay=f"https://web.archive.org/web/{rec.timestamp}id_/{rec.original}"
            item={
                "timestamp":rec.timestamp,
                "cdx_digest":rec.digest,
                "mimetype":rec.mimetype,
                "original":rec.original,
                "replay_url":replay,
            }
            try:
                data=fetch(replay)
                kind=image_kind(data)
                aq=assess_track_a_artifact(
                    artifact_version_date=f"{rec.timestamp[:4]}-{rec.timestamp[4:6]}-{rec.timestamp[6:8]}",
                    outcome_date=CORRECTION_DATE,
                    immutable_or_historical_snapshot=True,
                    historical_equivalence="archive_snapshot_of_published_version",
                    provenance_source="Internet Archive Wayback CDX + replay",
                    title="",
                    filename_or_path=rec.original,
                    leading_text="",
                    current_metadata_has_update_relation=True,
                )
                identity_ok=(f"{DOI}.t001" in rec.original)
                image_ok=(kind is not None and len(data)>=1000)
                safe=(aq.status=="SAFE_EXACT" and identity_ok and image_ok)
                item.update({
                    "retrieved_sha256":hashlib.sha256(data).hexdigest(),
                    "retrieved_bytes":len(data),
                    "detected_mime":kind,
                    "identity_ok":identity_ok,
                    "generic_artifact_qualification":aq.to_dict(),
                    "safe_exact_table_image":safe,
                })
                if safe:
                    safe_images.append(item)
            except Exception as exc:
                item["replay_error"]=f"{type(exc).__name__}:{exc}"
            qrow["captures"].append(item)
        result["image_candidate_queries"].append(qrow)

    if wq is not None and wq.status=="SAFE_EXACT" and safe_images:
        chosen=sorted(safe_images,key=lambda x:x["timestamp"])[0]
        result.update({
            "qualification":"SAFE_EXACT",
            "track_a_eligible":True,
            "content_extraction_status":"PENDING_IMAGE_TABLE_EXTRACTION",
            "selected_table_image":chosen,
        })
    else:
        if not safe_images:
            result["reason"].append("no independently verified pre-correction table image object found")

    args.output.parent.mkdir(parents=True,exist_ok=True)
    args.output.write_text(json.dumps(result,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    print(json.dumps({
        "qualification":result["qualification"],
        "track_a_eligible":result["track_a_eligible"],
        "content_extraction_status":result["content_extraction_status"],
        "safe_image_n":len(safe_images),
        "reasons":result["reason"],
    },indent=2))


if __name__=="__main__":
    main()

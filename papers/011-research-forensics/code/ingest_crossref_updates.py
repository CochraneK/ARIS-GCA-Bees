"""Normalize Crossref update relations for ARIS4C011.

Crossref's update-type queries can return either a separate retraction/correction
notice work whose `update-to` relation points to the affected article, or a work
whose update relation points to itself. Therefore the top-level work DOI/title
must never be assumed to be metadata for the affected paper.

Input: Crossref REST JSON response with message.items[*].update-to
Output: one assertion row per update-to relation.

This module preserves assertion source (publisher vs retraction-watch) instead
of collapsing it prematurely. Multiple assertions can describe one event.
"""

from __future__ import annotations

import csv
import hashlib
import json
from pathlib import Path
import sys
from typing import Any, Dict, Iterable, List


def normalize_doi(value: str) -> str:
    value = (value or "").strip().lower()
    for prefix in ("https://doi.org/", "http://doi.org/", "doi:"):
        if value.startswith(prefix):
            value = value[len(prefix):].strip()
    return value


def date_parts_to_iso(obj: Dict[str, Any] | None) -> str:
    if not obj:
        return ""
    parts = obj.get("date-parts") or []
    if not parts or not parts[0]:
        return ""
    vals = list(parts[0])
    y = vals[0]
    m = vals[1] if len(vals) > 1 else 1
    d = vals[2] if len(vals) > 2 else 1
    return f"{int(y):04d}-{int(m):02d}-{int(d):02d}"


def first_text(value: Any) -> str:
    if isinstance(value, list):
        return str(value[0]) if value else ""
    return str(value or "")


def stable_key(*parts: str) -> str:
    raw = "\x1f".join(parts).encode("utf-8")
    return hashlib.sha256(raw).hexdigest()[:20]


def extract_assertions(payload: Dict[str, Any]) -> List[Dict[str, str]]:
    items = ((payload or {}).get("message") or {}).get("items") or []
    out: List[Dict[str, str]] = []

    for item in items:
        source_work_doi = normalize_doi(item.get("DOI", ""))
        source_title = first_text(item.get("title"))
        source_journal = first_text(item.get("container-title"))
        source_published = date_parts_to_iso(item.get("published"))

        for rel in item.get("update-to") or []:
            target_doi = normalize_doi(rel.get("DOI", ""))
            relation_type = str(rel.get("type") or "").strip().lower()
            assertion_source = str(rel.get("source") or "").strip().lower()
            update_date = date_parts_to_iso(rel.get("updated"))
            record_id = str(rel.get("record-id") or "").strip()

            if not target_doi or not relation_type:
                continue

            notice_doi = source_work_doi if source_work_doi != target_doi else ""
            event_key = stable_key(target_doi, relation_type, update_date)
            assertion_key = stable_key(
                target_doi, relation_type, update_date,
                assertion_source, record_id, source_work_doi,
            )

            out.append({
                "assertion_key": assertion_key,
                "event_key": event_key,
                "crossref_source_work_doi": source_work_doi,
                "notice_doi": notice_doi,
                "target_doi": target_doi,
                "relation_type": relation_type,
                "relation_label": str(rel.get("label") or "").strip(),
                "assertion_source": assertion_source,
                "update_date": update_date,
                "retraction_watch_record_id": record_id,
                "source_work_title": source_title,
                "source_work_journal": source_journal,
                "source_work_published": source_published,
                "target_metadata_resolved": "0",
            })
    return out


def event_summary(rows: Iterable[Dict[str, str]]) -> List[Dict[str, str]]:
    """Collapse assertion rows only for event-level inventory, not provenance."""
    grouped: Dict[str, List[Dict[str, str]]] = {}
    for row in rows:
        grouped.setdefault(row["event_key"], []).append(row)

    out = []
    for event_key, members in grouped.items():
        first = members[0]
        out.append({
            "event_key": event_key,
            "target_doi": first["target_doi"],
            "relation_type": first["relation_type"],
            "update_date": first["update_date"],
            "assertion_count": str(len(members)),
            "assertion_sources": ";".join(
                sorted({m["assertion_source"] for m in members if m["assertion_source"]})
            ),
            "retraction_watch_record_ids": ";".join(
                sorted({m["retraction_watch_record_id"] for m in members if m["retraction_watch_record_id"]})
            ),
        })
    return sorted(out, key=lambda x: (x["target_doi"], x["relation_type"], x["update_date"]))


def write_csv(path: Path, rows: List[Dict[str, str]]) -> None:
    if not rows:
        path.write_text("", encoding="utf-8")
        return
    fields = list(rows[0].keys())
    with path.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        w.writerows(rows)


def main(argv: List[str]) -> int:
    if len(argv) != 3:
        print("Usage: python ingest_crossref_updates.py input.json out_dir", file=sys.stderr)
        return 2
    src = Path(argv[1])
    out = Path(argv[2])
    out.mkdir(parents=True, exist_ok=True)

    payload = json.loads(src.read_text(encoding="utf-8"))
    assertions = extract_assertions(payload)
    events = event_summary(assertions)

    write_csv(out / "crossref_update_assertions.csv", assertions)
    write_csv(out / "crossref_update_events.csv", events)

    meta = {
        "source_file": src.name,
        "assertion_rows": len(assertions),
        "event_rows": len(events),
        "warning": (
            "Top-level Crossref work metadata describes the source/update work, "
            "not necessarily the target article. Resolve target_doi metadata separately."
        ),
    }
    (out / "crossref_update_meta.json").write_text(
        json.dumps(meta, indent=2) + "\n", encoding="utf-8"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))

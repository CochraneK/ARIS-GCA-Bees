"""Wayback/CDX discovery helpers for ARIS4C011 historical artifacts.

Discovery is not qualification. A CDX hit is only a candidate historical
object. It still needs identity checking, content/version verification, and
the artifact-safety gate before entering Track A.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import date, timedelta
import json
from typing import Iterable, List, Optional
from urllib.parse import urlencode
from urllib.request import Request, urlopen


CDX_ENDPOINT = "https://web.archive.org/cdx/search/cdx"


@dataclass(frozen=True)
class CdxRecord:
    timestamp: str
    original: str
    digest: str
    statuscode: str = "200"
    mimetype: str = ""

    @property
    def capture_date(self) -> date:
        return date(
            int(self.timestamp[0:4]),
            int(self.timestamp[4:6]),
            int(self.timestamp[6:8]),
        )


def build_cdx_url(
    original_url: str,
    *,
    event_date: str,
    from_year: Optional[int] = None,
    include_mimetype: bool = True,
) -> str:
    """Build a fail-closed CDX query ending on the day before the event."""
    event = date.fromisoformat(event_date[:10])
    cutoff = event - timedelta(days=1)
    fields = ["timestamp", "original", "digest", "statuscode"]
    if include_mimetype:
        fields.append("mimetype")

    params = {
        "url": original_url,
        "output": "json",
        "filter": "statuscode:200",
        "to": cutoff.strftime("%Y%m%d"),
        "fl": ",".join(fields),
        "collapse": "digest",
    }
    if from_year is not None:
        params["from"] = str(int(from_year))
    return CDX_ENDPOINT + "?" + urlencode(params)


def parse_cdx_json(payload: str) -> List[CdxRecord]:
    data = json.loads(payload)
    if not data:
        return []
    header = data[0]
    records: List[CdxRecord] = []
    for row in data[1:]:
        item = dict(zip(header, row))
        records.append(CdxRecord(
            timestamp=str(item.get("timestamp", "")),
            original=str(item.get("original", "")),
            digest=str(item.get("digest", "")),
            statuscode=str(item.get("statuscode", "")),
            mimetype=str(item.get("mimetype", "")),
        ))
    return records


def filter_identity(
    records: Iterable[CdxRecord],
    identity_marker: Optional[str],
) -> List[CdxRecord]:
    """Filter wildcard collisions using a target-specific URL marker.

    A prefix wildcard can return a neighboring article whose identifier merely
    starts with the target identifier. For example, a search around 54_1_1 can
    also return 54_1_101, 54_1_107, or 54_1_13.
    """
    if not identity_marker:
        return list(records)
    marker = str(identity_marker)
    return [record for record in records if marker in record.original]


def pre_event_records(
    records: Iterable[CdxRecord],
    event_date: str,
) -> List[CdxRecord]:
    """Return only status-200 captures strictly earlier than the event date."""
    event = date.fromisoformat(event_date[:10])
    valid = [
        r for r in records
        if len(r.timestamp) >= 8
        and r.statuscode == "200"
        and r.capture_date < event
    ]
    return sorted(valid, key=lambda r: r.timestamp)


def discover(
    original_url: str,
    *,
    event_date: str,
    from_year: Optional[int] = None,
    identity_marker: Optional[str] = None,
    timeout: int = 20,
) -> List[CdxRecord]:
    """Perform live CDX discovery and conservative identity/time filtering."""
    url = build_cdx_url(
        original_url,
        event_date=event_date,
        from_year=from_year,
    )
    req = Request(url, headers={"User-Agent": "ARIS4C011-Research-Forensics/0.2"})
    with urlopen(req, timeout=timeout) as response:
        payload = response.read().decode("utf-8")
    records = parse_cdx_json(payload)
    records = filter_identity(records, identity_marker)
    return pre_event_records(records, event_date)

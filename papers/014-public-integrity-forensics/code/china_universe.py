"""Official China institution-universe seed adapters for OpenIntegrity.

Universe membership is a routing/provenance fact, never a risk signal.
Only organization names and official source provenance are retained here.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
from datetime import datetime
from hashlib import sha256
from html.parser import HTMLParser
import json
import re

from china_scope import InstitutionType


SASAC_CENTRAL_SOE_URL = (
    "https://wap.sasac.gov.cn/n2588045/n27271785/n27271792/c14159097/content.html"
)
CAS_RESEARCH_UNITS_URL = "https://www.cas.cn/zz/jg/ys/yj/"


@dataclass(frozen=True)
class InstitutionSeed:
    name: str
    institution_type: str
    source_name: str
    source_url: str
    source_tier: str = "CN-A"
    corruption_inference: bool = False


@dataclass(frozen=True)
class UniverseSnapshot:
    source_url: str
    retrieved_at: str
    html_sha256: str
    seeds: tuple[InstitutionSeed, ...]
    warnings: tuple[str, ...] = ()

    def as_json(self) -> dict:
        return {
            "source_url": self.source_url,
            "retrieved_at": self.retrieved_at,
            "html_sha256": self.html_sha256,
            "warnings": list(self.warnings),
            "seeds": [asdict(x) for x in self.seeds],
        }


class _TextCellParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self._tag: str | None = None
        self._buf: list[str] = []
        self.cells: list[str] = []
        self.anchor_texts: list[str] = []

    def handle_starttag(self, tag: str, attrs) -> None:
        low = tag.lower()
        if low in {"td", "th", "a"}:
            self._tag = low
            self._buf = []

    def handle_data(self, data: str) -> None:
        if self._tag:
            self._buf.append(data)

    def handle_endtag(self, tag: str) -> None:
        low = tag.lower()
        if self._tag == low:
            text = " ".join("".join(self._buf).split()).strip()
            if text:
                if low in {"td", "th"}:
                    self.cells.append(text)
                if low == "a":
                    self.anchor_texts.append(text)
            self._tag = None
            self._buf = []


def _clean_name(value: str) -> str:
    return re.sub(r"^\s*\d+[、.．]?\s*", "", value).strip()


def parse_sasac_central_soe(html: str, *, retrieved_at: str) -> UniverseSnapshot:
    parser = _TextCellParser()
    parser.feed(html)

    candidates: list[str] = []
    for text in parser.cells + parser.anchor_texts:
        n = _clean_name(text)
        if not n or len(n) > 80:
            continue
        if any(
            n.endswith(s)
            for s in (
                "集团有限公司",
                "有限责任公司",
                "有限公司",
            )
        ):
            candidates.append(n)

    # Some SASAC table layouts place multiple numbered names in one cell.
    all_text = " ".join(parser.cells)
    for m in re.finditer(
        r"(?:^|\s)\d{1,3}\s+([^\d]{2,80}?(?:集团有限公司|有限责任公司|有限公司))(?=\s+\d{1,3}\s+|$)",
        all_text,
    ):
        candidates.append(_clean_name(m.group(1)))

    names = tuple(dict.fromkeys(candidates))
    warnings: list[str] = []
    if not names:
        warnings.append("no_central_soe_names_parsed")

    seeds = tuple(
        InstitutionSeed(
            name=n,
            institution_type=InstitutionType.SOE.value,
            source_name="国务院国资委央企名录",
            source_url=SASAC_CENTRAL_SOE_URL,
        )
        for n in names
    )
    return UniverseSnapshot(
        source_url=SASAC_CENTRAL_SOE_URL,
        retrieved_at=retrieved_at,
        html_sha256=sha256(html.encode("utf-8")).hexdigest(),
        seeds=seeds,
        warnings=tuple(warnings),
    )


_CAS_RESEARCH_SUFFIXES = (
    "研究所",
    "研究院",
    "研究中心",
    "科学中心",
    "国家天文台",
    "天文台",
    "植物园",
)


def parse_cas_research_units(html: str, *, retrieved_at: str) -> UniverseSnapshot:
    parser = _TextCellParser()
    parser.feed(html)
    candidates: list[str] = []
    for text in parser.anchor_texts + parser.cells:
        n = _clean_name(text).lstrip("*").strip()
        if not n or len(n) > 80:
            continue
        if any(n.endswith(s) for s in _CAS_RESEARCH_SUFFIXES):
            # Navigation labels like "研究单位" are intentionally excluded.
            if n in {"研究单位", "研究中心"}:
                continue
            candidates.append(n)

    # Fallback for official pages that render the institute list as plain text
    # rather than links/cells.
    if not candidates:
        all_text = re.sub(r"\s+", " ", html)
        for m in re.finditer(
            r"([\u4e00-\u9fffA-Za-z0-9（）()·\-]{2,40}(?:研究所|研究院|研究中心|科学中心|天文台|植物园))",
            all_text,
        ):
            n = m.group(1).lstrip("*").strip()
            if n not in {"研究单位", "研究中心"}:
                candidates.append(n)

    names = tuple(dict.fromkeys(candidates))
    warnings: list[str] = []
    if not names:
        warnings.append("no_cas_research_units_parsed")

    seeds = tuple(
        InstitutionSeed(
            name=(
                n
                if n.startswith("中国科学院")
                else f"中国科学院{n}"
            ),
            institution_type=InstitutionType.RESEARCH_INSTITUTE.value,
            source_name="中国科学院院属研究单位",
            source_url=CAS_RESEARCH_UNITS_URL,
        )
        for n in names
    )
    return UniverseSnapshot(
        source_url=CAS_RESEARCH_UNITS_URL,
        retrieved_at=retrieved_at,
        html_sha256=sha256(html.encode("utf-8")).hexdigest(),
        seeds=seeds,
        warnings=tuple(warnings),
    )


def _fetch_verified(url: str, *, timeout: float = 20.0) -> str:
    """Fetch with Requests/certifi in live workflows; TLS verification stays on."""
    import requests

    resp = requests.get(
        url,
        timeout=timeout,
        headers={
            "User-Agent": "OpenIntegrity-ARIS4C014/0.1 (+public-data feasibility research)"
        },
    )
    resp.raise_for_status()
    if not resp.encoding or resp.encoding.lower() == "iso-8859-1":
        resp.encoding = resp.apparent_encoding or "utf-8"
    return resp.text


def fetch_live_universes() -> list[UniverseSnapshot]:
    now = datetime.now().astimezone().isoformat()
    sasac_html = _fetch_verified(SASAC_CENTRAL_SOE_URL)
    cas_html = _fetch_verified(CAS_RESEARCH_UNITS_URL)
    return [
        parse_sasac_central_soe(sasac_html, retrieved_at=now),
        parse_cas_research_units(cas_html, retrieved_at=now),
    ]


def dump_universe_report(snapshots: list[UniverseSnapshot]) -> str:
    return json.dumps(
        {
            "snapshots": [x.as_json() for x in snapshots],
            "aggregate": {
                "sources": len(snapshots),
                "organization_seeds": sum(len(x.seeds) for x in snapshots),
                "by_type": {
                    kind: sum(
                        1
                        for x in snapshots
                        for s in x.seeds
                        if s.institution_type == kind
                    )
                    for kind in sorted(
                        {
                            s.institution_type
                            for x in snapshots
                            for s in x.seeds
                        }
                    )
                },
                "corruption_inference": False,
                "interpretation": (
                    "Official organization-universe provenance only; "
                    "membership is not an integrity-risk signal."
                ),
            },
        },
        ensure_ascii=False,
        indent=2,
    ) + "\n"

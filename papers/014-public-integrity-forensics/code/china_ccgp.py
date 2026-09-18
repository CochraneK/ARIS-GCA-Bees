"""Bounded China Government Procurement Network (CCGP) discovery utilities.

This module is intentionally conservative:
- list-page discovery only;
- no authentication bypass or CAPTCHA handling;
- no personal contact extraction;
- no corruption scoring;
- institution classification is a routing heuristic, not a risk signal.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
from datetime import datetime
from hashlib import sha256
from html.parser import HTMLParser
import json
import re
from typing import Iterable
from urllib.parse import urljoin
from urllib.request import Request, urlopen

from china_scope import InstitutionType


CCGP_BASE = "https://www.ccgp.gov.cn"
DEFAULT_LIST_URLS = (
    f"{CCGP_BASE}/cggg/zygg/zbgg/index.htm",
    f"{CCGP_BASE}/cggg/dfgg/zbgg/index.htm",
)

_RE_META = re.compile(
    r"发布时间[:：]\s*(?P<published>\d{4}-\d{2}-\d{2}(?:\s+\d{2}:\d{2})?)"
    r".*?地域[:：]\s*(?P<region>.*?)\s+采购人[:：]\s*(?P<buyer>.+?)\s*$"
)


@dataclass(frozen=True)
class CCGPAwardLead:
    title: str
    url: str
    published_at: str | None
    region: str | None
    buyer_name: str | None
    institution_type: str
    source: str = "中国政府采购网"
    source_tier: str = "CN-A"
    corruption_inference: bool = False


@dataclass(frozen=True)
class CCGPDiscoveryResult:
    source_url: str
    retrieved_at: str
    html_sha256: str
    leads: tuple[CCGPAwardLead, ...]
    warnings: tuple[str, ...] = ()

    def as_json(self) -> dict:
        return {
            "source_url": self.source_url,
            "retrieved_at": self.retrieved_at,
            "html_sha256": self.html_sha256,
            "warnings": list(self.warnings),
            "leads": [asdict(x) for x in self.leads],
        }


class _CCGPListParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self._li_depth = 0
        self._li_text: list[str] = []
        self._anchors: list[tuple[str, str]] = []
        self._anchor_href: str | None = None
        self._anchor_text: list[str] = []
        self.rows: list[tuple[str, str, str]] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        attrs_d = dict(attrs)
        if tag.lower() == "li":
            if self._li_depth == 0:
                self._li_text = []
                self._anchors = []
            self._li_depth += 1
        if self._li_depth and tag.lower() == "a":
            self._anchor_href = attrs_d.get("href")
            self._anchor_text = []

    def handle_data(self, data: str) -> None:
        if self._li_depth:
            self._li_text.append(data)
            if self._anchor_href is not None:
                self._anchor_text.append(data)

    def handle_endtag(self, tag: str) -> None:
        low = tag.lower()
        if self._li_depth and low == "a" and self._anchor_href is not None:
            text = " ".join("".join(self._anchor_text).split())
            self._anchors.append((self._anchor_href, text))
            self._anchor_href = None
            self._anchor_text = []
        if low == "li" and self._li_depth:
            self._li_depth -= 1
            if self._li_depth == 0:
                text = " ".join("".join(self._li_text).split())
                for href, title in self._anchors:
                    # CCGP commonly uses directory-relative detail links such
                    # as ./202609/t20260917_....htm, so the raw href may not
                    # contain /cggg/ or /zbgg/. Restrict by award-result title
                    # here, then validate the resolved path downstream.
                    if (
                        href
                        and title
                        and href.lower().endswith((".htm", ".html"))
                        and any(k in title for k in ("中标", "成交", "结果公告"))
                    ):
                        self.rows.append((href, title, text))
                        break


def classify_buyer(name: str | None) -> InstitutionType:
    """Conservative institution routing from buyer name only.

    Ambiguous names remain OTHER rather than being over-classified.
    This classification is never itself an integrity finding.
    """
    n = (name or "").strip()
    if not n:
        return InstitutionType.OTHER

    # Hospital/medical first because many are university-affiliated.
    if any(k in n for k in ("医院", "卫生院", "妇幼保健院", "医学中心")):
        return InstitutionType.HOSPITAL

    # Research institutes before universities because CAS institute names can
    # contain school-like words in project titles but the buyer itself is an institute.
    if (
        "中国科学院" in n
        and any(k in n for k in ("研究所", "研究院", "中心"))
    ) or n.endswith(("研究所", "研究院")):
        return InstitutionType.RESEARCH_INSTITUTE

    if "大学" in n or n.endswith(("学院", "职业技术学院", "高等专科学校")):
        return InstitutionType.UNIVERSITY

    # Strong government/public-agency tokens only. Many public institutions do
    # not contain these tokens and therefore remain PUBLIC_INSTITUTION/OTHER.
    if any(
        k in n
        for k in (
            "人民政府",
            "财政局",
            "公安局",
            "海关",
            "税务局",
            "人民法院",
            "人民检察院",
            "消防救援",
            "委员会",
            "管理局",
            "监督管理局",
            "厅",
        )
    ):
        return InstitutionType.GOVERNMENT

    if any(k in n for k in ("中心", "馆", "站", "学校")):
        return InstitutionType.PUBLIC_INSTITUTION

    return InstitutionType.OTHER


def parse_ccgp_award_list(
    html: str,
    *,
    source_url: str,
    retrieved_at: str,
    limit: int | None = None,
) -> CCGPDiscoveryResult:
    parser = _CCGPListParser()
    parser.feed(html)

    leads: list[CCGPAwardLead] = []
    warnings: list[str] = []
    seen: set[str] = set()

    for href, title, row_text in parser.rows:
        url = urljoin(source_url, href)
        # After resolving relative links, require the official award-result
        # directory. This prevents navigation/news links from entering Pilot 0.
        if "/cggg/" not in url or "/zbgg/" not in url:
            continue
        if url in seen:
            continue
        seen.add(url)

        meta = _RE_META.search(row_text)
        if meta:
            published = meta.group("published").strip()
            region = meta.group("region").strip() or None
            buyer = meta.group("buyer").strip() or None
        else:
            published = None
            region = None
            buyer = None
            warnings.append(f"metadata_parse_failed:{url}")

        leads.append(
            CCGPAwardLead(
                title=title,
                url=url,
                published_at=published,
                region=region,
                buyer_name=buyer,
                institution_type=classify_buyer(buyer).value,
            )
        )
        if limit is not None and len(leads) >= limit:
            break

    return CCGPDiscoveryResult(
        source_url=source_url,
        retrieved_at=retrieved_at,
        html_sha256=sha256(html.encode("utf-8")).hexdigest(),
        leads=tuple(leads),
        warnings=tuple(warnings),
    )


def fetch_text(url: str, *, timeout: float = 20.0) -> str:
    req = Request(
        url,
        headers={
            "User-Agent": "OpenIntegrity-ARIS4C014/0.1 (+public-data feasibility research)"
        },
    )
    with urlopen(req, timeout=timeout) as resp:
        raw = resp.read()
        content_type = resp.headers.get("Content-Type", "")
    declared = re.search(r"charset=([\w-]+)", content_type, re.I)
    encodings = [declared.group(1)] if declared else []
    encodings.extend(["utf-8", "gb18030"])
    for enc in dict.fromkeys(encodings):
        try:
            return raw.decode(enc)
        except (UnicodeDecodeError, LookupError):
            continue
    return raw.decode("utf-8", errors="replace")


def discover_live(
    urls: Iterable[str] = DEFAULT_LIST_URLS,
    *,
    per_page_limit: int = 50,
) -> list[CCGPDiscoveryResult]:
    now = datetime.now().astimezone().isoformat()
    out: list[CCGPDiscoveryResult] = []
    for url in urls:
        html = fetch_text(url)
        out.append(
            parse_ccgp_award_list(
                html,
                source_url=url,
                retrieved_at=now,
                limit=per_page_limit,
            )
        )
    return out


def aggregate(results: Iterable[CCGPDiscoveryResult]) -> dict:
    unique: dict[str, CCGPAwardLead] = {}
    for result in results:
        for lead in result.leads:
            unique.setdefault(lead.url, lead)

    by_type: dict[str, int] = {}
    with_buyer = 0
    with_published = 0
    for lead in unique.values():
        by_type[lead.institution_type] = by_type.get(lead.institution_type, 0) + 1
        with_buyer += int(bool(lead.buyer_name))
        with_published += int(bool(lead.published_at))

    return {
        "unique_award_notice_leads": len(unique),
        "buyer_metadata_coverage": (
            with_buyer / len(unique) if unique else 0.0
        ),
        "publication_time_coverage": (
            with_published / len(unique) if unique else 0.0
        ),
        "institution_type_counts": dict(sorted(by_type.items())),
        "corruption_inference": False,
        "interpretation": (
            "Source-feasibility and institution-routing statistics only; "
            "no integrity or corruption inference."
        ),
    }


def dumps_live_report(results: Iterable[CCGPDiscoveryResult]) -> str:
    results = list(results)
    return json.dumps(
        {
            "source_results": [r.as_json() for r in results],
            "aggregate": aggregate(results),
        },
        ensure_ascii=False,
        indent=2,
    ) + "\n"

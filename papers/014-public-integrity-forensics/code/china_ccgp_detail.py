"""CCGP award-detail normalization for OpenIntegrity China Pilot 0.

The parser deliberately keeps public procurement facts needed for entity/event
linkage while excluding personal contact names, phone numbers and addresses
from its normalized public output.

One CCGP notice may contain multiple packages/suppliers. Percentage/discount
quotes are not converted into currency amounts.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
from hashlib import sha256
from html.parser import HTMLParser
import json
import re
from typing import Iterable

from china_ccgp import classify_buyer, fetch_text


_BLOCK_TAGS = {
    "p", "div", "tr", "td", "th", "li", "br", "h1", "h2", "h3", "h4",
    "h5", "h6", "section", "article", "table",
}


class _VisibleText(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.parts: list[str] = []

    def handle_starttag(self, tag: str, attrs) -> None:
        if tag.lower() in _BLOCK_TAGS:
            self.parts.append("\n")

    def handle_endtag(self, tag: str) -> None:
        if tag.lower() in _BLOCK_TAGS:
            self.parts.append("\n")

    def handle_data(self, data: str) -> None:
        self.parts.append(data)

    def text(self) -> str:
        text = "".join(self.parts).replace("\xa0", " ")
        lines = [" ".join(x.split()) for x in text.splitlines()]
        return "\n".join(x for x in lines if x)


@dataclass(frozen=True)
class CCGPAwardLot:
    lot_index: int
    package_name: str | None
    supplier_name: str
    award_value_yuan: float | None
    award_value_raw: str | None
    pricing_basis: str
    result_status: str = "awarded"
    candidate_rank: int | None = None
    score: float | None = None
    item_name: str | None = None
    corruption_inference: bool = False


@dataclass(frozen=True)
class CCGPAwardNotice:
    source_url: str
    retrieved_at: str
    html_sha256: str
    published_at: str | None
    project_id: str | None
    procurement_plan_id: str | None
    project_name: str | None
    buyer_name: str | None
    buyer_institution_type: str
    procurement_agency_name: str | None
    lots: tuple[CCGPAwardLot, ...]
    warnings: tuple[str, ...] = ()
    corruption_inference: bool = False

    def as_json(self) -> dict:
        return {
            **{k: v for k, v in asdict(self).items() if k != "lots"},
            "lots": [asdict(x) for x in self.lots],
        }


def html_to_text(html: str) -> str:
    p = _VisibleText()
    p.feed(html)
    return p.text()


def _numbered_field(text: str, number: str, label: str) -> str | None:
    """Extract a numbered CCGP body field whether value is same-line or next-line."""
    m = re.search(
        rf"(?:^|\n){re.escape(number)}、\s*{re.escape(label)}\s*[：:]?\s*([^\n]+)",
        text,
    )
    if not m:
        return None
    value = m.group(1).strip()
    return value or None


def _clean_project_id(value: str | None) -> str | None:
    if not value:
        return None
    # Central notices often append "(招标文件编号：...)" after the actual ID.
    value = re.split(r"[（(]\s*招标文件编号", value, maxsplit=1)[0].strip()
    return value or None


def _first_label(text: str, label: str) -> str | None:
    # Handles "采购单位 | 江汉大学", "采购单位：江汉大学" and normalized
    # line-separated table cells. It intentionally does not parse address/contact labels.
    patterns = [
        rf"(?:^|\n){re.escape(label)}\s*[|：:]\s*([^\n|]+)",
        rf"(?:^|\n){re.escape(label)}\s*\n([^\n]+)",
    ]
    for p in patterns:
        m = re.search(p, text)
        if m:
            value = m.group(1).strip()
            if value:
                return value
    return None


def _published_at(text: str) -> str | None:
    for p in (
        r"公告时间\s*[|：:]?\s*(\d{4}年\d{2}月\d{2}日\s+\d{2}:\d{2})",
        r"发布日期[：:]?\s*(\d{4}-\d{2}-\d{2}\s+\d{2}:\d{2})",
        r"(\d{4}年\d{2}月\d{2}日\s+\d{2}:\d{2})\s+来源",
    ):
        m = re.search(p, text)
        if m:
            return m.group(1)
    return None


def _parse_value(raw: str | None) -> tuple[float | None, str]:
    if not raw:
        return None, "unknown"
    compact = raw.replace(" ", "")
    num_m = re.search(r"(-?\d+(?:\.\d+)?)", compact)
    value = float(num_m.group(1)) if num_m else None

    if "万元" in compact and value is not None:
        return round(value * 10000.0, 2), "currency"
    if re.search(r"(?<!万)元", compact) and value is not None:
        return round(value, 2), "currency"
    if "%" in compact or "％" in compact:
        return None, "percentage"
    return None, "unknown"


def _award_section(text: str) -> str:
    # Central/local templates vary in both section number and heading wording.
    heading = r"(?:中标（成交）信息|中标信息|成交信息)"
    for current, nxt in (("四", "五"), ("三", "四")):
        m = re.search(
            rf"(?:^|\n){current}、\s*{heading}\s*\n(?P<body>.*?)(?=\n{nxt}、)",
            text,
            re.S,
        )
        if m:
            return m.group("body")
    return ""


def _nearby_field(segment: str, labels: Iterable[str]) -> str | None:
    for label in labels:
        m = re.search(
            rf"(?:^|\n){re.escape(label)}[：:]\s*([^\n]+)",
            segment,
        )
        if m:
            return m.group(1).strip()
    return None


def _award_value_raw(segment: str) -> str | None:
    """Extract amount without losing a unit embedded in the field label."""
    m = re.search(
        r"(?:^|\n)(?:中标|成交)金额\s*[（(]\s*(万元|元|%|％)\s*[）)]\s*[：:]\s*([^\n]+)",
        segment,
    )
    if m:
        unit, value = m.group(1), m.group(2).strip()
        return f"{value}({unit})"
    return _nearby_field(
        segment,
        ("中标（成交）金额", "中标金额", "成交金额"),
    )


def _supplier_status(raw_name: str) -> tuple[str, str, int | None]:
    """Separate ranked candidates from final award relationships."""
    value = raw_name.strip()
    m = re.match(
        r"第([一二三四五六七八九十\d]+)中标候选人[：:]\s*(.+)",
        value,
    )
    if not m:
        return value, "awarded", None

    rank_token = m.group(1)
    chinese = {
        "一": 1, "二": 2, "三": 3, "四": 4, "五": 5,
        "六": 6, "七": 7, "八": 8, "九": 9, "十": 10,
    }
    rank = int(rank_token) if rank_token.isdigit() else chinese.get(rank_token)
    return m.group(2).strip(), "candidate", rank


def _score(segment: str) -> float | None:
    m = re.search(r"(?:综合评分法|评审总得分)[：:]\s*(\d+(?:\.\d+)?)", segment)
    return float(m.group(1)) if m else None


def parse_ccgp_award_detail(
    html: str,
    *,
    source_url: str,
    retrieved_at: str,
) -> CCGPAwardNotice:
    text = html_to_text(html)
    warnings: list[str] = []

    project_id = _clean_project_id(_numbered_field(text, "一", "项目编号"))
    procurement_plan_id = _numbered_field(text, "二", "采购计划备案号")
    if procurement_plan_id:
        project_name = _numbered_field(text, "三", "项目名称")
    else:
        project_name = _numbered_field(text, "二", "项目名称")
    buyer = _first_label(text, "采购单位")
    agency = _first_label(text, "代理机构名称")

    body = _award_section(text)
    supplier_matches = list(
        re.finditer(r"(?:^|\n)供应商名称[：:]\s*([^\n]+)", body)
    )
    lots: list[CCGPAwardLot] = []

    for idx, m in enumerate(supplier_matches, start=1):
        start = m.start()
        end = (
            supplier_matches[idx].start()
            if idx < len(supplier_matches)
            else len(body)
        )
        # package name belongs before supplier; inspect only since previous supplier
        prev_end = supplier_matches[idx - 2].end() if idx > 1 else 0
        prefix = body[prev_end:start]
        pkg_matches = list(
            re.finditer(r"(?:^|\n)包名称[：:]\s*([^\n]+)", prefix)
        )
        package = pkg_matches[-1].group(1).strip() if pkg_matches else None

        segment = body[start:end]
        supplier_raw = m.group(1).strip()
        supplier, result_status, candidate_rank = _supplier_status(supplier_raw)
        raw_value = _award_value_raw(segment)
        amount, basis = _parse_value(raw_value)

        item = _nearby_field(segment, ("名称",))
        lots.append(
            CCGPAwardLot(
                lot_index=idx,
                package_name=package,
                supplier_name=supplier,
                award_value_yuan=amount,
                award_value_raw=raw_value,
                pricing_basis=basis,
                result_status=result_status,
                candidate_rank=candidate_rank,
                score=_score(segment),
                item_name=item,
            )
        )

    if not lots:
        warnings.append("no_supplier_lots_parsed")
    if not project_id:
        warnings.append("project_id_missing")
    if not buyer:
        warnings.append("buyer_missing")

    return CCGPAwardNotice(
        source_url=source_url,
        retrieved_at=retrieved_at,
        html_sha256=sha256(html.encode("utf-8")).hexdigest(),
        published_at=_published_at(text),
        project_id=project_id,
        procurement_plan_id=procurement_plan_id,
        project_name=project_name,
        buyer_name=buyer,
        buyer_institution_type=classify_buyer(buyer).value,
        procurement_agency_name=agency,
        lots=tuple(lots),
        warnings=tuple(warnings),
    )


def fetch_and_parse_detail(url: str, *, retrieved_at: str) -> CCGPAwardNotice:
    return parse_ccgp_award_detail(
        fetch_text(url),
        source_url=url,
        retrieved_at=retrieved_at,
    )


def dump_detail_report(notices: Iterable[CCGPAwardNotice]) -> str:
    notices = list(notices)
    lots = [lot for n in notices for lot in n.lots]
    return json.dumps(
        {
            "notices": [n.as_json() for n in notices],
            "aggregate": {
                "notices": len(notices),
                "lots": len(lots),
                "supplier_name_coverage": (
                    sum(bool(x.supplier_name) for x in lots) / len(lots)
                    if lots else 0.0
                ),
                "currency_value_coverage": (
                    sum(x.award_value_yuan is not None for x in lots) / len(lots)
                    if lots else 0.0
                ),
                "percentage_pricing_lots": sum(
                    x.pricing_basis == "percentage" for x in lots
                ),
                "final_award_lots": sum(
                    x.result_status == "awarded" for x in lots
                ),
                "candidate_lots": sum(
                    x.result_status == "candidate" for x in lots
                ),
                "corruption_inference": False,
                "privacy_note": (
                    "Normalized public output excludes personal contact names, "
                    "phone numbers and addresses."
                ),
            },
        },
        ensure_ascii=False,
        indent=2,
    ) + "\n"


def safe_structural_debug_lines(html: str, *, limit: int = 80) -> list[str]:
    """Return procurement-structure lines only, excluding contact/address material."""
    text = html_to_text(html)
    keep_tokens = (
        "项目编号", "采购计划备案号", "项目名称", "中标（成交）信息",
        "中标信息", "成交信息", "包名称", "供应商名称", "中标（成交）金额",
        "中标金额", "成交金额", "采购单位", "代理机构名称",
    )
    drop_tokens = (
        "地址", "联系方式", "联系电话", "联系人", "评审专家", "评审小组",
        "电 话", "电话",
    )
    out: list[str] = []
    for line in text.splitlines():
        if not any(k in line for k in keep_tokens):
            continue
        if any(k in line for k in drop_tokens):
            continue
        # Strip long digit runs as an additional privacy guard. Project IDs with
        # mixed letters/punctuation remain structurally useful.
        line = re.sub(r"(?<![A-Za-z])\d{7,}(?![A-Za-z])", "[REDACTED_NUM]", line)
        out.append(line[:300])
        if len(out) >= limit:
            break
    return out

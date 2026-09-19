#!/usr/bin/env python3
"""Generate README visuals from canonical ARIS4C portfolio metadata.

Stdlib-only so GitHub Actions can refresh the README assets without extra dependencies.
"""

from __future__ import annotations

import html
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PAPERS = ROOT / "papers"
ASSET_DIR = ROOT / "docs" / "assets" / "readme"

BG = "#0b1220"
PANEL = "#111b2e"
GRID = "#20304b"
TEXT = "#f8fafc"
MUTED = "#9fb0c8"
ACTIVE = "#48c78e"
GATED = "#f2c14e"
QUIET = "#8aa0b8"
BLOCKED = "#ef6a6a"
ACCENT = "#77a7ff"


def esc(x: object) -> str:
    return html.escape(str(x), quote=True)


def load():
    dashboard = json.loads((PAPERS / "dashboard.json").read_text(encoding="utf-8"))
    rows = []
    for manifest in sorted(PAPERS.glob("[0-9][0-9][0-9]-*/paper.json")):
        p = json.loads(manifest.read_text(encoding="utf-8"))
        d = dashboard["projects"].get(p["id"], {})
        handoff = manifest.parent / "handoff"
        handoff_ok = handoff.is_dir() and len(list(handoff.glob("*.md"))) >= 8
        rows.append({
            "id": p["id"],
            "short_title": p.get("short_title") or p["title"],
            "progress": int(d.get("progress", 0)),
            "activity": d.get("activity", "active"),
            "handoff": handoff_ok,
            "pdf_ready": bool(p.get("links", {}).get("paper_en_pdf") and p.get("links", {}).get("paper_zh_pdf")),
        })
    return dashboard, rows


def svg_start(width: int, height: int, title: str) -> list[str]:
    return [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}" role="img">',
        f'<title>{esc(title)}</title>',
        f'<rect width="{width}" height="{height}" rx="24" fill="{BG}"/>',
        '<style>',
        'text{font-family:Inter,ui-sans-serif,system-ui,-apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif}',
        '.title{font-size:28px;font-weight:700;fill:#f8fafc}.sub{font-size:15px;fill:#9fb0c8}.label{font-size:14px;fill:#d8e2ef}.small{font-size:12px;fill:#9fb0c8}.metric{font-size:34px;font-weight:750;fill:#f8fafc}',
        '</style>',
    ]


def hero(rows: list[dict]) -> str:
    counts = {k: sum(r["activity"] == k for r in rows) for k in ("active", "gated", "quiet", "blocked")}
    avg = round(sum(r["progress"] for r in rows) / max(1, len(rows)))
    continuity = sum(r["handoff"] for r in rows)
    ready = sum(r["pdf_ready"] for r in rows)
    w, h = 1200, 330
    s = svg_start(w, h, "ARIS4C research portfolio")
    s += [
        f'<path d="M0 260 C240 210 360 335 610 270 S970 170 1200 235 V330 H0 Z" fill="#10233b"/>',
        f'<circle cx="1050" cy="65" r="110" fill="#132a47"/>',
        f'<circle cx="1110" cy="35" r="55" fill="#17385d"/>',
        '<text x="62" y="74" class="small">ARIS FOR COCHRANE · RESEARCH PORTFOLIO</text>',
        '<text x="62" y="126" class="title" style="font-size:42px">Research as a living system.</text>',
        '<text x="62" y="158" class="sub">Papers, evidence, bilingual outputs, review gates, and cross-agent continuity in one canonical repository.</text>',
    ]
    metrics = [
        (62, len(rows), "tracked papers"),
        (285, avg, "mean maturity", "%"),
        (508, counts["active"], "active"),
        (731, counts["gated"], "at gate"),
        (954, continuity, "handoff ready", f"/{len(rows)}"),
    ]
    for x, val, label, *suffix in metrics:
        suffix_text = suffix[0] if suffix else ""
        s += [
            f'<rect x="{x}" y="205" width="185" height="82" rx="16" fill="{PANEL}" stroke="{GRID}"/>',
            f'<text x="{x+18}" y="244" class="metric">{val}{esc(suffix_text)}</text>',
            f'<text x="{x+18}" y="271" class="small">{esc(label)}</text>',
        ]
    s += [
        f'<text x="62" y="312" class="small">{ready} project(s) currently expose bilingual PDF delivery · Continuity {continuity}/{len(rows)}</text>',
        '</svg>',
    ]
    return "\n".join(s)


def status(rows: list[dict]) -> str:
    counts = {k: sum(r["activity"] == k for r in rows) for k in ("active", "gated", "quiet", "blocked")}
    colors = {"active": ACTIVE, "gated": GATED, "quiet": QUIET, "blocked": BLOCKED}
    labels = {"active": "Active", "gated": "At gate", "quiet": "Quiet", "blocked": "Blocked"}
    total = len(rows)
    w, h = 1200, 260
    s = svg_start(w, h, "ARIS4C portfolio state")
    s += [
        '<text x="50" y="55" class="title">Portfolio state</text>',
        '<text x="50" y="82" class="sub">MECE management states from papers/dashboard.json</text>',
    ]
    x0, y, bar_w, bar_h = 50, 118, 1100, 42
    x = x0
    for key in ("active", "gated", "quiet", "blocked"):
        width = bar_w * counts[key] / total if total else 0
        if width:
            s.append(f'<rect x="{x:.1f}" y="{y}" width="{width:.1f}" height="{bar_h}" fill="{colors[key]}"/>')
            x += width
    legend_x = [50, 315, 580, 845]
    for x, key in zip(legend_x, ("active", "gated", "quiet", "blocked")):
        s += [
            f'<circle cx="{x+8}" cy="205" r="7" fill="{colors[key]}"/>',
            f'<text x="{x+24}" y="210" class="label">{labels[key]} · {counts[key]}</text>',
        ]
    s += [
        f'<text x="1150" y="210" text-anchor="end" class="small">Total {total}</text>',
        '</svg>',
    ]
    return "\n".join(s)


def maturity(rows: list[dict]) -> str:
    w, h = 1200, 690
    s = svg_start(w, h, "ARIS4C maturity by paper")
    s += [
        '<text x="50" y="55" class="title">Portfolio maturity by paper</text>',
        '<text x="50" y="82" class="sub">Management estimate, not a scientific result. 100% means the repository-level final output contract is satisfied.</text>',
    ]
    color = {"active": ACTIVE, "gated": GATED, "quiet": QUIET, "blocked": BLOCKED}
    cols = [50, 620]
    for i, r in enumerate(rows):
        col = 0 if i < 8 else 1
        row = i if i < 8 else i - 8
        x = cols[col]
        y = 125 + row * 66
        label = f'{r["id"]} · {r["short_title"]}'
        if len(label) > 42:
            label = label[:39] + "…"
        s += [
            f'<text x="{x}" y="{y}" class="label">{esc(label)}</text>',
            f'<text x="{x+500}" y="{y}" text-anchor="end" class="small">{r["progress"]}%</text>',
            f'<rect x="{x}" y="{y+13}" width="500" height="14" rx="7" fill="{GRID}"/>',
            f'<rect x="{x}" y="{y+13}" width="{5*r["progress"]}" height="14" rx="7" fill="{color.get(r["activity"], ACTIVE)}"/>',
        ]
    s += [
        f'<circle cx="50" cy="655" r="6" fill="{ACTIVE}"/><text x="64" y="660" class="small">Active</text>',
        f'<circle cx="150" cy="655" r="6" fill="{GATED}"/><text x="164" y="660" class="small">At gate</text>',
        f'<circle cx="265" cy="655" r="6" fill="{QUIET}"/><text x="279" y="660" class="small">Quiet</text>',
        f'<circle cx="360" cy="655" r="6" fill="{BLOCKED}"/><text x="374" y="660" class="small">Blocked</text>',
        '</svg>',
    ]
    return "\n".join(s)


def readiness(rows: list[dict]) -> str:
    total = len(rows)
    continuity = sum(r["handoff"] for r in rows)
    pdf = sum(r["pdf_ready"] for r in rows)
    avg = round(sum(r["progress"] for r in rows) / max(1, total))
    w, h = 1200, 300
    s = svg_start(w, h, "ARIS4C delivery readiness")
    s += [
        '<text x="50" y="55" class="title">Repository delivery & continuity</text>',
        '<text x="50" y="82" class="sub">The repository is designed to survive conversation, account, computer, and agent changes.</text>',
    ]
    cards = [
        (50, total, "Tracked projects", "canonical paper.json entries"),
        (330, continuity, "Continuity-ready", f"{continuity}/{total} handoff packages"),
        (610, pdf, "Bilingual PDF-ready", f"{pdf}/{total} currently expose EN + ZH PDFs"),
        (890, f"{avg}%", "Mean maturity", "portfolio-management estimate"),
    ]
    for x, val, label, note in cards:
        s += [
            f'<rect x="{x}" y="115" width="250" height="125" rx="18" fill="{PANEL}" stroke="{GRID}"/>',
            f'<text x="{x+20}" y="164" class="metric">{esc(val)}</text>',
            f'<text x="{x+20}" y="193" class="label">{esc(label)}</text>',
            f'<text x="{x+20}" y="220" class="small">{esc(note)}</text>',
        ]
    s += ['</svg>']
    return "\n".join(s)



def architecture(rows: list[dict]) -> str:
    w, h = 1200, 560
    s = svg_start(w, h, "ARIS4C research system architecture")
    s += [
        '<text x="50" y="55" class="title">A research system, not a pile of papers</text>',
        '<text x="50" y="82" class="sub">Scientific work flows forward; handoff context loops back so another executor can safely continue.</text>',
    ]

    # primary spine
    cards = [
        (50, 150, 180, 112, "01", "Research question", "Idea · hypothesis · scope"),
        (280, 150, 180, 112, "02", "ARIS engine", "Search · design · critique"),
        (510, 128, 220, 156, "03", "Paper workspace", "Canonical evidence hub"),
        (780, 150, 180, 112, "04", "Review gates", "Science · reproducibility"),
        (1010, 150, 140, 112, "05", "Public output", "EN + ZH PDF"),
    ]
    for x, y, cw, ch, num, title, note in cards:
        fill = "#13233c" if num != "03" else "#17365b"
        stroke = "#2b466c" if num != "03" else "#77a7ff"
        s += [
            f'<rect x="{x}" y="{y}" width="{cw}" height="{ch}" rx="18" fill="{fill}" stroke="{stroke}" stroke-width="1.5"/>',
            f'<text x="{x+18}" y="{y+27}" class="small">{num}</text>',
            f'<text x="{x+18}" y="{y+58}" class="label" style="font-size:17px;font-weight:700">{esc(title)}</text>',
            f'<text x="{x+18}" y="{y+84}" class="small">{esc(note)}</text>',
        ]
    # arrows
    for x1, x2 in [(230,280),(460,510),(730,780),(960,1010)]:
        s += [
            f'<line x1="{x1}" y1="206" x2="{x2-12}" y2="206" stroke="#6f86a8" stroke-width="3"/>',
            f'<path d="M{x2-12} 200 L{x2} 206 L{x2-12} 212 Z" fill="#6f86a8"/>',
        ]

    # paper workspace sublayers
    subcards = [
        (385, 348, 195, 90, "Evidence", "data · code · provenance"),
        (600, 348, 195, 90, "Bilingual paper", "EN + ZH"),
        (815, 348, 195, 90, "Visual narrative", "figures · tables"),
        (1030, 348, 120, 90, "Handoff", "8-file pack"),
    ]
    for x, y, cw, ch, title, note in subcards:
        s += [
            f'<rect x="{x}" y="{y}" width="{cw}" height="{ch}" rx="16" fill="{PANEL}" stroke="{GRID}"/>',
            f'<text x="{x+16}" y="{y+35}" class="label" style="font-weight:700">{esc(title)}</text>',
            f'<text x="{x+16}" y="{y+61}" class="small">{esc(note)}</text>',
        ]
    # branch from workspace
    s += [
        '<path d="M620 284 C620 320 482 320 482 348" stroke="#466486" stroke-width="2.5" fill="none"/>',
        '<path d="M620 284 C620 320 697 320 697 348" stroke="#466486" stroke-width="2.5" fill="none"/>',
        '<path d="M620 284 C620 320 912 320 912 348" stroke="#466486" stroke-width="2.5" fill="none"/>',
        '<path d="M620 284 C620 320 1090 320 1090 348" stroke="#466486" stroke-width="2.5" fill="none"/>',
    ]

    # continuity loop / command-center bar
    s += [
        '<rect x="50" y="475" width="1100" height="48" rx="14" fill="#0f1a2b" stroke="#20304b"/>',
        '<text x="72" y="505" class="label" style="font-weight:700">Cross-agent continuity</text>',
        '<text x="245" y="505" class="small">Git → handoff/ → next computer / account / agent → same canonical paper workspace</text>',
        '<path d="M1090 438 C1090 468 270 468 270 430" stroke="#77a7ff" stroke-width="2.5" fill="none" stroke-dasharray="8 7"/>',
        '<path d="M264 437 L270 425 L276 437 Z" fill="#77a7ff"/>',
        '</svg>',
    ]
    return "\n".join(s)


def main() -> int:
    _, rows = load()
    ASSET_DIR.mkdir(parents=True, exist_ok=True)
    outputs = {
        "hero.svg": hero(rows),
        "portfolio-status.svg": status(rows),
        "portfolio-maturity.svg": maturity(rows),
        "delivery-readiness.svg": readiness(rows),
        "architecture.svg": architecture(rows),
    }
    for name, content in outputs.items():
        path = ASSET_DIR / name
        path.write_text(content + "\n", encoding="utf-8")
        print(path.relative_to(ROOT))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

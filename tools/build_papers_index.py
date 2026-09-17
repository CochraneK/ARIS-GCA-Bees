#!/usr/bin/env python3
"""Build docs/index.html from papers/*/paper.json manifests."""

from __future__ import annotations

import html
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PAPERS = ROOT / "papers"
OUT = ROOT / "docs" / "index.html"


def load_papers() -> list[dict]:
    items = []
    for manifest in sorted(PAPERS.glob("[0-9][0-9][0-9]-*/paper.json")):
        data = json.loads(manifest.read_text(encoding="utf-8"))
        data["_folder"] = manifest.parent.name
        items.append(data)
    return items


def esc(value: object) -> str:
    return html.escape(str(value or ""), quote=True)


def link(href: str, label: str, primary: bool = False) -> str:
    if not href:
        return ""
    cls = "btn primary" if primary else "btn"
    return f'<a class="{cls}" href="{esc(href)}">{esc(label)}</a>'


def card(p: dict) -> str:
    links = p.get("links", {})
    aris = p.get("aris", {})
    tags = "".join(f'<span class="tag">{esc(t)}</span>' for t in p.get("tags", [])[:5])
    buttons = "".join([
        link(links.get("paper_en", ""), "Paper", True),
        link(links.get("paper_zh", ""), "中文"),
        link(links.get("pipeline", ""), "Pipeline"),
        link(links.get("source", ""), "Source"),
    ])
    return f"""
    <article class="paper-card">
      <div class="paper-topline"><span>#{esc(p.get('id'))}</span><span>{esc(p.get('status'))}</span></div>
      <h2>{esc(p.get('title'))}</h2>
      <p class="summary">{esc(p.get('summary'))}</p>
      <div class="meta"><span>{esc(p.get('year'))}</span><span>{esc(p.get('domain'))}</span><span>ARIS {esc(aris.get('version'))}</span></div>
      <div class="tags">{tags}</div>
      <div class="actions">{buttons}</div>
    </article>"""


def build(papers: list[dict]) -> str:
    cards = "\n".join(card(p) for p in papers)
    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width,initial-scale=1">
  <title>ARIS Research Hub · Cunyi Kang</title>
  <meta name="description" content="A living collection of papers and research artifacts developed with ARIS.">
  <style>
    :root {{ --bg:#f7f7f5; --card:#fff; --text:#171717; --muted:#707070; --line:#e7e5e4; --accent:#111827; --soft:#f1f0ed; }}
    * {{ box-sizing:border-box; }}
    body {{ margin:0; font-family:Inter,ui-sans-serif,system-ui,-apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif; background:var(--bg); color:var(--text); }}
    .shell {{ width:min(1080px,calc(100% - 36px)); margin:0 auto; }}
    header {{ padding:72px 0 38px; border-bottom:1px solid var(--line); }}
    .eyebrow {{ color:var(--muted); font-size:.82rem; letter-spacing:.12em; text-transform:uppercase; font-weight:700; }}
    h1 {{ font-size:clamp(2.3rem,6vw,5rem); line-height:.98; letter-spacing:-.05em; margin:14px 0 20px; max-width:850px; }}
    .lede {{ max-width:720px; color:var(--muted); font-size:1.08rem; line-height:1.7; }}
    .stats {{ display:flex; gap:10px; flex-wrap:wrap; margin-top:24px; }}
    .stat {{ border:1px solid var(--line); background:var(--card); border-radius:999px; padding:8px 12px; font-size:.9rem; }}
    main {{ padding:34px 0 70px; }}
    .grid {{ display:grid; grid-template-columns:repeat(2,minmax(0,1fr)); gap:18px; }}
    .paper-card {{ background:var(--card); border:1px solid var(--line); border-radius:22px; padding:24px; min-height:330px; display:flex; flex-direction:column; }}
    .paper-topline,.meta {{ display:flex; gap:12px; flex-wrap:wrap; color:var(--muted); font-size:.82rem; }}
    .paper-topline {{ justify-content:space-between; text-transform:uppercase; letter-spacing:.06em; font-weight:700; }}
    h2 {{ font-size:1.55rem; line-height:1.18; letter-spacing:-.025em; margin:24px 0 12px; }}
    .summary {{ color:var(--muted); line-height:1.65; margin:0 0 18px; }}
    .meta {{ margin-top:auto; padding-top:18px; border-top:1px solid var(--line); }}
    .tags {{ display:flex; gap:7px; flex-wrap:wrap; margin:16px 0; }}
    .tag {{ background:var(--soft); border-radius:999px; padding:6px 9px; font-size:.78rem; color:#555; }}
    .actions {{ display:flex; flex-wrap:wrap; gap:8px; }}
    .btn {{ display:inline-flex; align-items:center; justify-content:center; border:1px solid var(--line); color:var(--text); text-decoration:none; border-radius:999px; padding:8px 12px; font-weight:650; font-size:.88rem; }}
    .btn.primary {{ background:var(--accent); color:#fff; border-color:var(--accent); }}
    footer {{ color:var(--muted); border-top:1px solid var(--line); padding:24px 0 40px; font-size:.88rem; }}
    @media(max-width:760px) {{ header{{padding-top:50px}} .grid{{grid-template-columns:1fr}} .paper-card{{min-height:0}} }}
  </style>
</head>
<body>
  <header><div class="shell">
    <div class="eyebrow">ARIS Research Hub</div>
    <h1>Papers as a living research system.</h1>
    <p class="lede">One repository for research produced with ARIS: each paper keeps its manuscript, code, figures, process records, provenance, and reproducibility trail while the research engine can keep evolving independently.</p>
    <div class="stats"><span class="stat">{len(papers)} paper{'s' if len(papers) != 1 else ''}</span><span class="stat">Manifest-driven</span><span class="stat">ARIS-upgradable</span></div>
  </div></header>
  <main><div class="shell"><section class="grid">{cards}</section></div></main>
  <footer><div class="shell">Generated from <code>papers/*/paper.json</code>. Paper metadata is the source of truth.</div></footer>
</body>
</html>
"""


def main() -> None:
    papers = load_papers()
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(build(papers), encoding="utf-8")
    print(f"Wrote {OUT.relative_to(ROOT)} with {len(papers)} paper(s)")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Build docs/index.html for ARIS4C from paper manifests + portfolio dashboard metadata."""

from __future__ import annotations

import html
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PAPERS = ROOT / "papers"
OUT = ROOT / "docs" / "index.html"
DASHBOARD = PAPERS / "dashboard.json"
REPO_URL = "https://github.com/CochraneK/ARIS4C"


def load_papers() -> list[dict]:
    items = []
    for manifest in sorted(PAPERS.glob("[0-9][0-9][0-9]-*/paper.json")):
        data = json.loads(manifest.read_text(encoding="utf-8"))
        data["_folder"] = manifest.parent.name
        items.append(data)
    return items


def load_dashboard() -> dict:
    if not DASHBOARD.exists():
        return {"projects": {}}
    return json.loads(DASHBOARD.read_text(encoding="utf-8"))


def esc(value: object) -> str:
    return html.escape(str(value or ""), quote=True)


def link(href: str, label: str, primary: bool = False) -> str:
    if not href:
        return ""
    cls = "btn primary" if primary else "btn"
    return f'<a class="{cls}" href="{esc(href)}">{esc(label)}</a>'


def paper_repo_file_link(p: dict, href: str) -> str:
    """Resolve paper-local file links to stable GitHub blob URLs."""
    if not href:
        return ""
    if href.startswith(("https://", "http://", "#", "/")):
        return href
    clean = href.removeprefix("./")
    return f"{REPO_URL}/blob/main/papers/{p['_folder']}/{clean}"


def paper_display_link(p: dict, href: str) -> str:
    """Keep generated site pages local; route other paper-local artifacts to GitHub."""
    if not href:
        return ""
    if href.startswith(("https://", "http://", "#", "/")):
        return href
    if href.startswith("paper/"):
        return href
    return paper_repo_file_link(p, href)


def activity_label(value: str) -> tuple[str, str]:
    key = (value or "unknown").lower()
    labels = {
        "active": ("Active", "active"),
        "gated": ("At gate", "gated"),
        "quiet": ("Quiet", "quiet"),
        "blocked": ("Blocked", "blocked"),
    }
    return labels.get(key, ("Tracked", "quiet"))


def card(p: dict, dashboard: dict) -> str:
    links = p.get("links", {})
    aris = p.get("aris", {})
    d = dashboard.get("projects", {}).get(str(p.get("id")), {})
    progress = max(0, min(100, int(d.get("progress", 0))))
    stage = d.get("stage") or p.get("status") or "Unclassified"
    evidence = d.get("evidence") or "Not yet classified"
    next_gate = d.get("next_gate") or "Not yet recorded"
    blocker = d.get("blocker") or "Not yet recorded"
    activity_text, activity_class = activity_label(d.get("activity", ""))
    tags = "".join(f'<span class="tag">{esc(t)}</span>' for t in p.get("tags", [])[:4])
    pipeline_href = paper_repo_file_link(p, links.get("pipeline", ""))
    buttons = "".join([
        link(paper_display_link(p, links.get("paper_en", "")), "Paper", True),
        link(paper_display_link(p, links.get("paper_zh", "")), "中文"),
        link(pipeline_href, "Pipeline"),
        link(links.get("source", ""), "Source"),
    ])
    return f"""
    <article class="paper-card" data-progress="{progress}" data-activity="{esc(activity_class)}">
      <div class="paper-topline">
        <span class="paper-id">#{esc(p.get('id'))}</span>
        <span class="heartbeat {esc(activity_class)}"><i></i>{esc(activity_text)}</span>
      </div>
      <div class="statusline">{esc(p.get('status'))}</div>
      <h2>{esc(p.get('title'))}</h2>
      <div class="progress-head"><span>{esc(stage)}</span><strong>{progress}%</strong></div>
      <div class="progress-track" aria-label="Portfolio progress {progress}%"><span style="width:{progress}%"></span></div>
      <p class="summary">{esc(p.get('summary'))}</p>
      <div class="milestones">
        <div><span>Evidence</span><strong>{esc(evidence)}</strong></div>
        <div><span>Next gate</span><strong>{esc(next_gate)}</strong></div>
      </div>
      <div class="blocker"><span>Blocker</span>{esc(blocker)}</div>
      <div class="meta"><span>{esc(p.get('year'))}</span><span>{esc(p.get('domain'))}</span><span>ARIS {esc(aris.get('version'))}</span></div>
      <div class="tags">{tags}</div>
      <div class="actions">{buttons}</div>
    </article>"""


def build(papers: list[dict], dashboard: dict) -> str:
    cards = "\n".join(card(p, dashboard) for p in papers)
    projects = dashboard.get("projects", {})
    progresses = [int(projects.get(str(p.get("id")), {}).get("progress", 0)) for p in papers]
    avg = round(sum(progresses) / len(progresses)) if progresses else 0
    active = sum(1 for p in papers if projects.get(str(p.get("id")), {}).get("activity") == "active")
    near_final = sum(1 for v in progresses if v >= 85)
    real_work = sum(1 for p in papers if int(projects.get(str(p.get("id")), {}).get("progress", 0)) >= 45)
    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width,initial-scale=1">
  <title>ARIS4C · Research Command Center</title>
  <meta name="description" content="ARIS4C — a living research command center for Cochrane's ARIS projects.">
  <style>
    :root {{ --bg:#f4f4f1; --card:#fff; --text:#151515; --muted:#6f706f; --line:#e5e5df; --accent:#171717; --soft:#f0f0eb; --green:#247a52; --amber:#9a6a16; --red:#a94141; }}
    * {{ box-sizing:border-box; }}
    html {{ scroll-behavior:smooth; }}
    body {{ margin:0; font-family:Inter,ui-sans-serif,system-ui,-apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif; background:linear-gradient(180deg,#fafaf8 0,#f4f4f1 420px); color:var(--text); }}
    .shell {{ width:min(1180px,calc(100% - 36px)); margin:0 auto; }}
    header {{ padding:64px 0 34px; }}
    .eyebrow {{ color:var(--muted); font-size:.78rem; letter-spacing:.14em; text-transform:uppercase; font-weight:800; }}
    h1 {{ font-size:clamp(2.6rem,6vw,5.4rem); line-height:.96; letter-spacing:-.055em; margin:13px 0 18px; max-width:920px; }}
    .lede {{ max-width:790px; color:var(--muted); font-size:1.08rem; line-height:1.7; }}
    .overview {{ display:grid; grid-template-columns:repeat(4,minmax(0,1fr)); gap:12px; margin-top:30px; }}
    .metric {{ border:1px solid var(--line); background:rgba(255,255,255,.78); backdrop-filter:blur(12px); border-radius:18px; padding:17px 18px; }}
    .metric strong {{ display:block; font-size:1.65rem; letter-spacing:-.04em; }}
    .metric span {{ color:var(--muted); font-size:.82rem; }}
    .portfolio-progress {{ margin-top:14px; border:1px solid var(--line); background:rgba(255,255,255,.72); border-radius:18px; padding:15px 18px; }}
    .portfolio-progress .row {{ display:flex; align-items:center; justify-content:space-between; gap:16px; font-size:.9rem; }}
    .portfolio-progress .row span {{ color:var(--muted); }}
    main {{ padding:10px 0 74px; }}
    .section-head {{ display:flex; justify-content:space-between; align-items:end; gap:20px; margin:24px 0 16px; }}
    .section-head h3 {{ margin:0; font-size:1.25rem; letter-spacing:-.025em; }}
    .section-head p {{ margin:0; color:var(--muted); font-size:.86rem; }}
    .grid {{ display:grid; grid-template-columns:repeat(2,minmax(0,1fr)); gap:16px; }}
    .paper-card {{ background:var(--card); border:1px solid var(--line); border-radius:22px; padding:22px; display:flex; flex-direction:column; box-shadow:0 1px 0 rgba(0,0,0,.02); }}
    .paper-card:hover {{ transform:translateY(-1px); box-shadow:0 10px 28px rgba(0,0,0,.045); transition:.18s ease; }}
    .paper-topline {{ display:flex; justify-content:space-between; align-items:center; gap:12px; }}
    .paper-id {{ font-size:.85rem; font-weight:850; letter-spacing:.08em; }}
    .heartbeat {{ display:inline-flex; align-items:center; gap:7px; border:1px solid var(--line); padding:5px 9px; border-radius:999px; color:var(--muted); font-size:.74rem; font-weight:750; }}
    .heartbeat i {{ width:7px; height:7px; border-radius:50%; background:#aaa; }}
    .heartbeat.active i {{ background:var(--green); box-shadow:0 0 0 4px rgba(36,122,82,.09); }}
    .heartbeat.gated i {{ background:var(--amber); }}
    .heartbeat.blocked i {{ background:var(--red); }}
    .statusline {{ margin-top:11px; color:var(--muted); font-size:.72rem; text-transform:uppercase; letter-spacing:.07em; font-weight:750; }}
    h2 {{ font-size:1.42rem; line-height:1.2; letter-spacing:-.028em; margin:12px 0 16px; }}
    .progress-head {{ display:flex; align-items:center; justify-content:space-between; gap:12px; font-size:.83rem; }}
    .progress-head span {{ color:var(--muted); }}
    .progress-head strong {{ font-size:.95rem; }}
    .progress-track {{ height:8px; background:var(--soft); border-radius:999px; overflow:hidden; margin:8px 0 17px; }}
    .progress-track span {{ display:block; height:100%; background:linear-gradient(90deg,#303030,#111); border-radius:inherit; }}
    .summary {{ color:var(--muted); line-height:1.58; font-size:.91rem; margin:0 0 17px; }}
    .milestones {{ display:grid; grid-template-columns:1fr 1fr; gap:9px; margin-bottom:9px; }}
    .milestones div,.blocker {{ background:#fafaf7; border:1px solid var(--line); border-radius:13px; padding:11px 12px; }}
    .milestones span,.blocker span {{ display:block; text-transform:uppercase; letter-spacing:.07em; font-size:.66rem; font-weight:800; color:#8a8a84; margin-bottom:5px; }}
    .milestones strong {{ display:block; font-size:.82rem; line-height:1.38; }}
    .blocker {{ font-size:.8rem; color:#555; margin-bottom:15px; }}
    .meta {{ display:flex; gap:9px; flex-wrap:wrap; color:var(--muted); font-size:.74rem; padding-top:14px; border-top:1px solid var(--line); }}
    .tags {{ display:flex; gap:6px; flex-wrap:wrap; margin:13px 0; }}
    .tag {{ background:var(--soft); border-radius:999px; padding:5px 8px; font-size:.7rem; color:#555; }}
    .actions {{ display:flex; flex-wrap:wrap; gap:7px; margin-top:auto; }}
    .btn {{ display:inline-flex; align-items:center; justify-content:center; border:1px solid var(--line); color:var(--text); text-decoration:none; border-radius:999px; padding:7px 11px; font-weight:700; font-size:.8rem; }}
    .btn:hover {{ background:#f5f5f1; }}
    .btn.primary {{ background:var(--accent); color:#fff; border-color:var(--accent); }}
    footer {{ color:var(--muted); border-top:1px solid var(--line); padding:24px 0 40px; font-size:.82rem; line-height:1.6; }}
    code {{ background:#ecece7; border-radius:6px; padding:2px 5px; }}
    @media(max-width:820px) {{ .overview{{grid-template-columns:repeat(2,1fr)}} .grid{{grid-template-columns:1fr}} }}
    @media(max-width:520px) {{ header{{padding-top:44px}} .overview{{grid-template-columns:1fr 1fr}} .milestones{{grid-template-columns:1fr}} .shell{{width:min(100% - 24px,1180px)}} }}
  </style>
</head>
<body>
  <header><div class="shell">
    <div class="eyebrow">ARIS4C · Research Command Center</div>
    <h1>Research as a living system.</h1>
    <p class="lede">A portfolio of ARIS-driven research projects with visible maturity, evidence state, next gates, and reproducibility trails. Progress values are management estimates—not scientific results.</p>
    <div class="overview">
      <div class="metric"><strong>{len(papers)}</strong><span>tracked projects</span></div>
      <div class="metric"><strong>{avg}%</strong><span>mean portfolio maturity</span></div>
      <div class="metric"><strong>{active}</strong><span>active execution tracks</span></div>
      <div class="metric"><strong>{near_final}</strong><span>near-final manuscripts</span></div>
    </div>
    <div class="portfolio-progress">
      <div class="row"><span>Portfolio maturity · {real_work} projects at ≥45%</span><strong>{avg}%</strong></div>
      <div class="progress-track"><span style="width:{avg}%"></span></div>
    </div>
  </div></header>
  <main><div class="shell">
    <div class="section-head"><div><h3>Project portfolio</h3><p>Idea → design → pilot → empirical analysis → manuscript → final</p></div><p>Dashboard metadata: <code>papers/dashboard.json</code></p></div>
    <section class="grid">{cards}</section>
  </div></main>
  <footer><div class="shell">ARIS4C · Scientific metadata comes from <code>papers/*/paper.json</code>. Portfolio progress, activity, next-gate and blocker annotations come from <code>papers/dashboard.json</code> so management estimates remain separate from scientific claims.</div></footer>
</body>
</html>
"""


def main() -> None:
    papers = load_papers()
    dashboard = load_dashboard()
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(build(papers, dashboard), encoding="utf-8")
    print(f"Wrote {OUT.relative_to(ROOT)} with {len(papers)} paper(s)")


if __name__ == "__main__":
    main()

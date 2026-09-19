#!/usr/bin/env python3
"""Build the ARIS4C Research Command Center from paper manifests + dashboard metadata."""

from __future__ import annotations

import hashlib
import html
import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PAPERS = ROOT / "papers"
OUT = ROOT / "docs" / "index.html"
DASHBOARD = PAPERS / "dashboard.json"
PROGRESS_HISTORY = PAPERS / "progress_history.json"
REPO_URL = "https://github.com/CochraneK/ARIS4C"


def asset_version(path: Path) -> str:
    """Short content hash for cache-busting public static assets."""
    try:
        return hashlib.sha256(path.read_bytes()).hexdigest()[:12]
    except OSError:
        return "missing"


def last_commit_iso(folder: Path) -> str:
    """Return the last Git commit timestamp touching a paper folder."""
    try:
        proc = subprocess.run(
            ["git", "log", "-1", "--format=%cI", "--", str(folder.relative_to(ROOT))],
            cwd=ROOT, check=True, capture_output=True, text=True, timeout=10,
        )
        return proc.stdout.strip()
    except (subprocess.SubprocessError, OSError, ValueError):
        return ""


def load_papers() -> list[dict]:
    items = []
    for manifest in sorted(PAPERS.glob("[0-9][0-9][0-9]-*/paper.json")):
        data = json.loads(manifest.read_text(encoding="utf-8"))
        data["_folder"] = manifest.parent.name
        data["_last_commit"] = last_commit_iso(manifest.parent)
        items.append(data)
    return items


def load_dashboard() -> dict:
    if not DASHBOARD.exists():
        return {"projects": {}}
    return json.loads(DASHBOARD.read_text(encoding="utf-8"))


def load_progress_history() -> dict:
    if not PROGRESS_HISTORY.exists():
        return {"schema_version": 1, "points": []}
    return json.loads(PROGRESS_HISTORY.read_text(encoding="utf-8"))


def latest_day_history(history: dict) -> dict:
    """Return only checkpoints from the local date encoded by the latest Git timestamp."""
    points = list(history.get("points", []) or [])
    if not points:
        return {"schema_version": history.get("schema_version", 1), "date": "", "points": []}
    latest = str(points[-1].get("timestamp", ""))
    day = latest[:10]
    return {
        "schema_version": history.get("schema_version", 1),
        "source": history.get("source", ""),
        "date": day,
        "points": [p for p in points if str(p.get("timestamp", ""))[:10] == day],
    }


def esc(value: object) -> str:
    return html.escape(str(value or ""), quote=True)


def link(href: str, label: str, primary: bool = False) -> str:
    if not href:
        return ""
    cls = "btn primary" if primary else "btn"
    return f'<a class="{cls}" href="{esc(href)}">{esc(label)}</a>'


def paper_button(href: str, label: str, primary: bool = False) -> str:
    if href:
        cls = "btn primary" if primary else "btn"
        return f'<a class="{cls}" href="{esc(href)}">{esc(label)}</a>'
    cls = "btn disabled primary" if primary else "btn disabled"
    return f'<span class="{cls}" aria-disabled="true" title="Full text not ready yet">{esc(label)}</span>'


def paper_repo_file_link(p: dict, href: str) -> str:
    if not href:
        return ""
    if href.startswith(("https://", "http://", "#", "/")):
        return href
    clean = href.removeprefix("./")
    return f"{REPO_URL}/blob/main/papers/{p['_folder']}/{clean}"


def paper_display_link(p: dict, href: str) -> str:
    if not href:
        return ""
    if href.startswith(("https://", "http://", "#", "/")):
        return href
    if href.startswith("paper/"):
        return href
    return paper_repo_file_link(p, href)


def activity_label(value: str) -> tuple[str, str]:
    key = (value or "wait").lower()
    labels = {
        "finish": ("Finish", "finish"),
        "active": ("Active", "active"),
        "wait": ("Wait", "wait"),
        "block": ("Block", "block"),
    }
    return labels.get(key, ("Wait", "wait"))


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
    series_id = str(p.get("series_id", "") or "").strip()
    tags_list = p.get("tags", [])[:4]
    tags = "".join(f'<span class="tag">{esc(t)}</span>' for t in tags_list)
    search_blob = " ".join([
        str(p.get("id", "")),
        str(p.get("title", "")),
        str(p.get("short_title", "")),
        series_id,
        str(p.get("domain", "")),
        str(p.get("status", "")),
        str(stage),
        " ".join(str(t) for t in p.get("tags", [])),
    ])
    en_href = links.get("paper_en_pdf") or links.get("paper_en_full") or links.get("paper_en", "")
    zh_href = links.get("paper_zh_pdf") or links.get("paper_zh_full") or links.get("paper_zh", "")
    buttons = "".join([
        paper_button(paper_display_link(p, en_href) if en_href else "", "English", True),
        paper_button(paper_display_link(p, zh_href) if zh_href else "", "中文"),
    ])
    blocker_class = "blocker is-clear" if str(blocker).lower().startswith("none") else "blocker"
    last_commit = p.get("_last_commit", "")
    return f"""
    <article class="paper-card" data-id="{esc(p.get('id'))}" data-progress="{progress}" data-activity="{esc(activity_class)}" data-last-commit="{esc(last_commit)}" data-search="{esc(search_blob)}">
      <div class="paper-topline">
        <span class="paper-id">#{esc(p.get('id'))}{(" · " + esc(series_id)) if series_id else ""}</span>
        <span class="heartbeat"><i></i>{esc(activity_text)}</span>
      </div>
      <div class="statusline">{esc(p.get('status'))}</div>
      <h3>{esc(p.get('title'))}</h3>
      <div class="progress-head"><span>{esc(stage)}</span><strong>{progress}%</strong></div>
      <div class="card-progress" aria-label="Portfolio maturity {progress}%"><span style="width:{progress}%"></span></div>
      <p class="summary">{esc(p.get('summary'))}</p>
      <div class="evidence-grid">
        <div class="evidence-cell"><span>Evidence</span><strong>{esc(evidence)}</strong></div>
        <div class="evidence-cell"><span>Next gate</span><strong>{esc(next_gate)}</strong></div>
      </div>
      <div class="{blocker_class}"><span>Blocker</span>{esc(blocker)}</div>
      <div class="meta"><span class="commit-heartbeat" data-commit-time="{esc(last_commit)}">Last commit · —</span><span>{esc(p.get('year'))}</span><span>{esc(p.get('domain'))}</span><span>ARIS {esc(aris.get('version'))}</span></div>
      <div class="tags">{tags}</div>
      <div class="actions">{buttons}</div>
    </article>"""



def showcase_card(p: dict, dashboard: dict) -> str:
    links = p.get("links", {})
    d = dashboard.get("projects", {}).get(str(p.get("id")), {})
    progress = max(0, min(100, int(d.get("progress", 0))))
    stage = d.get("stage") or p.get("status") or "Unclassified"
    activity_text, activity_class = activity_label(d.get("activity", ""))
    series_id = str(p.get("series_id", "") or "").strip()
    en_href = links.get("paper_en_pdf") or links.get("paper_en_full") or links.get("paper_en", "")
    zh_href = links.get("paper_zh_pdf") or links.get("paper_zh_full") or links.get("paper_zh", "")
    buttons = "".join([
        paper_button(paper_display_link(p, en_href) if en_href else "", "English", True),
        paper_button(paper_display_link(p, zh_href) if zh_href else "", "中文"),
    ])
    search_blob = " ".join([
        str(p.get("id", "")),
        str(p.get("title", "")),
        str(p.get("short_title", "")),
        str(p.get("domain", "")),
        str(p.get("status", "")),
        str(stage),
        " ".join(str(t) for t in p.get("tags", [])),
    ])
    last_commit = p.get("_last_commit", "")
    return f"""
      <article class="showcase-card" data-showcase-original="true" data-id="{esc(p.get('id'))}" data-progress="{progress}" data-activity="{esc(activity_class)}" data-last-commit="{esc(last_commit)}" data-search="{esc(search_blob)}">
        <div class="showcase-top">
          <span class="showcase-id">#{esc(p.get('id'))}{(" · " + esc(series_id)) if series_id else ""}</span>
          <span class="showcase-state"><i></i>{esc(activity_text)}</span>
        </div>
        <h3>{esc(p.get('short_title') or p.get('title'))}</h3>
        <p>{esc(stage)}</p>
        <div class="showcase-progress"><span style="width:{progress}%"></span></div>
        <div class="showcase-bottom">
          <strong>{progress}%</strong>
          <div class="showcase-actions">{buttons}</div>
        </div>
      </article>"""


def build(papers: list[dict], dashboard: dict, history: dict) -> str:
    projects = dashboard.get("projects", {})

    # Public command center is an execution surface, not an archive:
    # hide untouched (0%) and completed (100%) projects while keeping the
    # canonical dashboard unchanged for scheduling/audit/history.
    papers = [
        p for p in papers
        if 0 < int(projects.get(str(p.get("id")), {}).get("progress", 0)) < 100
    ]
    visible_ids = {str(p.get("id")) for p in papers}

    cards = "\n".join(card(p, dashboard) for p in papers)
    showcase = "\n".join(showcase_card(p, dashboard) for p in papers)
    progresses = [int(projects.get(str(p.get("id")), {}).get("progress", 0)) for p in papers]
    avg = round(sum(progresses) / len(progresses)) if progresses else 0
    finish = sum(1 for p in papers if projects.get(str(p.get("id")), {}).get("activity") == "finish")
    active = sum(1 for p in papers if projects.get(str(p.get("id")), {}).get("activity") == "active")
    wait = sum(1 for p in papers if projects.get(str(p.get("id")), {}).get("activity") == "wait")
    block = sum(1 for p in papers if projects.get(str(p.get("id")), {}).get("activity") == "block")
    mature = sum(1 for v in progresses if v >= 45)
    day_history = latest_day_history(history)
    day_history["points"] = [
        {
            **point,
            "projects": {
                pid: value
                for pid, value in (point.get("projects", {}) or {}).items()
                if pid in visible_ids and 0 < int(value) < 100
            },
        }
        for point in day_history.get("points", [])
    ]
    history_json = json.dumps(day_history, ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/")
    css_version = asset_version(OUT.parent / "command-center.css")
    js_version = asset_version(OUT.parent / "command-center.js")
    history_summary = (
        f"{day_history.get('date') or 'Today'} · {len(day_history.get('points', []))} checkpoints · "
        f"{len(papers)} papers on one chart"
    )

    return f"""<!doctype html>
<html lang="en" data-theme="light">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width,initial-scale=1">
  <meta name="color-scheme" content="light dark">
  <meta name="description" content="ARIS4C — Cochrane Kang's living research command center.">
  <meta name="theme-color" content="#f3f1ea">
  <title>ARIS4C · Research Command Center</title>
  <link rel="stylesheet" href="./command-center.css?v={css_version}">
</head>
<body>
  <div class="app">
    <aside class="sidebar" aria-label="Research portfolio navigation">
      <div class="identity"><span class="avatar">A4</span><div class="identity-copy"><strong>ARIS4C</strong><span>Research command center</span></div></div>
      <nav class="nav" aria-label="MECE project status">
        <button class="nav-item is-active" type="button" data-filter="all" data-label="All projects"><span class="nav-icon">◉</span><span>All projects</span><span id="navAllCount" class="nav-count">{len(papers)}</span></button>
        <button class="nav-item" type="button" data-filter="active" data-label="Active"><span class="nav-icon">↗</span><span>Active</span><span id="navActiveCount" class="nav-count">{active}</span></button>
        <button class="nav-item" type="button" data-filter="wait" data-label="Wait"><span class="nav-icon">◇</span><span>Wait</span><span id="navWaitCount" class="nav-count">{wait}</span></button>
        <button class="nav-item" type="button" data-filter="block" data-label="Block"><span class="nav-icon">×</span><span>Block</span><span id="navBlockCount" class="nav-count">{block}</span></button>
      </nav>
      <div class="sidebar-section">
        <p class="sidebar-label">Heartbeat semantics</p>
        <div class="legend">
          <div class="legend-row"><i class="dot active"></i><span>Meaningful work is moving now</span></div>
          <div class="legend-row"><i class="dot wait"></i><span>Can continue, but not moving now</span></div>
          <div class="legend-row"><i class="dot block"></i><span>External dependency prevents progress</span></div>
        </div>
      </div>
      <div class="sidebar-spacer"></div>
      <div class="sidebar-meta">
        <span>Scientific metadata ≠ management estimates</span>
        <a href="{REPO_URL}" target="_blank" rel="noreferrer">Open ARIS4C source ↗</a>
        <a href="https://cochranek.github.io/repo-auditor/" target="_blank" rel="noreferrer">Sibling · Audit Terminal ↗</a>
      </div>
    </aside>

    <section class="workspace">
      <header class="topbar">
        <div class="breadcrumbs"><span>Research portfolio</span><span>/</span><strong id="currentViewLabel">All projects</strong></div>
        <div class="topbar-actions">
          <label class="quick-search"><span aria-hidden="true">⌕</span><span class="sr-only">Search projects</span><input id="searchInput" type="search" placeholder="Search papers, fields, tags…" autocomplete="off"></label>
          <button id="themeToggle" class="icon-btn" type="button" aria-label="Toggle theme">◐</button>
          <a class="icon-btn" href="{REPO_URL}" target="_blank" rel="noreferrer" aria-label="Open GitHub">↗</a>
        </div>
      </header>

      <main class="content">
        <section class="hero">
          <div class="hero-main">
            <p class="eyebrow">ARIS4C · RESEARCH BRIDGE</p>
            <h1>Research as a living system.</h1>
            <p class="hero-copy">A portfolio of ARIS-driven papers and agents currently in motion: moving now, ready but idle, or externally blocked. Untouched and 100% completed projects stay in Git but are intentionally omitted here.</p>
            <div class="overview">
              <div class="metric"><strong>{active}</strong><span>active now</span></div>
              <div class="metric"><strong>{wait}</strong><span>wait</span></div>
              <div class="metric"><strong>{block}</strong><span>block</span></div>
            </div>
            <div class="portfolio-progress"><div class="row"><span>{len(papers)} in-progress papers · {active} active now · {wait} wait · {block} block</span><strong>{avg}%</strong></div><div class="progress-track"><span style="width:{avg}%"></span></div></div>
          </div>

          <section id="progressHistorySection" class="progress-history-panel hero-history" aria-labelledby="progressHistoryTitle">
            <div class="progress-history-head">
              <div>
                <p class="eyebrow">TODAY · GIT-DERIVED</p>
                <h2 id="progressHistoryTitle">Today's progress</h2>
                <p>In-progress papers only · today's dashboard checkpoints.</p>
              </div>
              <strong class="progress-history-day">{esc(day_history.get("date", ""))}</strong>
            </div>
            <div class="progress-history-chart-wrap">
              <svg id="progressHistoryChart" class="progress-history-chart" viewBox="0 0 1000 330" role="img" aria-label="Today's ARIS4C progress for all papers"></svg>
            </div>
            <div id="progressHistoryLegend" class="progress-history-legend" aria-label="Paper legend"></div>
            <div class="progress-history-foot"><span id="progressHistorySummary">{esc(history_summary)}</span><span>management estimate</span></div>
          </section>
        </section>

        <div class="control-bar">
          <div class="control-left"><span id="resultCount" class="result-count">{len(papers)} / {len(papers)} projects</span></div>
          <div class="control-right">
            <select id="sortFilter" aria-label="Sort projects"><option value="id">ID order</option><option value="progress-desc">Maturity high → low</option><option value="progress-asc">Maturity low → high</option><option value="activity">Activity state</option><option value="recent">Recent commit</option></select>
            <button id="clearFilters" class="filter-chip" type="button">Reset</button>
          </div>
        </div>

        <section id="showcaseSection" class="showcase" aria-labelledby="showcaseTitle">
          <div class="showcase-head">
            <div>
              <p class="eyebrow">LIVE RESEARCH SHOWCASE</p>
              <h2 id="showcaseTitle">ARIS4C rolling research board</h2>
              <p>All in-progress papers, continuously rotating. Hover, focus, drag or use the arrows to pause and explore.</p>
            </div>
            <div class="showcase-controls" aria-label="Showcase controls">
              <button id="showcasePrev" class="showcase-arrow" type="button" aria-label="Previous projects">←</button>
              <button id="showcaseNext" class="showcase-arrow" type="button" aria-label="Next projects">→</button>
            </div>
          </div>
          <div id="showcaseViewport" class="showcase-viewport" tabindex="0" aria-label="Rolling ARIS4C project showcase">
            <div id="showcaseTrack" class="showcase-track">
              {showcase}
            </div>
          </div>
        </section>

        <section id="portfolioSection" class="portfolio-panel hidden" aria-labelledby="portfolioTitle">
          <div class="section-head">
            <div>
              <h2 id="portfolioTitle">Project portfolio</h2>
              <p>Idea → design → pilot → empirical analysis → manuscript → final</p>
            </div>
            <p>Management layer: <code>papers/dashboard.json</code></p>
          </div>
          <section id="paperGrid" class="grid">{cards}</section>
          <div id="emptyState" class="empty-state hidden">No projects match this view.</div>
        </section>
      </main>

      <footer>ARIS4C · Scientific metadata comes from <code>papers/*/paper.json</code>. Portfolio maturity comes from <code>papers/dashboard.json</code>. Public project cards expose PDF-first English and Chinese paper entrances.</footer>
    </section>
  </div>
  <script id="progressHistoryData" type="application/json">{history_json}</script>
  <script src="./command-center.js?v={js_version}" defer></script>
</body>
</html>
"""


def main() -> None:
    papers = load_papers()
    dashboard = load_dashboard()
    history = load_progress_history()
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(build(papers, dashboard, history), encoding="utf-8")
    print(f"Wrote {OUT.relative_to(ROOT)} with {len(papers)} paper(s)")


if __name__ == "__main__":
    main()

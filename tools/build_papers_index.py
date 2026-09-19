#!/usr/bin/env python3
"""Build the ARIS4C Research Command Center from paper manifests + dashboard metadata."""

from __future__ import annotations

import html
import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PAPERS = ROOT / "papers"
OUT = ROOT / "docs" / "index.html"
DASHBOARD = PAPERS / "dashboard.json"
REPO_URL = "https://github.com/CochraneK/ARIS4C"


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
    key = (value or "quiet").lower()
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
    tags_list = p.get("tags", [])[:4]
    tags = "".join(f'<span class="tag">{esc(t)}</span>' for t in tags_list)
    search_blob = " ".join([
        str(p.get("id", "")),
        str(p.get("title", "")),
        str(p.get("short_title", "")),
        str(p.get("domain", "")),
        str(p.get("status", "")),
        str(stage),
        " ".join(str(t) for t in p.get("tags", [])),
    ])
    en_href = links.get("paper_en_full") or links.get("paper_en", "")
    zh_href = links.get("paper_zh_full") or links.get("paper_zh", "")
    buttons = "".join([
        paper_button(paper_display_link(p, en_href) if en_href else "", "English", True),
        paper_button(paper_display_link(p, zh_href) if zh_href else "", "中文"),
    ])
    blocker_class = "blocker is-clear" if str(blocker).lower().startswith("none") else "blocker"
    last_commit = p.get("_last_commit", "")
    return f"""
    <article class="paper-card" data-id="{esc(p.get('id'))}" data-progress="{progress}" data-activity="{esc(activity_class)}" data-last-commit="{esc(last_commit)}" data-search="{esc(search_blob)}">
      <div class="paper-topline">
        <span class="paper-id">#{esc(p.get('id'))}</span>
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
    en_href = links.get("paper_en_full") or links.get("paper_en", "")
    zh_href = links.get("paper_zh_full") or links.get("paper_zh", "")
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
          <span class="showcase-id">#{esc(p.get('id'))}</span>
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


def build(papers: list[dict], dashboard: dict) -> str:
    projects = dashboard.get("projects", {})
    cards = "\n".join(card(p, dashboard) for p in papers)
    showcase = "\n".join(showcase_card(p, dashboard) for p in papers)
    progresses = [int(projects.get(str(p.get("id")), {}).get("progress", 0)) for p in papers]
    avg = round(sum(progresses) / len(progresses)) if progresses else 0
    active = sum(1 for p in papers if projects.get(str(p.get("id")), {}).get("activity") == "active")
    gated = sum(1 for p in papers if projects.get(str(p.get("id")), {}).get("activity") == "gated")
    quiet = sum(1 for p in papers if projects.get(str(p.get("id")), {}).get("activity") == "quiet")
    blocked = sum(1 for p in papers if projects.get(str(p.get("id")), {}).get("activity") == "blocked")
    mature = sum(1 for v in progresses if v >= 45)

    return f"""<!doctype html>
<html lang="en" data-theme="light">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width,initial-scale=1">
  <meta name="color-scheme" content="light dark">
  <meta name="description" content="ARIS4C — Cochrane Kang's living research command center.">
  <meta name="theme-color" content="#f3f1ea">
  <title>ARIS4C · Research Command Center</title>
  <link rel="stylesheet" href="./command-center.css">
</head>
<body>
  <div class="app">
    <aside class="sidebar" aria-label="Research portfolio navigation">
      <div class="identity"><span class="avatar">A4</span><div class="identity-copy"><strong>ARIS4C</strong><span>Research command center</span></div></div>
      <nav class="nav" aria-label="MECE project status">
        <button class="nav-item is-active" type="button" data-filter="all" data-label="All projects"><span class="nav-icon">◉</span><span>All projects</span><span id="navAllCount" class="nav-count">{len(papers)}</span></button>
        <button class="nav-item" type="button" data-filter="active" data-label="Active"><span class="nav-icon">↗</span><span>Active</span><span id="navActiveCount" class="nav-count">{active}</span></button>
        <button class="nav-item" type="button" data-filter="gated" data-label="At gate"><span class="nav-icon">◇</span><span>At gate</span><span id="navGatedCount" class="nav-count">{gated}</span></button>
        <button class="nav-item" type="button" data-filter="quiet" data-label="Quiet"><span class="nav-icon">○</span><span>Quiet</span><span id="navQuietCount" class="nav-count">{quiet}</span></button>
        <button class="nav-item" type="button" data-filter="blocked" data-label="Blocked"><span class="nav-icon">×</span><span>Blocked</span><span id="navBlockedCount" class="nav-count">{blocked}</span></button>
      </nav>
      <div class="sidebar-section">
        <p class="sidebar-label">Heartbeat semantics</p>
        <div class="legend">
          <div class="legend-row"><i class="dot active"></i><span>Active execution</span></div>
          <div class="legend-row"><i class="dot gated"></i><span>Scientific / review gate</span></div>
          <div class="legend-row"><i class="dot quiet"></i><span>Near-final / complete</span></div>
          <div class="legend-row"><i class="dot blocked"></i><span>Hard blocker</span></div>
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
          <p class="eyebrow">ARIS4C · RESEARCH BRIDGE</p>
          <h1>Research as a living system.</h1>
          <p class="hero-copy">A portfolio of ARIS-driven papers and agents with visible maturity, evidence state, gates and blockers. Each project exposes only the English and Chinese full-text paper entrances on the public card.</p>
          <div class="overview">
            <div class="metric"><strong>{len(papers)}</strong><span>tracked projects</span></div>
            <div class="metric"><strong>{avg}%</strong><span>mean portfolio maturity</span></div>
            <div class="metric"><strong>{active}</strong><span>active execution tracks</span></div>
            <div class="metric"><strong>{quiet}</strong><span>quiet tracks</span></div>
          </div>
          <div class="portfolio-progress"><div class="row"><span>Portfolio maturity · {mature} projects at ≥45% · {gated + blocked} at gate/blocker</span><strong>{avg}%</strong></div><div class="progress-track"><span style="width:{avg}%"></span></div></div>
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
              <p>All current papers, continuously rotating. Hover, focus, drag or use the arrows to pause and explore.</p>
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

      <footer>ARIS4C · Scientific metadata comes from <code>papers/*/paper.json</code>. Portfolio maturity comes from <code>papers/dashboard.json</code>. Public project cards expose only English and Chinese full-text paper entrances.</footer>
    </section>
  </div>
  <script src="./command-center.js" defer></script>
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

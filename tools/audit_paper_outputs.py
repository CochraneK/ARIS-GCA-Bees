#!/usr/bin/env python3
"""Audit ARIS4C final-output completeness without collapsing scientific quality to one score."""

from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PAPERS = ROOT / "papers"
DASHBOARD = PAPERS / "dashboard.json"

FINAL_RE = re.compile(r"(^|[-_])(final|final-manuscript|submission-ready|submission-package-ready)($|[-_])", re.I)
HANDOFF_REQUIRED = [
    "README.md", "STATUS.md", "TODO.md", "DECISIONS.md",
    "CONTEXT.md", "CHATLOG.md", "AGENT_HANDOFF.md", "SESSION_LOG.md",
]

def main() -> int:
    rows = []
    dashboard = json.loads(DASHBOARD.read_text(encoding="utf-8")) if DASHBOARD.exists() else {"projects": {}}
    for manifest in sorted(PAPERS.glob("[0-9][0-9][0-9]-*/paper.json")):
        p = json.loads(manifest.read_text(encoding='utf-8'))
        links = p.get('links', {})
        outputs = p.get('outputs', {})
        activity = dashboard.get("projects", {}).get(str(p.get("id")), {}).get("activity", "")
        en = outputs.get('paper_en') in {'complete','final'}
        zh = outputs.get('paper_zh') in {'complete','final'}
        en_pdf_link = str(links.get('paper_en_pdf', '') or '').strip()
        zh_pdf_link = str(links.get('paper_zh_pdf', '') or '').strip()

        def pdf_exists(link: str) -> bool:
            if not link:
                return False
            if link.startswith('paper/'):
                return (ROOT / 'docs' / link).is_file()
            if link.startswith(('https://', 'http://')):
                # External PDFs are link-audited elsewhere; presence of a declared stable URL
                # satisfies the local output audit.
                return True
            return (manifest.parent / link).is_file()

        en_pdf = pdf_exists(en_pdf_link)
        zh_pdf = pdf_exists(zh_pdf_link)
        fig = outputs.get('figures', {}) if isinstance(outputs.get('figures'), dict) else {}
        tab = outputs.get('tables', {}) if isinstance(outputs.get('tables'), dict) else {}
        fig_count = int(fig.get('count', 0) or 0)
        tab_count = int(tab.get('count', 0) or 0)
        exception = str(outputs.get('exception', '') or '').strip()
        visuals_ok = (fig_count > 0 and tab_count > 0) or bool(exception)
        status = p.get('status','')
        pdf_required = bool(FINAL_RE.search(status))
        pdf_ok = (en_pdf and zh_pdf) if pdf_required else True
        handoff_dir = manifest.parent / "handoff"
        handoff_ok = all((handoff_dir / name).is_file() and (handoff_dir / name).read_text(encoding="utf-8").strip() for name in HANDOFF_REQUIRED)
        one_page = outputs.get("one_page_visual", {}) if isinstance(outputs.get("one_page_visual"), dict) else {}
        one_page_path = str(one_page.get("repo_path", "") or "").strip()
        one_page_ok = bool(one_page_path) and (ROOT / one_page_path).is_file()
        finish_visual_ok = one_page_ok if activity == "finish" else True
        complete = en and zh and visuals_ok and pdf_ok and handoff_ok and finish_visual_ok
        rows.append((p['id'], status, activity, en, zh, en_pdf, zh_pdf, fig_count, tab_count, handoff_ok, one_page_ok, complete, exception))

    print('| ID | status | activity | EN | ZH | EN PDF | ZH PDF | figures | tables | handoff | one-page visual | output gate |')
    print('|---|---|---|---:|---:|---:|---:|---:|---:|---|---|---|')
    failures = []
    for pid,status,activity,en,zh,en_pdf,zh_pdf,figs,tabs,handoff_ok,one_page_ok,complete,exception in rows:
        gate = 'PASS' if complete else ('OPEN' if not FINAL_RE.search(status) and activity != "finish" else 'FAIL')
        print(f'| {pid} | {status} | {activity} | {"Y" if en else "N"} | {"Y" if zh else "N"} | {"Y" if en_pdf else "N"} | {"Y" if zh_pdf else "N"} | {figs} | {tabs} | {"Y" if handoff_ok else "N"} | {"Y" if one_page_ok else "N"} | {gate} |')
        if (FINAL_RE.search(status) or activity == "finish") and not complete:
            failures.append(pid)
    if failures:
        print('\nFinal/submission projects missing required outputs: ' + ', '.join(failures))
        return 1
    return 0

if __name__ == '__main__':
    raise SystemExit(main())

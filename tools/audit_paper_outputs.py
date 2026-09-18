#!/usr/bin/env python3
"""Audit ARIS4C final-output completeness without collapsing scientific quality to one score."""

from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PAPERS = ROOT / "papers"

FINAL_RE = re.compile(r"(^|[-_])(final|final-manuscript|submission-ready|submission-package-ready)($|[-_])", re.I)

def main() -> int:
    rows = []
    for manifest in sorted(PAPERS.glob("[0-9][0-9][0-9]-*/paper.json")):
        p = json.loads(manifest.read_text(encoding='utf-8'))
        links = p.get('links', {})
        outputs = p.get('outputs', {})
        en = outputs.get('paper_en') in {'complete','final'}
        zh = outputs.get('paper_zh') in {'complete','final'}
        fig = outputs.get('figures', {}) if isinstance(outputs.get('figures'), dict) else {}
        tab = outputs.get('tables', {}) if isinstance(outputs.get('tables'), dict) else {}
        fig_count = int(fig.get('count', 0) or 0)
        tab_count = int(tab.get('count', 0) or 0)
        exception = str(outputs.get('exception', '') or '').strip()
        complete = en and zh and ((fig_count > 0 and tab_count > 0) or bool(exception))
        rows.append((p['id'], p.get('status',''), en, zh, fig_count, tab_count, complete, exception))

    print('| ID | status | EN | ZH | figures | tables | output gate |')
    print('|---|---|---:|---:|---:|---:|---|')
    failures = []
    for pid,status,en,zh,figs,tabs,complete,exception in rows:
        gate = 'PASS' if complete else ('OPEN' if not FINAL_RE.search(status) else 'FAIL')
        print(f'| {pid} | {status} | {"Y" if en else "N"} | {"Y" if zh else "N"} | {figs} | {tabs} | {gate} |')
        if FINAL_RE.search(status) and not complete:
            failures.append(pid)
    if failures:
        print('\nFinal/submission projects missing required outputs: ' + ', '.join(failures))
        return 1
    return 0

if __name__ == '__main__':
    raise SystemExit(main())

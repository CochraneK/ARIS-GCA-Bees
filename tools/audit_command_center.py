#!/usr/bin/env python3
"""Audit user-facing ARIS4C command-center visibility and control invariants."""
from __future__ import annotations

import json
import re
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
INDEX=ROOT/"docs"/"index.html"
JS=ROOT/"docs"/"command-center.js"
PAPERS=ROOT/"papers"
DASH=PAPERS/"dashboard.json"

def fail(msg:str)->None:
    raise SystemExit("COMMAND_CENTER_AUDIT_FAIL: "+msg)

def main()->None:
    html=INDEX.read_text(encoding="utf-8")
    js=JS.read_text(encoding="utf-8")
    dashboard=json.loads(DASH.read_text(encoding="utf-8"))
    manifests=sorted(PAPERS.glob("[0-9][0-9][0-9]-*/paper.json"))
    ids=[str(json.loads(p.read_text(encoding="utf-8")).get("id")) for p in manifests]

    # Complete portfolio visibility: every paper must remain in BOTH the rolling
    # showcase and the detailed-card surface, regardless of progress/state.
    for pid in ids:
        if not re.search(rf'class="showcase-card"[^>]*data-showcase-original="true"[^>]*data-id="{re.escape(pid)}"',html):
            fail(f"paper {pid} missing from All-projects showcase")
        if not re.search(rf'class="paper-card"[^>]*data-id="{re.escape(pid)}"',html):
            fail(f"paper {pid} missing from detailed portfolio cards")

    required_controls={
        "navFinishCount":"Finish navigation",
        "navActiveCount":"Active navigation",
        "navWaitCount":"Wait navigation",
        "navBlockCount":"Block navigation",
        "clearFilters":"Reset button",
        "themeToggle":"theme button",
        "showcasePrev":"showcase previous button",
        "showcaseNext":"showcase next button",
        "searchInput":"search input",
        "sortFilter":"sort control",
    }
    for dom_id,label in required_controls.items():
        if f'id="{dom_id}"' not in html:
            fail(f"{label} is missing from generated HTML")

    # Ensure the JS still wires the key control families.
    for token in ('[data-filter]','clearFilters','themeToggle','showcasePrev','showcaseNext','searchInput','sortFilter'):
        if token not in js:
            fail(f"control wiring token missing from JS: {token}")

    # The progress chart must use a visibly disclosed discontinuous time axis
    # so long computer-idle gaps cannot dominate the horizontal geometry.
    for token in ("idleThreshold","compressedIdleSpan","history-idle-break","Compressed inactive gap"):
        if token not in js:
            fail(f"idle-gap compression invariant missing from JS: {token}")

    m=re.search(r'<script id="progressHistoryData" type="application/json">(.*?)</script>',html,re.S)
    if not m:
        fail("progressHistoryData payload missing")
    history=json.loads(m.group(1))
    points=history.get("points",[]) or []
    chart_ids=set(map(str,history.get("chart_project_ids",[]) or []))
    finish_ids={
        str(pid) for pid,meta in dashboard.get("projects",{}).items()
        if str(meta.get("activity","")).lower()=="finish"
    }

    if chart_ids & finish_ids:
        fail(f"Finish papers leaked into today's curve: {sorted(chart_ids & finish_ids)}")

    seen={}
    for point in points:
        for pid,val in (point.get("projects",{}) or {}).items():
            pid=str(pid)
            if pid not in chart_ids:
                fail(f"history point contains non-chart project {pid}")
            seen.setdefault(pid,[]).append(int(val))

    for pid in chart_ids:
        values=seen.get(pid,[])
        if len(values)<2 or len(set(values))<2:
            fail(f"paper {pid} is on today's curve without measurable progress today")

    print(json.dumps({
        "status":"PASS",
        "portfolio_papers":len(ids),
        "chart_papers":len(chart_ids),
        "finish_hidden_from_curve":len(finish_ids),
        "controls_checked":len(required_controls),
        "chart_rule":history.get("chart_rule"),
    },indent=2))

if __name__=="__main__":
    main()

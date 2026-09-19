"""Validate ARIS4C010 pre-results SVG figures."""

from __future__ import annotations

import xml.etree.ElementTree as ET
from pathlib import Path

HERE=Path(__file__).resolve().parent
ROOT=HERE.parent
FIG=ROOT/"figures"
EXPECTED={
    "fig01_semantic_query_overhead.svg",
    "fig02_response_protocols.svg",
    "fig03_evidence_ladder.svg",
}


def main():
    files={p.name for p in FIG.glob("*.svg")}
    missing=EXPECTED-files
    assert not missing, f"missing figures: {sorted(missing)}"

    for name in sorted(EXPECTED):
        path=FIG/name
        root=ET.parse(path).getroot()
        assert root.tag.endswith("svg")
        viewbox=root.attrib.get("viewBox")
        assert viewbox=="0 0 1200 700", (name,viewbox)
        titles=[x.text for x in root.iter() if x.tag.endswith("title")]
        assert titles and titles[0].strip(), name

    print("PASS pre-results figure validation")
    print("SVG figures:",len(EXPECTED))
    print("viewBox: 1200x700")


if __name__=="__main__":
    main()

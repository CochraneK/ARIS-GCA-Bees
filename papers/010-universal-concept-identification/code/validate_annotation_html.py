"""Validate standalone UCID annotation HTML bundle."""

from __future__ import annotations
from pathlib import Path

HERE=Path(__file__).resolve().parent
ROOT=HERE.parent
OUT=ROOT/"data"/"human_forms"/"html"


def main():
    pages=sorted(p for p in OUT.glob("*.html") if p.name!="index.html")
    assert len(pages)==108
    assert (OUT/"index.html").exists()
    for page in pages:
        text=page.read_text(encoding="utf-8")
        assert "phenomenon_tags" not in text
        assert '"is_retest"' not in text
        assert "fetch(" not in text
        assert "XMLHttpRequest" not in text
        assert "download()" in text
        assert "response_time_ms" in text
    print("PASS standalone HTML validation")
    print("participant pages: 108")
    print("network submission code: none")


if __name__=="__main__":
    main()

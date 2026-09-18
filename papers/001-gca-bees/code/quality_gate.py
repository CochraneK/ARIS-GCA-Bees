"""Fail CI if retired legacy claims re-enter canonical Paper 001 outputs.

Historical/adversarial audit files may quote a retired claim in order to reject it.
"""

from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
TARGETS = [
    ROOT / "papers" / "001-gca-bees" / "paper.json",
    ROOT / "papers" / "001-gca-bees" / "README.md",
    ROOT / "papers" / "001-gca-bees" / "manuscript",
    ROOT / "docs" / "paper" / "en" / "main.html",
    ROOT / "docs" / "paper" / "zh" / "main.html",
]

BANNED = {
    "83.5%": "legacy circular GCA-variance result",
    "r = -0.658": "legacy simulated metacognition-GCA correlation",
    "-0.658 → +0.730": "legacy simulated sign-flip claim",
    "p*=0.563": "legacy grid-search optimum",
    "p^*= 0.563": "legacy grid-search optimum",
    "first formal computational theory of insect functional self-awareness": "retired priority/mechanism claim",
}

failures = []
for target in TARGETS:
    files = [target] if target.is_file() else list(target.rglob("*"))
    for file in files:
        if not file.is_file() or file.suffix.lower() not in {".md", ".json", ".html", ".py"}:
            continue
        text = file.read_text(encoding="utf-8", errors="ignore")
        for token, reason in BANNED.items():
            if token in text:
                failures.append(f"{file.relative_to(ROOT)}: {reason} ({token})")

if failures:
    raise SystemExit("Retired Paper 001 claims detected:\n" + "\n".join(failures))

print("Paper 001 stale-claim gate passed.")

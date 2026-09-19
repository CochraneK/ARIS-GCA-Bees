#!/usr/bin/env python3
"""Build a LOCAL-ONLY blinded boundary-calibration packet for ARIS4C009.

The default output lives under paper data/raw/, which is gitignored. This script
intentionally writes source text for independent AI judges and therefore MUST NOT be
used to publish GitHub artifacts or committed outputs.
"""

from __future__ import annotations

import argparse
import csv
import html
import json
import random
import re
import zipfile
from collections import defaultdict
from pathlib import Path
from xml.etree import ElementTree as ET

BLOCK = re.compile(
    r"<(INT|[0-9]{2}[A-Z]{2,3}[0-9]{2})>(.*?)</\1>",
    re.DOTALL | re.IGNORECASE,
)
TIMESTAMP = re.compile(r"#\d{2}:\d{2}:\d{2}(?:[-.]\d+)?#")
XML_TAG = re.compile(r"<[^>]+>")
RTF_CONTROL = re.compile(r"\\[A-Za-z]+-?\d* ?")
WORD = re.compile(r"\b[\w'-]+\b", re.UNICODE)
TARGETS = (20, 40)


def read_docx(path: Path) -> str | None:
    try:
        with zipfile.ZipFile(path) as zf:
            raw = zf.read("word/document.xml")
        root = ET.fromstring(raw)
        ns = {"w": "http://schemas.openxmlformats.org/wordprocessingml/2006/main"}
        paras = []
        for p in root.findall(".//w:p", ns):
            bits = []
            for node in p.iter():
                if node.tag.endswith("}t") and node.text:
                    bits.append(node.text)
                elif node.tag.endswith("}tab"):
                    bits.append("\t")
                elif node.tag.endswith("}br"):
                    bits.append("\n")
            if bits:
                paras.append("".join(bits))
        return "\n".join(paras)
    except Exception:
        return None


def read_text(path: Path) -> str | None:
    if path.suffix.lower() == ".docx":
        return read_docx(path)
    for enc in ("utf-8", "latin-1"):
        try:
            return html.unescape(path.read_text(encoding=enc))
        except UnicodeDecodeError:
            continue
        except Exception:
            return None
    return None


def clean_visible(text: str) -> str:
    text = XML_TAG.sub(" ", text)
    text = RTF_CONTROL.sub(" ", text)
    text = text.replace("{", " ").replace("}", " ")
    text = re.sub(r"\s+", " ", text).strip()
    return text


def wc(text: str) -> int:
    return len(WORD.findall(text))


def cohort(path: Path) -> str:
    parts = {x.upper() for x in path.parts}
    if "DAI-C-CL" in parts:
        return "clinical"
    if "DAI-C-CO" in parts:
        return "comparison"
    return "unknown"


def parse_microepisodes(text: str) -> list[dict]:
    blocks = []
    for tag, body in BLOCK.findall(text):
        role = "interviewer" if tag.upper() == "INT" else "participant"
        visible = clean_visible(body)
        blocks.append((role, visible, wc(visible)))

    episodes = []
    current = None
    idx = 0
    for role, visible, words in blocks:
        if role == "interviewer":
            if current is not None:
                episodes.append(current)
                idx += 1
            current = {
                "micro_index": idx,
                "interviewer": visible,
                "participant_parts": [],
                "participant_words": 0,
            }
        elif current is not None:
            current["participant_parts"].append(visible)
            current["participant_words"] += words

    if current is not None:
        episodes.append(current)
    return episodes


def windows_for(micro: list[dict], target: int, source: str, group: str) -> list[dict]:
    windows = []
    current = None

    def finish(cur):
        if cur is None:
            return
        cur["participant_text"] = "\n".join(
            p for p in cur.pop("participant_parts") if p
        )
        cur["interview_text"] = "\n".join(cur.pop("display_parts"))
        windows.append(cur)

    for ep in micro:
        if current is None:
            current = {
                "source": source,
                "cohort": group,
                "target": target,
                "start_micro": ep["micro_index"],
                "end_micro": ep["micro_index"],
                "participant_words": 0,
                "participant_parts": [],
                "display_parts": [],
            }

        current["end_micro"] = ep["micro_index"]
        current["participant_words"] += ep["participant_words"]
        current["participant_parts"].extend(ep["participant_parts"])
        current["display_parts"].append(f"INTERVIEWER: {ep['interviewer']}")
        participant = " ".join(ep["participant_parts"]).strip()
        current["display_parts"].append(f"PARTICIPANT: {participant}")

        if current["participant_words"] >= target:
            finish(current)
            current = None

    finish(current)
    return windows


def overlaps(a: dict, b: dict) -> bool:
    return (
        a["source"] == b["source"]
        and not (
            a["end_micro"] < b["start_micro"]
            or b["end_micro"] < a["start_micro"]
        )
    )


def take_nonoverlap(candidates: list[dict], n: int, used: list[dict], rng: random.Random) -> list[dict]:
    candidates = candidates[:]
    rng.shuffle(candidates)
    chosen = []
    for item in candidates:
        if any(overlaps(item, other) for other in used + chosen):
            continue
        chosen.append(item)
        if len(chosen) == n:
            break
    if len(chosen) < n:
        raise RuntimeError(f"Could select only {len(chosen)} of requested {n} non-overlapping items")
    used.extend(chosen)
    return chosen


def write_judge(path: Path, items: list[dict], rng: random.Random) -> None:
    rows = items[:]
    rng.shuffle(rows)
    fields = [
        "item_id",
        "interview_text",
        "coherent_boundary",
        "sufficient_nontrivial",
        "mixed_unrelated_topics",
        "recommended_action",
        "confidence_1_5",
        "notes",
    ]
    with path.open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fields, delimiter="\t", quoting=csv.QUOTE_MINIMAL)
        w.writeheader()
        for x in rows:
            w.writerow({
                "item_id": x["item_id"],
                "interview_text": x["interview_text"].replace("\t", " "),
                "coherent_boundary": "",
                "sufficient_nontrivial": "",
                "mixed_unrelated_topics": "",
                "recommended_action": "",
                "confidence_1_5": "",
                "notes": "",
            })


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", required=True, help="Extracted DAIS-C root")
    ap.add_argument(
        "--out",
        default="papers/009-phenomenology-preserving-computational-psychiatry/data/raw/boundary_calibration",
    )
    ap.add_argument("--seed", type=int, default=20260919)
    ap.add_argument("--regular-per-condition", type=int, default=60)
    ap.add_argument("--stress-per-condition", type=int, default=10)
    ap.add_argument("--training-items", type=int, default=20)
    ap.add_argument("--judge-count", type=int, default=3)
    args = ap.parse_args()

    if args.judge_count < 2:
        raise ValueError("--judge-count must be at least 2; 3+ materially different models are recommended")

    rng = random.Random(args.seed)
    root = Path(args.root)
    out = Path(args.out)
    out.mkdir(parents=True, exist_ok=True)

    by_target = {t: [] for t in TARGETS}

    for path in root.rglob("*"):
        if not path.is_file() or path.suffix.lower() not in {".docx", ".rtf"}:
            continue
        if "Full tagged pass" not in str(path) or "Speaker_only_for_analysis" in str(path):
            continue
        text = read_text(path)
        if text is None or len(TIMESTAMP.findall(text)) >= 3:
            continue
        tags = [t.upper() for t, _ in BLOCK.findall(text)]
        if "INT" not in tags or not any(t != "INT" for t in tags):
            continue

        rel = str(path.relative_to(root))
        micro = parse_microepisodes(text)
        for target in TARGETS:
            by_target[target].extend(windows_for(micro, target, rel, cohort(path)))

    condition_labels = ["A", "B"]
    rng.shuffle(condition_labels)
    target_to_condition = dict(zip(TARGETS, condition_labels))

    selected = []
    used = []

    for target in TARGETS:
        cond = target_to_condition[target]
        per_cohort = args.regular_per_condition // 2
        for group in ("clinical", "comparison"):
            regular = [
                x for x in by_target[target]
                if x["cohort"] == group
                and target <= x["participant_words"] <= 250
            ]
            chosen = take_nonoverlap(regular, per_cohort, used, rng)
            for x in chosen:
                x["condition"] = cond
                x["stratum"] = "regular"
                selected.append(x)

        stress = [
            x for x in by_target[target]
            if x["participant_words"] < target or x["participant_words"] > 250
        ]
        chosen = take_nonoverlap(stress, args.stress_per_condition, used, rng)
        for x in chosen:
            x["condition"] = cond
            x["stratum"] = "stress"
            selected.append(x)

    # Draw discussion-allowed training items from source regions not used by the
    # independent primary/stress packet.
    if args.training_items % 4 != 0:
        raise ValueError("--training-items must be divisible by 4 for target/cohort balance")

    training = []
    training_per_target_cohort = args.training_items // 4
    for target in TARGETS:
        cond = target_to_condition[target]
        for group in ("clinical", "comparison"):
            candidates = [
                x for x in by_target[target]
                if x["cohort"] == group
                and target <= x["participant_words"] <= 250
            ]
            chosen = take_nonoverlap(candidates, training_per_target_cohort, used, rng)
            for x in chosen:
                x["condition"] = cond
                x["stratum"] = "training"
                training.append(x)

    rng.shuffle(selected)
    for i, x in enumerate(selected, 1):
        x["item_id"] = f"BC{i:04d}"

    rng.shuffle(training)
    for i, x in enumerate(training, 1):
        x["item_id"] = f"TR{i:03d}"

    for j in range(1, args.judge_count + 1):
        write_judge(
            out / f"judge_{j:02d}.tsv",
            selected,
            random.Random(args.seed + j),
        )
        write_judge(
            out / f"training_judge_{j:02d}.tsv",
            training,
            random.Random(args.seed + 100 + j),
        )

    manifest = {
        "warning": "PRIVATE EXECUTION METADATA TEMPLATE. DO NOT COMMIT IF IT CONTAINS SENSITIVE ENDPOINT DETAILS.",
        "required_judge_count": args.judge_count,
        "judges": [
            {
                "judge_file": f"judge_{j:02d}.tsv",
                "provider": "",
                "model_family": "",
                "model_version": "",
                "execution_date": "",
                "temperature_or_determinism": "",
                "data_handling_mode": "",
                "prompt_file": "process/AI_JUDGE_PROMPT_BOUNDARY.md",
            }
            for j in range(1, args.judge_count + 1)
        ],
    }
    (out / "judge_manifest.template.json").write_text(
        json.dumps(manifest, indent=2) + "\n", encoding="utf-8"
    )

    key = {
        "seed": args.seed,
        "warning": "PRIVATE LOCAL KEY. DO NOT COMMIT OR UPLOAD.",
        "condition_map": {v: k for k, v in target_to_condition.items()},
        "items": {
            x["item_id"]: {
                "condition": x["condition"],
                "target": x["target"],
                "stratum": x["stratum"],
                "cohort": x["cohort"],
                "source": x["source"],
                "start_micro": x["start_micro"],
                "end_micro": x["end_micro"],
                "participant_words": x["participant_words"],
            }
            for x in selected
        },
    }
    (out / "private_key.json").write_text(
        json.dumps(key, indent=2) + "\n", encoding="utf-8"
    )

    training_key = {
        "seed": args.seed,
        "warning": "PRIVATE TRAINING KEY. MAY BE OPENED ONLY FOR DISCUSSION TRAINING.",
        "condition_map": {v: k for k, v in target_to_condition.items()},
        "items": {
            x["item_id"]: {
                "condition": x["condition"],
                "target": x["target"],
                "cohort": x["cohort"],
                "source": x["source"],
                "start_micro": x["start_micro"],
                "end_micro": x["end_micro"],
                "participant_words": x["participant_words"],
            }
            for x in training
        },
    }
    (out / "training_key.json").write_text(
        json.dumps(training_key, indent=2) + "\n", encoding="utf-8"
    )

    readme = """# ARIS4C009 AI boundary calibration packet — PRIVATE

Do not commit or upload this directory.

## Judge architecture

Use at least three materially different model families/providers where feasible.

Each model receives:
- the same frozen prompt from process/AI_JUDGE_PROMPT_BOUNDARY.md;
- its own independently shuffled judge file;
- no access to another judge's output;
- no access to private_key.json.

Generated primary files are judge_01.tsv, judge_02.tsv, ... .
Generated dry-run files are training_judge_01.tsv, training_judge_02.tsv, ... .

The 20 training windows are for parser/refusal/instruction-following dry runs only.
They never enter the primary agreement estimate and judges do not discuss or reconcile them.

## Allowed values

- coherent_boundary: yes / no
- sufficient_nontrivial: yes / no
- mixed_unrelated_topics: yes / no
- recommended_action: keep / merge / split / reject
- confidence_1_5: 1–5

Do not inspect private_key.json until all primary judge outputs are frozen.

Primary calibration excludes items marked as stress in the private key.

After all judges finish, run score_boundary_ratings.py with repeated --judge arguments
to produce an aggregate, public-safe cross-model summary.

## Privacy

Only use local models or external endpoints whose data-use and retention terms are
compatible with the source-data governance. Never upload this packet as a public CI
artifact.
"""
    (out / "README_PRIVATE.md").write_text(readme, encoding="utf-8")

    print(
        f"Wrote private packet with {len(selected)} primary/stress items "
        f"and {len(training)} disjoint training items to {out}"
    )
    print("Do not commit or upload the packet directory.")


if __name__ == "__main__":
    main()

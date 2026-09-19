#!/usr/bin/env python3
"""Publish public-safe ARIS4C009 AI boundary-calibration artifacts.

Reads the aggregate scorer output plus the per-judge execution manifests and writes a
reviewed, aggregate-only copy under paper data/derived/. Source text, packet rows and
local absolute paths never enter the published artifacts.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import textwrap
from pathlib import Path

REGISTRY_KEYS = (
    "judge_file", "packet_file", "provider", "model_family", "model_version",
    "endpoint_reported_models", "execution_date", "temperature_or_determinism",
    "data_handling_mode", "prompt_file", "items_total", "items_rated", "items_failed",
)
PRIVATE_MARKERS = ("INTERVIEWER:", "PARTICIPANT:")


def strip_private_strings(obj):
    if isinstance(obj, dict):
        return {k: strip_private_strings(v) for k, v in obj.items()}
    if isinstance(obj, list):
        return [strip_private_strings(v) for v in obj]
    if isinstance(obj, str) and any(marker in obj for marker in PRIVATE_MARKERS):
        raise ValueError("refusing to publish an artifact that contains source speech")
    return obj


def wrap(text: str) -> list[str]:
    """Free text becomes short lines so JSON stays reviewable and length heuristics stay meaningful."""
    return textwrap.wrap(" ".join(text.split()), 160)


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--score-json", required=True)
    ap.add_argument("--score-md", required=True)
    ap.add_argument("--manifest", action="append", required=True,
                    help="judge manifest written by run_ai_boundary_judges.py; repeat per judge")
    ap.add_argument("--excluded-manifest", action="append", default=[],
                    help="manifest for a judge run excluded from the ensemble; repeat as needed")
    ap.add_argument("--reason", default="", help="why excluded runs were dropped")
    ap.add_argument("--out-dir", required=True)
    ap.add_argument("--prompt-file", default="papers/009-phenomenology-preserving-computational-psychiatry/"
                                            "process/AI_JUDGE_PROMPT_BOUNDARY.md",
                    help="frozen prompt re-hashed here to confirm the judges used it")
    ap.add_argument("--run-date", default="")
    ap.add_argument("--packet-seed", type=int, default=20260919)
    args = ap.parse_args()

    out = Path(args.out_dir)
    out.mkdir(parents=True, exist_ok=True)

    score = strip_private_strings(json.loads(Path(args.score_json).read_text(encoding="utf-8")))
    records = []
    for path in args.manifest + args.excluded_manifest:
        manifest = json.loads(Path(path).read_text(encoding="utf-8"))
        sha, base = manifest.get("prompt_sha256", ""), manifest.get("endpoint_base_url", "")
        if not sha or not base:
            raise ValueError(f"manifest {path} is missing prompt_sha256 or endpoint_base_url")
        for judge in manifest["judges"]:
            records.append((judge, sha, base, manifest.get("manifest_note", "")))

    def provenance(judge, sha, base, note):
        entry = {k: judge.get(k) for k in REGISTRY_KEYS} | {
            "judge_label": Path(judge["judge_file"]).stem,
            "prompt_sha256": sha,
            "endpoint_base_url": base,
        }
        if note:
            entry["manifest_note"] = note
        return entry

    labeled = {str(label) for label in score["judge_labels"]}
    judges = sorted(
        (provenance(*rec) for rec in records if Path(rec[0]["judge_file"]).stem in labeled),
        key=lambda x: x["judge_file"])
    excluded = sorted(
        (provenance(*rec) for rec in records if Path(rec[0]["judge_file"]).stem not in labeled),
        key=lambda x: x["judge_file"])

    missing = sorted(labeled - {j["judge_label"] for j in judges})
    if missing:
        raise ValueError(f"no manifest provenance for published judges: {missing}")
    prompt_shas = {j["prompt_sha256"] for j in judges}
    if len(prompt_shas) > 1:
        raise ValueError(f"judges did not share one frozen prompt: {sorted(prompt_shas)}")
    # The executor hashes the prompt as read in text mode, so compare against LF bytes.
    frozen_sha = hashlib.sha256(
        Path(args.prompt_file).read_bytes().replace(b"\r\n", b"\n")).hexdigest()
    if prompt_shas and frozen_sha not in prompt_shas:
        raise ValueError(f"prompt {args.prompt_file} no longer matches the judged prompt: "
                         f"{frozen_sha} vs {sorted(prompt_shas)}")
    for judge in judges:
        if judge["items_failed"] != 0 or judge["items_rated"] != judge["items_total"]:
            raise ValueError(f"judge {judge['judge_file']} is not complete: {judge}")
    if excluded and not args.reason:
        raise ValueError("excluded runs must be disclosed: pass --reason")

    registry = {
        "warning": "Aggregate execution provenance only. Contains no interview text.",
        "run_date": args.run_date,
        "prompt_file": "papers/009-phenomenology-preserving-computational-psychiatry/"
                       "process/AI_JUDGE_PROMPT_BOUNDARY.md",
        "prompt_sha256": prompt_shas.pop() if prompt_shas else "",
        "endpoint_base_url": judges[0]["endpoint_base_url"] if judges else "",
        "packet_seed": args.packet_seed,
        "packet": {
            "items_per_judge": judges[0]["items_total"] if judges else None,
            "regular_items_scored": score["regular_items_scored"],
            "strata": "primary regular + stress windows; a disjoint training set was used for dry runs only",
        },
        "judges": judges,
        "independence": wrap("Each judge received only its own independently shuffled item file and the "
                             "frozen prompt; no judge saw another judge's output or the private key."),
        "excluded_runs": excluded,
        "exclusion_reason": wrap(args.reason),
        "interpretation_boundary": wrap("Cross-model AI-judge agreement is an engineering calibration "
                                        "signal, not human inter-rater reliability."),
    }
    strip_private_strings(registry)

    markdown = strip_private_strings(Path(args.score_md).read_text(encoding="utf-8"))
    (out / "boundary_score.json").write_text(json.dumps(score, indent=2) + "\n", encoding="utf-8")
    (out / "judge_registry.json").write_text(json.dumps(registry, indent=2) + "\n", encoding="utf-8")
    (out / "boundary_score.md").write_text(markdown, encoding="utf-8")
    print(f"Published {len(judges)} judge records "
          f"(+{len(excluded)} excluded) to {out}")


if __name__ == "__main__":
    main()

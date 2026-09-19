# ARIS4C011 · Confirmatory freeze protocol

Status: **PRE_FREEZE**  
Machine contract: `data/protocol/confirmatory_freeze_v0.json`

## Purpose

The development pilots are deliberately enriched and have influenced detector design, artifact acquisition, applicability rules, controls, and comparator selection. They therefore cannot be recycled into confirmatory performance estimation.

Before any confirmatory score is computed, ARIS4C011 must freeze a broader time-safe corpus and prove four separations:

1. **development separation** — every DOI exposed through structured seed/pilot artifacts is excluded from the confirmatory manifest;
2. **split separation** — a DOI and every non-empty known/text/image cluster stay within exactly one split;
3. **temporal separation** — the temporal test slice uses outcomes strictly after a prespecified development cutoff;
4. **label separation** — Track A contains only allowlisted content fields and no notice/retraction/correction/ground-truth fields or status tokens.

## Development-contamination registry

`code/build_development_exclusion_registry.py` builds a conservative denylist from structured files under:

- `data/seed/`;
- `data/pilot/`;
- `data/results/pilot*`.

The registry intentionally over-excludes rather than trying to recover statistical efficiency from papers already visible during development. Once the confirmatory protocol is frozen, the registry must itself be versioned/frozen; newly scored confirmatory papers must not be retroactively added to the development registry.

## Split contract

The eventual confirmatory manifest must contain at least `target_doi` and `split`. When available, `known_cluster_id`, `text_cluster_id`, and `image_cluster_id` are group constraints, not model features.

A confirmatory manifest fails preflight if:

- a development DOI is reused;
- one DOI appears in more than one split;
- any non-empty grouping cluster crosses splits;
- a temporal-test outcome is not strictly after the frozen cutoff;
- the cutoff is missing when a temporal slice is present.

## Track A leakage contract

Track A remains content-only. The manifest allowlist and feature allowlist are machine-readable in the contract and mirror the benchmark-v0 design. Notice reason/type/date, correction/retraction metadata, ground-truth labels, outcome fields, assertion/update relations, and explicit status tokens are forbidden.

## Freeze gate

`code/confirmatory_preflight.py` is informative while the contract state is `PRE_FREEZE`. It may produce a valid report whose result is **NOT READY**. This is expected and is not a scientific failure.

Confirmatory scoring becomes authorized only after:

- the broader time-safe corpus and SAFE_EXACT / PROXY_ONLY / BLOCKED attrition are frozen;
- grouped + temporal manifests and cutoff are frozen;
- detector versions, known-defect policy, applicability rules, and thresholds are frozen;
- the label-leakage audit passes;
- human-review procedure and reviewer-burden measure are frozen;
- every machine freeze gate is true;
- the final preflight has zero blockers.

Until then, Pilot 2/3 outputs remain descriptive development evidence only.

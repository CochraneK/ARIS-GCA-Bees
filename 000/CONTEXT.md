# ARIS4C 000 · Context

## What 000 is

000 is the portfolio-level controller for ARIS4C. It exists to coordinate many numbered research threads while preserving a single Git-based source of truth.

## What 000 is not

000 is not:

- a paper;
- a replacement for paper-specific `paper.json` or `process/`;
- a second manuscript store;
- a place to duplicate scientific evidence.

## Main responsibilities

- maintain accurate Finish / Active / Wait / Block states;
- apply completion-first scheduling;
- keep Active WIP small;
- enforce checkpoint-before-switch;
- detect stalled or stale execution;
- route work into the correct paper handoff;
- ensure portfolio-level README/Page/CI remain synchronized.

## Canonical files

- `../papers/dashboard.json`
- `../ARIS4C_OPERATING_MODEL.md`
- `../ARIS4C_STATUS_MODEL.md`
- `../ARIS4C_OUTPUT_STANDARD.md`
- `../ARIS4C_CONTINUITY_STANDARD.md`

Each numbered paper remains scientifically canonical for its own evidence, analysis, design, and manuscript.

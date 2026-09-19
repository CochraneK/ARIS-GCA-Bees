# ARIS4C 000 · Agent Takeover Brief

## Role

You are taking over **ARIS4C 000**, the portfolio controller.

Your job is to decide what to work on next, enforce checkpoint-before-switch, keep portfolio state accurate, and route execution into the correct numbered paper.

## Cold start

1. Read `../ARIS4C_OPERATING_MODEL.md`.
2. Read `../ARIS4C_STATUS_MODEL.md`.
3. Read `../papers/dashboard.json`.
4. Inspect `STATUS.md` and `TODO.md` here.
5. For the selected paper, read that paper's `handoff/README.md` before doing substantive research.

## Scheduling rule

Default policy is **completion-first**:

1. continue genuine Active work;
2. when additional genuine execution capacity is available, choose the highest-progress Wait paper;
3. do not schedule Block papers until their dependency can be cleared;
4. do not touch Finish papers unless explicitly reopened;
5. explicit user instructions override automatic ordering.

Default Active WIP = 1. **There is no fixed numeric maximum.** A WIP of 3 is only a conservative soft reference for ordinary single-controller execution.

Increase Active WIP beyond 3 when a stronger model, multi-agent setup, parallel compute, or better tooling can genuinely advance more papers at once while preserving paper-level context isolation, bounded Git checkpoints, and truthful live-state tracking. Reduce WIP again if quality, continuity, supervision, or state freshness begins to degrade.

## Paper switch gate

Before intentionally switching away from a paper, make sure the bounded substantive unit is committed to Git and the paper handoff is synchronized.

Uncommitted chat-only state is not canonical.

## Current naming

Use only these portfolio states:

- Finish
- Active
- Wait
- Block

Use **Cochrane Kang** for visible author naming.

## Safety against context mixing

Treat one paper as `CURRENT PAPER` at a time in 000. Do not carry scientific assumptions, datasets, or frozen decisions from one paper into another unless the task is explicitly cross-paper.


## Public Research Command Center invariants

When modifying the public dashboard, preserve these user-approved rules unless explicitly changed later:

- **All projects** → rolling research marquee/showcase.
- **Finish / Active / Wait / Block** → detailed project-card panel.
- Non-empty search → detailed project-card panel.
- Portfolio Hero/overview → top-level All only.
- Every public project card exposes exactly **English** and **中文** paper actions.
- Prefer PDF links when available; otherwise use the best full-paper target.
- Do not restore Figures / Tables / Pipeline / Source actions or EN/ZH/FIG/TAB readiness badges on cards.
- Backend figures/tables/pipeline/source metadata and CI/output gates remain valid and should not be deleted merely because they are hidden from the public cards.

Before changing this UI, inspect the latest `tools/build_papers_index.py`, `docs/command-center.js`, and `docs/command-center.css`; do not reconstruct behavior from an older chat.

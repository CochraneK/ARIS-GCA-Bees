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
2. when an Active slot is free, choose the highest-progress Wait paper;
3. do not schedule Block papers until their dependency can be cleared;
4. do not touch Finish papers unless explicitly reopened;
5. explicit user instructions override automatic ordering.

Default Active WIP = 1. Normal maximum = 3.

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

# ARIS4C004 · Agent takeover brief

## What this project is

**The Counterfactual Cost of Exclusion: Mental Health and Keystone Individuals in Human Knowledge Networks**

A sign-neutral counterfactual network study of how scientific, intellectual, and cultural development changes when the productive participation of historically realized contributors is reduced, with mental-health evidence, discrimination, adaptive substitution, identity uncertainty, and retrospective documentation handled as separate components.

## Current state

- Activity: **block**
- Progress: **74%** (portfolio estimate; not a scientific result)
- Stage: **P4 pre-exposure audit · independent identity second-review gate**
- Canonical process state: **P0–P3 complete**
- Identity100: **52 VERIFIED / 38 NO_GRAPH / 8 AMBIGUOUS_COLLISION / 2 EXCLUDED_IDENTITY_ERROR / 0 provisional**
- Work/network100: **2,956 unique person-work records, 0 fetch errors; 25/100 network-observable**
- Held VERIFIED identities: **13 insufficient clean works + 14 unresolved work contamination**, terminal for the frozen pre-exposure frame
- Required independent blind identity review: **40 cases**

No mental-health exposure coding has started.

## Immediate next action

**Have an independent reviewer complete the frozen 40-case blind identity review, then adjudicate disagreements and write/hash PREEXPOSURE_FRAME_FREEZE.md.**

Primary blind assignment:

`data/derived/identity_second_review_blind_assignment.csv`

Reviewer instructions:

`process/IDENTITY_SECOND_REVIEW_HANDOFF.md`

Protocol:

`process/IDENTITY_SECOND_REVIEW_PROTOCOL.md`

### Important independence constraint

The independent reviewer must not inspect before locking all 40 judgments:

- `data/derived/identity_decisions_100.csv`
- first-review notes/verdicts
- mental-health/exposure files
- CPE/network-removal results

The current assistant's own re-review does **not** count as independent.

## Current blocker / gate

The only scientific blocker to the pre-exposure freeze is the **external/independent 40-case identity second review and adjudication of disagreements**.

The earlier 334-work held-person audit is **not an open blocker anymore**. P3 was closed with terminal person-level work/network decisions:

- 25 released network-observable;
- 13 `HOLD_INSUFFICIENT_CLEAN_WORKS`;
- 14 `HOLD_UNRESOLVED_WORK_CONTAMINATION`.

Do not reopen held work corpora merely to increase N.

## Work that may continue while blocked

Without touching mental-health exposure:

- simulator calibration/validation plan against empirical star-loss shocks;
- simulation-based precision/N design;
- closest-prior-work / novelty review packet;
- preregistration/adversarial methods audit;
- manuscript methods/limitations skeleton.

## Canonical files / entry points

Read in this order:

1. `process/STATUS.md`
2. `process/NETWORK100_WORK_GATE_FREEZE.md`
3. `process/IDENTITY_SECOND_REVIEW_HANDOFF.md`
4. `process/IDENTITY_SECOND_REVIEW_PROTOCOL.md`
5. `data/derived/identity_decisions_100.csv`
6. `data/derived/network100_person_work_decisions_v1.csv`
7. `data/derived/observability_summary.json`
8. `data/derived/ford_observability_summary.json`
9. `process/PREEXPOSURE_EXIT_GATE.md`
10. `process/EXECUTION_PHASES.md`

Source:
https://github.com/CochraneK/ARIS4C/tree/main/papers/004-counterfactual-cost-of-exclusion

## Continuity note — 2026-09-19 pre-chat-deletion reconciliation

The live Git repository was re-read before the current ChatGPT conversation is deleted. Git is ahead of some earlier chat narration: any earlier statement that identity100 or the P3 work audit was still running is superseded by the committed canonical state above.

**Repository state, not deleted chat history, is the source of truth.**

## Before changing anything

1. Read `TODO.md`, `DECISIONS.md`, and newest `CHATLOG.md` / `SESSION_LOG.md`.
2. Preserve frozen/preregistered decisions unless an explicit amendment is recorded.
3. Do not broaden claims beyond current evidence.
4. Use **Cochrane Kang** for visible author naming.
5. Do not commit secrets, credentials, hidden chain-of-thought, or unnecessary sensitive personal data.
6. After material changes, update canonical research files first, then handoff files.

## Handoff completion rule

Before ending a substantial session:
- update `TODO.md`;
- append material decisions to `DECISIONS.md`;
- append a public-safe conversation summary to `CHATLOG.md`;
- append executed/validated work to `SESSION_LOG.md`.

# ARIS4C003 — Coder B Blind Bundle

## Purpose

This directory is the **only permitted input surface** for the independent
second IKES coding pass (Coder B).

The goal is procedural independence. Coder B must score historical
imperial/colonial knowledge entanglement without seeing Coder A scores and
without seeing contemporary country-by-discipline performance.

## WorkBuddy access rule

For the independent pass, WorkBuddy should read **only**:

1. `WORKBUDDY_HANDOFF.md`
2. `OUTPUT_TEMPLATE.md`

Do not browse upward into the parent paper directory. Do not search the repo for
IKES, Coder A, OpenAlex outcomes, ranking results, or prior ARIS interpretations.

If WorkBuddy has already seen any prohibited material in the same context, that
context is contaminated and must not be used as confirmatory Coder B.

## Explicitly prohibited

Do not read or retrieve:

- `../IKES_CODER_A.csv`
- `../IKES_CODER_A.md`
- `../AUTO_REVIEW.md`
- `../STATUS.md`
- `../GATE_CLOSURE_AUDIT.md`
- any OpenAlex country×discipline result;
- any QS/THE/Shanghai country/discipline result used for this project;
- any previous discussion predicting which disciplines should score high/low;
- any Coder B draft from another model/session.

## Allowed external evidence

Coder B may independently search historical scholarly literature needed to
score the rubric. Prefer peer-reviewed history-of-science/history-of-discipline
work, scholarly books, authoritative academic reference chapters, and
well-documented institutional/archival histories.

Modern rankings and modern country-by-discipline output/citation/collaboration
performance are prohibited.

## Output

Return one raw Markdown response exactly following
`WORKBUDDY_HANDOFF.md`. Do not edit it after the independent model produces it.

The untouched response will later be stored under
`process/gptpage/<date>_ikes-coder-b-raw.md` and ingested by the existing
ARIS4C003 validation pipeline.

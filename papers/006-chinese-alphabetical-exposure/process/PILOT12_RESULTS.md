# ARIS4C006 · Pilot 12 — within-author exposure variation

Last updated: 2026-09-18

## Verdict

**Prospectively frozen within-author exposure-variation gate: PASS.**

The longitudinal extension may remain in the research design.

GitHub Actions run: `35301296596`  
Artifact: `aris4c006-exposure-switch-pilot`

This is the corrected version using OpenAlex `primary_topic.field.id`.

## Prospective gate

Before reading the result:

Retain a within-author longitudinal exposure design only if:

1. >=50 sampled authors have >=3 exposure-defined years; and
2. >=50% of those authors have within-author field-exposure range >=0.05.

Otherwise within-author longitudinal exposure would be downgraded to secondary/exploratory.

## Result

Random recent seed authors: **100**

Authors with >=3 exposure-defined years:
- **70 / 100 = 70%**

Among those 70:
- median within-author exposure range: **0.0727**
- median within-author exposure SD: **0.0298**
- share with range >=0.05: **81.4%**
- share with range >=0.10: **32.9%**

Both predeclared gate conditions passed comfortably.

## Interpretation

Measured alphabetization exposure is not merely a static field label.

A substantial majority of sufficiently observed authors experience meaningful changes in the primary-topic-field convention environment over time.

This supports:
- time-varying prior exposure;
- within-author longitudinal analyses;
- separating stable surname vulnerability from changing institutional context.

## Caveat

The pilot used a random 2024 seed only to test exposure variation and therefore remains survivor-selected.

It does **not** define the confirmatory career cohort.

The final longitudinal sample must use the frozen entry-based cohort rule in `COHORT_PROTOCOL.md`.

## Exposure estimates in this pilot

The field-window estimates were based on small random convention samples and exist only to test whether within-author variation is structurally available.

They are not the final exposure table.

The confirmatory exposure will:
- use all eligible primary work types;
- use `primary_topic.field.id`;
- use the prior 3 complete years;
- apply exact chance correction;
- use canonical author IDs;
- apply exact LOAO subtraction;
- require `D^{-i}_{ct} >= 50`;
- use 3+ author convention estimation as mandatory robustness.

## Gate consequence

**Within-author longitudinal variation: PASS.**

The longitudinal extension remains eligible for one preregistered distal confirmatory slot, subject to final cohort/time-window freeze.

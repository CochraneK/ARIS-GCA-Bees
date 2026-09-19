# ARIS4C006 · Frozen execution-materialization acceptance rules

Last updated: 2026-09-19

These rules are frozen before the 26-field aggregate artifacts are inspected.

They govern only whether the outcome-blind materialized datasets are structurally adequate to proceed to preregistration lock.

## A. Final convention / exposure build

Expected structural grid:

- fields: all 26 OpenAlex primary-topic fields, IDs 11–36;
- convention source years: 2008–2024;
- focal exposure target years: 2011–2025;
- primary work types: article + conference-paper.

### Hard structural requirements

All must hold:

1. all 26 fields present;
2. all 442 field × source-year annual cells present (26 × 17);
3. all 390 field × focal-year rolling cells present (26 × 15);
4. no scientific outcome, H1/H2/H3 coefficient, p-value, or focal predictor-outcome association was computed;
5. every retained convention work has validated structured family-order evidence and canonical author IDs under the frozen builder;
6. primary field assignment is `primary_topic.field.id`.

### Information-support acceptance

Primary rolling field exposure:

- at least **95%** of the 390 field-year rolling cells must satisfy full-field `D >= 50`;
- every field must have at least **10 of 15** focal years with `D >= 50`.

3+ author robustness exposure:

- at least **80%** of rolling cells must satisfy `D3 >= 50`;
- every field must have at least **8 of 15** focal years with `D3 >= 50`.

If a field-year fails `D >= 50`, focal rows in that field-year are excluded by the frozen LOAO rule rather than assigned a fallback exposure.

### Gate interpretation

- If hard structure fails: STOP and repair engineering.
- If support thresholds fail modestly: narrow eligible field-years under the frozen D rule; do not lower D.
- If fewer than 90% primary cells are supported or any field has <8 supported years, return to research-design and reassess field-year scope before preregistration.

## B. Primary focal-work frame

Expected structural grid:

- 26 fields × 2011–2025 = **390 field-year cells**;
- target = 40 informative eligible works per cell;
- minimum retain threshold = 20 works per cell;
- no H1/H2/H3 coefficient or p-value may be computed.

### Hard structural requirements

1. all 26 fields present;
2. all 15 focal years present;
3. exactly 390 field-year count records;
4. all focal rows use canonical author IDs;
5. all retained works satisfy the frozen work type, surname-map, byline-reconstruction, focal-count, and within-work-rank-variation rules;
6. no effect/p-value computation.

### Sample adequacy thresholds

Proceed to preregistration lock if:

- at least **90%** of field-year cells are retained at >=20 informative works;
- every field retains at least **10 of 15** years;
- aggregate retained works >= **10,000**;
- aggregate focal authorship rows >= **20,000**;
- unique canonical focal authors >= **10,000**;
- aggregate field-year clusters used by the structural frame >= **350**.

The target-met rate (40 works) is reported but is not itself a hard criterion.

### Gate interpretation

A below-target cell with 20–39 informative works remains eligible exactly as frozen.

A <20-work cell is excluded; its threshold is not lowered.

If the aggregate adequacy rules fail, the design remains locked and the field/year scope must be narrowed prospectively before any focal coefficient is opened.

## C. Identity-risk QA

The prelock prevalence audit passes when:

1. at least **100** unique canonical candidate authors are audited;
2. hard identity exclusions are deterministically classifiable for >=95% of audited candidates;
3. R1–R6 prevalence can be reported without outcome information;
4. no persistence endpoint or effect estimate was computed;
5. the low-risk and ORCID-anchored subset sizes are non-zero.

No maximum acceptable prevalence of R1 (missing ORCID) is imposed because missing ORCID is a sensitivity flag, not a hard exclusion.

If hard identity-integrity failures exceed 5% in the audited candidate sample, longitudinal H3 remains locked pending a targeted identity investigation; H1/H2 work-level design is unaffected.

## D. Prelock transition

Only after A, B, and C pass may:

- `DESIGN_GATES.json` record the three materialization gates as PASS;
- the execution checklist in `PREREGISTRATION_DRAFT.md` be checked;
- `27_prereg_lock.py --lock` be allowed to create the preregistration hash.

No confirmatory coefficient is opened during this transition.

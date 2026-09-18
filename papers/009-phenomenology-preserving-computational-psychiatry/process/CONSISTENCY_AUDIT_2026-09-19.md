# ARIS4C009 · Canonical consistency audit

**Date:** 2026-09-19

## Problem detected

After the acquisition/encoding split was introduced, several earlier files still contained legacy language:

- `RESEARCH_PLAN.md` described real self-report as though it were a same-source encoding;
- `POWER_PRECISION_009A.md` called R3 a self-report abstraction;
- `FIDELITY_METRICS_009A.md` mixed acquisition burden into the fixed-source A1 manipulation;
- the data dictionary lacked an explicit acquisition/representation separation.

These inconsistencies could recreate the confound that the adversarial audit had already identified.

## Corrections

### Research plan

Canonical sequence is now:

- 009A1 = fixed-source encoding benchmark;
- 009A2 = acquisition-method benchmark;
- 009B = cross-level mechanism;
- 009C = longitudinal dynamics;
- 009D = intervention/perturbation.

### Representation labels

- R3P = questionnaire-format **projection** from the fixed source;
- R4P = symptom-code **projection** from the fixed source.

Neither is a native self-report/clinical interview.

### Cost accounting

For A1:

- source acquisition is fixed;
- encoding burden is experimentally compared.

For deployment:

[
C_{total}=C_{acquisition}+C_{encoding}
]

may be reported separately.

### Data schema

Every record now distinguishes:

- acquisition method;
- assessment order/sequence;
- native measure vs projection;
- encoding protocol;
- physical/context anchor provenance.

## Result

The canonical documents now tell one consistent story:

[
H ightarrow A_m ightarrow X^{(m)} ightarrow E_k ightarrow Z^{(m,k)}
]

No remaining canonical file should equate actual self-report with an interview-derived projection.

Historical Git versions preserve the earlier formulation.

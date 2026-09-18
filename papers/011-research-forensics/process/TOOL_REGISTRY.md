# Detector implementation and defect registry

Updated: 2026-09-18

This registry exists because an integrated forensic system inherits implementation bugs, calibration drift, and scope errors from every component it wraps.

A detector is not confirmatory-eligible merely because it exists.

| Family | Detector / implementation | Intended evidence | Current status | Key applicability / defect notes |
|---|---|---|---|---|
| F1 | statcheck / equivalent recomputation | E1 statistical-reporting consistency | candidate confirmatory baseline | Supported test/reporting forms only; corrections, tails, df adjustments and rounding require explicit handling. |
| F2 | GRIM | E1 discrete-mean feasibility | candidate confirmatory baseline | Requires granular integer-valued observations/composite structure that matches implementation assumptions and a valid N. |
| F2 | GRIMMER / scrutiny implementation | E1 variability feasibility | **restricted pending known defect review** | scrutiny documentation currently warns that GRIMMER test 3 can produce false positives; test 1/2 and GRIM are stated as unaffected. Pin exact version and never treat test-3 output as clean confirmatory evidence until fixed/validated. |
| F2 | SPRITE | reconstruction / feasibility support | exploratory or corroborative | Heuristic reconstruction; non-unique candidate distributions. Do not convert reconstruction failure/success directly to misconduct. |
| F2 | DEBIT / scrutiny | E1 binary-summary consistency | candidate confirmatory baseline | Binary data only; sample vs population SD, rounding, grouping and denominator assumptions matter. Preserve input strings/trailing zeros. |
| F2 | Benford / digit preference | E5 unless strong generative case | restricted | Must justify a reference distribution before execution; never universal. |
| F4 | image-duplication engine(s) | E3/E4 image similarity | adapter-dependent | Separate a reproducible match from interpretation of legitimate reuse/manipulation. Human verification required for consequential decisions. |
| F5 | Crossref DOI/update relations | E0/E2 bibliographic provenance | eligible | Preserve assertion source; same event can have publisher and Retraction Watch assertions. Current metadata can leak later outcomes. |
| F5 | semantic citation support model | E4 citation-context anomaly | research | Requires source access and calibration; semantic mismatch is not automatically a false citation. |
| F6 | paper-mill text classifier | E4 textual/template similarity | research | Group template families across train/test; audit language/style/geography shortcuts. |
| F7 | generic AI-text detector | E5 provenance heuristic | weak evidence only | No standalone misconduct inference; test false positives, editing sensitivity and evasion. |
| F7 | generator-side watermark detector | E2-E4 depending scheme | conditional | Only when generator/watermark/version/key assumptions and text length/transformation conditions are satisfied. |
| F8 | LLM semantic-coherence checker | E4 extracted contradiction | research | Must provide source spans; deterministic verifier should be used whenever possible. |
| F9 | registry/protocol timestamp checks | E2 provenance | candidate confirmatory | Registration type and prospective/retrospective rules are domain-specific. |
| F10 | graph anomaly detector | E4 network anomaly | research | Collaboration, field and venue structure are major confounders; no country/name-origin suspicion features. |

## Promotion rule

Before a detector can enter the confirmatory benchmark, freeze:
- implementation source and version/hash;
- applicability rule;
- evidence class;
- known defects;
- calibration reference if probabilistic;
- dependency group policy;
- failure/abstention behavior;
- unit tests on positive, negative, and not-applicable cases.

A material bug discovered after confirmatory freeze triggers either a documented prespecified fix policy or a new benchmark version. Silent replacement is prohibited.

## Current known defect requiring action

The public scrutiny documentation currently warns that GRIMMER test 3 may flag consistent values as inconsistent. Until the implementation is fixed and independently checked, ARIS4C011 must:
1. pin the tested scrutiny version;
2. expose the reason/test number in the finding;
3. downgrade or exclude test-3-only flags from confirmatory E1 analyses;
4. retain them only as exploratory alerts when useful.

Source: https://lhdjung.github.io/scrutiny/reference/grimmer.html

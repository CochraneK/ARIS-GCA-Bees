# ARIS4C016 Reliability Protocol

Updated: 2026-09-18

## Goal

Estimate how reproducibly the ARIS4C016 multi-axis ontology can be applied
across languages **before** using harmonized semantic prevalence as a
cross-cultural outcome.

The audit is designed to detect ontology failure, not to maximize apparent
agreement.

## Audit sample

Target: approximately **300 lexical rows** from Study 1.

Sampling is deterministic from the public OSF file and uses stable hashes.
The public manifest contains only:
- source sample;
- source row index;
- stable row hash;
- selection stratum;
- whether source categories are missing/multi-label/unresolved.

It does **not** publish the taboo expression itself.

A local/private review sheet can be regenerated from the OSF source by joining
the row index/hash.

### Community allocation

- default: 15 rows per community;
- low-coverage communities (Spanish ES, Setswana BW): 30 rows each.

This yields 300 target rows before de-duplication/backfill.

### Within-community priority strata

Where available, sample from:
1. missing-category rows;
2. unresolved-label rows;
3. multi-label rows;
4. ordinary/random rows.

Low-coverage samples deliberately oversample missing-category rows because the
main scientific risk is not only mapping ambiguity but absent annotation.

## Blinding

Coder A and Coder B should:
- receive native expression, source-language metadata and minimally necessary
  source context;
- **not** receive each other's labels;
- ideally not receive the project's country-level hypotheses;
- preserve `UNRESOLVED` / `CONTEXT_REQUIRED` rather than guessing.

English translations can be displayed as secondary evidence but should not be
the sole evidence for identity-target or pragmatic-function coding.

## Required coding axes

Primary reliability axes:
- semantic source;
- social-indexical basis.

Secondary / context-sensitive axes:
- target;
- pragmatic function;
- taboo mechanism.

Form/phonology is handled separately because many fields can be derived
mechanically or require language-specific expertise.

## Agreement metrics

Because coding is multi-label and sparse, no single coefficient is sufficient.

Report per axis:

1. **Exact-set agreement**
   - proportion of rows where both coders assign exactly the same set.

2. **Jaccard similarity**
   - intersection / union of coder label sets;
   - report mean, median and bootstrap interval.

3. **Labelwise agreement**
   - for each canonical label, treat presence/absence as binary;
   - report prevalence and raw agreement;
   - report Cohen's kappa where prevalence is adequate;
   - add a prevalence-robust coefficient such as Gwet's AC1 when feasible.

4. **Unresolved-rate agreement**
   - whether both coders agree that evidence is insufficient.

Do not collapse disagreements into a single macro score without showing
label-level behavior.

## Reliability gate

No universal fixed threshold is assumed in advance.

Instead, an ontology axis is eligible for confirmatory prevalence analysis
only if:
- disagreement is not concentrated in one community/language;
- no major canonical label is effectively coder-specific;
- bootstrap uncertainty is reported;
- ambiguous mappings are adjudicated or explicitly excluded;
- conclusions are stable when analyses are restricted to independently agreed
  high-confidence rows.

Axes that fail remain exploratory.

## Adjudication

After independent coding:
1. freeze raw A/B annotations;
2. compute agreement;
3. review disagreements with a third adjudicator or native-language expert;
4. record the reason for every mapping-rule change;
5. increment ontology version;
6. rerun the audit without rewriting historical A/B labels.

## Native-speaker principle

A native speaker is particularly important when:
- the English gloss is broad or euphemistic;
- the item is a local political/historical expression;
- an identity/slur interpretation is possible;
- morphology changes target or intensity;
- the source label is absent;
- pragmatic use depends strongly on register/context.

Native-speaker judgement is evidence, not an automatic gold standard; coder
instructions and adjudication provenance remain necessary.

## Privacy/publication

Public artifacts should prefer:
- hashes;
- category aggregates;
- censored examples;
- summarized disagreement patterns.

The project should not become a browsable repository of identity slurs merely
because the scientific source data contain them.

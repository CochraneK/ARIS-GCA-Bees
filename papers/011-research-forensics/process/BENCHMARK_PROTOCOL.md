# Benchmark protocol — v0 frozen specification

## Benchmark object model

A paper is not assigned a single binary "fraud" truth value.

```
Paper
 ├─ source metadata
 ├─ documents / versions
 ├─ Issue[0..n]
 │   ├─ issue_type
 │   ├─ evidence_source
 │   ├─ official_status
 │   ├─ confidence_of_ground_truth
 │   ├─ detector_eligibility
 │   └─ adjudication notes
 └─ cluster IDs for leakage control
```

## Ground-truth tiers

GT-A: official notice explicitly identifies the issue.  
GT-B: correction/corrigendum explicitly documents the error.  
GT-C: primary-source institutional/journal investigation documents the issue.  
GT-D: reproducible public forensic finding without official adjudication.  
GT-E: suspicion/commentary only.

Primary confirmatory evaluation uses GT-A/B/C. GT-D is exploratory. GT-E is not positive ground truth.

## Initial data sources

1. **Crossref Retraction Watch data**
   - open production access;
   - updated on working days;
   - provides retractions and some other update types;
   - use as notice/provenance backbone, not as a universal misconduct label.

2. **Publisher correction/retraction notices**
   - parse reason text into controlled issue types;
   - preserve verbatim source pointer but avoid using reason text as a Track-A model feature.

3. **PubMed/Crossref/OpenAlex-style bibliographic metadata**
   - metadata verification and comparator matching;
   - final source choice frozen before Benchmark v1.

4. **Curated canonical forensic cases**
   - e.g. publicly documented statistical inconsistency cases for deterministic module validation;
   - kept separate from learned-model test sets if used during development.

5. **Existing published paper-mill corpora/benchmarks**
   - eligible only when provenance and cluster grouping are recoverable;
   - near-duplicate/template-family leakage must be prevented.

## Comparator matching

For each problem/correction paper, candidate comparators are sampled without a known integrity notice as of the extraction date.

Matching/covariate balancing candidates:
- field;
- year;
- article type;
- journal or journal stratum;
- accessibility/full-text availability;
- broad manuscript length;
- presence of tables/figures;
- empirical vs non-empirical status.

Do not match on variables produced by the detectors themselves.

## Primary evaluation population

All GT-A/B/C issues for which at least one preregistered detector family is eligible.

This avoids penalising the system for issue types that cannot be assessed from available artefacts, while the overall **coverage** metric separately penalises limited applicability.

## Primary metrics

1. Eligible issue-type recall.
2. False alerts per comparator manuscript.
3. Coverage.
4. Human review minutes per true issue surfaced.

A single ROC-AUC is insufficient because:
- issue families differ;
- applicability differs;
- human alert burden matters;
- the target is triage rather than autonomous adjudication.

## Confirmatory comparison

At a frozen mean false-alert burden:
- integrated framework vs strongest eligible single-family baseline;
- integrated framework vs LLM-only baseline.

Report paired bootstrap confidence intervals clustered by paper family.

## Ablation

For each detector family f:

```
Delta_f = Metric(full) - Metric(full minus f)
```

Estimate:
- Delta issue recall;
- Delta false-alert burden;
- Delta review time;
- unique issue yield.

## Leakage checks

Automated preflight must fail if:
- same DOI exists in multiple splits;
- same known template cluster crosses train/test;
- high-similarity text cluster crosses train/test above frozen threshold;
- image hash family crosses train/test where image model is learned;
- label-defining notice text is present in Track A;
- exact corrected/retracted status token appears in a Track-A input field;
- a later paper version leaks the correction into a pre-correction test version.

## Temporal evaluation

At minimum one test slice uses papers whose integrity outcomes became known after the training/development cutoff.

The extraction date and notice dates are stored.

## Human adjudication

Two-reviewer independent coding for a stratified sample.

Disagreement resolution:
1. reviewers record independent issue labels and severity;
2. disagreements are discussed with evidence spans visible;
3. unresolved cases go to a third reviewer;
4. original independent labels are retained for agreement statistics.

## Error taxonomy

False alert causes are coded:
- extraction/OCR error;
- detector applicability mistake;
- legitimate reuse;
- rounding/reporting convention;
- benign citation mismatch;
- model shortcut;
- ambiguous source;
- true anomaly absent from benchmark label;
- other.

This is necessary because benchmark "false positives" may include previously unknown real errors.

## Versioning

Every benchmark release records:
- extraction date;
- source versions;
- inclusion/exclusion logic;
- deduplication code hash;
- label schema version;
- split manifest hash;
- detector eligibility rules.

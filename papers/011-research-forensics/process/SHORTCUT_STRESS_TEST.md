# Shortcut stress test — ARIS4C011

## Motivation

A classifier can distinguish retracted from non-retracted papers for the wrong reasons.

Examples of possible shortcuts:
- journal identity or journal metrics;
- publication year;
- institution metadata;
- article length/format;
- field/subfield;
- writing style or language variety;
- publisher-specific formatting;
- known paper-mill template families shared across splits;
- post-publication language accidentally retained in the input;
- repeated authors or collaboration components.

The goal is to measure whether performance survives when these shortcuts are removed or neutralised.

## S1 — Metadata-only ceiling

Train/evaluate a deliberately shallow model using:
- year;
- journal identity/stratum;
- article type;
- broad field;
- manuscript length;
- number of references;
- number of figures/tables;
- non-sensitive venue metadata.

Purpose:
Estimate how much of a binary retraction benchmark is predictable without integrity evidence.

Institution/country/name-origin features are excluded from the production framework. A research-only sensitivity analysis may inspect already-public aggregate metadata only if ethically justified and preregistered; it must never become an operational suspicion feature.

## S2 — Strict matched benchmark

Match problem/error/comparator manuscripts within:
- journal where feasible;
- publication year/window;
- article type;
- field;
- access/full-text availability;
- broad length/figure/reference strata.

Re-evaluate all baselines.

If performance collapses, the original benchmark was likely dominated by nuisance structure.

## S3 — Correction/error adversarial set

Add papers with known corrections or honest/documented errors.

Key question:
Does a detector flag a real inconsistency while avoiding the unsupported escalation to "misconduct"?

Report:
- anomaly recall;
- review priority;
- rate of erroneous misconduct-like language from LLM baselines.

## S4 — Family-grouped split

Create connected components / cluster IDs for:
- paper-mill templates;
- high text similarity;
- duplicated or reused images;
- author collaboration;
- special issues;
- known batch retractions.

No cluster may cross train and confirmatory test where it could provide a shortcut.

## S5 — Temporal holdout

Train/develop only on evidence available before cutoff T.

Test on papers whose integrity outcomes become known after T.

Freeze:
- corpus snapshot;
- detector versions;
- notice extraction date;
- threshold.

## S6 — Style/language perturbation

For text-based learned models:
- strip headers/venue formatting;
- normalise citation style;
- compare title+abstract vs body-only;
- paraphrase benign sections in a controlled diagnostic subset;
- test translated/edited variants only where provenance permits.

Measure prediction stability.

A model whose output changes strongly under meaning-preserving style edits receives a shortcut-risk warning.

## S7 — Evidence-only vs context-rich models

Compare:

A. metadata-only;
B. text embedding only;
C. extracted integrity-evidence features only;
D. A+B+C multimodal classifier;
E. 011 evidence-graph triage.

The confirmatory claim is not "E has highest AUC".

The key questions are:
- which model finds more labelled issue types at the same alert burden?
- which model retains performance under matched/grouped/temporal stress tests?
- which model produces auditable evidence?
- which model avoids false escalation on correction/error cases?

## S8 — Label heterogeneity test

Run binary retracted/non-retracted classification, then stratify the positive set by controlled reason.

Estimate per-reason performance.

If the model succeeds only on a subset (e.g. paper-mill/template cases), report that rather than calling it general misconduct detection.

## S9 — Leave-context-out tests

Where feasible, independently remove:
- journal identifiers/metrics;
- affiliations;
- author strings;
- references;
- acknowledgements/funding;
- formatting/layout.

Estimate delta in binary classification and issue-level detection.

Large binary-performance drops without corresponding drops in issue evidence are evidence of shortcut dependence.

## S10 — Negative-control labels

Permutation checks:
- shuffle labels within tightly matched strata;
- use benign metadata labels unrelated to integrity;
- confirm learned models do not recover signal beyond chance after leakage removal.

## Primary shortcut diagnostics

- delta AUROC / AUPRC after strict matching;
- delta issue recall;
- calibration shift;
- performance by retraction reason;
- performance under temporal holdout;
- fraction of model importance attributable to prohibited/non-causal context;
- stability under meaning-preserving text changes.

## Interpretation

The study may produce a useful negative result:

> High binary retraction classification can coexist with poor issue-level forensic value.

That would itself justify issue-level benchmarks and evidence-first screening.

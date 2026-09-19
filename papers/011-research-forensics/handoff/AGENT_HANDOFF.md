# ARIS4C011 · Agent takeover brief

## What this project is

**Research Forensics at Scale: An Auditable Multi-Evidence Framework for Scientific Integrity Screening**

An auditable, multi-evidence research-integrity framework that routes manuscripts to applicability-aware statistical, numerical, table, citation, provenance, image/text, registration and corpus/network checks, then presents evidence for human review without equating anomalies with misconduct.

## Current state

- **Activity:** wait
- **Portfolio progress:** 78%
- **Stage:** Pilot 3 · five pre-outcome development true-positive evaluations across four target papers
- **Scientific status:** development evidence is real and time-safe, but confirmatory detector-performance inference has **not** begun.
- **Immediate hard blocker:** none.
- **Confirmatory gate:** broader time-safe corpus, grouped/temporal split freeze, detector/version freeze, no-leakage validation, and human-review protocol.

## Development evidence already established

Five correction-blind / pre-outcome true-positive detector evaluations now exist across four target papers:

1. **PLOS 10.1371/journal.pone.0258910 · F5 cited-source consistency**
   - historical target table vs contemporaneously available Harper & Rhodes (2021);
   - N matches; RMSEA, CFI and best-fitting model disagree;
   - later correction is manager-only ground truth.

2. **PLOS 10.1371/journal.pone.0293412 · F3 raw-data→table recomputation**
   - publication-day publisher PDF + pre-publication OSF data are time-safe;
   - Mexico variants deterministically recompute to 17 / 4.8%, historical table reports 16 / 4.5%;
   - within-table totals still sum correctly because the Mexico error is offset by Other, demonstrating detector complementarity.

3. **PLOS 10.1371/journal.pone.0180906 · F8 body↔caption scope coherence**
   - historical Results text attributes multiple-analysis findings to Table 1;
   - historical caption describes only univariate logistic regression;
   - later correction independently confirms caption error.

4. **Same Toxoplasma paper · F3 table-schema structure**
   - preserved-original PMC Table 1 object is SAFE_EXACT;
   - section A exposes five result columns while section B exposes two;
   - correction-blind schema-drop detector FLAGs; manager-only correction confirms omitted columns.

5. **PLOS 10.1371/journal.pone.0180395 · F1 significance/p-direction**
   - preserved-original PMC body text says “significant increases ... (p>.05)”;
   - correction-blind F1 detector FLAGs the internal contradiction;
   - later correction independently confirms the direction fix.

All five are **development examples**. Do not compute or imply confirmatory sensitivity, precision, superiority, or prevalence from Pilot 3.

## Immediate next actions

1. Run the formatting/honest-error CONTROL case `10.1371/journal.pone.0263337` through the same reporting stack and confirm that it is not escalated as a scientific contradiction.
2. Build a small matched **no-known-integrity-concern comparator** set; never call these “clean controls”.
3. Continue the unresolved structured-content queue with the voxel/Brodmann-area table case.
4. Produce only a descriptive development summary of detector-family yield, complementarity, applicability and abstention.
5. Prepare the frozen confirmatory cohort: grouped/temporal splits, no label-bearing features, frozen detector versions/applicability rules, and human-review protocol.

## Locked methodological boundaries

- Unit of truth is **issue-level evidence**, not author-level misconduct.
- Automated outputs are anomaly/evidence/review-priority only; never infer motive, guilt, fraud, or misconduct.
- Track A is time-safe content-only; Track B is open-world practical triage.
- Corrections/retractions may be used by the **manager/evaluator as ground truth**, but must never enter Track A detector-visible inputs.
- Track A eligibility is `paper × issue × required artifact role`, not one Boolean per paper.
- ABSTAIN is not PASS.
- Current metadata can be outcome-contaminated.
- Pilot 3 is an enriched development queue, not the confirmatory benchmark.
- Do not infer undocumented data-recoding rules merely to manufacture a match.
- No-known-notice comparators are not evidence of absence of problems.

## Canonical files / entry points

Read these first:

- `process/STATUS.md`
- `data/results/pilot3_candidate_queue.csv`
- `data/results/pilot3b_second_true_positive.json`
- `data/results/pilot3c_third_true_positive.json`
- `data/results/pilot3_toxo_f3_evaluation.json`
- `data/results/pilot3_adaptive_f1_evaluation.json`
- `manuscript/DRAFT.md`
- `agent/research-forensics/SKILL.md`

Repository source:
https://github.com/CochraneK/ARIS4C/tree/main/papers/011-research-forensics

## Before changing anything

1. Read `TODO.md`, `DECISIONS.md`, and newest `CHATLOG.md` / `SESSION_LOG.md`.
2. Prefer machine-readable results and canonical scientific files over stale prose.
3. Preserve frozen design decisions unless a documented amendment is required.
4. Use **Cochrane Kang** for visible author naming.
5. Never commit secrets, private credentials, hidden chain-of-thought, or unnecessary sensitive personal data.
6. After a material change, update canonical research files first, then continuity files.

## Handoff completion rule

Before ending a substantial session:
- update `TODO.md`;
- append material research decisions to `DECISIONS.md`;
- append a public-safe conversation summary to `CHATLOG.md`;
- append executed/validated work to `SESSION_LOG.md`.

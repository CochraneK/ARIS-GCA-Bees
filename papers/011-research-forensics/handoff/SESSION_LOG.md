# ARIS4C011 · Session log

Append substantial execution sessions in reverse chronological order or chronological order, but remain consistent.

## 2026-09-19 · Continuity retrofit

- Added the standardized ARIS4C per-paper handoff package.
- Bootstrapped project context, current state, TODO, decision history, and a public-safe conversation record.
- Established Git as the cross-device / cross-account / cross-agent continuity surface.
- Future material sessions must append execution results and validation here.

## 2026-09-19 · Pre-deletion reconciliation session

- Read current `main` rather than trusting chat-local state.
- Detected that Git scientific results had advanced beyond the older continuity snapshot.
- Confirmed five pre-outcome development true-positive detector evaluations across four target papers:
  1. PLOS morality / F5 cited-source consistency;
  2. PLOS music-country / F3 raw-data aggregate recomputation;
  3. Toxoplasma / F8 body↔caption scope coherence;
  4. Toxoplasma / F3 preserved-original table-schema column-drop;
  5. Adaptive Interaction / F1 significance-claim vs p-direction.
- Confirmed Toxoplasma preserved-original PMC Table 1 and Adaptive preserved-original PMC body text are qualified SAFE_EXACT with correction/outcome metadata excluded from detector-visible inputs.
- Reconciled canonical `process/STATUS.md`, Pilot 3 candidate CSV, generated queue, and portfolio dashboard.
- Marked the Adaptive F1 case COMPLETE and moved the next unresolved structured-content queue focus to the voxel/Brodmann-area table case.
- Replaced stale handoff status/TODO/takeover text and appended current decisions/conversation/session history.
- No confirmatory performance claim was introduced.

## 2026-09-19 · Pilot 3 formatting-control execution

- Materialized the existing SAFE_EXACT construction-decimal control into an executable Track-A evaluation.
- Added `code/pilot3_format_control.py` and a dedicated GitHub Actions workflow.
- Workflow run 35440672452 completed successfully and committed the machine-readable report/evaluation.
- DOI 10.1371/journal.pone.0263337 produced 10 PASS findings, 0 flags, review priority NONE, and no misconduct inference; correction metadata was not detector-visible.
- Preserved the development-only claim boundary: no specificity or superiority estimate was made.
- Promoted ARIS4C011 from Wait to Active at 80%; next bounded unit is a small matched no-known-integrity-concern comparator set.


## 2026-09-19 · Comparator freeze, development summary, and voxel BA completion

- Resumed ARIS4C011 from the Git-backed checkpoint after the prior controller chat reached its context limit.
- Added and tested a comparator full-text provenance freeze. An initial CI failure exposed an over-broad PubMed XML query that included reference-list PMCIDs; the parser was narrowed to the primary `PubmedData/ArticleIdList`, after which all four selected comparators froze successfully.
- Comparator result: 4/4 matched no-known-integrity-concern development comparators passed the indexed notice screen and current retrieved full-text freeze; hashes and provenance were persisted without committing full text.
- Added a reproducible Pilot 3 development-summary generator, tests, and CI. It now records six pre-outcome FLAG evaluations across five target papers, family counts F1=1 / F3=3 / F5=1 / F8=1, four development comparators, five genuine abstention checks, and the formatting-control non-escalation result.
- Added CI for the preserved-original voxel/Brodmann-area case. The SAFE_EXACT PMC Table 2 fixture produced 6 findings: 5 PASS and exactly 1 FLAG on original token `9月8日`; correction metadata was not detector-visible and no misconduct inference was produced.
- Fixed a status-layer bug caught by CI: voxel evaluation `status=PASS` denotes evaluation-contract success and must not be mistaken for detector PASS; the summary now uses the one detector FLAG explicitly.
- Refreshed the Pilot 3 acquisition queue. Voxel and formatting-control cases are COMPLETE; all previously completed positive cases remain COMPLETE; the only remaining candidates are low-priority DEFER entries with no active rank.
- Advanced canonical portfolio state from 80% to 84%, stage `Pilot 3 · six development FLAGs · comparator freeze · confirmatory transition`.
- Updated `paper.json`, `papers/dashboard.json`, generated development artifacts, process status, TODO, decisions, and handoff snapshots. Confirmatory scoring remains locked pending broader corpus scale-up and protocol freeze.


## 2026-09-19 · 80-record blinded confirmatory-feasibility frame

- Inherited and audited the PRE_FREEZE confirmatory contract, development-exclusion registry, split/cluster leakage preflight, temporal holdout rule, and Track-A allowlists.
- Added/validated the blinded feasibility-frame execution path. Fixed two CI engineering defects before allowing acquisition to proceed: the workflow test invocation conflicted with Python's standard-library `code` module, and test-only exclusion paths outside the repository broke `Path.relative_to`; both were repaired without changing the scientific selection contract.
- Successful workflow froze 80 journal-article targets across all 20 calendar-year × update-type strata (2016–2025 × correction/retraction; 4 per stratum), with all 42 development-exposed DOIs excluded and no detector output visible to selection.
- Workload/leakage signals only: 79/80 Crossref full-text links, 33/80 abstracts, 70 distinct journals, 25/80 current-title status markers, and 80/80 current update relations.
- Added `process/CONFIRMATORY_FEASIBILITY_V0.md` documenting allowed/forbidden uses and the next manager-only adjudication gate.
- Advanced portfolio maturity to 86%. Confirmatory scoring remains explicitly disabled.


## 2026-09-19 · Feasibility-frame deduplication repair

- Audited the first 80-row frame before manager first-pass coding and found six duplicate target-event occupancies.
- Root cause: within-stratum duplicate candidates were appended before the global `seen` set was updated.
- Hardened selection to reject duplicate event keys and duplicate target DOIs before stratum ranking/slicing; added unit and CI assertions for 80 unique targets and 80 unique event keys.
- Re-ran the frozen deterministic selection without detector outputs. The repaired frame again contains 80 records, 20/20 strata at four records each, and no development-exposed DOI.
- Reconciled feasibility statistics: 79 journal-article + 1 proceedings-article; 79/80 Crossref full-text links; 37/80 abstracts; 28/80 current-title status markers; 71 distinct containers.
- Added a manager-only adjudication packet, frozen adjudication ontology v0.1.1, structural validator, short-evidence acquisition layer, and safe workflow-run cascade. No first-pass issue labels had been committed before this repair.

# ARIS4C011 · Decision log

This file is append-oriented. Preserve superseded decisions when they explain why the project changed direction; mark them as superseded rather than deleting them.

## 2026-09-19 · Continuity-standard bootstrap

**Decision:** Adopt the repository-level ARIS4C continuity/handoff contract for this paper.

**Why:** The project must remain recoverable across ChatGPT conversations, accounts, computers, and external agents without relying on one chat's memory.

**Project-specific decisions distilled from surviving project context:**
- Use applicability-aware detectors and an evidence graph.
- An anomaly is a review lead, not a misconduct verdict.

**Canonical follow-up:** Future material decisions should be appended with date, rationale, and affected files/commits when known.

## 2026-09-19 · Track A development evidence and handoff reconciliation

**Decision:** Treat the current Pilot 2/3 set as an enriched development set only. It may demonstrate feasibility, evidence routes, complementarity, abstention and failure modes, but it must not be used to claim confirmatory sensitivity, precision, prevalence or superiority.

**Decision:** Corrections/retractions are manager/evaluator-only ground truth. A detector true-positive is valid only when its inputs were available before the outcome and contain no correction/outcome metadata.

**Decision:** Track A qualification remains object- and issue-specific: `paper × issue × required artifact role`. One correction notice may contain multiple sub-issues with different readiness states.

**Decision:** Source-anatomy work may reroute a development candidate to a different detector family before confirmatory freeze. Example: the music-country case moved from within-table arithmetic to raw-data→table recomputation when public OSF data proved more diagnostic.

**Decision:** Do not infer undocumented recoding/grouping rules merely to make a published table agree with deposited data. Restrict deterministic checks to explicit, source-verifiable transformations.

**Decision:** Preserved-original repository/PMC objects can qualify as SAFE_EXACT when provenance, date, version preservation and outcome separation are explicitly documented. Current bibliographic update relations remain outside detector-visible Track A inputs.

**Decision:** A formatting/honest-error control must be allowed to remain low-severity/non-escalated even when a discrepancy is real. Anomaly detection is not a misconduct classifier.

**Evidence state at this checkpoint:** five pre-outcome development true-positive detector evaluations across four target papers (F5 cited-source consistency; F3 raw-data recomputation; F8 scope coherence; F3 table-schema structure; F1 significance/p-direction).

## 2026-09-19 · Formatting-control non-escalation passed

**Decision:** Count DOI `10.1371/journal.pone.0263337` only as a development-stage formatting/honest-error control. The SAFE_EXACT pre-correction Table 2 fixture was run through the real Track-A orchestrator with correction metadata excluded.

**Observed control result:** 10/10 numeric-range findings PASS, 0 FLAG, review priority NONE, decimal-comma parsing preserved, and no misconduct inference.

**Claim boundary:** This single enriched control demonstrates that the current reporting stack can conservatively non-escalate this locale-formatting case. It is **not** a specificity, false-positive-rate, or clean-control estimate. The next negative-side development unit must use the term **no-known-integrity-concern comparator** and keep selection independent of detector output.


## 2026-09-19 · Comparator freeze, voxel completion, and development-cycle closure

**Decision:** Negative-side development examples remain **matched no-known-integrity-concern comparators**, never “clean controls.” Four matches were selected independently of detector output, passed indexed Crossref/PubMed notice-negative screening, and had the retrieved PMC full-text version frozen by SHA-256. Their state is development provenance only; it does not support specificity, false-positive-rate, or superiority estimates.

**Decision:** DOI `10.1371/journal.pone.0163749` contributes one additional development FLAG route only for the preserved-original malformed Brodmann-area token. The SAFE_EXACT PMC Table 2 fixture exposes six original BA cells, correction-blind F3 produces five PASS and one FLAG on `9月8日`, and correction metadata remains manager-only. Other later documented BA row-shift fixes are outside this syntax-check claim.

**Decision:** Keep evaluation-run success distinct from detector output. For the voxel case, top-level evaluation `status=PASS` means the validation contract succeeded; detector evidence still contains exactly one `FLAG`. Downstream summaries must not collapse these two status layers.

**Decision:** Close the enriched Pilot 2/3 acquisition-development loop at six pre-outcome FLAG evaluations across five target papers, one SAFE_EXACT formatting/honest-error non-escalation control, four matched development comparators, and a descriptive complementarity/abstention summary. Remaining low-yield Pilot 3 candidates are DEFER; the next work is broader time-safe corpus construction and confirmatory protocol freeze.

**Claim boundary:** The enriched development set remains non-confirmatory. No sensitivity, precision, specificity, false-positive-rate, prevalence, superiority, intent, guilt, or misconduct estimate is authorized from this checkpoint.


## 2026-09-19 · Blinded 80-record confirmatory-feasibility frame

**Decision:** Freeze an 80-record **feasibility-only** frame before issue/artifact adjudication: 2016–2025 × correction/retraction, four records per stratum. Selection excludes every DOI in the 42-entry development-contamination registry and uses deterministic provenance hashing rather than detector output, review priority, or anomaly score.

**Decision:** The frame is not yet the confirmatory benchmark sample. Its permitted uses are acquisition workload, adjudication workload, time-safe artifact missingness/attrition, and sample-size planning without detector-effect peeking. It may not be used for detector performance, threshold tuning, sensitivity/specificity estimation, or confirmatory hypothesis testing.

**Observation / design implication:** 25/80 current target titles contain a post-publication status marker and all 80 have current Crossref update relations. These are leakage-risk observations, not model features or performance signals. Track A therefore continues to require historical object qualification and the frozen content-only allowlist.

**Next gate:** Manager-only issue adjudication assigns issue family, ground-truth tier, and required artifact role for the frozen frame before historical artifact qualification and SAFE_EXACT / PROXY_ONLY / BLOCKED attrition are frozen.


## 2026-09-19 · Feasibility-frame target-uniqueness hardening

**Finding:** The first 80-row feasibility-frame implementation could retain duplicate copies of the same target/event inside one stratum because the global `seen` set was updated only after selecting the stratum slice. Six duplicate target-event occupancies were detected before any confirmatory first-pass issue labels were committed.

**Decision:** The feasibility frame now requires both globally unique target DOI and unique target-notice event key. Duplicate candidates are removed before ranking/slicing within each stratum, and replacements are drawn under the same frozen SHA-256 ranking rule until every 2016–2025 × correction/retraction stratum again contains four records.

**Result:** The re-frozen frame has 80/80 unique target DOIs and 80/80 unique event keys while retaining all 20 balanced strata and the 42-DOI development exclusion. No detector output was used to repair or reseed the frame.

**Metadata reconciliation:** The unique frame contains 79 journal-article targets and one proceedings-article target; the protocol did not freeze a journal-only population, so article type is retained as a matching/description variable rather than post-hoc exclusion. Workload signals are 79/80 Crossref full-text links, 37/80 abstracts, 28/80 current-title status markers, and 71 distinct containers.

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


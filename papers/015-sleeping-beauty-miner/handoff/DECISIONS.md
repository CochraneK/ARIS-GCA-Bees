# ARIS4C015 · Decision log

This file is append-oriented. Preserve superseded decisions when they explain why the project changed direction; mark them as superseded rather than deleting them.

## 2026-09-19 · Continuity-standard bootstrap

**Decision:** Adopt the repository-level ARIS4C continuity/handoff contract for this paper.

**Why:** The project must remain recoverable across ChatGPT conversations, accounts, computers, and external agents without relying on one chat's memory.

**Project-specific decisions distilled from surviving project context:**
- Separate retrospective SB identification, mechanism inference, and prospective rediscovery.
- Do not infer mechanisms when the robust SB case set is empty or unstable.

**Canonical follow-up:** Future material decisions should be appended with date, rationale, and affected files/commits when known.


## 2026-09-19 · Risk-set controls may be reused across case event times

**Decision:** Align the primary event-time risk-set matcher with standard
incidence-density sampling: an eligible control may be selected for more than
one distinct case risk set and may later itself become a case. Controls remain
unique within a single case risk set.

**Why:** The previous global no-replacement implementation introduced
case-order-dependent depletion when multiple Sleeping Beauty cases shared the
same publication-year/field risk set. Standard nested case-control/risk-set
sampling permits repeated control membership across distinct event-time risk
sets. This is a design correction, not a relaxation of the prespecified
absolute-SMD < 0.10 balance gate.

**Method references:**
- https://pmc.ncbi.nlm.nih.gov/articles/PMC4558410/
- https://pmc.ncbi.nlm.nih.gov/articles/PMC3828645/
- https://pmc.ncbi.nlm.nih.gov/articles/PMC8962511/

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

## 2026-09-19 · Freeze Pilot-M primary cases and stop random-reservoir escalation

**Decision:** For the current validation pilot, the primary event-time risk-set
case set is frozen to the three literature-known Sleeping Beauties (Hummers
1958, EPR 1935, Washburn 1921). Robust SBs discovered incidentally inside a
random control reservoir remain discovery candidates and do not enter the
primary case set until independent annual-trajectory / Beauty-Coefficient
validation.

**Why:** Allowing randomly sampled controls to become primary cases made the
case set change whenever the reservoir changed, confounding matching-design
comparisons.

**Decision:** Separate OpenAlex acquisition from risk-set analysis. Reuse the
saved 603-paper artifact for matcher and estimand diagnostics rather than
re-querying the API for every design change.

**Decision:** Do not keep escalating random reservoir size after the frozen
case-set diagnostics. The acquired 200-controls/case cohort still fails the
prespecified abs-SMD < 0.10 gate, and support diagnostics identify a strong
overlap shortage for Washburn 1921 (minimum observed event-time sleep-rate gap
1.180). The next acquisition step is the complete exact field × publication
year frame, not another random sample and not a relaxed balance threshold.

**Canonical evidence:** `data/pilotM_riskset_diagnostics_2026-09-19.json`.

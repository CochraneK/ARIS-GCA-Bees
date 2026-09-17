# STATUS — ARIS4C005

**Last updated:** 2026-09-18  
**State:** `PILOT_READY / PRE-DATA`  
**ARIS provenance:** v0.4.26 @ `951654847b015585385b2448c5667dcd04e7b56b`

## Canonical research identity

**The Hidden Burden of Bad Science: Estimating the Global Scale and Downstream Cost of Research Integrity Failures**

The project is no longer in free-form idea generation. Scope is frozen and the next valid work is empirical pilot execution.

---

# Completed

## Concept / scope

- [x] Idea saturation pass completed.
- [x] Five-layer Loss Ontology frozen.
- [x] E1/E2/E3 exposure separation frozen.
- [x] Further distinction added between:
  - E1-S severe scientific unreliability with integrity evidence;
  - E1-M confirmed major misconduct;
  - E1-P publication-process integrity failure;
  - E3 broader unreliability/research waste.
- [x] Primary / secondary / exploratory estimands defined.
- [x] Sleeping Beauty outcome explicitly downgraded to exploratory structural counterfactual.
- [x] No-single-score rule frozen.

## Evidence

- [x] Initial atomic numeric evidence ledger created.
- [x] Current Crossref/OpenAlex universe anchors verified.
- [x] Researcher-level misconduct/QRP meta-analysis anchors verified.
- [x] Netherlands randomized-response survey anchor verified.
- [x] VITALITY I contamination cascade and leave-out effects verified.
- [x] Collateral collaborator citation-effect anchor retrieved.
- [x] Participant nonpublication/waste anchor retrieved.
- [x] Peer-review labor context anchor retrieved.
- [x] Sleeping Beauty/Prince large-network feasibility anchor retrieved.
- [x] 2026 NIH retraction-cost preprint recorded as QUALIFIED, not peer-reviewed evidence.

## Method

- [x] Formal estimands written.
- [x] Causal + measurement DAG written.
- [x] Detection/governance bias explicitly modeled conceptually.
- [x] Article-level latent prevalence separated from researcher survey prevalence.
- [x] Primary latent model simplified to binary severe-failure state for identifiability.
- [x] Capture-recapture demoted to sensitivity analysis.
- [x] Manual audit design specified.
- [x] Material citation-dependence taxonomy specified.
- [x] Knowledge Ghost Half-Life identification constraints specified.
- [x] Innovation Delay event-study/synthetic-control requirements specified.
- [x] Retraction Watch reason/exposure codebook written.
- [x] Adversarial AUTO_REVIEW completed with 20 major concerns and gates.

## Data / implementation

- [x] Data feasibility + acquisition plan written.
- [x] `build_universe.py` scaffold created for OpenAlex core article/review counts.
- [x] `classify_retractions.py` conservative reason classifier created.
- [x] `scenario_model.py` created for explicitly non-empirical Fermi scenarios.
- [x] Example scenario input/output created and segregated from evidence ledger.
- [x] Invariant unit tests created for retraction classification and scenario engine.
- [x] ARIS4C005 smoke CI workflow added.
- [x] Public-repository data governance rules documented.

---

# Important current findings / anchors

These are evidence anchors, not the final global estimate:

- Crossref (2026-09-16): `187,832,048` total metadata records; `125,897,384` journal DOIs.
- OpenAlex core: `327,203,926` scholarly works at initialization; work types are broader than papers.
- Xie et al. 2021: researcher-level pooled FFP-type misconduct self-report `2.9% (95% CI 2.1–3.8%)`; this **cannot** be multiplied by paper counts.
- Gopalakrishna et al. 2022: Netherlands researcher self-report using randomized response: fabrication `4.3%`, falsification `4.2%`; also not paper prevalence.
- VITALITY I: 1,330 retracted RCTs; 312 contaminated 4,095 meta-analyses from 847 systematic reviews; 218 substantially affected meta-analyses in 68 reviews were used by 157 English-language guidelines. Removing retracted trials changed pooled-effect direction in 8.4% and P-value significance in 16.0% of the analyzed meta-analyses.
- Hussinger & Pellens 2019: uninvolved prior collaborators experienced an estimated 8–9% citation penalty after documented misconduct cases.
- Yilmaz et al. 2018: 66,655 participants in completed but unpublished AD/MCI trials and 18,246 in unpublished discontinued trials — E3 research-waste evidence, not fraud evidence.

See `data/numeric_evidence.csv` for the canonical numeric ledger and qualifications.

---

# Current blockers / gates

## BLOCKER A — actual denominator extraction

The code exists, but the current local execution container has no outbound DNS to GitHub/OpenAlex. This is an execution-environment constraint, not a design blocker.

**Resolution path:** run via GitHub Actions/Codex/normal networked environment and freeze output/provenance.

## BLOCKER B — correction join pilot

Need actual Retraction Watch CSV snapshot and join audit before any detected-rate result.

## BLOCKER C — manual adjudication protocol / reviewers

The label ontology is defined, but a real gold-standard audit requires actual article review and adjudication resources.

## BLOCKER D — detector acquisition

Need to settle legally/reproducibly accessible detector sources before Pilot B.

## BLOCKER E — RLY calibration

The vivid scenario engine works, but no empirical RLY scaling is allowed until study-type effort distributions are anchored.

## BLOCKER F — semantic contamination classifier

No global Scientific Contamination Footprint until material dependence is validated beyond raw citation counts.

## BLOCKER G — innovation/Sleeping Beauty causal chain

IDY requires valid matched topic controls/pre-trends. NWSB remains exploratory even if IDY succeeds.

---

# Tool/access notes

- Elicit API attempt: blocked by current plan (`api_access_denied`). Not a dependency.
- Scite literature retrieval: available.
- Scite Collection creation attempt: HTTP 402/payment required. Not a dependency.
- Local container: no DNS for direct GitHub clone / OpenAlex API during initialization.
- GitHub connector: repository read/write works; all canonical state is committed there.

---

# Next execution queue

1. Run ARIS4C005 smoke CI and fix any failing tests.
2. Execute `build_universe.py` in a networked runner; commit annual counts + provenance.
3. Pin/download Retraction Watch CSV snapshot and checksum/date it.
4. Run `classify_retractions.py` and audit a stratified sample of reason mappings.
5. Produce Pilot A baseline: publication counts, detected E1-S/E1-M/E1-P rates, correction latency.
6. Freeze a practical detector set and manual adjudication form for Pilot B.
7. Only after Pilot B/C: fit latent prevalence.
8. Then start contamination graph / NIH cost / innovation modules.

---

# Do not do next

- Do not publish the example Fermi outputs as findings.
- Do not calculate `2.9% × global papers`.
- Do not calculate `global R&D × misconduct rate`.
- Do not rank countries by raw retraction rate.
- Do not call every citation to a retracted paper contamination.
- Do not claim a global count of Never-Woken Sleeping Beauties before the innovation-delay chain validates.

---

# Handoff sentence

If this chat is lost, resume from this file and run **Pilot A (OpenAlex universe + Retraction Watch correction join)**. Do not reopen idea mining unless new evidence reveals a genuinely new first-order loss category.

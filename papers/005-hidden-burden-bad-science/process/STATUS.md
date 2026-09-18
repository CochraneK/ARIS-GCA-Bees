# STATUS — ARIS4C005

**Last updated:** 2026-09-18  
**State:** `SCALED_AUDIT_COMPLETE / AI_BATCHES_READY / CITATION_AI_READY`  
**ARIS provenance:** v0.4.26 @ `951654847b015585385b2448c5667dcd04e7b56b`

## Canonical research identity

**The Hidden Burden of Bad Science: Estimating the Global Scale and Downstream Cost of Research Integrity Failures**

Scope remains frozen. The 10,000-work confirmatory random audit and dual-AI input batches are complete. The prevalence-critical dependency is execution/calibration of AI adjudication, not sampling or ontology design. Citation-edge AI adjudication is also packaged for execution.

---

# Completed

## Concept / measurement

- [x] Five-layer Loss Ontology frozen.
- [x] E1-S / E1-M / E1-P / E2 / E3 separation frozen.
- [x] No-single-score rule frozen.
- [x] Primary binary severe-failure latent target frozen for identifiability.
- [x] Researcher-level self-report prevalence explicitly separated from article-level prevalence.
- [x] Detection/governance bias explicitly treated as part of the observation model.
- [x] Sleeping Beauty permanent-loss count kept exploratory.

## Evidence

- [x] Canonical numeric evidence ledger exists.
- [x] Crossref/OpenAlex denominator anchors recorded.
- [x] VITALITY I contamination cascade recorded.
- [x] 2025 JAMA Network Open paper-mill systematic-review contamination benchmark added.
- [x] 2026 BMJ paper-mill ML detector study recorded as detector-feasibility / bias precedent.
- [x] Human-time, participant, collaborator and NIH-cost context anchors recorded with qualifications.

## Pilot A — live public-data acquisition

- [x] GitHub Actions networked runner operational.
- [x] OpenAlex core article+review universe extracted for 2000–2025.
- [x] Frozen OpenAlex query returned **137,445,874** works under the target metadata definition.
- [x] Annual counts and query provenance committed.
- [x] Retraction Watch snapshot pinned to Git commit `448a0ed262c6348dd6f06ac03f5602bae4ef2d01`.
- [x] Snapshot summarized without redistributing raw CSV.
- [x] 72,577 correction/event rows observed.
- [x] 63,434 unique resolvable original-paper DOIs observed.
- [x] 60,971 unique original DOIs had at least one event with nature `Retraction`.
- [x] Row-level vs unique-work counts separated.
- [x] Retraction dates parsed chronologically rather than lexically.
- [x] Current reason labels/renames handled case-insensitively.
- [x] CI smoke gate passes.

**Interpretation:** these are detected/corrected records, not latent prevalence.

## Pilot B — engineering layer

- [x] Adjudication protocol frozen.
- [x] Pilot B data contract frozen.
- [x] Adjudication CSV template committed.
- [x] Probability-aware two-phase sampler implemented.
- [x] Sampling uses independent Bernoulli/Poisson random + enrichment components with exact first-order inclusion probability.
- [x] Design weights retained for every selected work.
- [x] Design-weighted detector calibration diagnostic implemented.
- [x] Kish effective sample size reported.
- [x] Unresolved/indeterminate labels are never silently recoded as negatives.
- [x] Sampling/calibration invariant tests pass in GitHub Actions.

---


## Pilot D — citation exposure / ghost pilot

- [x] Semantic citation-edge ontology frozen.
- [x] Raw citation exposure pilot executed on 25 high-propagation narrow E1-S sources.
- [x] 914 candidate sources resolved; top 25 selected as a deliberate stress-test.
- [x] 7,443 observed incoming citation exposures across selected sources.
- [x] 1,753 exposures occurred after the source retraction date (**23.55%** of observed exposure in this non-representative stress-test).
- [x] 486 post-retraction citation edges sampled for semantic adjudication.
- [x] Citation Ghost Half-Life estimator implemented with right censoring.
- [x] Corrected yearly-series bug; current descriptive pilot: 23 estimable sources, 20 half-life events, 3 right-censored, Kaplan–Meier median 1 year.
- [ ] Dependence Ghost Half-Life pending semantic citation-context adjudication.

**Interpretation:** raw citation exposure decays faster than cumulative exposure disappears. The 1-year median is descriptive for deliberately high-citation sources and is not a global contamination half-life.

## AI adjudication / confirmatory design

- [x] AI adjudication protocol frozen.
- [x] Locked prompt v1 frozen.
- [x] Dual-AI consensus/arbitration merger implemented.
- [x] AI error design scenarios executed.
- [x] Random-audit design simulation executed.
- [x] Confirmatory random sample decision: **5,000 minimum / 10,000 preferred**.
- [x] Scaled full-period random audit executed: **10,000 works** over 2000–2025.
- [x] Dual-AI blinded inputs generated: **20,000 assignments / 80 deterministic batches**.
- [x] Public-safe scaled-audit summary and batch manifest committed.
- [x] External AI adjudication handoff specification written.
- [x] Citation-edge dual-AI packet generated: **486 edges / 972 assignments / 10 batches**.
- [ ] Run dual-AI article adjudication + arbitration.
- [ ] Run dual-AI citation-edge adjudication + arbitration.
- [ ] Calibrate AI error using high-confidence anchors and sensitivity analysis.

# Live Pilot A anchors

Primary target denominator:

`OpenAlex core + type:article|review + publication_year:2000-2025`

- metadata count: **137,445,874**
- source: OpenAlex Works API
- extraction timestamp stored in `data/pilot/openalex_universe_provenance.json`

Retraction Watch snapshot:

- event rows: **72,577**
- unique original-paper DOIs: **63,434**
- unique original DOIs with Retraction nature: **60,971**
- paper-mill signal unique DOIs: **11,706**
- narrow auto E1-S unique DOIs: **2,020**
- strong E1-M unique DOIs: **18,863**
- strong E1-P unique DOIs: **20,417**
- rows/cases requiring manual review remain large; these auto flags are screening variables only.

See `data/pilot/retraction_watch_snapshot_summary.json`.

---

# Important external calibration anchors

- Xie et al. 2021 pooled researcher-level FFP self-report: 2.9% (95% CI 2.1–3.8%); **not paper prevalence**.
- VITALITY I: retracted RCTs propagated into meta-analyses and clinical guidelines, demonstrating that source-paper count alone understates downstream burden.
- Tang & Cai 2025: among 200,000 life-science systematic reviews, 299 incorporated at least one already-retracted paper-mill article into evidence synthesis (0.15%); 124/385 qualifying citations occurred after retraction. This is a detected-pathway contamination benchmark, not latent paper-mill prevalence.
- Scancar et al. 2026 demonstrates large-scale text screening feasibility but also why detector training on known/retracted cases cannot replace population-random adjudication.

---

# Current blockers / gates

## GATE B1 — real Pilot B feature frame — PASS

Completed real 2015–2020 seed frame:

- OpenAlex core article+review target denominator: **38,451,124**;
- population-random works: **600**;
- Retraction Watch enrichment works resolved into the target universe: **739**;
- unique selected works: **1,339**;
- exact inclusion probabilities/design weights retained;
- OpenAlex ID remains first-class because **229/600** population-random works lacked a DOI;
- no region/nationality/institution/language feature is used as a suspicion feature.

See `process/PILOT_B_SEED_RESULTS.md` and `data/pilot/pilot_b_seed_summary.json`.

## GATE B2 — calibrated adjudication — INPUTS COMPLETE / AI EXECUTION PENDING

Confirmatory random audit now supersedes the 600-work engineering random component for final prevalence estimation.

- target universe: OpenAlex core article+review, 2000–2025;
- live scaled denominator: **137,436,109** works;
- random audit: **10,000** works;
- six publication-period strata with explicit inclusion probabilities/design weights;
- **3,747 / 10,000** sampled works lack a DOI;
- dual blinded article adjudication: **20,000 assignments / 80 batches**.

Earlier Pilot A denominator was 137,445,874. The -9,765 difference (~-0.0071%) is retained as live-database snapshot drift.

See `process/SCALED_AUDIT_RESULTS.md` and `process/AI_ADJUDICATION_HANDOFF.md`.

AI may provide most labels, but its measurement error must be calibrated or sensitivity-tested. Dual-model agreement is not gold-standard truth.

## GATE C — latent prevalence identification

No global hidden-case estimate until:

- random-audit estimate and latent model are reconcilable;
- posterior materially updates the prior;
- one detector/field does not dominate;
- missingness sensitivity does not change estimates by an order of magnitude.

## GATE D — semantic contamination — AI INPUTS COMPLETE / LABELS PENDING

The real high-propagation stress-test contains:

- 25 source papers;
- 7,443 observed incoming citation exposures;
- 1,753 post-retraction exposures;
- 486 sampled post-retraction edges;
- **972 dual-AI semantic assignments / 10 deterministic batches**;
- 200 edges with full-text signal and 290 with OA signal.

Raw citation exposure remains distinct from contamination. SCF and Dependence Ghost Half-Life require semantic labels and calibration. See `process/CITATION_AI_HANDOFF.md`.

## GATE F — RLY / cost scaling

Scenario model remains non-empirical until effort distributions are calibrated. Whole associated grants are never called wasted funding.

## GATE G/H — innovation and Sleeping Beauty

Innovation Delay requires valid matched topic controls and pre-trends. Permanent Never-Woken Sleeping Beauty counts remain downstream exploratory work.

---

# Next execution queue

1. Execute the **80 article-adjudication batches** with AI_A and AI_B under `AI-ADJ-V1`.
2. Merge article outputs with `merge_ai_adjudications.py`; arbitrate disagreements/LOW/INDETERMINATE cases.
3. Execute the **10 citation-edge batches** under `CIT-EDGE-V1`.
4. Calibrate/sensitivity-test AI measurement error with formal/high-confidence anchors.
5. Fit weighted latent prevalence only after calibration.
6. Convert semantic citation labels into SCF and **Dependence Ghost Half-Life**.
7. Continue RLY/cost calibration and Innovation Delay event-study infrastructure.
8. Keep Never-Woken Sleeping Beauty counterfactual behind the causal-identification gate.

---

# Do not do

- Do not multiply researcher self-report prevalence by global publication counts.
- Do not divide all Retraction Watch events by all OpenAlex works and call the result fraud prevalence.
- Do not add overlapping E1-S/E1-M/E1-P counts.
- Do not infer fraud from country, language, institution or journal.
- Do not treat text/image detector positives as guilt.
- Do not call every citation contamination.
- Do not publish Fermi scenario output as empirical finding.
- Do not claim a global count of never-awakened discoveries before the causal chain validates.

---

# Handoff sentence

If this chat is lost, resume from this file. **The 10,000-work confirmatory random audit is complete; 20,000 article-level AI assignments are split into 80 deterministic batches; the 486-edge semantic-citation task is split into 972 assignments / 10 batches. The next prevalence-critical work is executing and calibrating AI labels, not rebuilding samples. Do not estimate global latent prevalence before calibration.**

# STATUS — ARIS4C005

**Last updated:** 2026-09-18  
**State:** `PILOT_A_COMPLETE / PILOT_B_ENGINEERING_READY`  
**ARIS provenance:** v0.4.26 @ `951654847b015585385b2448c5667dcd04e7b56b`

## Canonical research identity

**The Hidden Burden of Bad Science: Estimating the Global Scale and Downstream Cost of Research Integrity Failures**

Scope remains frozen. The project has moved from design-only work into live public-data execution.

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

## GATE B1 — real Pilot B feature frame

Need a reproducible row-level frame combining:

- a population-random OpenAlex component;
- formal correction/retraction/EOC signals;
- at least one additional independent detector stream if legally/reproducibly available;
- explicit detector applicability/missingness.

The frame must not use region/nationality as a suspicion feature.

## GATE B2 — manual adjudication capacity

A real article-level prevalence estimate requires human adjudication. Engineering dry-run threshold:

- >=100 resolved population-random adjudications;
- >=1 detector with estimable sensitivity and specificity.

Publication-scale target remains 750–1,500 adjudicated works with double coding of severe/disagreement cases.

## GATE C — latent prevalence identification

No global hidden-case estimate until:

- random-audit estimate and latent model are reconcilable;
- posterior materially updates the prior;
- one detector/field does not dominate;
- missingness sensitivity does not change estimates by an order of magnitude.

## GATE D — semantic contamination

Raw citation counts are not contamination. A validated material-dependence classifier/manual coding layer is still required for global SCF/KGH.

## GATE F — RLY / cost scaling

Scenario model remains non-empirical until effort distributions are calibrated. Whole associated grants are never called wasted funding.

## GATE G/H — innovation and Sleeping Beauty

Innovation Delay requires valid matched topic controls and pre-trends. Permanent Never-Woken Sleeping Beauty counts remain downstream exploratory work.

---

# Next execution queue

1. Build a **real Pilot B seed frame**: OpenAlex random works + formal correction-signal enrichment with public-safe provenance.
2. Run the probability-aware sampler on that frame.
3. Produce an adjudication packet with blinded sampling metadata separated from reviewer-facing fields.
4. Add at least one independent detector family only if its validation/applicability can be documented.
5. Run a small adjudication micro-pilot to test label usability and disagreement rate.
6. Freeze Pilot B calibration outputs.
7. Only then implement/fill the Bayesian latent prevalence model.
8. In parallel, begin the evidence-synthesis contamination module because VITALITY/Tang-Cai provide a strong validated pathway.

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

If this chat is lost, resume from this file. **Pilot A is complete. Pilot B engineering is ready. The next valid task is a real, probability-traceable Pilot B seed frame plus a small adjudication micro-pilot; do not reopen broad idea generation.**

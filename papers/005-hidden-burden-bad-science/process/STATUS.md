# STATUS — ARIS4C005

**Last updated:** 2026-09-19  
**State:** `AI_EXECUTION_READY / CALIBRATION_PIPELINE_READY / LATENT_MODEL_VALIDATED / IMPACT_SCAFFOLDS_READY`  
**ARIS provenance:** v0.4.26 @ `951654847b015585385b2448c5667dcd04e7b56b`

## Canonical research identity

**The Hidden Burden of Bad Science: Estimating the Global Scale and Downstream Cost of Research Integrity Failures**

Scope remains frozen. The 10,000-work confirmatory audit, all 90 AI input batches, batch-output integrity gates, latent prevalence model, correlated-error sensitivity, AI calibration design/candidate/reference-review infrastructure, RLY framework, Innovation Delay scaffold, and SB0/SB1 delayed-recognition infrastructure are complete. The prevalence-critical dependency is now actual AI adjudication labels plus actual reference-review/calibration labels, not further sampling or ontology design.

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
- [x] Direct narrow-domain time anchors added: 177 team-hours per retrospective publication, 14 manuscript-formatting hours, and a qualified 4–8 h peer-review context range; transportability and overlap limits are explicit.

## Pilot A — live public-data acquisition

- [x] GitHub Actions networked runner operational.
- [x] OpenAlex core article+review universe extracted for 2000–2025.
- [x] OpenAlex denominator is snapshot-dependent: an earlier frozen query returned **137,445,874** works; the latest Pilot A live snapshot on 2026-09-19 returned **137,434,060** under the same target metadata definition. Snapshot drift is retained rather than forced away.
- [x] Annual counts and query provenance committed.
- [x] Latest Retraction Watch snapshot pinned to Git commit `8324ad5ae03519e1f213d417c6cf3e02d7dc5d1f` (older snapshots retained in Git history).
- [x] Snapshot summarized without redistributing raw CSV.
- [x] Latest live Retraction Watch snapshot: **72,621** correction/event rows.
- [x] Latest live snapshot: **63,504** unique resolvable original-paper DOIs.
- [x] Latest live snapshot: **61,041** unique original DOIs had at least one event with nature `Retraction`.
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
- [x] Fail-closed batch-output collector implemented for all 80 article + 10 citation batches; checksum/row-count/adjudicator/prompt/vocabulary/abstention invariants enforced.
- [x] Calibrated dual-AI latent prevalence model implemented and six-stratum synthetic recovery passed.
- [x] Correlated-AI-error sensitivity implemented from conditional independence to maximal positive shared-error dependence.
- [x] Calibration anchor design implemented with exact rare-event specificity bounds: at 95% confidence and zero observed false positives, ~299 independent negatives support FPR<1%, ~598 support <0.5%, ~2,995 support <0.1%, ~5,990 support <0.05%, and ~29,956 support <0.01%.
- [x] Private Retraction Watch calibration-candidate builder implemented; row-level candidates are not committed/uploaded.
- [x] Latest candidate queues: **1,435 P_HIGH_REVIEW / 586 P_REVIEW / 5,314 N_PROCESS_REVIEW / 3,026 N_ERROR_REVIEW / 53,143 U_REVIEW**; these are review queues, not truth labels.
- [x] Blinded dual reference-review pipeline implemented: REF_A/REF_B receive neutral bibliography only, never queue labels or AI_A/AI_B outputs.
- [x] Reference merger preserves detailed states (`HONEST_MAJOR_ERROR`, `MINOR_OR_IMMATERIAL`, `NO_MATERIAL_PROBLEM_FOUND`) and only promotes dual-consensus A/B anchors; disagreements/unresolved/C-quality cases stay out of Se/Sp calibration.
- [ ] Run dual-AI article adjudication + arbitration.
- [ ] Run dual-AI citation-edge adjudication + arbitration.
- [ ] Execute REF_A/REF_B primary-evidence reference reviews on calibration candidates, merge dual-consensus anchors, then calibrate AI error using A-only primary / A+B sensitivity sets.

## RLY / human-time burden

- [x] RLY decomposition frozen as RLY-P / RLY-D / RLY-C / RLY-I.
- [x] Fail-closed RLY calculator implemented.
- [x] Empirical total is blocked when attribution, time conversion, or overlap resolution is missing.
- [x] Direct narrow-domain time anchors recorded with non-transportability warnings.
- [x] Participant sacrifice, career spillover, peer-review denominator and financial cost remain separate dimensions unless a valid time-conversion model exists.
- [ ] Calibrate attributable hours per severe-failure unit / material-dependence edge / correction event before any empirical global RLY total.

## Innovation Delay / Scientific Detour

- [x] Innovation Delay protocol and data contract frozen.
- [x] Matched event-study estimator implemented with baseline normalization, pre-trend diagnostics and bootstrap intervals.
- [x] Output-equivalent delay years implemented without relabeling them as literal discovery years.
- [x] Pre-shock OpenAlex semantic-neighborhood candidate builder implemented; post-treatment matching leakage is prohibited.
- [x] Azoulay et al. retraction-spillover study recorded as causal-design precedent.
- [ ] Run real matched topic event studies after adjudicated E1-S source set is available.

## Sleeping Beauty / delayed recognition

- [x] Ke et al. Beauty Coefficient and awakening-time definitions implemented.
- [x] Historical citation trajectories reconstruct full incoming-citation years using live OpenAlex grouped queries; truncated Work `counts_by_year` is explicitly forbidden for mature histories.
- [x] Mature random engineering pilot completed on **200/200** cited article/review works published 1990–2005 and observed through 2025.
- [x] Current main-run SB0 pilot: B median **2.5**, q95 **26.78**, max **85**; peak age median **6 y**; awakening age median **4.5 y**.
- [x] Leakage-safe SB1 landmark dataset implemented and live-tested.
- [x] With landmark age 5 and 10-year horizon, **200/200** pilot papers had mature follow-up; **56** had engineering awakening-after-landmark outcomes and **74** had late-peak outcomes.
- [x] SB1 early-citation baseline implemented with publication-year-blocked out-of-fold validation: **AUC 0.614**, **Brier 0.1973** vs prevalence-baseline **0.2045** (improvement **0.0072**). Interpretation: early citation trajectory carries only modest signal and is not enough for lost-discovery identification.
- [ ] Add temporally frozen semantic/network predictors for SB1.
- [ ] Run SB2 integrity-exposure / awakening-hazard analysis only after E1-S/SCF exposure is empirically available.
- [ ] Keep SB3 suppressed-opportunity / never-awoken counterfactual behind calibration and causal-identification gates.

---

# Live Pilot A anchors

Primary target denominator:

`OpenAlex core + type:article|review + publication_year:2000-2025`

- latest Pilot A metadata count (2026-09-19 snapshot): **137,434,060**
- source: OpenAlex Works API
- extraction timestamp stored in `data/pilot/openalex_universe_provenance.json`

Retraction Watch snapshot:

- latest event rows: **72,621**
- latest unique original-paper DOIs: **63,504**
- latest unique original DOIs with Retraction nature: **61,041**
- paper-mill signal unique DOIs: **11,706**
- narrow auto E1-S unique DOIs: **2,021**
- strong E1-M unique DOIs: **18,871**
- strong E1-P unique DOIs: **20,429**
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

Calibration-candidate infrastructure is now operational. Latest public-safe aggregate queue counts are stored in `data/pilot/ai_calibration_candidate_summary.json`; row-level candidates remain private/ephemeral. `CAL-REF-V1` supports independent REF_A/REF_B evidence review. Machine dual-consensus is explicitly reported as machine-assisted reference evidence, not a human gold standard.

## GATE C — latent prevalence identification — MODEL READY / LABELS PENDING

- [x] Weighted six-stratum latent prevalence model implemented.
- [x] AI sensitivity/specificity treated as uncertain measurement parameters.
- [x] Synthetic truth recovery passed.
- [x] Positive correlated-error sensitivity implemented for shared AI false positives/false negatives.
- [ ] Actual article AI labels not yet available.
- [ ] Anchor calibration and missingness sensitivity still required before a global hidden-case estimate.

No global hidden-case estimate is authorized until actual labels, calibration and sensitivity checks are complete.

## GATE D — semantic contamination — AI INPUTS COMPLETE / LABELS PENDING

The real high-propagation stress-test contains:

- 25 source papers;
- 7,443 observed incoming citation exposures;
- 1,753 post-retraction exposures;
- 486 sampled post-retraction edges;
- **972 dual-AI semantic assignments / 10 deterministic batches**;
- 200 edges with full-text signal and 290 with OA signal.

Raw citation exposure remains distinct from contamination. SCF and Dependence Ghost Half-Life require semantic labels and calibration. See `process/CITATION_AI_HANDOFF.md`.

## GATE F — RLY / cost scaling — FRAMEWORK READY / ATTRIBUTION PENDING

The fail-closed RLY component model and several direct time anchors exist, but a global empirical RLY total remains blocked until attributable affected-unit counts, hours-per-unit distributions, overlap resolution, and a defensible research-year conversion are calibrated. Whole associated grants are never called wasted funding.

## GATE G — Innovation Delay — ESTIMATOR READY / REAL MATCHED PANELS PENDING

Protocol, pre-shock candidate discovery, matched event-study estimation, pre-trend diagnostics and output-equivalent delay metrics are implemented. Real causal estimates require adjudicated source exposure plus frozen pre-treatment controls.

## GATE H — Sleeping Beauty — SB0/SB1 ENGINEERING PASS / SB2-SB3 PENDING

Historical B/awakening measurement and a leakage-safe landmark dataset are operational. No universal B cutoff is imposed. Integrity-related awakening suppression (SB2) and suppressed-opportunity counts (SB3) remain downstream of calibrated exposure and causal identification.

---

# Next execution queue

1. Execute the **80 article-adjudication batches** with independent AI_A and AI_B under `AI-ADJ-V1` (or continue any already-started external run without changing prompt/schema).
2. Run `collect_ai_batch_outputs.py --mode article` to verify all 20,000 returned assignments against the canonical manifest before any merge.
3. Merge A/B article outputs, route disagreements/LOW/INDETERMINATE cases to arbitration, and preserve abstentions.
4. Execute the **10 citation-edge batches** under `CIT-EDGE-V1`.
5. Run `collect_ai_batch_outputs.py --mode citation`, then semantic disagreement/arbitration.
6. Regenerate private calibration candidates via Pilot A as needed, create blinded REF_A/REF_B packets, execute `CAL-REF-V1`, merge only dual-consensus A/B anchors, then calibrate AI measurement error; report correlated-error, anchor-quality and missingness sensitivity.
7. Fit the weighted six-stratum global latent-prevalence model.
8. Convert calibrated semantic citation labels into SCF and **Dependence Ghost Half-Life**.
9. Run real Innovation Delay matched event studies using adjudicated E1-S sources and pre-shock controls.
10. Calibrate RLY attributable-time components; keep unsupported components scenario-only or NOT_IDENTIFIED.
11. Add temporally frozen semantic/network predictors to SB1, then test SB2 integrity exposure; keep SB3 suppressed-opportunity counts exploratory until causal gates pass.

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
- Do not hand-concatenate AI batch outputs; run the manifest/checksum collector first.
- Do not add 14 h formatting time on top of a full idea-to-publication time estimate when that estimate already includes submission/revision labor.

---

# Handoff sentence

If this chat is lost, resume from this file plus `process/CHAT_HANDOFF_2026-09-19.md`. **Sampling, 90 AI input batches, batch-output integrity validation, latent prevalence inference, correlated-error sensitivity, calibration design/candidate/reference-review infrastructure, RLY framework, Innovation Delay scaffold, and SB0/SB1 delayed-recognition infrastructure are complete. The next prevalence-critical work is actual execution of article/citation AI batches and REF_A/REF_B evidence reviews, followed by collector validation, arbitration, calibration and the weighted latent model. Do not rebuild the 10,000-work sample, expose private candidate rows, hand-concatenate outputs, or estimate global prevalence/RLY/lost discoveries before their gates pass.**

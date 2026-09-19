# ARIS4C005 — Chat / Cross-Agent Handoff

**Handoff date:** 2026-09-19  
**Canonical repository:** `CochraneK/ARIS4C`  
**Paper path:** `papers/005-hidden-burden-bad-science/`  
**Canonical branch:** `main`  
**Main HEAD observed before this handoff branch:** `3327b7beb9624dfb94f519e9bbe12692264ec1f1`

This file is the deletion-safe recovery point for the ChatGPT thread that developed ARIS4C005. It records conversation-derived decisions, current progress, recovery instructions and next actions so another ChatGPT conversation, computer, account or agent can continue from Git without reconstructing the project from chat memory.

---

## 1. Research identity

**ARIS4C005 — The Hidden Burden of Bad Science: Estimating the Global Scale and Downstream Cost of Research Integrity Failures**

Core question:

> How much of the global scholarly literature is affected by serious research-integrity failures or broader reliability problems, and how far do these problems propagate through scientific knowledge, human time, funding, participant burden and delayed/lost innovation?

The project deliberately separates:

- observed detections from latent prevalence;
- severe scientific-integrity failure from honest error / QRP / process fraud;
- source-paper count from downstream contamination;
- money, Researcher-Life-Years, participant burden, output delay and delayed recognition into separate units.

Do not collapse them into one universal “bad-science cost score”.

---

## 2. Frozen ontology / scope

Exposure families:

- **E1-S** — severe scientific integrity failure materially affecting scientific claims/results;
- **E1-M** — misconduct/integrity violation that may not invalidate the scientific result;
- **E1-P** — publication/process integrity failure such as paper mills, forged authorship or compromised peer review;
- **E2** — probable/uncertain integrity failure;
- **E3** — broader research waste / honest major error / nonpublication / unreliability without established misconduct.

Loss ontology:

1. production loss;
2. career loss;
3. knowledge loss;
4. innovation loss;
5. societal loss.

Primary article-level binary latent target for prevalence modelling:

- positive = `SEVERE_SUPPORTED`;
- unresolved states are not silently recoded as negative.

---

## 3. Global denominator / live snapshots

Primary publication universe:

`OpenAlex core + type:article|review + publication_year:2000-2025`

Latest Pilot A live snapshot at handoff:

- OpenAlex works: **137,434,060**
- retrieval stored in `data/pilot/openalex_universe_provenance.json`

Confirmatory 10k audit used its own live snapshot:

- denominator: **137,436,109**
- difference from latest Pilot A is normal live-database snapshot drift and must be preserved, not “fixed”.

Retraction Watch latest live snapshot:

- source Git commit: `8324ad5ae03519e1f213d417c6cf3e02d7dc5d1f`
- event rows: **72,621**
- unique original-paper DOIs: **63,504**
- unique DOIs with Retraction nature: **61,041**
- narrow auto E1-S unique DOIs: **2,021**
- strong E1-M unique DOIs: **18,871**
- strong E1-P unique DOIs: **20,429**
- paper-mill signal unique DOIs: **11,706**

These are detected/corrected records, never latent prevalence.

---

## 4. Confirmatory article prevalence pipeline — current state

Completed:

- 10,000-work full-period stratified random audit;
- six publication-period strata;
- exact inclusion probabilities / design weights;
- **3,747 / 10,000** sampled works have no DOI;
- DOI-less cases remain in the target universe; DOI-only inference is forbidden;
- dual AI input: **20,000 assignments / 80 deterministic batches**;
- fail-closed output collector validates exact manifest row counts, checksums, adjudicator IDs, prompt versions, vocabulary, duplicates and abstentions;
- calibrated measurement-error latent prevalence model implemented;
- six-stratum synthetic recovery passed;
- correlated AI shared-error sensitivity implemented.

Canonical article handoff:

- `process/AI_ADJUDICATION_HANDOFF.md`
- prompt: `process/AI_ADJUDICATION_PROMPT_V1.md`
- prompt version: `AI-ADJ-V1`
- batch manifest: `data/pilot/scaled_ai_batch_manifest.json`

Canonical post-fix 10k workflow artifact provenance is recorded in `process/SCALED_AUDIT_RESULTS.md`.

### Do not

- rebuild the 10,000 sample;
- drop no-DOI cases;
- hand-concatenate returned batches;
- treat AI agreement as gold truth;
- report global latent prevalence before actual labels + calibration + sensitivity checks.

---

## 5. Citation contamination pipeline — current state

Stress-test source set:

- 25 high-propagation narrow E1-S sources;
- 7,443 incoming citation exposures;
- 1,753 exposures after retraction (**23.55%** in this deliberately non-representative stress-test);
- 486 sampled post-retraction citation edges;
- **972 dual-AI assignments / 10 deterministic batches**.

Current raw Citation Ghost Half-Life pilot:

- 23 estimable sources;
- 20 half-life events;
- 3 right-censored;
- Kaplan–Meier median: **1 year**.

This is citation persistence, not semantic contamination.

Canonical citation handoff:

- `process/CITATION_AI_HANDOFF.md`
- prompt: `process/CITATION_AI_ADJUDICATION_PROMPT_V1.md`
- prompt version: `CIT-EDGE-V1`

After semantic adjudication, upgrade to:

- Scientific Contamination Footprint;
- Dependence Ghost Half-Life;
- Epistemic reproduction / branching analysis.

---

## 6. AI calibration — current state

### 6.1 Exact rare-event specificity design

Implemented in:

- `code/calibration_anchor_design.py`
- `data/pilot/ai_calibration_anchor_design.json`
- `process/AI_CALIBRATION_ANCHOR_PROTOCOL.md`

At 95% confidence with **zero observed false positives**, approximate independent negative-anchor counts required to bound FPR below:

- 1% → **299**
- 0.5% → **598**
- 0.1% → **2,995**
- 0.05% → **5,990**
- 0.01% → **29,956**

Interpretation: a small calibration panel cannot prove 99.9–99.99% specificity. Final prevalence inference must retain specificity/shared-error sensitivity.

### 6.2 Private calibration candidate queues

Row-level candidates are intentionally runner-private / ephemeral and must not be committed or publicly uploaded.

Latest public-safe aggregate:

- `P_HIGH_REVIEW`: **1,435**
- `P_REVIEW`: **586**
- `N_PROCESS_REVIEW`: **5,314**
- `N_ERROR_REVIEW`: **3,026**
- `U_REVIEW`: **53,143**

Stored at:

- `data/pilot/ai_calibration_candidate_summary.json`

Important semantics:

- queues are **review candidates, not truth labels**;
- `N_ERROR_REVIEW` means error/reproducibility signal without strong integrity flags and still needs evidence that it is non-severe / honest error;
- absence of a flag is never a negative reference standard.

### 6.3 Dual machine-assisted reference review

Implemented on main:

- `process/AI_CALIBRATION_REFERENCE_PROMPT_V1.md`
- `data/ai_calibration_reference_review_template.csv`
- `code/make_calibration_reference_packets.py`
- `code/merge_calibration_reference_reviews.py`

Rules:

- reviewers are `REF_A` and `REF_B`;
- they receive neutral bibliography only;
- they do **not** see candidate queue, Retraction Watch reason flags, AI_A/AI_B output, design weight or the other reference reviewer;
- prompt version = `CAL-REF-V1`;
- detailed states are preserved:
  - `SEVERE_SUPPORTED`
  - `HONEST_MAJOR_ERROR`
  - `MINOR_OR_IMMATERIAL`
  - `NO_MATERIAL_PROBLEM_FOUND`
  - `SERIOUS_UNRESOLVED`
  - `INDETERMINATE`
- A anchors = primary calibration;
- A+B = sensitivity;
- C / unresolved / reviewer disagreement = excluded from Se/Sp calibration;
- `HONEST_MAJOR_ERROR` can be a binary negative anchor while remaining scientifically material;
- machine dual-consensus must be reported as **machine-assisted reference evidence**, not independent human gold standard.

The user explicitly intends to let another model replace human raters. Preserve this distinction in the manuscript.

---

## 7. RLY / “wasted research youth” module

Implemented:

- `process/RLY_PARAMETER_EVIDENCE.md`
- `data/rly_parameter_ledger.csv`
- `data/rly_model_template.json`
- `code/rly_cost.py`

Components:

- RLY-P — production;
- RLY-D — downstream misdirection;
- RLY-C — replication/correction;
- RLY-I — integrity-maintenance labor.

Fail-closed rule:

No empirical total unless affected units, hours/unit, attribution fraction, overlap handling and research-year conversion are defensibly calibrated.

Direct narrow-domain anchors currently include:

- **177 team-hours/publication** for a specific retrospective surgical-study sample;
- **14 h/manuscript** formatting burden from an international survey;
- peer-review contextual range around **4–8 h/review**.

Do not globally extrapolate these as universal constants.

Do not add the 14h formatting anchor on top of an idea-to-publication estimate that already includes manuscript/submission/revision time.

Participant burden, career spillover and money remain separate units unless a valid time conversion exists.

---

## 8. Innovation Delay / Scientific Detour

Implemented:

- `process/INNOVATION_DELAY_PROTOCOL.md`
- `process/INNOVATION_DELAY_DATA_CONTRACT.md`
- `code/build_innovation_candidates.py`
- `code/innovation_delay.py`

Design:

- treated unit = pre-shock topic neighborhood, not author;
- matching uses pre-shock information only;
- post-treatment leakage is prohibited;
- event study uses baseline normalization, pre-trend diagnostics and bootstrap intervals;
- output-equivalent delay years are not literal “discovery delayed by X years”.

Real causal analysis waits for adjudicated source exposure.

---

## 9. Sleeping Beauty / delayed recognition

Implemented:

- Ke et al. Beauty Coefficient;
- awakening-time estimator;
- complete historical incoming-citation reconstruction via live `cites:<work>&group_by=publication_year`;
- mature random pilot;
- leakage-safe 5-year landmark / 10-year horizon dataset;
- publication-year-blocked out-of-fold early-citation baseline.

Important OpenAlex rule:

Do **not** use Work-level `counts_by_year` for mature historical citation trajectories because it is truncated to roughly recent years.

Latest engineering pilot:

- mature papers: **200/200**
- landmark-horizon awakening outcomes: **56**
- late-peak outcomes: **74**
- SB1 early-citation baseline:
  - AUC **0.6139**
  - Brier **0.19734**
  - prevalence-baseline Brier **0.20450**
  - improvement **0.00716**

Interpretation: early citation trajectory has only modest predictive signal. It is not enough to claim identification of buried discoveries.

Next SB work:

- add temporally frozen semantic/network predictors;
- then SB2 integrity-exposure / awakening-hazard analysis;
- keep SB3 suppressed-opportunity / “never-awoken” count exploratory until calibration and causal gates pass.

---

## 10. Actual next execution queue

1. Execute / finish the **80 article AI batches** under `AI-ADJ-V1`.
2. Run `collect_ai_batch_outputs.py --mode article`; do not hand-merge.
3. Merge AI_A/AI_B outputs; preserve LOW / INDETERMINATE / disagreement and arbitrate.
4. Execute / finish the **10 citation-edge batches** under `CIT-EDGE-V1`.
5. Run `collect_ai_batch_outputs.py --mode citation`; then semantic disagreement/arbitration.
6. Rerun Pilot A if private calibration candidate rows need regeneration.
7. Build blinded REF_A / REF_B packets.
8. Execute `CAL-REF-V1` using independent model runs/accounts where possible.
9. Merge only dual-consensus A/B reference anchors.
10. Estimate Se/Sp and abstention by anchor quality / access state; retain shared-error and specificity sensitivity.
11. Fit weighted six-stratum global latent prevalence.
12. Convert semantic citation labels into SCF / Dependence Ghost Half-Life.
13. Run real Innovation Delay matched panels.
14. Calibrate RLY components.
15. Add frozen semantic/network SB1 predictors; only then test SB2/SB3.

---

## 11. Files a new agent should read first

Read in this order:

1. `process/STATUS.md`
2. this file
3. `process/AI_ADJUDICATION_HANDOFF.md`
4. `process/CITATION_AI_HANDOFF.md`
5. `process/AI_CALIBRATION_ANCHOR_PROTOCOL.md`
6. `process/AI_CALIBRATION_REFERENCE_PROMPT_V1.md`
7. `process/RLY_PARAMETER_EVIDENCE.md`
8. `process/INNOVATION_DELAY_PROTOCOL.md`
9. `process/SLEEPING_BEAUTY_PROTOCOL.md`

Then inspect `data/pilot/` summaries and manifests before changing any design.

---

## 12. Conversation-derived decisions that must not be lost

- The paper should be vivid and quantify not only false papers but also “how much researcher life was consumed, how much good science was crowded out/delayed, and how many delayed-recognition opportunities may have been suppressed.”
- Those human/innovation outputs must remain scientifically conservative and multidimensional, not one sensational total.
- The editorial line “the largest cost of bad science may be the true discoveries we never got to see” is allowed as framing only, not an empirical conclusion.
- User prefers continuous GO mode with minimal confirmation.
- Once requirements are clear, continue implementation → test → fix → merge rather than stopping at planning.
- Every important state must be persisted to Git; do not rely on chat context.
- AI can replace human raters for this project, but the paper must explicitly distinguish dual-machine reference evidence from human gold-standard adjudication.
- Do not infer misconduct from country, language, institution, prestige or journal.
- No raw Retraction Watch candidate accusation list should be publicly committed.

---

## 13. Open PR hygiene at handoff

Several older ARIS4C005 PRs remain open because main advanced through clean-rebased/superseding branches or automated summary commits. Their functionality has already been verified on main where noted.

Known stale/superseded open PRs at the time of handoff include:

- #18 latent prevalence old branch
- #41 RLY old branch
- #45 Innovation Delay old branch
- #65 AI collector old branch
- #70 / #71 / #72 calibration-design old branches
- #76 earlier reference-review branch
- #78 honest-error candidate branch
- #81 clean-rebased reference-review branch

Do not assume an open PR means the feature is absent. Check main first. These can be closed later as superseded after confirming no unique diff remains.

---

## 14. Resume sentence

**Do not redesign ARIS4C005. Resume from actual execution and calibration.** The infrastructure is already extensive; the main scientific bottleneck is real article/citation adjudication plus reference-evidence calibration. Once those labels exist, run the already-built measurement-error / weighting / contamination / impact pipeline rather than inventing a new one.

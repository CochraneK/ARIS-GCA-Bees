# ARIS4C009 · Deletion-safe chat / cross-agent handoff

**Date:** 2026-09-19  
**Paper:** 009 — Phenomenology-Preserving Computational Psychiatry  
**Canonical repository:** `CochraneK/ARIS4C`  
**Canonical paper path:** `papers/009-phenomenology-preserving-computational-psychiatry/`

This file exists so the current ChatGPT conversation can be deleted without losing the
scientific decisions, empirical progress, implementation state, or the next execution queue.

---

## 1. Research identity

Working title:

> **The Fidelity Frontier in Computational Psychiatry: Decomposing Acquisition and Encoding Loss in Psychopathology**

The project is not merely a review of computational psychiatry plus phenomenology.
Its core contribution is an empirical measurement architecture for asking how much
psychiatric information is lost at different stages of measurement and representation.

Canonical decomposition:

[
H \rightarrow A_m \rightarrow X^{(m)} \rightarrow E_k \rightarrow Z^{(m,k)}
]

where:

- `H` = lived state, not directly observable;
- `A_m` = acquisition / elicitation method;
- `X^(m)` = evidence produced under that acquisition method;
- `E_k` = encoding / representation method;
- `Z^(m,k)` = derived representation.

Critical rule:

> **Do not confuse acquisition divergence with encoding loss.**

A real self-report questionnaire is not a compressed version of a phenomenological
interview. Same-source projections can be compared for encoding loss; independently
administered methods belong in the acquisition benchmark.

---

## 2. Measurement philosophy that must remain frozen

The project uses a multi-objective / Pareto framing rather than one universal score.

Keep separate:

- phenomenological / source-grounded fidelity;
- reliability;
- intended-use validity;
- predictive or intervention utility;
- burden / privacy / representation rate;
- physical/context correspondence.

Do not collapse them into one scalar unless explicitly justified for a secondary analysis.

The project preserves raw evidence and builds lossy analytical representations downstream:

> **lossless source preservation + lossy analytical representation**

No latent model is treated as the physical essence of the patient.

Physical/context data may constrain claims about time, place, activity, sleep, physiology,
medication timing, etc., but must not be treated as deciding subjective ownership,
agency, salience, meaning, reality quality, or self/world boundaries.

---

## 3. Paper sequence

- **009A1** — fixed-source encoding benchmark.
- **009A2** — acquisition-method benchmark.
- **009B** — cross-level mechanism / neurophenomenology.
- **009C** — longitudinal idiographic dynamics.
- **009D** — perturbation / intervention validation.

Do not merge A1 and A2 back together.

---

## 4. Novelty boundary

Broad novelty claims were already audited and retired.

Do **not** claim invention of:

- computational phenomenology;
- neurophenomenology;
- phenomenological fidelity;
- phenomenological interviewing;
- narrative distortion;
- psychiatric text summarization;
- ecological-validity concerns in computational psychiatry;
- use-conditioned validity;
- rate-distortion theory.

The surviving novelty candidate is the integrated experimental architecture:

1. acquisition / encoding decomposition;
2. same-source multi-representation psychiatric benchmark;
3. representation-blind query generation and evaluation;
4. semantic / relational / contextual / temporal / participant-endorsed reconstruction;
5. acquisition loss analyzed separately from encoding loss;
6. fidelity separated from reliability / intended-use validity / prediction;
7. equal-rate / equal-burden comparisons;
8. use-conditioned Pareto analysis.

Safe wording:

> We propose a framework for decomposing information loss in psychopathology into acquisition- and encoding-stage components and for empirically benchmarking multiple same-source psychiatric representations using blinded, source-grounded reconstruction tasks while treating phenomenological fidelity, reliability, intended-use validity, predictive utility, and burden as separate objectives.

Gate A is only a **conditional research-development pass**. A submission-stage
multi-database novelty search is still required.

---

## 5. Pilot-0 dataset and privacy

Pilot-0 uses:

> **DAIS-C — Discussing Abstract Ideas in Schizophrenia Corpus**

The corpus is open, but raw psychiatric transcripts are **never mirrored into public
ARIS4C**.

Current public-safe engineering facts:

- 28 usable full-interaction transcripts recovered;
- 1,908 interviewer-anchored candidate microepisodes;
- 1,871 with participant responses;
- participant words per valid microepisode: median 14, IQR 2–50.

The one-Q/A-turn rule was rejected as too granular.

Segmentation sensitivity:

- target 20 words → 953 windows, median 52 participant words, median 1 microepisode/window;
- target 40 words → 745 windows, median 79 words, median 2 microepisodes/window;
- target 80 words → 550 windows, median 116 words, median 3 microepisodes/window.

20 and 40 advance to calibration. 80 remains a rescue condition.

Important limitation:

> **Do not infer schizophrenia-vs-comparison disease effects from Pilot-0 window counts, lengths, or interview structure.**

The source groups are not acquisition/topic-exchangeable.

---

## 6. Boundary-calibration history and final decision from this chat

The original design used two independent human raters.

The user first asked whether one human rater could be enough. The methodological answer
was that one human can support feasibility but cannot support inter-rater reliability.

The user then explicitly decided:

> **Cancel human raters; use different AI models instead.**

This decision is now canonical.

PR **#90** was merged into main:

> `009: switch boundary calibration to multi-model AI judges`

Merge commit:

> `8010eb7fa61cbe751368901417a4c0fe7eb09faf`

PR #89 is an older superseded branch and should not be treated as the canonical change.

---

## 7. Canonical Gate-C AI-judge design

Pilot-0 Gate C now uses **at least three materially different model families/providers
where feasible**.

Rules:

1. same frozen judge prompt and output schema;
2. same blinded source items;
3. no judge sees another judge's output;
4. no judge sees target word count, cohort, participant ID, source filename, or private key;
5. no browsing / retrieval augmentation;
6. fresh or equivalently isolated item context;
7. deterministic or near-deterministic decoding where supported;
8. record provider, family, exact version/date, decoding setting, and data-handling mode;
9. no post-hoc prompt changes after primary scoring starts.

Do not treat several aliases/checkpoints from one model family as strong independence.

Cross-model agreement is an automated robustness test, **not** human reliability evidence.

Permitted manuscript language:

- **AI-judge agreement**
- **cross-model agreement**

Do **not** call it:

- human inter-rater reliability;
- clinician agreement;
- human validation.

---

## 8. Gate-C packet and scoring implementation

Private packet builder:

- `code/build_private_boundary_packet.py`

Default primary/stress packet:

- 60 regular condition-A items;
- 60 regular condition-B items;
- 10 stress items per condition;
- 140 total primary/stress items;
- primary analysis uses 120 regular items;
- 20 disjoint real-data dry-run windows remain outside primary agreement.

Current generated judge files:

- `judge_01.tsv`
- `judge_02.tsv`
- `judge_03.tsv`
- more judges are supported.

The builder also creates a private judge-manifest template recording:

- provider;
- model family;
- model version;
- execution date;
- determinism / temperature;
- data-handling mode;
- frozen prompt file.

Frozen prompt:

- `process/AI_JUDGE_PROMPT_BOUNDARY.md`

Judge manual:

- `process/RATER_MANUAL_BOUNDARY.md`

The filename is legacy, but its contents now describe AI judging.

Scorer:

- `code/score_boundary_ratings.py`

It now supports N judges and computes:

- multi-model percent agreement;
- multi-model Gwet AC1;
- all pairwise Gwet AC1 values;
- judge-specific usable rates;
- majority-usable rate;
- unanimous-usable rate;
- action distributions;
- model-family outlier patterns.

Operational usable window:

- coherent = yes;
- sufficient = yes;
- mixed unrelated topics = no;
- action = keep.

---

## 9. Gate-C dry run and CI truth boundary

Before the AI redesign, a real-DAIS-C packet/scorer smoke workflow had passed end-to-end.

PR #90 updated that workflow to generate and score **three mock AI judge files**.

However, at this handoff the GitHub connector returns **no workflow run/status attached
to merge commit `8010eb7...`**.

Therefore the precise state is:

- three-AI smoke **code exists on main**;
- the earlier real-DAIS-C smoke passed;
- **do not claim that a post-PR90 three-AI workflow run was independently observed as green from this chat**.

A future agent should verify the workflow run on current main before upgrading that statement.

---

## 10. Gate-C decision rule

Primary comparison remains 20-word target versus 40-word target.

Revise segmentation if:

- cross-model AC1 is clearly inadequate;
- >25% of regular windows require merge / split / reject across the ensemble;
- insufficiency dominates the shorter strategy;
- mixed-topic judgments materially increase in the longer strategy;
- one model family is a systematic outlier and the conclusion depends on including it.

If 20 and 40 perform similarly:

> prefer the lower-bandwidth 20-word strategy and let the later query-bank pilot test whether more context is necessary.

If both fail, reopen 80-word or semantic-boundary segmentation.

---

## 11. Current exact blocker / next execution

There is **no human-rater blocker anymore**.

The current unresolved Gate-C task is exactly:

> **Run the frozen 140-item private packet through at least three approved, materially different AI judge models and score cross-model agreement.**

Do not write as though those actual AI judgments already exist. They do not yet exist
in the public Git state.

If external APIs are used, DAIS-C source text may only be sent to endpoints whose
retention/training/data-use terms are compatible with source-data governance.

Local models are acceptable and may be preferable for privacy.

After the three judge files are frozen:

1. run `score_boundary_ratings.py`;
2. inspect multi-model and pairwise AC1;
3. inspect judge outliers;
4. unblind A/B only after judge outputs are frozen;
5. choose 20 vs 40 or reopen segmentation;
6. freeze segmentation;
7. proceed to Gate D source-only query/relation calibration.

---

## 12. Gate D onward

After segmentation is frozen:

### Gate D — query / relation calibration

- construct source-only questions;
- estimate answerability;
- cluster / remove redundant queries;
- calibrate relation annotation;
- estimate evaluator variance;
- test R3P / R4P projection feasibility;
- keep representation-blind query generation.

### Gate E — DAIS-C representation benchmark

Candidate representations:

- R0 rich source;
- R1 structured episode graph;
- R2-lite specialist phenomenological coding;
- R3P questionnaire-format same-source projection;
- R4P conventional symptom/clinical same-source projection;
- R5 compact quantitative representation;
- optional frozen LLM exploratory representation.

R3P and R4P are **same-source projections**, not independently administered instruments.

### Gate F — AMP-SCZ Pilot-1

Minimum access plan is already drafted in:

- `process/PILOT1_AMPSCZ_MINIMUM_ACCESS.md`
- `process/AMPSCZ_VARIABLE_MINSET.csv`

Tier 1 prioritizes language/transcript evidence, PSYCHS structured measures,
participant/visit linkage, and minimal conventional comparators.

### Gate G — 009A2 purpose-collected acquisition study

Separate future human study; randomized/counterbalanced acquisition design remains
conceptually separate and requires ethics approval.

---

## 13. Files a new agent should read first

Read in this order:

1. `process/STATUS.md`
2. this file
3. `process/RESEARCH_PLAN.md`
4. `process/GATE_A_NOVELTY_REVIEW_2026-09-19.md`
5. `process/BOUNDARY_CALIBRATION_PROTOCOL.md`
6. `process/AI_JUDGE_PROMPT_BOUNDARY.md`
7. `process/RATER_MANUAL_BOUNDARY.md`
8. `process/PILOT0_DAISC_STRUCTURE.md`
9. `process/PILOT0_DAISC_EPISODES.md`
10. `process/PILOT0_DAISC_SEGMENTATION.md`
11. `process/PILOT0_DAISC_LIMITATIONS.md`
12. `process/PILOT1_AMPSCZ_MINIMUM_ACCESS.md`

Then inspect the packet builder, scorer, and `.github/workflows/aris4c009-boundary-smoke.yml`.

---

## 14. Do not lose these conversation-derived decisions

- The user prefers GO mode: once scope is clear, implement → inspect → fix → continue without repeated confirmation.
- Important project state must live in Git, not only in chat.
- Human raters are intentionally removed from Pilot-0 Gate C.
- Use multiple heterogeneous AI judges rather than pretending one or two same-family models provide independent validation.
- AI agreement must never be presented as human reliability.
- Do not expose raw DAIS-C psychiatric text in public Git, public CI artifacts, issues, or unsafe external APIs.
- Do not infer disease effects from DAIS-C group differences in interview/window structure.
- Preserve the acquisition-vs-encoding decomposition.
- Preserve fidelity, reliability, validity, prediction, burden and physical correspondence as distinct objectives.
- Do not make broad “first-ever” novelty claims without the final formal search.

---

## 15. Open-PR hygiene

- PR **#90** is merged and is canonical for the AI-judge switch.
- PR **#89** is an older superseded open PR from the same migration. Do not assume it
  represents missing work; compare against main before closing it.

---

## 16. Resume sentence

**Do not redesign ARIS4C009.** Resume at Gate C execution. The conceptual framework,
DAIS-C source engineering, privacy protections, segmentation sensitivity, private packet
builder, frozen AI-judge prompt, N-judge scorer, and AMP-SCZ access plan are already in
Git. The next empirical task is to run the frozen private packet through at least three
approved heterogeneous AI models, score cross-model agreement, freeze 20-vs-40
segmentation, and only then proceed to source-only query/relation calibration.

---

## 17. Superseded on 2026-09-19 — Gate C executed

Sections 12 and 16 are preserved as history, not as the live task list. That task is complete:
the frozen 140-item packet was rated by three blinded, materially different model families,
cross-model agreement was scored, and the **40-word** segmentation target was selected.

Current state lives in `AI_JUDGE_CALIBRATION_RESULTS_2026-09-19.md` and `STATUS.md`.
**Do not reopen the 20-vs-40 choice.** Resume from Gate D implementation, and derive any boundary
label from ≥2-of-3 model consensus.

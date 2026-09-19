# ARIS4C009 Pilot-0 · AI boundary-calibration protocol

## Why this gate exists

The first machine rule produced 1,908 interviewer-anchored microepisodes, but many were too short to support nontrivial reconstruction:

- participant-response median = 14 words;
- 25th percentile = 2 words.

Structural accumulation improved the unit size:

| Target | Windows | Median participant words | Median microepisodes/window | >250 words |
|---:|---:|---:|---:|---:|
| 20 | 953 | 52 | 1 | 58 |
| 40 | 745 | 79 | 2 | 61 |
| 80 | 550 | 116 | 3 | 66 |

The 80-word strategy is not advanced to primary calibration because it mixes more question-answer units while increasing long-window burden.

The primary calibration compares **20 versus 40 participant-word targets** using multiple blinded AI judges.

## Judge architecture

Pilot-0 uses **at least three materially different AI model families/providers where feasible**.

A valid judge run must satisfy all of the following:

- same frozen task prompt and answer schema;
- no access to the target word count;
- no access to cohort, participant identifier or source file;
- no access to other judges' answers;
- no web browsing or retrieval augmentation;
- fresh context per item or an equivalently isolated batch protocol;
- deterministic or near-deterministic decoding where supported;
- model/provider/version/date recorded;
- no post-hoc prompt changes after primary scoring begins.

Using several aliases or checkpoints from the same model family is not treated as strong independence. Cross-model agreement is a robustness check, not evidence of human inter-rater reliability.

## Prompt-development phase

Synthetic practice cases may be used to debug the prompt and output parser.

The 20 disjoint real-data training windows are a **private dry run** for refusal, formatting, context-length and obvious instruction-following failures. They never enter the primary agreement estimate.

AI judges do not discuss training cases with one another and do not see one another's outputs. Once the prompt is frozen, it is not modified using primary-item results.

## Blinding

The packet generator randomizes the two strategies to labels A/B.

Judges do not see:

- target word count;
- clinical/comparison cohort;
- participant identifier;
- source file name;
- another judge's decision;
- the private condition key.

The private key remains sealed until all primary judge outputs are frozen.

## Calibration sample

Default packet:

- 60 regular windows from condition A;
- 60 regular windows from condition B;
- within each condition: 30 clinical-source and 30 comparison-source windows;
- 10 stress windows per condition sampled from below-target tails or >250-word windows.

Total = 140 primary/stress items.

Stress items are excluded from the primary strategy comparison.

## Judge questions

For each window:

1. **coherent_boundary** — does this form one interpretable conversational unit?
2. **sufficient_nontrivial** — is there enough information for at least one nontrivial source-grounded question?
3. **mixed_unrelated_topics** — are unrelated topics combined?
4. **recommended_action** — keep / merge / split / reject.
5. **confidence_1_5**.
6. optional brief note.

## Primary engineering outputs

- multi-judge percent agreement;
- multi-rater Gwet AC1 applied to AI judges;
- every pairwise Gwet AC1;
- usable-without-modification rate for each judge;
- majority-usable and unanimous-usable rates;
- merge/split/reject profile by blinded strategy;
- judge-specific outlier patterns.

A window is operationally "usable" for a judge only when:

- coherent = yes;
- sufficient = yes;
- mixed unrelated topics = no;
- action = keep.

## Decision logic

These are engineering rules, not confirmatory clinical thresholds.

### Revise segmentation if

- cross-model AC1 is clearly inadequate after the prompt is frozen;
- >25% of regular windows require merge/split/reject across the judge ensemble;
- "insufficient" dominates the shorter strategy;
- "mixed unrelated topics" materially increases in the longer strategy;
- one model family behaves as a systematic outlier and the result depends on including it.

### Candidate strategy selection

Prefer a strategy that improves query-sufficiency without materially increasing mixed-topic judgments.

If 20- and 40-word strategies perform similarly, prefer the lower-bandwidth 20-word strategy and let the later query-bank pilot test whether extra context is needed.

If both are inadequate, reopen the 80-word or semantic-boundary strategy.

## What AI agreement can and cannot establish

It can establish whether the segmentation decision is robust across different automated judges under a frozen rubric.

It does **not** establish:

- human interpretability;
- clinician agreement;
- participant-meaning fidelity;
- EASE validity;
- clinical validity;
- schizophrenia effects;
- representation fidelity.

Any later claim requiring human/clinical judgment must be validated in a separate study.

## Privacy and data governance

The packet contains psychiatric interview text.

Therefore:

- output defaults to a gitignored private directory;
- do not upload source packets as GitHub Actions artifacts;
- do not commit judge inputs or private keys;
- use only local models or external endpoints whose retention/training terms are compatible with the source-data governance;
- record the execution environment and provider data-handling mode;
- only aggregate scorer outputs may be published after review.

## Commands

After locally extracting DAIS-C:

`python code/build_private_boundary_packet.py --root /path/to/daisc --judge-count 6`

Start more judges than the ensemble needs, because endpoint quota routinely prevents some from
finishing. Packet contents are deterministic in the seed: drawing extra judge files does not
change `judge_01..NN` or `private_key.json`.

Then run each judge independently (the executor resumes already-rated items, so the packet can be
completed across as many runs as endpoint throttling requires):

`python code/run_ai_boundary_judges.py --packet-dir <packet> --prompt-file process/AI_JUDGE_PROMPT_BOUNDARY.md --judge judge_01=MODEL_A --out-dir <ratings> --data-handling "<endpoint retention statement>"`

Freeze inclusion **before unblinding**: a judge enters the ensemble only if
`items_rated == items_total` and `items_failed == 0`. Partial runs are excluded, never scored on
the item subset they happened to finish, and must be disclosed to the publisher so the exclusion
is auditable rather than invisible.

Only after every included judge file is complete and frozen:

`python code/score_boundary_ratings.py --judge <ratings>/rated_judge_01__MODEL_A.tsv --judge ... --key <packet>/private_key.json --json-out boundary_score.json --md-out boundary_score.md`

Publish aggregate-only artifacts (the publisher refuses to write if a judge is incomplete, if the
judges did not share one frozen prompt hash, if the committed prompt no longer matches what the
judges were given, or if anything contains source speech):

`python code/publish_boundary_ai_calibration.py --score-json boundary_score.json --score-md boundary_score.md --manifest <ratings>/judge_01__MODEL_A.manifest.json ... --excluded-manifest ... --reason "<disclosure>" --out-dir data/derived/boundary_ai_judges --run-date YYYY-MM-DD`

## Executed outcome — 2026-09-19

Three complete judges (`gpt-oss-120b`, `nemotron-3-ultra`, `stepfun-3.7-flash`), 140/140 items
each, 0 failures; three further families were started and excluded for quota/route failures.
Aggregate artifacts live in `data/derived/boundary_ai_judges/`.

Decisions taken under the rules above, and the caveats that survive them, are recorded in
`AI_JUDGE_CALIBRATION_RESULTS_2026-09-19.md`. The prompt is now history: it cannot be revised
against these items, so any rerubrication requires a new frozen prompt and a new packet.

## Interpretation boundary

This gate only determines whether Pilot-0 has a defensible automated unit of analysis. It is explicitly an **AI-judge calibration**, not a substitute claim for human rating reliability.

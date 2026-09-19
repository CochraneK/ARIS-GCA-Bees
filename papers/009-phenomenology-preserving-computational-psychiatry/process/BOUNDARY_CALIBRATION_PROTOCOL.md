# ARIS4C009 Pilot-0 · Boundary calibration protocol

## Why this gate exists

The first machine rule produced 1,908 interviewer-anchored microepisodes, but many were
too short to support nontrivial reconstruction:

- participant-response median = 14 words;
- 25th percentile = 2 words.

Structural accumulation improved the unit size:

| Target | Windows | Median participant words | Median microepisodes/window | >250 words |
|---:|---:|---:|---:|---:|
| 20 | 953 | 52 | 1 | 58 |
| 40 | 745 | 79 | 2 | 61 |
| 80 | 550 | 116 | 3 | 66 |

The 80-word strategy is not advanced to primary calibration because it mixes more
question-answer units while increasing long-window burden.

The human calibration therefore compares **20 versus 40 participant-word targets**.

## Blinding

The packet generator randomizes the two strategies to labels A/B.

Raters do not see:

- target word count;
- clinical/comparison cohort;
- participant identifier;
- source file name;
- the other rater's decisions.

The private key remains sealed until both ratings are frozen.

## Calibration sample

Default packet:

- 60 regular windows from condition A;
- 60 regular windows from condition B;
- within each condition: 30 clinical-source and 30 comparison-source windows;
- 10 stress windows per condition sampled from below-target tails or >250-word windows.

Total = 140 items.

Stress items are excluded from the primary strategy comparison.

The packet builder prevents selected A/B windows from sharing the same source
microepisode region where possible.

## Rater questions

For each window:

1. **coherent_boundary** — does this look like one interpretable conversational unit?
2. **sufficient_nontrivial** — is there enough information to support at least one
   nontrivial semantic/relational/context question?
3. **mixed_unrelated_topics** — does the window appear to combine unrelated topics?
4. **recommended_action** — keep / merge / split / reject.
5. **confidence_1_5**.
6. optional note.

## Primary engineering outputs

- percent agreement;
- Gwet AC1;
- usable-without-modification rate;
- merge/split/reject profile by blinded strategy.

A window is operationally "usable" only when a rater marks:

- coherent = yes;
- sufficient = yes;
- mixed unrelated topics = no;
- action = keep.

## Decision logic

These are engineering rules, not confirmatory clinical thresholds.

### Revise segmentation if

- primary-item AC1 is clearly inadequate after rater training;
- >25% of regular windows require merge/split/reject;
- "insufficient" dominates the shorter strategy;
- "mixed unrelated topics" materially increases in the longer strategy.

### Candidate strategy selection

Prefer a strategy that improves query-sufficiency without materially increasing
mixed-topic judgments.

If 20- and 40-word strategies perform similarly, prefer the lower-bandwidth 20-word
strategy and let the later query-bank pilot test whether additional context is needed.

If both are inadequate, reopen the 80-word or semantic-boundary strategy.

## Privacy

The packet contains source interview text.

Therefore:

- output defaults to `data/raw/boundary_calibration/`;
- this location is ignored by Git;
- do not upload the packet as a GitHub Actions artifact;
- do not commit rater files or the private key;
- only aggregate scorer outputs may be published after review.

## Commands

After locally extracting DAIS-C:

`python code/build_private_boundary_packet.py --root /path/to/daisc`

After two independent raters finish:

`python code/score_boundary_ratings.py --rater-a ... --rater-b ... --key ... --json-out ... --md-out ...`

## What this gate does not answer

Boundary calibration does not establish:

- EASE validity;
- participant-meaning fidelity;
- representation fidelity;
- schizophrenia effects;
- clinical utility.

It only determines whether Pilot-0 has a defensible unit of analysis.

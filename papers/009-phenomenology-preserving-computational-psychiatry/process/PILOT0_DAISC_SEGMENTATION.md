# ARIS4C009 Pilot-0 · Segmentation sensitivity

**Generated:** 2026-09-19T05:15:16.263916+00:00

## Privacy rule
No transcript text, file names, or participant IDs are emitted.

## Structural strategy
Adjacent interviewer-response microepisodes are greedily accumulated until a target
number of participant words is reached. Source turns are never split.

This does **not** claim that word count defines phenomenological episodes. It creates
candidate windows for human calibration.

| Target participant words | Windows | Median participant words | IQR | Median microepisodes/window | Below target | >250 words |
|---:|---:|---:|---:|---:|---:|---:|
| 20 | 953 | 52 | 31.0–107.0 | 1 | 28 | 58 |
| 40 | 745 | 79 | 52.0–132.0 | 2 | 28 | 61 |
| 80 | 550 | 116.0 | 92.0–182.0 | 3.0 | 28 | 66 |

## Interpretation rule

The preferred engineering target should:

- eliminate most trivial one-word/yes-no units;
- keep most windows short enough for independent human reconstruction;
- avoid requiring many unrelated question-answer pairs per window;
- preserve enough windows for calibration and later benchmarking.

No target becomes canonical from these statistics alone.

## Next gate
Select one or at most two candidate targets for a blinded human boundary-calibration
sample. Human split/merge/reject judgments determine whether the structural rule is
acceptable.

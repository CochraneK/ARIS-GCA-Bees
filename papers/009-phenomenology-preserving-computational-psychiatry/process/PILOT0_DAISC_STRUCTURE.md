# ARIS4C009 Pilot-0 · DAIS-C structural classification

**Generated:** 2026-09-18T23:38:53.741321+00:00

## Privacy rule

No transcript text or participant IDs are emitted. Classification occurs only inside
the transient GitHub Actions runner.

## Structural classes

| Class | Files | Unique pseudonymous speaker IDs | Participant words | Interviewer words |
|---|---:|---:|---:|---:|
| interactional | 8 | 8 | 27,707 | 10,430 |
| non_transcript_text | 30 | 0 | 0 | 0 |
| speaker_only | 28 | 28 | 85,667 | 0 |
| timestamped | 7 | 7 | 2,152 | 2,146 |

## Published validation reference

The DAIS-C resource paper reports approximately:

- 97,357 corpus tokens;
- 1,284.8 audio minutes.

Those values are **not** expected to match this script exactly because the archive
contains multiple representations of the same speech and the script uses a simple
Unicode word tokenizer. They are used to detect gross duplication or parser failure.

## Canonical-candidate rule

For Pilot-0 episode parsing, the preferred source class is:

> `interactional` — files containing both a participant XML block and `<INT>`
> interviewer blocks, while excluding timestamp-only representations.

If this class does not recover approximately one transcript representation per
participant or produces implausible aggregate scale, the parser must be revised before
any fidelity analysis.

## Next gate

Freeze an episode parser on calibration-only files and report only aggregate episode
counts, length distributions, and annotation feasibility before manual fidelity scoring.

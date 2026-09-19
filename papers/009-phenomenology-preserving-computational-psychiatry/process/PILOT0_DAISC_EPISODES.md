# ARIS4C009 Pilot-0 · DAIS-C episode inventory

**Generated:** 2026-09-19T05:12:32.493539+00:00

## Privacy rule

No transcript text, participant IDs, or raw file names are emitted.

## Frozen engineering episode rule

> One interviewer block starts an episode. All immediately following participant
> blocks belong to that episode until the next interviewer block.

This is a **parser rule**, not yet a validated phenomenological episode definition.

## Corpus-level result

- full-interaction transcripts selected: 28
- interviewer turns: 1908
- participant turns: 1889
- candidate episodes: 1908
- episodes with participant response: 1871
- episodes without participant response: 37
- orphan participant turns: 0
- consecutive-interviewer pairs: 14

## Cohort structure

| Cohort | Transcripts | Candidate episodes | With response | No response | Orphan participant turns |
|---|---:|---:|---:|---:|---:|
| clinical | 15 | 1273 | 1249 | 24 | 0 |
| comparison | 13 | 635 | 622 | 13 | 0 |

## Valid-episode length distributions

### Participant words

- median: 14
- IQR: 2.0–50.0
- p10–p90: 1.0–126.0
- min–max: 0–1031

### Interviewer words

- median: 10
- IQR: 2.5–23.0
- p10–p90: 1.0–42.0

### Participant turns per episode

- median: 1
- IQR: 1.0–1.0
- p10–p90: 1.0–1.0

## Sample-availability note

The DAIS-C publication/data record describes 15 clinical and 14 comparison speakers.
The public archive's full-interaction source layer is inventoried separately here.
A recruited participant without a usable full-interaction source is not silently treated
as an analyzable fidelity episode.

## Human validation gate

Before any semantic/phenomenological fidelity result:

1. draw a calibration-only sample of parsed episodes;
2. have two trained raters judge whether the machine boundary is coherent;
3. record split / merge / reject decisions;
4. revise the parser rule if boundary error is material;
5. freeze the rule before benchmark scoring.

Only after this gate can machine-derived candidate episodes become annotation units.

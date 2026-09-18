# ARIS4C009 Pilot-0 · DAIS-C structural classification

**Generated:** 2026-09-18T23:41:02.071313+00:00

## Privacy rule
No transcript text or participant IDs are emitted. TXT/RTF/DOCX parsing occurs only
inside the transient GitHub Actions runner.

## Readable formats
- `.docx`: 41
- `.rtf`: 15
- `.txt`: 58

## Structural classes
| Class | Files | Unique pseudonymous speaker IDs | Participant words | Interviewer words |
|---|---:|---:|---:|---:|
| interactional | 28 | 28 | 86,014 | 33,068 |
| non_transcript_text | 30 | 0 | 0 | 0 |
| speaker_only_xml | 28 | 28 | 85,667 | 0 |
| timestamped | 28 | 27 | 5,854 | 5,909 |

## Sanitized archive path patterns
Speaker identifiers and long numeric strings are masked.
- `interactional: DAIS-C-Annotated - Upload/DAI-C-CL/Interactional/Full tagged pass/<PID>-FULL.docx` × 7
- `interactional: DAIS-C-Annotated - Upload/DAI-C-CL/Interactional/Full tagged pass/<PID>-FULL.rtf` × 8
- `interactional: DAIS-C-Annotated - Upload/DAI-C-CO/Interactional/Full tagged pass/<PID>-FULL.docx` × 13
- `non_transcript_text: DAIS-C-Annotated - Upload/DAI-C-CL/Speaker Only_Raw/<PID>_Raw.txt` × 15
- `non_transcript_text: DAIS-C-Annotated - Upload/DAI-C-CL/Speaker Only_Raw/WMatrix-full-clinical-raw.txt` × 1
- `non_transcript_text: DAIS-C-Annotated - Upload/DAI-C-CO/Speaker Only_Raw/<PID>_Raw.txt` × 13
- `non_transcript_text: DAIS-C-Annotated - Upload/Readme.txt` × 1
- `speaker_only_xml: DAIS-C-Annotated - Upload/DAI-C-CL/Interactional/Full tagged pass/Speaker_only_for_analysis/<PID>_speaker.txt` × 15
- `speaker_only_xml: DAIS-C-Annotated - Upload/DAI-C-CO/Interactional/Full tagged pass/Speaker_only_for_analysis/<PID>_speaker.txt` × 13
- `timestamped: DAIS-C-Annotated - Upload/DAI-C-CL/Timestamped/21UNI11-TS.docx` × 1
- `timestamped: DAIS-C-Annotated - Upload/DAI-C-CL/Timestamped/<PID>-TS.docx` × 7
- `timestamped: DAIS-C-Annotated - Upload/DAI-C-CL/Timestamped/<PID>-TS.rtf` × 7
- `timestamped: DAIS-C-Annotated - Upload/DAI-C-CO/Timestamped/<PID>-TS.docx` × 13

## Published validation reference
The DAIS-C paper reports approximately 97,357 total corpus tokens
(58,444 clinical; 33,025 comparison) and 1,284.8 audio minutes.
These are validation references rather than exact tokenizer targets.

## Canonical-source gate
A source class is acceptable only if it contains interviewer + participant speech,
excludes timestamp-only versions, has plausible corpus scale, and does not duplicate
the same interview through multiple formats.

If no full-interaction class passes, Pilot-0 must either use speaker-only XML with an
explicit context limitation or switch corpus.

## Next gate
Freeze an episode parser only after the canonical source class is identified.

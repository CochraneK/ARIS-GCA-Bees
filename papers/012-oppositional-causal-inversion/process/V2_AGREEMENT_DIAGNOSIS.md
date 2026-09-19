# V2 AGREEMENT DIAGNOSIS — ARIS4C012

Sample: fresh v2 blind validation set V201..V230 (Pilot 0B excluded)
Coders: A2 and B2, independent, both frozen before comparison
Input bundle: `9f0d8b785b8f8f739cdd41cf7c6f9f6fc3f7fbdf2299587cbab6d732bdddfc51`
Response hashes: A2 `5256b8a64f1a4d11276fa3ffcbfc4c5859b510f9ac08c8d2bde9c8e8c082bd86`, B2 `e2f0065cb603a9e8cd8a2a13db8f8a6f15f9d90147e8338f369f38bf7b0f16c6`
Scored by `code/score_v2_agreement.py` -> `data/reliability/v2_reliability_summary.json`

**Gate outcome: `REVISE_V2_INSTRUMENT`.** The 165-record evidence-map frame remains locked.

## 1. Headline numbers

| metric | value | threshold | pass |
| --- | --- | --- | --- |
| `opposition_valid` Cohen's kappa | 0.481 | >= 0.70 | no |
| median kappa, informative axes (33/33 informative) | 0.372 | >= 0.70 | no |
| secondary axes passing (kappa >= 0.60 and raw >= 0.80) | 1 / 32 | all | no |
| disagreement cells | 380 | — | — |

Only `idx_level_switch` (kappa 0.632, raw 0.800) passes the secondary gate.

## 2. The primary gate failure is not a base-rate artifact

For `opposition_valid` the coders agree on 0.733 of records against a Cohen
chance expectation of 0.487, giving kappa 0.481 and Krippendorff's nominal alpha
0.471; the two agree closely, so the low kappa is not the prevalence paradox
(no category is used by either coder more than 73% of the time). It is a
systematic liberality shift: `yes` prevalence is 0.53 for A2 and 0.73 for B2, and
7 of the 8 focal `opposition_valid` disagreements run in the same direction
(A2 `no` -> B2 `yes`). Records: V203, V205, V211, V214, V215, V225, V228 (A2
negative, B2 positive); V227 is the single reverse case.

## 3. Partition of the 380 disagreement cells

| failure mode | cells | share |
| --- | --- | --- |
| `0` vs `uncertain` | 259 | 68.2% |
| other (multi-category ordinal) | 56 | 14.7% |
| `0` vs `1` (substantive) | 37 | 9.7% |
| `1` vs `uncertain` | 28 | 7.4% |

By axis group: mechanism 122, evidence mode 107, relation 57, ordinal/valence 40,
index 38, entry gate 16.

On the evidence-mode axes, 96 of 107 cells are the same direction: A2 `uncertain`
/ B2 `0`. A2's `uncertain` rate over the vector axes is 0.479 versus B2's 0.406.
This is one rule-application conflict, not 107 independent judgements.

## 4. Root causes

**RC1 — schema precedence rule 4 is undecidable as written.** Section 1 says
missing information is not coded `no`, and rule 4 says use `uncertain` rather than
`0` when the packet does not resolve an axis. But the vectors are multi-label
negatives-by-default: a given paper genuinely does not *use* a randomized
experiment whether or not the packet is informative about it. `0` therefore carries
two incompatible readings ("absent in this packet" vs "the record does not have it"),
and `uncertain` is the only escape hatch. Coders split on which reading applies.
This alone accounts for 68% of all cells.

**RC2 — `opposition_valid` and `oci_candidate` are redundant.** The two fields are
identical within each coder for 30/30 records, and their 16 disagreement cells are
the same 8 records duplicated. They are one item scored twice, which inflates the
informative-axis count without adding information.

**RC3 — `evidence_strength` has no anchored scale.** Raw agreement 0.367 against a
Cohen chance expectation of 0.227, i.e. kappa 0.181 and nominal alpha 0.172 — the
coders do beat chance, but only just, and the marginals show why: A2 spreads over
`moderate` (11), `weak` (8) and `none` (6) and uses `uncertain` 3 times, while B2
concentrates on `uncertain` (10) and `weak` (9) and reaches `strong` once. They are
scaling the same word differently, and no anchor ties strength to a concrete
feature of the packet.

**RC4 — mechanism vectors have no positive test.** Mechanism fields are the worst
passing group (all kappa <= 0.18, `mech_capacity_overload` at -0.041). The schema
lists mechanism names but no observable packet feature that distinguishes "present"
from "plausible", so both coders fall back to `uncertain` about half the time.

## 5. What v2 got right

The v2 changes that targeted Pilot 0B's avoidable failures did land. There are
**zero** lexical/token-vocabulary cells (Pilot 0B had 30): every one of the 380
cells is a legitimate schema value on both sides, and both coder files passed
`freeze_v2_coder.py` validation with no invalid tokens. Multi-label vectors also
removed the forced-exclusivity overlaps (Pilot 0B: 24 cells). The remaining
disagreement is concentrated in RC1, which v2 introduced by adding `uncertain` to
the vectors.

## 6. Consequences

- No full 165-record screening on v2 as frozen.
- Pilot 0B and this v2 result are both immutable failures of their instruments;
  neither may be re-scored by post-hoc harmonization.
- A v3 amendment must target RC1-RC4 and be validated on a *new* independent
  sample that does not overlap V201..V230.

## 7. Proposed v3 changes, in priority order

1. **Kill the `0`/`uncertain` ambiguity (RC1).** Restrict `uncertain` to the two
   entry fields only. For every vector axis define `0` operationally as "not
   asserted as present in the supplied packet" and require `1` only when the
   packet contains a locatable supporting statement. This is a narrowing of the
   coding question from ontology to packet contents, and it removes 68% of cells
   by construction rather than by persuasion.
2. **Retire `oci_candidate` as a confirmatory item (RC2)**, or give it a decision
   rule that is not "the same judgement" — e.g. restrict it to records where the
   authors use reversal vocabulary but the construct definition is contested.
3. **Anchor `evidence_strength` to packet-visible features (RC3):** a fixed
   ladder keyed to whether the packet contains an identified design, an effect
   estimate, and a focal reversal test, instead of a holistic quality read.
4. **Demote mechanism vectors from confirmatory to exploratory (RC4)** until a
   positive test exists; report them descriptively and keep them out of the
   median-kappa gate.
5. Re-run the gate on a fresh 30-record sample, with `opposition_valid` kappa
   >= 0.70 as the only hard gate and mechanism/evidence axes reported as
   descriptive until they carry a decidable rule.

## 8. Provenance and independence

Both coder files were produced by one driver script on a coding surface that read
only the frozen bundle (common evidence packet, `SCHEMA_V2_FROZEN.md`, the blank
response form's field list). Pilot 0B labels, adjudication materials, and the
other coder's responses were not read into any request. Each request was a
stateless call carrying only the frozen schema plus that batch of packet records,
so neither judge saw the other's labels, and both files were frozen before any
comparison.

What is independent here is the *judge*, not the harness: the prompt text and
field list were identical for A2 and B2 by design, because a reliability test
must vary the coder while holding the instrument fixed. The two coders were
already separate OS processes with separate checkpoint and provenance files; what
a v3 run cannot claim, and should not pretend to claim, is that the two coders
interpreted the schema separately — a shared prompt is a shared interpretation of
the codebook, and any residual ambiguity in that interpretation is exactly what
RC1 measures.

Per-call provenance is committed at
`data/v2_coding/A2_provenance.jsonl` and `B2_provenance.jsonl`, and the runner is
`code/run_v2_coders.py`. The record:

| coder | calls | served model | samples | temperature | retries |
| --- | ---: | --- | ---: | ---: | ---: |
| A2 | 10 | `nvidia/nemotron-3-super-120b-a12b` (2 calls served under the same id with a `:free` rate-limit tag) | 30/30 | 0 | 0 |
| B2 | 10 | `gpt-oss:120b` | 30/30 | 0 | 0 |

Both were requested by explicit model id, never by an `auto`/`claude-*` slot, so
gateway route drift cannot have substituted a different model underneath either
coder. Each coder file carries an identical `input_bundle_sha256`,
`input_evidence_packet_sha256` and `schema_sha256` in its freeze JSON, and
distinct `completed_response_sha256` values, confirming identical inputs and
independently produced outputs. Because the two coder families differ, the
agreement that does exist is not one model re-echoing its own labels.

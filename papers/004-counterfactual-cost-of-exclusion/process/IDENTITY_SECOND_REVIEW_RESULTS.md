# IDENTITY SECOND-REVIEW AND ADJUDICATION RESULTS — ARIS4C004

Executed: 2026-09-19
Scripts: `code/review/` · Data: `data/derived/identity_second_review_*`

## 0. Read this first: what kind of independence this is

The user directive for this project is that the second review and the
adjudication are **AI surfaces**, not human curators; no human will adjudicate
these cases. So this file states exactly what independence is and is not claimed:

- **Blinding is real.** The second reviewer read only a freshly built public
  evidence packet (`data/derived/identity_second_review_evidence_packet_public.jsonl`,
  40 packets: Wikidata entity, frozen candidate-frame identifiers, and OpenAlex
  name-search candidates with works/topics/institutions). That file contains zero
  occurrences of `first_review*`, `identity_status` or `verified_openalex_ids` —
  the first review's verdicts and included Author-ID sets were not visible.
- **Model separation is real between review 2 and the adjudicator**: review 2 ran
  on `gpt-oss:120b`, the adjudicator on `nvidia/nemotron-3-super-120b-a12b`, both
  at temperature 0 with explicit model ids and per-call provenance logs.
- **Model separation is NOT established against review 1.** The first review's
  `reviewer` field records procedural labels only
  (`ARIS4C pre-exposure evidence review`, `ARIS4C automated pre-exposure triage`,
  …), with no model id. So review 2 is independent of review 1 **procedurally**
  (separate session, blinded inputs, no shared context), not provably by model
  family. Any downstream claim must be worded that way.
- **Blinded-to-mental-health means no exposure tier, no CPE result and no
  first-review status were shown** — the protocol's actual blinding list. It does
  *not* mean the packet contains no mental-health-adjacent words: public OpenAlex
  topic labels such as `Mental Health and Psychiatry` (case `cv_Q95927`) and
  `Alcohol Consumption and Health Effects` (`cv_Q1393663`) appear as *candidate
  author-profile topics*, which the protocol explicitly permits as identity
  evidence. Do not cite this pass as content-level MH-blind.

## 1. Second review: 40/40 executed and scored

Deterministic 40-case set from `identity_second_review_blind_assignment.csv`
(every `VERIFIED_CLUSTER`, `AMBIGUOUS_COLLISION`, `EXCLUDED_IDENTITY_ERROR`, plus
the seeded 25% sample of `VERIFIED_SINGLE`). 11 API calls, all served
`gpt-oss:120b`; one batch needed a retry because the model silently omitted the
trailing case, and the retry re-requested only that case.

| protocol metric | value |
| --- | --- |
| number second-reviewed | 40 |
| exact state agreement | 0.600 (24 / 40) |
| exact Author-ID-set agreement, state-matching verified cases | 0.682 (15 / 22) |
| false-positive identity mapping count | 1 |
| first-review fragments the second review does not include | 18 |
| fragments only the second review includes | 12 |
| collision / error reversals | 1 |
| disagreements requiring adjudication | 23 (16 state, 7 Author-ID-set only) |

By first-review state: `VERIFIED_SINGLE` 9 cases, state agreement 0.889, ID-set
agreement 1.000 · `VERIFIED_CLUSTER` 21, 0.667, 0.500 · `AMBIGUOUS_COLLISION` 8,
0.250 · `EXCLUDED_IDENTITY_ERROR` 2, 0.000.

**This 0.600 is not a precision estimate for the 100-row frame.** The set was
deliberately enriched for hard cases, so it is a disagreement-hunting sample, and
the reviewer is a language model working from OpenAlex/Wikidata signals.

## 2. What the disagreement structure says

- Singles are solid: 8 of 9 first-review singles reproduced exactly, state and ID.
  The identity method's high-confidence regime is not the problem.
- Clusters are the problem and the error is **directional**: 6 of 21 first-review
  clusters were downgraded to single, and 18 first-review fragments were not
  reproduced versus 12 new ones. That asymmetry is an over-merge signature, not
  noise — and over-merging is the dangerous direction here, because a merged
  cluster inflates a person's output and their dependence edges, which feeds the
  counterfactual-removal quantity directly.
- `AMBIGUOUS_COLLISION` at 0.250 is partly a definitional boundary: 2 moved to
  `EXCLUDED_IDENTITY_ERROR` and 2 to `NO_GRAPH_RECORD` (adjacent "do not include"
  states), while 2 moved to a VERIFIED state, which is a genuine conflict.
  `EXCLUDED_IDENTITY_ERROR → NO_GRAPH_RECORD` (2/2) is the same boundary and
  should be logged as a codebook ambiguity, not reviewer error.

## 3. Adjudication: 23/23 executed by evidence, not by vote

`code/review/adjudicate_identity_disagreements.py` — isolated surface, temp 0,
3 cases per call. Its prompt forbids resolving by reviewer preference, vote
counting or confidence heuristics, requires Author IDs to be copied verbatim from
the packet, and instructs it to take the **narrower** option plus
`retrieval_needed=true` when the packet cannot decide. Structural audit
(`data/derived/identity_second_review_adjudication_audit.json`):

| check | result |
| --- | --- |
| cases adjudicated | 23 / 23 |
| included IDs not present in the retrieved packet | 0 |
| invented IDs (dropped by the sanitizer) | 0 |
| verdicts broader than **both** reviews | 0 |
| verdicts equal to the union of both sides | 8 |
| verdicts narrower than both sides | 3 |
| other within-union mixes | 3 |
| adopted second review exactly / first review exactly / neither | 13 / 7 / 3 |
| final states | 14 cluster, 2 single, 3 collision, 2 no-graph, 2 excluded-error |
| still flagged for additional retrieval | 3 (`cv_Q1577507`, `cv_Q6213800`, `cv_Q7416679`) |

The adjudicator is not a tie-breaker: it produced 3 verdicts that match neither
side exactly, and the absence of any "broader than both" verdict plus a net loss
of one included fragment (below) argues against a merge-happy adjudicator. Two
quality caveats are recorded instead of hidden:

- Siding with review 2 in 13/23 cases is a pattern worth a human-free sanity
  check, though review 2 is the *different* model family from the adjudicator, so
  it is not explainable as self-preference.
- `cv_Q24287044` is the weakest deciding rationale in the set: it keeps a
  plant-sciences fragment by asserting an authority link ("SciELO/Universidad del
  Bio-Bio … directly linking") whose citation is not retrievable from the packet.
  Treat this case as unresolved-lean-included, not as settled.

## 4. Effect on the frame (candidate only — canonical table untouched)

`code/resolve/apply_second_review_adjudication.py` folds only the 23 adjudicated
rows into a **candidate** table and fails closed if any other row changes:

- `data/derived/identity_decisions_100.csv` — the frozen first review — is **not
  modified**; the merged result is
  `data/derived/identity_decisions_100_second_review_adjudicated.csv`.
- 8 of 23 statuses changed; 15 of 23 Author-ID sets changed; **10 fragments
  added, 11 removed** (net −1, i.e. the adjudicated frame is marginally *narrower*
  than the first review).
- Within the 23 touched rows: clusters 14→14, singles 1→2, collisions 6→3,
  no-graph 0→2, excluded-errors 2→2.

The candidate table is not the confirmatory frame. Rewriting an included Author-ID
set invalidates the derived verified-work corpus and the network100 frame, so
`PREEXPOSURE_FRAME_FREEZE.md` must be re-derived from the candidate table and the
network rebuilt before exposure coding starts.

## 5. Consequences and next queue

1. Exposure coding remains locked, as the protocol requires.
2. Re-derive the verified-work corpus + network frame from the candidate identity
   table and re-run the observability summaries; only then freeze the frame.
3. Resolve the 3 `retrieval_needed` cases with additional OpenAlex/Wikidata
   retrieval, and re-open `cv_Q24287044` for a citation-grounded decision.
4. Consider the protocol-sanctioned **narrowing** option rather than a gate
   lowering: require one additional strong identifier (ORCID, or an exact
   venue/coauthor/timing triple) for `VERIFIED_CLUSTER`. The cluster-level
   ID-set agreement of 0.500 is the evidence for that change.
5. Amend `IDENTITY_CODEBOOK.md` on the collision / excluded-error / no-graph
   boundaries, which produced 4 of the 16 state disagreements.
6. Record in `DECISIONS.md` that review 2 and adjudication are AI surfaces with
   the independence claim limited to §0.

## 6. Files

- `code/review/build_second_review_packet.py` — blind packet construction (needs `requests`)
- `code/review/run_004_second_review.py` — review-2 runner (needs `FREELLMAPI_BASE_URL` / `FREELLMAPI_API_KEY`)
- `code/review/score_second_review_agreement.py` — protocol precision metrics
- `code/review/adjudicate_identity_disagreements.py` — evidence adjudication surface
- `code/review/audit_adjudication.py` — structural audit of the adjudication
- `code/resolve/apply_second_review_adjudication.py` — non-destructive merge to candidate table
- scratch defaults live outside the tree; set `ARIS4C004_REVIEW_SCRATCH` to choose the output
  directory and `ARIS4C_PAPER_DIR` to point at a different paper checkout

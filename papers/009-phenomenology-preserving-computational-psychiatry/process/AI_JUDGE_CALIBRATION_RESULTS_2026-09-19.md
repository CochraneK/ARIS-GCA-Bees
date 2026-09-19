# ARIS4C009 Gate C · AI boundary-calibration run results

**Executed:** 2026-09-19
**Packet:** frozen private 140-item A/B primary + stress packet (seed `20260919`), plus 20 disjoint dry-run windows
**Prompt:** `process/AI_JUDGE_PROMPT_BOUNDARY.md`, SHA-256 `ec443063ad6a5aa3eb9e5cd8705023a8044cc163cc4f6fa7b32c8acc6f1cb30d` (LF-normalised hash of the committed file)
**Aggregate artifacts:** `data/derived/boundary_ai_judges/{boundary_score.json,boundary_score.md,judge_registry.json}`
**Status:** Gate C executed. Three complete, materially different AI judges scored the frozen packet; cross-model agreement computed and the segmentation decision taken below.

## 1. Question

Does the 20-versus-40 participant-word segmentation survive an independent, blinded
multi-model rubric check, and is the resulting unit of analysis defensible enough to build
Gate-D queries and Gate-E encodings on?

This is an engineering calibration of a machine segmentation rule. It is **cross-model
AI-judge agreement**, not human inter-rater reliability.

## 2. Execution record

| Judge file (blinded) | Model family / provider | Items rated | Failed | Decoding | Start (UTC) |
|---|---|---:|---:|---|---|
| `judge_04` | `gpt-oss-120b` (OpenAI gpt-oss; endpoint reported `@cf/openai/gpt-oss-120b`, `gpt-oss:120b`) | 140/140 | 0 | `temperature=0` | 2026-09-19T06:31:07 |
| `judge_05` | `nemotron-3-ultra` (NVIDIA) | 140/140 | 0 | `temperature=0` | 2026-09-19T06:57:35 |
| `judge_06` | `stepfun-3.7-flash` (StepFun) | 140/140 | 0 | `temperature=0` | 2026-09-19T08:05:01 |

Three families, three different labs, one frozen prompt, one frozen schema, no shared context.
Per-judge provenance (including the model ids each route actually reported back) is in
`judge_registry.json`.

Blinding held as designed: each judge received only its own independently shuffled item file
containing `item_id` and the window text, never the target word count, cohort, source file,
participant identifier, another judge's answers, or `private_key.json`. The key stayed sealed
until all three judge files were frozen.

### Runs started and excluded

| Model family | Items rated | Disposition |
|---|---:|---|
| `deepseek-v4-pro` | 53/140 | excluded — route began returning HTTP 404 mid-run |
| `glm-5.2` | 80/140 | excluded — sustained HTTP 429 on the shared gateway |
| `minimax-m2.7` | 14/140 | excluded — sustained HTTP 429 on the shared gateway |

Inclusion was frozen **before unblinding** as `items_rated == items_total` with
`items_failed == 0`. Partial runs were therefore dropped rather than scored on whatever item
subset they happened to finish, which would have made the two conditions non-comparable. The
three excluded families are recorded in `judge_registry.json` under `excluded_runs` so the
exclusion is auditable rather than invisible.

## 3. Data-handling disclosure

Executed through an OpenAI-compatible gateway listening on `127.0.0.1` only, with the packet
and all judge files kept in a local directory outside the repository. No packet, judge input,
private key, or transcript text was committed, staged as a CI artifact, or written to any
published file.

Important qualification, stated plainly rather than glossed: the loopback gateway forwards
several routes to hosted upstream inference (one judge's reported model id is a hosted
`@cf/...` route id). Interview text therefore left the machine for those routes, under each
upstream provider's own retention terms. No route was verified to be zero-retention. A stricter
reading of the privacy rule would require a fully local endpoint; see §8.

## 4. Cross-model agreement (120 regular windows, 3 judges)

| Field | Percent agreement | Gwet AC1 |
|---|---:|---:|
| `coherent_boundary` | 0.8111 | **0.7425** |
| `sufficient_nontrivial` | 0.9556 | 0.9525 |
| `mixed_unrelated_topics` | 0.9389 | 0.9340 |
| `recommended_action` | 0.7694 | 0.7416 |

Pairwise `coherent_boundary` AC1 ranged 0.6764–0.7924; `recommended_action` 0.6749–0.8074.
The two sufficiency/topicality fields are effectively consensus. The two judgement-call fields
are moderate — the models agree that a window is informative, and disagree about whether its
edges are the right edges.

## 5. Strategy comparison (blinded A/B, decoded after freeze)

Condition A = 40-word target, condition B = 20-word target; 60 regular windows each.

| Indicator | A (40-word) | B (20-word) |
|---|---|---|
| Usable-without-modification, per judge | 0.75 / 0.80 / 0.95 | 0.7333 / 0.7667 / 0.85 |
| ≥2-of-3 judges usable | **0.9167** | 0.8167 |
| All 3 judges usable | 0.6167 | 0.6167 |
| ≥2-of-3 judges request merge/split/reject | **0.0833** | 0.1833 |
| All 3 judges request merge/split/reject | **0.0333** | 0.0833 |
| ≥2 judges: `coherent_boundary = no` | **0.0833** | 0.1333 |
| ≥2 judges: `sufficient_nontrivial = no` | **0.0** | 0.0333 |
| ≥2 judges: `mixed_unrelated_topics = yes` | 0.0167 | 0.0333 |
| Median realised participant words (min–max) | 88 (40–229) | 76 (20–231) |

Keep / merge / split / reject counts (of 60), A: 45/9/6/0, 48/9/1/2, 57/2/1/0. B: 44/12/4/0,
46/12/0/2, 51/9/0/0.

## 6. Protocol decision logic, clause by clause

**Revise segmentation if…**

1. *cross-model AC1 clearly inadequate after the prompt is frozen* — **not triggered** for the
   rubric as a whole (0.93–0.95 on both sufficiency fields), but `coherent_boundary` at
   AC1 0.7425 is the weakest measurement in the gate and is carried forward as the named
   residual risk in §8.
2. *>25% of regular windows need merge/split/reject across the ensemble* — **not triggered**
   (8.33% at 40 words, 18.33% at 20 words under the ≥2-of-3 rule).
3. *`insufficient` dominates the shorter strategy* — **not triggered**: 3.33% of 20-word
   windows drew a ≥2-judge insufficiency flag. Small, but non-zero, and exactly 0.0% at
   40 words.
4. *`mixed unrelated topics` materially increases in the longer strategy* — **not triggered**;
   it did not increase at all (1.67% at 40 vs 3.33% at 20 words). The concern that motivated
   dropping the 80-word condition does not bite between these two targets.
5. *one family behaves as a systematic outlier and the result depends on including it* — see §7.
   Partly applicable, and it changes the strength of the claim, not its direction.

No revise trigger fired.

**Candidate strategy selection.** Prefer the strategy that improves query-sufficiency without
materially increasing mixed-topic judgments → **condition A, the 40-word target**.

The protocol's tie-break ("if 20 and 40 perform similarly, prefer the lower-bandwidth 20-word
strategy") is **not** invoked, for two reasons. First, the direction never reverses on any
ensemble view of the modification rate (see §7). Second, and less obvious before the run: the
two strategies are nearly the same size in practice. Greedy accumulation overshoots the target,
so the realised medians are 88 vs 76 participant words — about 16% apart, not 100%. The
bandwidth saving that would justify picking 20 is largely not there to collect.

Consequences for the next gates:

- 40-word windows are the primary segmentation for Gate D query construction and Gate E encodings;
- 20-word windows are retained as the low-bandwidth arm inside the fixed-source 009A1
  comparison rather than discarded, because their advantage is unproven, not disproven;
- 80-word remains a rescue condition only; this run gives no reason to promote it;
- window-level boundary labels downstream must be treated as a **≥2-of-3 model consensus**, not
  as a single-judge or expert verdict.

## 7. Judge sensitivity: does the answer depend on one family?

`stepfun-3.7-flash` is systematically the most permissive judge (usable 0.95/0.85 vs
0.73–0.80; modification requests 0.05/0.15 vs 0.20–0.27). Its self-reported confidence was not
higher (mean 3.95 vs 3.975 and 4.033), so this is a leniency difference rather than a certainty
difference — though the confidence field barely separates anything: all three judges wrote a note
on 100% of regular items, `gpt-oss-120b` used only values 3 and 4 (3×3, 4×117) and never 5, and
the other two concentrated on 4 as well. Treat `confidence_1_5` as uninformative for weighting in
Gate D rather than as a calibration signal.

Leave-one-judge-out, scored under strict agreement within each reduced ensemble:

| Ensemble | A usable | A modified | B usable | B modified |
|---|---:|---:|---:|---:|
| without `gpt-oss-120b` | 0.7833 | 0.0333 | 0.7333 | 0.1167 |
| without `nemotron-3-ultra` | 0.7333 | 0.0333 | 0.6833 | 0.1000 |
| without `stepfun-3.7-flash` | 0.6333 | 0.0833 | 0.6333 | 0.1333 |

Read honestly, this splits the conclusion:

- the **modification-rate ordering** (40-word needs less repair) survives every subset, with no
  reversal;
- the **usability gap** does not survive dropping the most permissive judge — with
  `stepfun-3.7-flash` removed, the two strategies tie at 0.6333 under strict unanimity.

So the defensible claim is narrow: 40-word windows require fewer structural repairs and are the
only arm with zero insufficiency flags. That 40-word windows are *more often usable outright* is
supported by the 3-judge ensemble but not by strict two-way unanimity without the permissive
judge. Selection is made on the first, stable part.

## 8. Instrument sanity checks

- **Dry run.** The 20 disjoint real-data training windows were rated 20/20 before any primary
  item was scored; the only defect found was truncation from too small a `max_tokens` budget on
  reasoning-style models, fixed in the executor before the primary phase. No primary item
  informed any prompt change.
- **Stress stratum behaves as designed.** On the 10 stress windows per condition (below-target
  tails and >250-word windows), ≥2-of-3 usable drops to 0.50 (A) and 0.60 (B), versus 0.9167 and
  0.8167 on regular windows, and ≥2-of-3 modification rises to 0.50 and 0.40. The rubric
  discriminates known-bad windows from known-good ones, which is the property that makes the
  primary estimate worth reading.
- **Determinism.** Temperature 0 on every judge. HTTP 429 retries were absorbed by the
  executor's backoff; the executor checkpoints every five items, so throttled runs resume
  without re-rating completed items.

## 9. What this result cannot be used to say

- It is not human inter-rater reliability, and does not establish that a clinician or the
  interviewee would find these windows coherent. Human interpretability remains untested and
  requires a separate study.
- It says nothing about EASE validity, clinical validity, or phenomenological fidelity.
- It supports no schizophrenia-versus-control inference. Clinical and comparison windows appear
  in equal numbers only to balance the calibration; the group difference in this corpus is
  confounded with acquisition and topic structure.
- Agreement among models that share training data and instruction-tuning ancestry is a
  robustness check against one vendor's idiosyncrasy, not independent human consensus. The
  0.74 AC1 on `coherent_boundary` is the concrete reminder.
- Percent agreement and AC1 here are computed over 120 items from 28 transcripts; the
  clustering of windows within a participant is not modelled, so treat these as descriptive
  calibration statistics rather than inferential estimates.

## 10. Reproduction

Private material stays local; only the aggregate step is reproducible from the repository.

```bash
python code/build_private_boundary_packet.py --root /path/to/daisc --judge-count 6   # local only
python code/run_ai_boundary_judges.py \
  --packet-dir <packet> \
  --prompt-file process/AI_JUDGE_PROMPT_BOUNDARY.md \
  --judge judge_04=gpt-oss-120b --judge judge_05=nemotron-3-ultra \
  --judge judge_06=stepfun-3.7-flash \
  --out-dir <ratings> --temperature 0 --data-handling "<retention statement>"
python code/score_boundary_ratings.py \
  --judge <ratings>/rated_judge_04__gpt-oss-120b.tsv \
  --judge <ratings>/rated_judge_05__nemotron-3-ultra.tsv \
  --judge <ratings>/rated_judge_06__stepfun-3.7-flash.tsv \
  --key <packet>/private_key.json \
  --json-out boundary_score.json --md-out boundary_score.md
python code/publish_boundary_ai_calibration.py \
  --score-json boundary_score.json --score-md boundary_score.md \
  --manifest <ratings>/judge_04__gpt-oss-120b.manifest.json \
  --manifest <ratings>/judge_05__nemotron-3-ultra.manifest.json \
  --manifest <ratings>/judge_06__stepfun-3.7-flash.manifest.json \
  --excluded-manifest <ratings>/judge_01__deepseek-v4-pro.manifest.json \
  --excluded-manifest <ratings>/judge_02__glm-5.2.manifest.json \
  --excluded-manifest <ratings>/judge_03__minimax-m2.7.manifest.json \
  --reason "<disclosure>" \
  --out-dir data/derived/boundary_ai_judges --run-date 2026-09-19
```

The publisher refuses to write if any judge is incomplete, if the judges did not share one
prompt hash, if the committed prompt no longer hashes to what the judges were given, or if any
string in an outgoing artifact contains source speech.
`.github/workflows/aris4c009-ai-judge-audit.yml` re-checks the same properties on every push.

Both workflow checks were executed locally against the committed aggregates before this record was
written: the privacy sweep and structure validation on the published files, and the three-judge mock
smoke path against the current scorer. The audit workflow itself has no run history on `main` yet, so
its first green run remains to be observed.

## 11. Open items carried into Gate D

1. `coherent_boundary` AC1 0.74 — boundary edges, not window content, are where the judges
   disagree; downstream work must use consensus labels and must not present them as validated
   episode boundaries.
2. Retention terms of the hosted routes actually used are unverified; if the stricter local-only
   reading is adopted, Gate C must be re-run against a fully local endpoint and this document
   superseded rather than edited.
3. Two of the three excluded runs had their manifests reconstructed from checkpointed ratings
   after their processes were interrupted, so their `execution_date` is absent; only their
   completion counts are used, and only to disclose the exclusion.
4. The 40-word selection should be re-examined once Gate D measures whether the extra realised
   words actually buy answerable queries — that is the question this gate can now hand forward.

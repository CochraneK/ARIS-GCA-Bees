# ARIS4C015 Status

Updated: 2026-09-18

## Stage

**Pilot 0 empirical validation in progress.**

The project has advanced beyond design-only status:

- reusable Agent Skill exists;
- deterministic core exists;
- GitHub Actions CI exists and has passed;
- live OpenAlex empirical cross-source probes exist;
- local SciSciNet-style cutoff-safe discovery scan exists;
- historical benchmark metrics and baseline evaluator exist.

A validated prospective Sleeping Beauty prediction model does **not** yet exist.

## Completed

### Agent surface

- `agent/sleeping-beauty-miner/SKILL.md`
- deterministic JSON orchestrator;
- Candidate Evidence Card schema;
- data/temporal contract;
- ARIS4C011 integrity adapter.

### Citation mechanics

- complete zero-filled annual history reconstruction from citation edges;
- historical cutoff truncation;
- OpenAlex historical query filter;
- local SciSciNet-style cutoff filtering;
- Beauty Coefficient B;
- peak time;
- awakening time.

### Transparent baselines

- total current citations;
- recent 3-year momentum;
- 3-year acceleration;
- partial-trajectory Beauty Coefficient;
- dormancy / longest zero-citation run.

### Evaluation scaffold

- Precision@K;
- Recall@K;
- NDCG@K;
- Brier score;
- calibration bins;
- historical-cutoff baseline evaluator;
- future outcomes kept separate from cutoff-visible features.

### ARIS4C011 integration

Prospective integrity findings are routed as:

- CLEAR;
- CAUTION;
- QUARANTINE;
- ABSTAIN.

Current default quarantine policy mirrors 011 evidence semantics:

- E0 = metadata observation;
- E1-E3 = stronger evidence classes;
- at least two independent cutoff-safe E1-E3 flag groups -> QUARANTINE;
- post-cutoff findings are excluded;
- unknown-time findings abstain in prospective mode.

Quarantine remains a review-routing decision, not a misconduct judgment.

## Empirical Pilot 0B results

Reference: Ke et al. (2015), Web of Science values.
Replication source: OpenAlex live API.
Observation endpoint: 2011.

| Case | OpenAlex citations <=2011 | B OpenAlex | B WoS | B relative difference | Awakening OpenAlex | Awakening WoS |
|---|---:|---:|---:|---:|---:|---:|
| Hummers & Offeman 1958 | 1,811 | 12,679.33 | 10,769 | +17.7% | 2007 | 2007 |
| Einstein-Podolsky-Rosen 1935 | 6,593 | 2,458.72 | 2,258 | +8.9% | 1991 | 1994 |
| Washburn 1921 | 1,857 | 2,472.08 | 2,184 | +13.2% | 1995 | 1995 |

Three-case descriptive summary:

- mean absolute relative B difference: ~13.3%;
- exact awakening-year matches: 2/3;
- mean absolute awakening-year difference: 1 year;
- maximum awakening-year difference: 3 years.

**Interpretation boundary:** these three famous, selected reference cases are implementation / cross-source probes. They do not establish general cross-database robustness.

## What the agent can do today

Given a paper with citation history or citing years:

- reconstruct its trajectory;
- compute retrospective metrics;
- freeze a prospective historical view;
- run cutoff-safe baselines;
- apply 011 integrity routing;
- emit a Candidate Evidence Card.

Given a bounded local SciSciNet-style slice:

- select a publication cohort;
- freeze at cutoff year;
- reconstruct citation histories in one pass;
- rank by a chosen transparent baseline;
- emit an auditable top-K shortlist.

The baseline scan intentionally keeps candidate state at `INSUFFICIENT_DATA` until stronger evidence and prospective validation exist.

## Immediate next steps

1. Expand cross-source Pilot 0 beyond three famous cases.
2. Obtain / query a reproducible SciSciNet-v2 subset rather than downloading the full data lake.
3. Validate against SciSciNet-v2's precomputed Sleeping Beauty metric where schema/source compatibility allows.
4. Build cohort-level historical-cutoff datasets.
5. Establish field- and age-normalized outcomes.
6. Add semantic novelty / atypical-combination features.
7. Add network bridge / community-diversity features.
8. Implement Prince-paper candidate extraction.
9. Run feature-family ablations.
10. Connect real 011 findings on the same corpus.
11. Only after those gates, train/calibrate prospective ranking models.

## Current blockers / constraints

- No canonical SciSciNet-v2 slice has yet been committed or connected to this project.
- Cross-database B values are not directly interchangeable.
- Modern semantic embeddings require explicit historical-leakage analysis.
- Prospective performance is unknown.
- No scientific claim should yet be made that 015 can predict future breakthroughs.

## Promotion gates

### Promote to "Pilot 0 complete" when

- a reproducible non-synthetic cohort, not only hand-picked reference cases, is processed;
- discrepancy/coverage report is produced;
- leakage tests pass;
- baseline benchmark is executed.

### Promote to "prospective model validated" only when

- chronological train/validation/test split passes;
- field/era holdouts are reported;
- simple citation baselines are beaten;
- calibration is acceptable if probabilities are emitted;
- shortcut/prestige audits pass;
- human-review utility is measured.

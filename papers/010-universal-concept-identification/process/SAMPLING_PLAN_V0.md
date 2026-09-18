# ARIS4C010 · Benchmark v0 Sampling Plan

**Target size:** approximately 320 target records  
**Goal:** enough diversity to falsify the simple-taxonomy hypothesis without pretending to sample "all concepts."

## Design principle

Benchmark v0 is a **stratified stress test**, not a prevalence estimate of the human conceptual repertoire.

Therefore equal or near-equal quotas across semantic regimes are intentional. Publication-level claims about how common a regime is in natural language would require a separate representative corpus design.

## Proposed target allocation

| Stratum | Approx. n | Primary source / construction |
|---|---:|---|
| concrete objects / organisms / substances | 45 | THINGS + Open English WordNet |
| events / processes / actions / states | 35 | Open English WordNet |
| properties / relations / roles | 35 | Open English WordNet + Wikidata |
| abstract / formal / informational | 35 | WordNet/Wikidata + curated formal examples |
| mental / social / institutional / normative | 35 | WordNet/Wikidata + curated concepts |
| fictional / hypothetical | 25 | curated + Wikidata where appropriate |
| lexical ambiguity / paired senses | 40 | Open English WordNet |
| compositional targets | 40 | UCID-generated from audited operators |
| vague / contextual | 15 | curated |
| semantic pathology / computability / ineffability boundary | 15 | curated |
| **Total** | **320** | |

Open-world/OOS evaluation is created by **withholding targets from these strata**, not necessarily by adding a separate semantic category.

## Lexical ambiguity design

Use at least 20 ambiguous surface forms with two or more senses, e.g. a structure like:

```text
surface form: bank
target A: financial institution sense
target B: river-edge sense
```

All senses sharing one surface form must stay in the same train/test partition family to prevent trivial string leakage.

## Compositional design

Sample operators separately and in combinations:

- negation/complement;
- conjunction;
- disjunction;
- relation-defined;
- quantification;
- comparison;
- modality;
- temporal modification;
- counterfactual;
- higher-order/metalinguistic.

### Difficulty levels

**C1 one operator**  
e.g. NOT mammal.

**C2 two operators**  
e.g. red AND NOT metallic.

**C3 relational/quantified**  
e.g. a person with exactly two siblings.

**C4 modal/contextual composition**  
e.g. something that could have happened yesterday but did not.

The benchmark should avoid uncontrolled combinatorial explosion. Composition depth is a measured predictor, not a contest to generate bizarre strings.

## Familiarity controls

Concept difficulty can be confounded by rarity.

For ordinary lexical concepts record, where available:
- corpus frequency;
- familiarity/nameability norm;
- concreteness/imageability;
- word length;
- number of senses.

Stress cases should be matched to ordinary controls where meaningful, or analyses should explicitly condition on familiarity.

## Split strategy

Avoid naive random target splits.

### Grouped hold-outs
Keep together:
- aliases/synonyms;
- senses of the same lemma;
- members generated from the same base concept + operator template;
- near-duplicate Wikidata entities;
- direct parent/child examples where leakage would trivialize the task.

### Suggested partitions
- development: 35%;
- calibration/adjudication: 25%;
- locked test: 40%.

This ratio is provisional; the locked set should not be used for query-prompt tuning.

## Open-world test

Construct OOS conditions by hiding legitimate targets from the active candidate universe while retaining the right to ask general queries.

At least three OOS severities:

1. **near OOS:** absent target has close in-support semantic neighbors;
2. **far OOS:** absent target occupies a poorly represented region;
3. **operator OOS:** base concepts are known but a compositional construction is not registered.

Measure whether the system:
- falsely collapses OOS onto a known candidate;
- abstains;
- requests ontology expansion;
- generates a useful new distinguishing query.

## Human calibration subset

Start with about **60 targets** spanning every semantic stratum, not only the easy concrete subset.

For each selected target:
- 15–25 diagnostic queries;
- repeated judgments on a subset;
- multiple raters;
- collect P2 and P6 conditions in counterbalanced order or between-subjects design;
- record response time and confidence.

Primary calibration questions:
1. Which query–target pairs have stable consensus?
2. Which semantic strata generate BORDERLINE/UNKNOWN/UNDEFINED/BOTH?
3. Does forced binary answering increase retest inconsistency?
4. Can the ontology's "applicability" labels predict invalid questions?

## Promotion gate from v0 to v1

Proceed only if:

- ≥95% of ordinary target pairs are separable by the full validated question bank;
- stress strata produce interpretable rather than arbitrary disagreement patterns;
- response-state annotation has usable human reliability;
- a multi-axis representation improves held-out separation and/or question validity over a matched-complexity single taxonomy;
- the benchmark can be redistributed under a clean documented license stack.

These thresholds are engineering gates, not preregistered scientific effect-size claims.

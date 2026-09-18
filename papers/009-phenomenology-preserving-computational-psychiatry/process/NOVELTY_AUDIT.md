# ARIS4C009 · Novelty and failure-mode audit

## Current novelty boundary

The broad program is **not novel**.

Prior work already establishes:

- computational phenomenology and generative passages;
- neurophenomenology;
- phenomenological fidelity as a methodological concern;
- EASE/EAWE/STEP-style quantification;
- interview-versus-self-report divergence;
- patient narrative distortion;
- clinical-interview summarization;
- ecological-validity/reliability problems in computational psychiatry;
- intended-use validity theory.

The surviving candidate contribution is narrower:

> **Decompose psychopathological information loss into acquisition and encoding stages, then benchmark multiple same-source representations with an independently generated reconstruction test and compare them on separate fidelity, reliability, use-validity, predictive-utility, and burden axes.**

See `GATE_A_NOVELTY_REVIEW_2026-09-19.md` for the expanded prior-art audit.

## Novelty conditions

A strong originality claim survives only if prior work does **not** already combine most of:

1. explicit (H \rightarrow A_m \rightarrow X^{(m)} \rightarrow E_k \rightarrow Z^{(m,k)}) decomposition;
2. same-source multi-representation psychiatric benchmark;
3. representation-blind query construction and evaluation;
4. semantic + relational + context + temporal reconstruction loss;
5. acquisition loss analyzed separately from encoding loss;
6. reliability and intended-use validity kept distinct from fidelity;
7. equal-rate/equal-burden comparisons;
8. use-conditioned Pareto analysis.

If a prior framework with this architecture is found, 009 becomes a replication/extension and the novelty claim must be rewritten.

## Why "digital twin" remains deferred

A digital-twin framing risks treating a model as the patient.

009 instead asks:

- what was elicited?
- by which acquisition process?
- how was it encoded?
- what was retained?
- what was omitted or transformed?
- for which intended use is the representation valid?
- what did the representation cost?

This is narrower and falsifiable.

## Major failure modes retained

### FM1 · Source evidence is mistaken for lived reality

Mitigation: (H \neq X); source material is a fixed evidential reference only.

### FM2 · Acquisition and encoding are confounded

Mitigation: 009A1 fixes the source; 009A2 studies actual acquisition-method divergence separately.

### FM3 · The benchmark is a strawman against brief tools

Mitigation: source fidelity is not universal validity. Evaluate intended use separately.

### FM4 · Question-bank ontology favoritism

Mitigation: source-only question construction, mixed query origins, participant questions, evaluator-background interactions.

### FM5 · More text always wins

Mitigation: rate matching, burden matching, controlled budget curves, Pareto analysis.

### FM6 · Query multiplication fakes sample size

Mitigation: redundancy clustering, query random effects, pilot effective-query estimates.

### FM7 · LLM circularity

Mitigation: human primary endpoint, frozen pipelines, source attribution, independent generation/evaluation.

### FM8 · Biological reductionism

Mitigation: biological evidence constrains models but does not adjudicate subjective meaning.

### FM9 · Cross-cultural translation loss

Mitigation: original language and translation provenance preserved; cross-language sensitivity analyses.

### FM10 · Reification of computational parameters

Mitigation: competing models, parameter recovery, out-of-sample prediction and perturbation evidence.

### FM11 · Ethics of total capture

Mitigation: privacy and participant burden enter the cost vector; "more data" is not automatically preferred.

## Competing explanations that are allowed to win

1. **Brief-tool sufficiency:** coarse same-source projections preserve nearly all information needed for their intended use.
2. **Narrative redundancy:** rich interviews mainly add stylistic detail.
3. **Acquisition dominance:** most observed divergence comes from elicitation method rather than encoding.
4. **Evaluator dependence:** representation rankings change by evaluator expertise.
5. **Temporal-density account:** repeated observations matter more than phenomenological coding.
6. **Low-dimensional sufficiency:** a compact representation preserves most scientifically important variance.
7. **Use-specific reversal:** a lower-fidelity representation outperforms richer ones for a specified screening/prediction task.

Any of these outcomes would refine rather than invalidate the value of the benchmark.

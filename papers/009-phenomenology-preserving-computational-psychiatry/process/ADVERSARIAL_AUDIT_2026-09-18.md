# ARIS4C009 · Adversarial audit

**Date:** 2026-09-18  
**Goal:** identify arguments that could invalidate the research design rather than merely weaken effect sizes.

## Fatal issue 1 · Acquisition and encoding were confounded

### Attack

An interactive phenomenological interview and a participant self-report questionnaire are not simply two compressions of the same evidence.

The interview can elicit, clarify and even co-construct articulable evidence through probing and mutual clarification.

Therefore:

[
EASE 
eq compression_1(H),quad selfreport 
eq compression_2(H)
]

in any directly observed sense.

### Evidence anchor

Parnas and colleagues' work on EASE explicitly emphasizes open conversation, concrete examples, probing and mutual clarification as necessary for faithful description of anomalous experience.

Cobanovic et al. (2025; PMID 40245844) found that self-rating substitutes for self-disorders remain inadequately validated against EASE.

Henriksen et al. (2026; PMID 42044094) directly compared IPASE and EASE and found substantial interpretive discrepancies.

### Fix adopted

Split:

- **009A1:** same-source encoding benchmark;
- **009A2:** independent acquisition benchmark.

A source-derived questionnaire-format representation is called a **projection**, not participant self-report.

## Fatal issue 2 · Intended-use strawman

### Attack

A diagnosis, screening scale and mechanistic latent state have different purposes.

If a diagnosis loses a large amount of narrative detail, that may be entirely compatible with its intended clinical role.

A benchmark that declares the longest representation "best" because it reconstructs the source most fully is trivial and unfair.

### Evidence anchor

Validity theory treats validity as a property of interpretations and uses of scores, not an instrument detached from purpose.

Kelly et al. (2005; PMID 16178998) explicitly frame clinical validity around intended interpretations/use.

### Fix adopted

Separate:

- source-grounded fidelity (F);
- intended-use validity (V_{use});
- intended-use utility (U);
- reliability (R);
- burden (C).

Construct Pareto frontiers conditional on a use case.

Diagnosis is removed from the primary semantic-fidelity competition unless used explicitly as a coarse negative control.

## Major issue 3 · Source interview is not ground truth

### Attack

Even the richest interview is a linguistic, social, memory-dependent and theory-influenced record.

Some experience may be preverbal, ineffable, forgotten or altered by reflection.

### Fix adopted

Use "source evidence" or "fixed evidential reference," never "ground truth experience."

Participant endorsement and independent cross-modal evidence constrain interpretation but do not convert the source into direct access to (H).

## Major issue 4 · Question bank can rig the benchmark

### Attack

Phenomenology-trained raters may construct questions that reward phenomenological representations.

A conventional clinician could analogously construct symptom questions that reward symptom scales.

### Fix adopted

- source-only query construction;
- mixed query origins;
- participant-generated preservation questions;
- blinded Panel C;
- query-origin stratification;
- evaluator-background interaction tests;
- no representation-aware question writing.

## Major issue 5 · More text can win by construction

### Attack

If fidelity means "recover more details," a longer record has a bandwidth advantage.

### Fix adopted

Always report:

- raw frontier;
- equal-description-rate comparison;
- equal-acquisition/encoding-burden comparison;
- controlled budget curves where possible.

R0 is treated as a ceiling/reference, not automatically the efficient optimum.

## Major issue 6 · Query multiplication can fake power

### Attack

Thirty paraphrases of the same relation are not thirty independent observations.

### Fix adopted

- explicit query clustering;
- redundancy screening;
- query-level random effects;
- pilot estimate of effective/usable query yield;
- power simulation includes query heterogeneity;
- confirmatory N is recalibrated to empirical redundancy.

## Major issue 7 · Evaluator expertise may determine results

### Attack

A phenomenology expert may decode R2 far better than a general clinician, while a computational specialist may decode latent vectors differently.

### Fix adopted

Record evaluator background and test:

[
representation 	imes evaluator_background
]

Primary estimates use a deliberately specified evaluator population.

No result is called representation-intrinsic without evaluator-population qualification.

## Major issue 8 · R3P may be an artificial object

### Attack

A questionnaire-format projection derived from an interview is not how questionnaires work in practice.

### Fix adopted

Correct: R3P exists only to isolate encoding loss.

Practical self-report performance is tested separately in 009A2.

Do not claim ecological validity for R3P.

## Major issue 9 · Participant validation can be unstable

### Attack

Retrospective endorsement can change with memory, insight, state and wording.

### Fix adopted

Participant fidelity is one constraint, not the reference truth.

Record assessment interval/state and disagreements.

## Major issue 10 · Cross-cultural semantic loss may dominate representation loss

### Attack

Translation can alter the very distinctions being scored.

### Fix adopted

Preserve original language, translation provenance and uncertainty.

Original-language analysis is primary where possible; translated analysis is a separate sensitivity layer.

## Major issue 11 · "Computational parameter = mechanism" reification

### Attack

A fitted latent parameter may only redescribe behavior.

### Fix adopted

Require:

- parameter recovery;
- discriminating predictions;
- alternative models;
- cross-level out-of-sample validation;
- perturbation/intervention evidence for strong mechanistic claims.

## Major issue 12 · Ethics can invalidate maximum-fidelity logic

### Attack

Richer data can be more identifiable and burdensome.

The scientifically richest representation may be ethically unacceptable.

### Fix adopted

Privacy risk and participant burden are constraints in (C(Z)), not afterthoughts.

"More data" is never a default objective.

## Current adversarial conclusion

The project is strongest when framed as:

> **A decomposition of psychiatric information loss into acquisition loss and encoding loss, with source fidelity evaluated separately from intended-use validity and burden.**

It is weaker if framed as:

> "Phenomenological interviews are more real than scales and computation."

The latter claim is neither required nor defensible.

## Remaining threats that require empirical pilot data

- actual query-bank reliability;
- effective number of nonredundant queries;
- evaluator variance;
- participant burden;
- source ambiguity rate;
- feasibility of R3P/R4P projection rules;
- stability across language/site;
- feasibility of participant meaning checks.

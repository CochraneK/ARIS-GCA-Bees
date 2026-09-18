# ARIS4C009A · Preregistration-ready protocol

## Title

**How Much Psychopathological Information Survives Encoding? A Blinded Same-Source Benchmark of Representation Fidelity**

## Status

Protocol skeleton for preregistration. No participant data have been collected under this protocol.

## Scope correction

009A is now explicitly **009A1: an encoding benchmark**.

It does **not** compare an actual participant self-report against an interactive phenomenological interview and call the difference "compression loss."

Different acquisition procedures can elicit different evidence. That question belongs to 009A2.

## Primary question

When the **same source episode** is encoded into different representations, how much source-grounded semantic, relational, contextual and temporal structure can a blinded evaluator recover?

## Source

The initial source is a rich, ethically collected, de-identified phenomenological interview episode.

The source is not treated as the participant's complete inner reality. It is the fixed evidential reference for the encoding experiment.

## Core encoding conditions

1. **R0 · Rich source record**  
   De-identified transcript segment, relevant prompts and contextual qualifiers.

2. **R1 · Structured phenomenological episode graph**  
   Entities, relations, temporal order, uncertainty, context and provenance.

3. **R2 · Specialist phenomenological coding**  
   Frozen trained-rater coding scheme based on selected EASE/EAWE/STEP-compatible constructs.

4. **R3P · Questionnaire-format projection**  
   A frozen mapping from the same source episode into the response format/content of a selected questionnaire.

   **R3P is not called self-report.** The participant did not generate it by completing the questionnaire.

5. **R4P · Conventional symptom-code projection**  
   A frozen mapping from the same source episode into selected conventional symptom/dimensional codes.

6. **R5 · Low-dimensional representation**  
   A compact latent/vector representation with frozen decoding instructions.

7. **R6 · LLM-assisted representation, exploratory only**  
   Frozen model/version/prompt, human primary endpoint retained.

## Excluded from the primary fidelity ranking

A DSM/ICD diagnosis or other categorical clinical label is not part of the primary source-reconstruction competition unless the study explicitly frames it as a deliberately coarse negative-control representation.

Low narrative fidelity of diagnosis is not interpreted as evidence that diagnosis fails its intended purpose.

## Acquisition benchmark deferred to 009A2

A later protocol will compare genuinely different acquisition methods in the same participants:

- phenomenological interview;
- participant-completed self-report;
- conventional clinical assessment;
- EMA where relevant.

009A2 must model:

- assessment order;
- interval between assessments;
- state change;
- priming/learning;
- interviewer effects;
- method-specific missingness.

## Query-bank construction

Three independent roles are retained:

- **Panel A:** constructs candidate questions from the source only;
- **Panel B:** adjudicates source answers and uncertainty;
- **Panel C:** sees one encoded representation and answers frozen questions.

Panel A and B never construct questions by inspecting R1–R6.

## Query classes

At minimum:

- semantic content;
- relations;
- context;
- temporal structure;
- participant-meaning checks where feasible.

Query origin is recorded:

- domain-general;
- phenomenology-informed;
- conventional-clinical;
- participant-generated.

Results are stratified by query origin to detect ontology favoritism.

## Primary endpoint

The primary endpoint is **source-grounded semantic reconstruction fidelity** at query level.

For categorical queries:

- correct;
- incorrect;
- indeterminate/abstain.

For uncertain source adjudication, use admissible answer sets or probabilistic scoring.

## Secondary endpoints

- relation precision/recall/F1;
- context-ablation loss;
- temporal-order concordance;
- participant-endorsed fidelity;
- evaluator calibration;
- inter-rater reliability;
- representation rate/length;
- encoding time;
- expert time;
- computational cost.

Acquisition time is reported for R0 source creation but is conceptually separated from encoding cost.

## Hypotheses

### H1 · Encoding gradient

Lower-bandwidth same-source encodings will show lower average source-reconstruction fidelity, with substantial overlap and exceptions.

### H2 · Domain interaction

Agency, mineness, self-world boundary, temporality and atmospheric/salience content will show larger loss than more concrete factual content under aggressive encoding.

### H3 · Context ablation

Removing contextual qualifiers will increase reconstruction error.

### H4 · Structured middle-layer efficiency

R1/R2 may occupy a favorable fidelity-versus-burden region relative to full source and coarse projections.

### H5 · No universal winner

A representation with lower narrative fidelity may still be superior for a different intended use; 009A1 does not generalize source fidelity into universal validity.

## Blinding

- evaluator does not see participant identity;
- evaluator sees only one representation condition for a given episode;
- representation creators do not evaluate their own representation;
- source adjudicators are separated from representation evaluation.

## Randomization

Use a balanced incomplete-block assignment so:

- every episode is evaluated under every representation condition across the evaluator pool;
- one evaluator does not see the same episode in multiple conditions;
- evaluator × representation imbalance is minimized.

Freeze code and seed before unblinding.

## Exclusion rules

Preregister before confirmatory data:

- source cannot support adjudication;
- transcript/source failure;
- representation violates frozen generation protocol;
- evaluator fails frozen training/attention criteria;
- duplicate episode.

Unusual clinical content is not an exclusion criterion.

## Primary model

A hierarchical logistic model for query-level correctness:

[
logit(P(Y=1))=
eta_0+eta_R+eta_D+eta_{R	imes D}
+u_{participant}+u_{episode}+u_{query}+u_{evaluator}
]

where (R) is representation and (D) is domain.

## Planned primary contrasts

Freeze after pilot calibration and before confirmatory access.

Candidate contrasts:

- R2 vs R3P;
- R2 vs R4P;
- R1 vs R4P;
- R0 vs R1.

R0 is a ceiling/reference condition, not expected to be burden-efficient.

## Missingness and abstention

"Cannot infer from this representation" is permitted.

Report:

- coverage;
- fidelity conditional on answer;
- overall proper scoring loss.

Do not force guessing.

## Power / precision

Use the simulation framework in:

`process/POWER_PRECISION_009A.md`

The final simulation must be recalibrated using pilot estimates of participant, episode, query and evaluator variance and query redundancy.

## Intended-use validity

009A1 measures source-reconstruction fidelity.

It does not claim that the highest-fidelity representation is best for every use.

Later analyses may estimate:

[
V_{use}(R,u),quad U(R,u)
]

for screening, diagnosis, prediction, monitoring or mechanism.

## Robustness

At minimum:

1. leave-one-participant-out;
2. leave-one-evaluator-out;
3. domain-specific effects;
4. query-origin stratification;
5. representation-rate matched comparison;
6. evaluator-background interaction;
7. original-language versus translated cases;
8. alternative source adjudication under unresolved ambiguity.

## Strong falsification

The central encoding thesis is weakened if:

- coarse projections preserve the same source information at much lower burden;
- fidelity advantages vanish under rate-matched analyses;
- query-bank reliability is inadequate;
- representation ordering is determined by evaluator school;
- results are driven by redundant paraphrased queries;
- richer encodings add only verbosity.

## LLM policy

If used:

- freeze model/version/date/prompt;
- use approved data handling;
- separate generation and evaluation pipelines;
- human evaluation remains primary initially;
- quantify stochastic variability;
- label outputs as derived representations, never source evidence.

## Registration gate

009A1 becomes registration-ready only after:

1. exact source interview/instruments and projection rules are frozen;
2. query-bank construction is piloted independently;
3. acceptable reliability thresholds are frozen;
4. pilot variance/redundancy estimates calibrate the sample-size simulation;
5. ethics/data-governance plan is approved.

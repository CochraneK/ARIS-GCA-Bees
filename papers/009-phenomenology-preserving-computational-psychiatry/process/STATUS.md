# ARIS4C009 · Status

**Current stage:** design / pre-ARIS deepening  
**ARIS baseline:** v0.4.26  
**Canonical scope:** fidelity benchmark first; mechanistic and longitudinal extensions second.

## Completed

- [x] Canonical research question defined.
- [x] Epistemic boundary defined: source evidence is not latent mental-state ground truth.
- [x] Representation ladder specified.
- [x] Phenomenological fidelity separated from reliability, validity, prediction and burden.
- [x] Multi-objective fidelity frontier specified.
- [x] Rate-distortion formulation added with psychiatry-specific distortion requirements.
- [x] Idiographic + hierarchical longitudinal extension specified.
- [x] Active inference demoted from assumed ontology to candidate model family.
- [x] Seed literature matrix created.
- [x] Novelty and failure-mode audit created.
- [x] Initial falsification criteria defined.
- [x] Targeted novelty search completed and logged.
- [x] 009A preregistration-ready protocol skeleton drafted.
- [x] Episode-level data dictionary drafted.
- [x] Reference Pareto-frontier code added.
- [x] Independent-panel fidelity metric specification drafted.
- [x] Minimal relation ontology drafted.
- [x] Synthetic engineering benchmark added with explicit non-empirical labeling.

## Next ARIS gates

### Gate A — systematic novelty search

**Status:** targeted audit complete; formal multi-database systematic novelty review remains.

Determine whether prior work already benchmarks explicit representational loss from phenomenological interview → scale → computational representation.

Pass condition: novelty claim is rewritten to the narrowest defensible form after database and citation-chain screening.

### Gate B — fidelity metric preregistration

**Status:** formal metric architecture complete; empirical calibration pending.

Completed:

- independent query-construction/adjudication/evaluation panels;
- semantic, relational, context, temporal and participant fidelity definitions;
- source-uncertainty propagation;
- rate- and burden-matched fairness analyses;
- relation ontology;
- provisional reliability gates.

Still required:

- pilot query bank on independent episodes;
- inter-rater calibration;
- frozen acceptable thresholds;
- simulation-based sample-size target.

Pass condition: metrics can be applied without knowing representation identity and without tuning on confirmatory cases.

### Gate C — pilot material

Use de-identified or purpose-collected episodes to verify annotation feasibility, graph extraction, blinded reconstruction and burden measurement.

Synthetic examples may be used only for engineering and must be labeled synthetic.

### Gate D — metric reliability

Pass condition: key fidelity components achieve prespecified acceptable rater agreement or are revised before substantive comparisons.

### Gate E — representation benchmark

Compare at minimum full context, structured graph, expert phenomenological code, self-report abstraction and conventional symptom abstraction.

Pass condition: effect estimates and uncertainty are reported; no universal representation winner is forced.

## Deferred

- EEG/fMRI mechanism study;
- digital phenotyping;
- intervention control;
- full digital-twin language;
- clinical decision support.

These are intentionally deferred until the representation-loss measurement problem is solved.

## Current main risk

The framework can become too broad.

**Control:** Paper 009A remains a measurement / representation paper. Everything else is a programmatic extension.

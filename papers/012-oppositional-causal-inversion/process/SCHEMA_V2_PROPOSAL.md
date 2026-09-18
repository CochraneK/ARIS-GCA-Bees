# SCHEMA V2 PROPOSAL — ARIS4C012

Updated: 2026-09-18

> **DO NOT USE FOR PILOT 0B.**  
> Pilot 0B must remain scored against the frozen v1 materials in `CODER_B_FREEZE.json`.  
> This document is a post-Gate-B redesign proposal created without access to any Coder B labels.

## Problem identified in v1

The v1 "eight mechanism families" mix at least three ontological levels:

1. **index changes** — where the apparent contradiction is located;
2. **generative mechanisms** — why the reversal occurs;
3. **relational allocation** — who benefits or loses.

For example:
- actor-switch and time-switch are not mechanisms;
- feedback is a mechanism;
- power asymmetry can be both an actor relation and a mechanism/context;
- construct substitution describes semantic/measurement structure rather than a dynamic process.

Treating all eight as one mutually exclusive categorical variable is therefore likely to produce avoidable coder disagreement.

## Proposed v2: orthogonal coding cube

Represent an OCI candidate on independent axes.

### Axis A — opposition validity

`opposition_valid ∈ {yes, no, uncertain}`

This remains the entry gate.

### Axis B — opposition relation

What exactly is being opposed?

- **B1 same-construct reversal**  
  More X at one indexed state yields less X at another indexed state.

- **B2 target reversal**  
  An intervention intended to move outcome Y in one direction moves Y in the opposite direction.

- **B3 functional reversal**  
  X increases but the function X is intended to provide decreases.

- **B4 relational reversal**  
  X benefits/empowers A by reducing an opposed state/capacity in B.

- **B5 proxy reversal**  
  An observed/targeted proxy improves while fidelity to the latent objective declines.

These categories may be nonexclusive; coding should permit multi-label assignment.

## Axis C — index-switch vector

Encode separately:

[
I = (A,L,T,D,E)
]

where:

- **A — actor switch**: actor/beneficiary differs;
- **L — level switch**: individual/dyad/group/organization/state/system differs;
- **T — time switch**: short- vs long-run or dynamic lag;
- **D — definition/construct switch**: nominal/formal/proxy vs substantive/effective construct;
- **E — environment/regime switch**: effect changes across ecological, strategic, or capacity regime.

Each is coded independently:
`{0,1,uncertain}`.

This is the central "missing subscript" representation.

## Axis D — generative mechanism vector

Mechanisms should be separated from index switches.

### D1 strategic/adaptive feedback
Other agents or system components respond to X and change the equilibrium.

Examples:
- security dilemma;
- Goodhart gaming;
- rebound behavior.

### D2 congestion / capacity overload
Additional X exceeds processing/network/choice capacity.

Examples:
- choice overload;
- traffic congestion.

### D3 nonlinear ecological dynamics
Thresholds, overcompensation, density dependence, hormesis, or other nonlinear state dynamics.

Examples:
- hydra effect;
- some safe-development dynamics.

### D4 information filtering / bias–variance tradeoff
Using fewer inputs improves performance because added information increases variance/noise/cost.

Examples:
- less-is-more heuristic effects.

### D5 norm / motivational reactance
Attempts at influence change motivation or perceived norms in ways that oppose the target.

Examples:
- freedom-threatening persuasion;
- descriptive-norm boomerang.

### D6 exposure / induced adaptation
Protection changes location, preparedness, vulnerability, or exposure.

Examples:
- levee/safe-development effect.

### D7 intervention toxicity / direct harm
The treatment/intervention has mechanisms that directly worsen the target condition.

Examples:
- iatrogenic psychological treatment.

### D8 coordination externality
An individually useful/common signal changes coordination so that aggregate welfare/performance falls.

Examples:
- public-information coordination models;
- some network/equilibrium paradoxes.

Mechanisms are multi-label; no forced single "primary mechanism" is required until empirical clustering shows one is useful.

## Axis E — evidence mode

Keep separate from truth/effect direction:

- randomized experiment;
- quasi-experiment;
- longitudinal observational;
- cross-sectional observational;
- formal model;
- simulation;
- qualitative/process evidence;
- systematic review;
- meta-analysis;
- conceptual/theory.

## Axis F — result direction

`result_support ∈ {supports_reversal, null, opposes_reversal, mixed, formal_only, not_tested}`

This remains separate from OCI candidacy.

## Axis G — normative valence

Do not assume inversion is good or bad.

- beneficial;
- harmful;
- mixed;
- actor-dependent;
- not normatively classified.

This is especially important for political, clinical, and ecological cases.

## New formal representation

For candidate (k):

[
OCI_k =
(O_k, I_k, M_k, E_k, R_k)
]

where:

- (O_k) = opposition relation;
- (I_k) = index-switch vector;
- (M_k) = mechanism vector;
- (E_k) = evidence mode/strength;
- (R_k) = result direction.

The causal core is:

[
do(X_{i} \uparrow)
\rightarrow M
\rightarrow O(X)_{j}
]

but v2 avoids pretending that (i \neq j) and (M) are the same type of classification.

## Why v2 may improve reliability

The current v1 asks coders for a single `primary_mechanism` while categories include both index switches and mechanisms. Two coders could agree completely about the paper yet disagree between labels such as:

- "time-switch"
- "feedback"
- "construct-switch"

because all three can simultaneously be true.

v2 turns this into:
- time_switch = 1;
- construct_switch = 1;
- adaptive_feedback = 1.

This converts artificial categorical disagreement into meaningful multi-dimensional agreement.

## Gate-B decision rule for adopting v2

After Coder B is ingested:

### Adopt v2 if
- v1 `primary_mechanism` agreement is materially lower than opposition-validity agreement; and
- disagreement inspection shows coders often chose different labels that are simultaneously defensible.

### Keep v1 if
- mechanism agreement is already high; and
- forced primary-mechanism labels show clear semantic coherence.

### Repeat a fresh pilot if v2 is adopted
Do not retroactively recode Pilot 0 into a "successful" v2 validation.

Instead:
1. adjudicate v1 only for descriptive diagnosis;
2. freeze v2;
3. draw a fresh balanced sample;
4. run new blind A2/B2 coding;
5. evaluate multi-label reliability per axis.

## Implication for the manuscript

The paper may ultimately be stronger if OCI is presented not as a list of "eight paradox types" but as an **indexed causal coordinate system**.

That would make the contribution:

> apparent causal paradoxes are decomposable into orthogonal dimensions of opposition, index switching, generative mechanism, and evidential status.

This is more precise and more compatible with the project's narrow novelty claim.

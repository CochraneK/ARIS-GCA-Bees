# When Opposites Become Causes: A Cross-Domain Science of Oppositional Causal Inversion

**Cunyi Kang**

> **Draft status (2026-09-18):** theory and methods draft. Coder A feasibility results are descriptive only. Independent Coder B reliability and reproducible retrieval Gate R must pass before any confirmatory claim about the framework is made.

## Abstract

Scientific literatures contain many claims in which increasing a desirable, protective, informative, or enabling quantity appears to generate its functional opposite: more road capacity can increase congestion, efficiency improvements can rebound into greater resource use, behavior-change messages can produce boomerang effects, organizational capabilities can become rigidities, and additional choice can sometimes impair decision outcomes. Literary slogans such as “war is peace,” “freedom is slavery,” and “ignorance is strength” dramatize the same surface form, but their literal identities are logically incoherent and their scientific mappings are heterogeneous. We propose **Oppositional Causal Inversion (OCI)** as a falsifiable representation of a narrower phenomenon: an intervention or state (X), indexed by actor, level, time, construct definition, and environment, causally increases a prespecified functional opposite after at least one index changes or a dynamic feedback process unfolds. The framework distinguishes actor-, level-, time-, construct-, equilibrium-, capacity-, filtering-, and power-asymmetry mechanisms and explicitly excludes rhetorical paradoxes, ordinary side effects, post-hoc antonyms, and same-index contradictions. A first 30-record single-coder feasibility stress test found that the schema rejected several tempting neighboring “paradox” cases rather than absorbing all of them; these counts are not prevalence estimates and await independent coding. We specify a dual-source, versioned OpenAlex/Crossref evidence-map pipeline, retain failed retrieval versions as provenance, and preregister reliability and retrieval gates before full screening. The central empirical question is therefore not whether opposites are secretly identical, but whether apparently paradoxical causal claims share a reliable, cross-domain indexed structure with predictable boundary conditions.

## 1. Introduction

Statements such as “more choice can make people less autonomous,” “more security can produce insecurity,” or “more capacity can make a network perform worse” are rhetorically striking because they appear to violate monotonic intuition. In their strongest colloquial form they resemble contradictions: (X = \neg X). Yet most scientifically credible examples do not assert simultaneous identity. They change the actor, aggregation level, time horizon, operational definition, strategic environment, or equilibrium state.

This distinction is easiest to see by restoring indices. Let

[
X[a,l,t,d,e]
]

denote a construct for actor (a), level (l), time (t), operational dimension (d), and environment (e). An apparent contradiction such as “security creates insecurity” may instead mean that a security-seeking action by actor A at (t_0) changes actor B's threat perception, elicits a response, and reduces A's security at (t_1). “More freedom reduces freedom” may distinguish nominal option quantity from effective autonomy after decision burden or social norms change. “Less information improves performance” may refer to selective filtering in an environment where additional cues mainly add variance or processing cost.

The missing indices transform a contradiction into an empirical causal proposition.

A large number of mature literatures already study particular instances of backfire, paradox, and unintended consequence: security dilemmas, choice overload, iatrogenic treatment effects, boomerang effects, rebound effects, Braess paradoxes, Goodhart-type target corruption, organizational capability–rigidity transitions, rational inattention, and ecological rationality. The contribution sought here is therefore **not** the observation that interventions sometimes backfire. Instead, we ask whether these literatures can be represented by a common indexed causal grammar that is narrow enough to reject superficially similar noncases and useful enough to predict boundary conditions across domains.

We call the candidate representation **Oppositional Causal Inversion (OCI)**.

## 2. From contradiction to indexed causation

### 2.1 What OCI is not

A literal statement

[
X_i = \neg X_i
]

under the same actor, level, time, operational definition, and environment is not an empirical discovery. It is ordinarily a logical or measurement inconsistency.

OCI instead concerns relations of the form

[
do(X_i \uparrow) \rightarrow M/F \rightarrow O(X)_j \uparrow,
]

or

[
do(X_i \uparrow) \rightarrow X_j \downarrow,
]

where (M/F) denotes a mediator or feedback process, (O(X)) is a **prespecified functional opposite**, and (i \neq j) on at least one declared index. A same-index dynamic reversal can still qualify when a time-varying feedback process is explicitly represented rather than hidden inside a simultaneous contradiction.

### 2.2 Functional opposition

The framework deliberately separates **functional opposition** from dictionary antonymy. A pair can qualify when opposition is justified before inspecting the focal result by at least one of four routes:

1. a validated bipolar scale or established construct pair;
2. a formal complement in the outcome definition;
3. domain theory specifying mutually incompatible functional states;
4. independent expert/coder agreement with written rationale.

This restriction is essential. Without it, almost any harmful side effect could be redescribed after the fact as an “opposite,” making the framework unfalsifiable.

### 2.3 Candidate mechanism families

We distinguish eight provisional mechanism families.

**Actor-switch inversion.** Increasing (X) for one actor generates the opposed state for another actor.

**Level-switch inversion.** An exposure at one aggregation level generates an opposed outcome at another; intergroup competition and intragroup cooperation are a canonical candidate.

**Temporal inversion.** A short-run improvement changes incentives, norms, or exposure so that the longer-run effect reverses.

**Construct substitution.** A nominal or formal version of a construct increases while its substantive or effective version falls.

**Strategic/equilibrium feedback.** Other agents respond to the focal action and the resulting equilibrium reverses the local effect.

**Capacity/overload nonlinearity.** Additional inputs are useful below a threshold but harmful above it because of congestion, complexity, noise, or processing limits.

**Selection/filtering inversion.** Ignoring inputs can improve performance when discarded information is noisy, redundant, manipulable, or costly.

**Power-asymmetry inversion.** Reducing information, autonomy, or coordination capacity for one actor increases another actor's relative control. This family must be kept conceptually separate from claims that the disadvantaged actor benefits.

The taxonomy is provisional until independent coding tests whether distinct reviewers can apply it reliably.

## 3. Relation to neighboring theories

### 3.1 Paradox theory

Organizational paradox theory examines contradictory yet interdependent elements that persist over time. It is broader than OCI: contradictory demands can coexist without one causing the functional opposite of the other. OCI therefore requires a directional causal representation and an explicitly defined opposite.

### 3.2 Unintended, perverse, boomerang, and iatrogenic effects

These traditions are much closer. A boomerang intervention may directly move behavior opposite the intended direction, and iatrogenic treatment can worsen the condition it aims to improve. Such cases can be OCI instances, but OCI additionally asks whether the same representation applies to nonintervention settings such as strategic equilibria, network capacity, information filtering, and organizational adaptation.

### 3.3 Rebound and Jevons effects

Efficiency improvements can be partly offset by behavioral or economic responses; in sufficiently strong cases total resource use can increase. Rebound theory already contains rich distinctions across mechanisms, levels, and time horizons. OCI should therefore treat rebound as a benchmark family rather than claim to rediscover it.

### 3.4 Braess-type network paradoxes

Braess paradox supplies one of the cleanest formal templates for OCI: adding a link or capacity can increase equilibrium travel cost under selfish routing and particular network conditions. Unlike literary paradoxes, the relevant exposure, outcome, equilibrium process, and boundary conditions can be stated mathematically.

### 3.5 Security dilemmas

Security-seeking actions can increase another actor's perceived threat, provoke countermeasures, and feed back into lower security. Again, the scientific claim is not “security is insecurity”; it is a strategic feedback model indexed by actors and time.

### 3.6 Choice overload and autonomy paradoxes

Choice-overload findings are strongly moderated and not universally negative. Likewise, mobile connectivity can increase short-run flexibility while contributing to collective expectations of continual availability. These literatures motivate the distinction between **formal freedom** and **effective autonomy**.

### 3.7 Rational inattention, deliberate ignorance, and ecological rationality

These neighboring theories illustrate why “ignorance is strength” is too coarse. Rational inattention concerns optimal allocation of finite information-processing capacity. Ecological rationality describes environments where simple heuristics using fewer cues can outperform more information-intensive rules. Deliberate ignorance and information avoidance include many motivations and outcomes, not all beneficial. OCI can only include a case when the causal performance or control outcome is explicitly defined.

### 3.8 Goodhart/Campbell-type feedback

Once a measure becomes a target, strategic adaptation can degrade its relationship with the underlying construct. This provides a construct-switch plus feedback template: measured performance may increase while measurement validity falls.

## 4. Why Orwell is a stress test rather than the theory

The slogans from *Nineteen Eighty-Four* are useful because they maximize the appearance of contradiction. They are scientifically unequal, however.

### 4.1 “War is peace”

The literal proposition is the weakest mapping. War, external threat, competition, deterrence, intragroup cohesion, regime support, and absence of violence are distinct variables. More defensible scientific mappings include:

[
IntergroupCompetition_{between} \rightarrow Cooperation_{within},
]

[
CredibleThreat/Capability \rightarrow Deterrence,
]

and, in the opposite direction,

[
SecuritySeeking_A \rightarrow ThreatPerception_B \rightarrow Response_B \rightarrow Insecurity_A.
]

None licenses the general proposition that war creates peace.

### 4.2 “Freedom is slavery”

A scientifically tractable version distinguishes formal from effective autonomy:

[
FormalChoice \uparrow \rightarrow Burden/NormFeedback \uparrow \rightarrow EffectiveAutonomy \downarrow.
]

Choice overload is conditional on complexity, task difficulty, preference uncertainty, and related moderators. Organizational autonomy paradoxes similarly depend on social and technological context. Extensive self-determination research linking autonomy with adaptive outcomes is essential counterevidence against universalization.

### 4.3 “Ignorance is strength”

This slogan collapses several mechanisms that must remain separate. A defensible filtering claim is closer to:

[
InformationUsed \downarrow \rightarrow Variance/ProcessingCost \downarrow \rightarrow PredictiveRobustness \uparrow
]

under specific environments. A power-asymmetry claim instead concerns one actor's information or coordination capacity being restricted to another actor's advantage. These are normatively and causally different. Generalized ignorance is not predicted to be beneficial.

## 5. Methods

### 5.1 Review design

The first empirical stage is a **systematic evidence map**, not an omnibus meta-analysis. Outcomes and interventions across war, networks, clinical treatment, organizational control, consumer choice, and information processing are too heterogeneous for a meaningful common effect size.

The review searches broad neutral language including paradox, backfire, boomerang, counterproductive, self-defeating, unintended/perverse consequence, iatrogenic, less-is-more, overload, security dilemma, counterfinality, rational inattention, deliberate ignorance, rebound, risk compensation, and target corruption.

### 5.2 Screening

A candidate must contain:
1. an identifiable exposure/intervention/state (X);
2. an outcome plausibly opposed to (X) or its intended function;
3. enough information to code the actor, level, time, construct, or environment indices;
4. a causal mechanism or design whose identification strength can be evaluated.

Literary commentary, wordplay, ordinary side effects unrelated to the focal construct, post-hoc antonyms, measurement artifacts, and reverse-causality errors are excluded from OCI-positive coding.

### 5.3 Evidence strength

Evidence strength is coded separately from effect direction and normative desirability. Randomized studies, credible quasi-experiments, longitudinal observational designs, formal models, reviews, and meta-analyses are not collapsed into one ordinal “truth” score without preserving design type.

### 5.4 Independent coding gate

At least two independent coding passes are required for opposition validity, index switches, mechanism family, evidence mode, causal-claim strength, and OCI candidacy. The second coder must not see first-coder labels. Opposition validity and mechanism-family agreement below the prespecified workflow threshold trigger schema revision and a fresh pilot rather than adjudication into an artificial consensus.

### 5.5 Reproducible retrieval

A versioned OpenAlex/Crossref pipeline records every request, raw JSON response, SHA-256 hash, deterministic deduplication decision, topical/type rejection, and selected candidate. Retrieval versions are immutable after execution. Failed versions are preserved.

The first reproducible retrieval (v0.1) returned 180 records but revealed predictable semantic contamination, including autonomic-neuropathy papers for “autonomy” and biographical records for “Goodhart.” Rather than silently clean the sample, v0.1 was frozen and the protocol was amended prospectively to v0.2 with scholarly record-type gates and prespecified title-anchor groups. These gates depend on topical identity, not whether a paper supports OCI.

## 6. Pilot 0A: single-coder feasibility stress test

Before independent reliability testing, a 30-record feasibility packet was assembled across six prespecified domains: conflict/security, autonomy/choice, information/attention, backfire/iatrogenic interventions, economic/network rebound, and organizational/measurement paradoxes.

Coder A labeled 21 of 30 records as OCI candidates, seven as noncandidates, and two as uncertain. Functional opposition was coded valid for 21 records, invalid for four, and uncertain for five. These counts are **not prevalence estimates**, were not derived from the final reproducible search frame, and must not be interpreted as independent validation.

The important feasibility result was discriminant rather than confirmatory. Broad organizational paradox theory, some strategic-paradox work, counterfinality, some diversionary-conflict research, and some deliberate-ignorance/rational-inattention work did not automatically qualify. The schema therefore did not simply absorb every paper containing the word “paradox.”

The packet also retained evidence contrary to simplistic inversion claims. Choice-overload effects are heterogeneous and can average near zero; autonomy-support literatures generally report adaptive associations; information sharing can improve prosocial outcomes; and some randomized normative-feedback studies show no predicted boomerang effect. The framework is intended to explain conditional reversals, not to select only successful paradoxes.

## 7. Testable hypotheses

**H1 — Indexing hypothesis.** A substantial proportion of apparent causal contradictions become logically coherent when actor, level, time, construct, and environment indices are restored.

**H2 — Moderator hypothesis.** Credible reversals concentrate in identifiable moderator regimes rather than appearing as universal negative slopes.

**H3 — Feedback hypothesis.** Strategic/equilibrium and capacity mechanisms yield more reproducible opposite-direction effects than purely rhetorical paradox categories.

**H4 — Predictability hypothesis.** Index-switch and mechanism features improve out-of-domain prediction/classification of reversal conditions relative to domain labels alone.

**H5 — Heterogeneity hypothesis.** The Orwell triad maps to multiple substantive mechanisms; any commonality exists at the level of causal representation rather than one shared mechanism.

## 8. Falsification conditions

The framework should be rejected or sharply narrowed if:

- independent coders cannot reliably prespecify functional opposites;
- apparently paradoxical examples mostly collapse into semantic relabeling or ordinary side effects;
- stronger causal designs fail to reproduce patterns suggested by observational or rhetorical literatures;
- mechanism classes fail to transfer across domains;
- index restoration improves exposition but not prediction, classification, or theory;
- candidate reversals are rare anomalies without predictable boundary conditions;
- an existing umbrella theory is found that already provides the same indexed representation and empirical program.

A null result would still be scientifically useful: it would show that superficially similar paradoxes are better understood through domain-specific theories rather than a general causal class.

## 9. Discussion

OCI is best viewed as a proposed **representation layer**, not a new substantive law. Braess paradox, rebound, security dilemmas, choice overload, autonomy paradoxes, iatrogenic effects, and Goodhart-type feedback do not share one physical or psychological mechanism. What they may share is a grammar: local improvement or increase in (X), a declared index change or feedback process, and an outcome that is functionally opposed to (X) or its intended function.

This distinction constrains the strongest possible conclusion. Even a successful OCI framework would not establish that “more is worse,” that contradiction is a general law of social systems, or that Orwell's slogans are scientifically true. It would establish only that a family of seemingly contradictory claims can be converted into comparable causal structures with explicit boundary conditions.

The most important empirical challenge is semantic discipline. If “opposite” can be chosen after observing a surprising effect, every failure becomes an inversion. Independent coding, prespecification, negative examples, and out-of-domain validation are therefore not peripheral quality checks; they are the central test of whether OCI is scientifically meaningful.

## 10. Current limitations and locked next steps

This draft precedes two hard gates.

First, the 30-record feasibility labels were produced by one coder. A blind Coder B packet has been frozen, but independent coding must occur in a genuinely separate context before agreement statistics are calculated.

Second, the first reproducible database retrieval exposed lexical contamination. Retrieval v0.2 was prospectively amended with type and topical anchors and must be audited before the evidence-map sampling frame is frozen.

No general-theory claim, prevalence estimate, or cross-domain predictive claim is permitted until both gates are passed.

## 11. Provisional conclusion

The scientifically productive question is not whether “war is peace,” “freedom is slavery,” or “ignorance is strength” are true. Their literal forms conflate variables and suppress indices. The stronger question is whether apparently opposite-producing phenomena across disciplines share an indexed causal architecture that can be defined before outcomes, applied reliably by independent coders, and used to predict where reversal occurs. ARIS4C012 is designed so that this proposition can fail.

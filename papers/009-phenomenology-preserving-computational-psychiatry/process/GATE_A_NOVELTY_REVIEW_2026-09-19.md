# ARIS4C009 · Gate A novelty review

**Date:** 2026-09-19  
**Status:** expanded, auditable novelty review completed; full multi-database systematic novelty review remains a manuscript-stage requirement.

## 1. Question

What, if anything, is genuinely new in ARIS4C009 after accounting for prior work on:

- phenomenological psychopathology;
- psychiatric interviewing;
- computational phenomenology / neurophenomenology;
- questionnaire-versus-interview validity;
- patient narrative distortion;
- clinical summarization;
- computational psychiatry reliability and ecological validity;
- modern intended-use validity theory?

## 2. Search families

Searches were run across public scholarly web/PubMed-indexed sources using combinations of:

- `"computational phenomenology" psychiatry lived experience`
- `"phenomenological fidelity" psychiatry psychopathology`
- `"rate distortion" psychiatry psychopathology phenomenology`
- `"information loss" psychiatric assessment interview questionnaire`
- `"representation loss" psychopathology psychiatric assessment`
- `"patient narrative distortion" diagnostic error`
- `"psychiatric interview" summarization fidelity information loss`
- `EASE self-report interview validity`
- `computational psychiatry ecological validity lived experience`
- `validity interpretation use patient reported outcomes`

Targeted backward/forward conceptual checks were also made around EASE, computational phenomenology, phenomenological fidelity, and narrative distortion.

This is broader than the initial seed search but is not presented as a PRISMA systematic review.

## 3. Closest prior art

### A. Psychiatric interview as transformation of lived experience

Nordgaard, Sass & Parnas (2013), DOI 10.1007/s00406-012-0366-z, PMID 23001456.

**Prior contribution:** explicitly analyzes the conversion of first-person experience into objective/actionable psychiatric information and argues that interview structure changes what can be validly elicited.

**Implication for 009:** acquisition cannot be treated as a neutral readout. This directly motivates separating (A_m) from encoding (E_k).

### B. Phenomenological fidelity is already an established methodological concern

Hurlburt & Heavey (2015), DOI 10.1016/j.concog.2014.11.002, PMID 25486341.

**Prior contribution:** explicitly distinguishes phenomenological fidelity from the usefulness/validity of questionnaires and other experience-sampling methods.

**Implication:** ARIS4C009 must not claim to invent "phenomenological fidelity."

### C. Computational phenomenology already formalizes lived experience

Ramstead et al. (2022), DOI 10.1007/s13164-021-00604-y, PMID 35317021.

**Prior contribution:** proposes generative models of phenomenological structure and "generative passages" between phenomenological and formal descriptions.

Deep computational neurophenomenology and generative neurophenomenology extend this program further.

**Implication:** "phenomenology + computation" is prior art, not 009 novelty.

### D. Phenomenology is already proposed as a translational resource in mental health

Ritunnano et al. (2023), DOI 10.1017/S2045796022000762, PMID 36645112.

**Prior contribution:** argues that complex subjective dimensions are inadequately represented by standard quantitative methods and should inform translational mental-health research.

**Implication:** 009's motivation is supported, but the translational bridge itself is not new.

### E. Interview versus self-report divergence has direct empirical evidence

Cobanovic et al. (2025), DOI 10.1159/000545364, PMID 40245844.

**Prior contribution:** systematic review finds self-rating alternatives for self-disorders inadequately validated against EASE.

Henriksen et al. (2026), DOI 10.1159/000552007, PMID 42044094.

**Prior contribution:** IPASE and EASE correlate only moderately; qualitative analysis shows ordinary, medication-related, and psychotic experiences can be conflated in self-report.

**Implication:** different acquisition methods can generate different constructs/evidence, not merely differently compressed versions of the same source.

### F. Patient narrative distortion has now been explicitly operationalized

Gupta (2026), *The patient narrative distortion index (PNDI)*, DOI 10.1515/dx-2026-0086, PMID 42446947.

**Prior contribution:** proposes a five-domain taxonomy of narrative distortion including completeness, meaning substitution, salience, context stripping, and bias-driven distortion.

**Implication:** ARIS4C009 must not claim that measuring narrative loss/distortion is itself unprecedented.

### G. Clinical narratives have long been shown to lose information during medical encoding

Sheaff et al. (2017), DOI 10.1111/1467-9566.12553.

**Prior contribution:** direct comparison of patient oral narratives with clinical records found patient viewpoints omitted, reframed, supplemented, or lost.

**Implication:** "narrative → clinical record loses information" is prior art.

### H. Psychiatric interview summarization already studies source-to-summary information preservation

Dhamala et al. (2021), *Knowledge-Infused Abstractive Summarization of Clinical Diagnostic Interviews*, DOI 10.2196/20865.

**Prior contribution:** develops psychiatric-interview summarization and explicitly notes that preprocessing/summarization can lose clinically critical information.

Recent psychiatric LLM work also extracts symptoms/stressors and generates summaries from interview transcripts.

**Implication:** same-source compression in psychiatric text is not by itself novel.

### I. Computational psychiatry already recognizes reliability and ecological-validity failures

Karvelis et al. (2023), DOI 10.1016/j.neubiorev.2023.105137, PMID 36940888.

Chen et al./related translational reviews and *Barriers and solutions to the adoption of translational tools for computational psychiatry* (2023), DOI 10.1038/s41380-023-02114-y, PMID 37280282.

**Prior contribution:** computational parameters often have weak psychometrics and laboratory tasks may poorly reflect clinically relevant real-world contexts.

**Implication:** 009 should not claim to discover the ecological-validity problem.

### J. Validity is already use-conditioned in modern measurement theory

Weinfurt (2021), DOI 10.1007/s11136-021-02776-7, PMID 33630235; Hawkins et al. (2021), DOI 10.1186/s41687-021-00332-y, PMID 34328558.

**Prior contribution:** validity concerns evidence supporting specified interpretations and uses, not a timeless property of an instrument.

**Implication:** source-reconstruction fidelity must be separated from intended-use validity.

## 4. Novelty claims explicitly retired

ARIS4C009 will **not** claim novelty for:

1. computational phenomenology;
2. neurophenomenology;
3. phenomenological fidelity;
4. phenomenological interviewing;
5. the claim that questionnaires can miss experiential nuance;
6. the claim that patient narratives can be distorted;
7. clinical-text summarization;
8. computational psychiatry's ecological-validity problem;
9. use-conditioned validity;
10. rate-distortion theory itself.

## 5. Narrow candidate contribution that survives

The strongest remaining contribution is a **joint benchmarking architecture** with all of the following features:

1. **explicit latent-state / acquisition / encoding decomposition**
   [
   H ightarrow A_m ightarrow X^{(m)} ightarrow E_k ightarrow Z^{(m,k)}
   ]

2. **same-source encoding benchmark**
   - hold (X) fixed;
   - generate multiple psychiatric/phenomenological representations;
   - measure what can be reconstructed from each;

3. **separate acquisition benchmark**
   - compare actual interview, self-report, conventional assessment, EMA, etc.;
   - do not mislabel acquisition divergence as compression loss;

4. **independent source-grounded reconstruction exam**
   - query constructors never inspect the competing representations;
   - evaluators see one representation only;

5. **multi-component distortion**
   - semantic;
   - relational;
   - contextual;
   - temporal;
   - participant-endorsed;

6. **fidelity separated from reliability and intended-use validity**
   - a representation can be low-fidelity for narrative reconstruction but high-value for screening;

7. **rate/burden matching**
   - compare raw performance;
   - equal-description-rate performance;
   - equal participant/expert-time performance;

8. **use-conditioned Pareto frontier**
   - no universal "best representation";
   - non-dominated representations differ by use and burden constraints.

## 6. Current novelty statement

### Safe wording

> We propose a framework for decomposing information loss in psychopathology into acquisition- and encoding-stage components and for empirically benchmarking multiple same-source psychiatric representations using blinded, source-grounded reconstruction tasks while treating phenomenological fidelity, reliability, intended-use validity, predictive utility, and burden as separate objectives.

### Wording to avoid

> We introduce the first way to measure loss of patient experience.

> We are the first to combine phenomenology and computation.

> Existing psychiatric measures destroy phenomenological reality.

> EASE is a ground-truth readout of lived experience.

## 7. Remaining novelty threat

The nearest conceptual threat is now **PNDI + clinical summarization + phenomenological fidelity** taken together.

A future paper could already combine these ideas in a way not surfaced here. Therefore the manuscript must use "we propose" rather than "we are the first" unless a formal multi-database search supports priority.

## 8. Gate A decision

**Conditional pass for research development.**

The novelty is no longer a broad philosophical claim. It is a concrete experimental architecture.

Before journal submission, complete database-level searches in at least:

- MEDLINE/PubMed;
- PsycINFO;
- Scopus or Web of Science;
- philosophy-of-mind/phenomenology index where available;

plus backward/forward citation chaining from:

- Ramstead et al. computational phenomenology;
- Hurlburt & Heavey phenomenological fidelity;
- Nordgaard et al. psychiatric interview;
- Cobanovic/Henriksen EASE vs self-report;
- Gupta PNDI;
- psychiatric diagnostic-interview summarization papers.

## 9. Consequence for project scope

Gate A no longer blocks pilot design.

The next blocker is empirical calibration of 009A1 on independent source episodes.

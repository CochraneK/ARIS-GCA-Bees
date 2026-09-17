# ARIS4C005 — The Hidden Burden of Bad Science

**Working title:** *The Hidden Burden of Bad Science: Estimating the Global Scale and Downstream Cost of Research Integrity Failures*

## One-line question

How much of the global scholarly record is affected by serious research-integrity failures, and how much money, human time, career capital, evidence quality, innovation time, and unrealized discovery do those failures cost?

## Why this is not a retraction-count paper

The project keeps four questions separate:

1. **How much has been detected and formally corrected?**
2. **How much serious integrity failure probably exists, including undetected cases?**
3. **How much broader research waste or distortion exists without proven misconduct?**
4. **How much downstream science and society is affected by these failures?**

The core rule is:

> retraction != fraud != irreproducibility != questionable research practice != research waste.

No researcher-level survey percentage will be multiplied directly by the number of papers. The units are different.

## Exposure layers

- **E1 — Confirmed misconduct / severe confirmed integrity failure.** Formal findings, retractions with strong evidence of fabrication/falsification or analogous serious failure, or independently verified severe integrity problems.
- **E2 — Probable integrity failure.** Multiple convergent article-level signals (for example validated image anomalies, impossible statistics, paper-mill signatures, or unresolved high-confidence integrity flags) without a formal misconduct finding.
- **E3 — Broader research waste / evidence distortion.** Nonpublication, major honest error, severe irreproducibility, avoidable design/reporting waste, or other failures that waste resources or distort evidence but should not be called fraud.

Results are reported separately by exposure layer.

## Primary estimands

1. **Global detected lower bound** — number/rate of E1 records under explicit publication universes.
2. **Latent severe-integrity prevalence** — model-estimated article-level prevalence with uncertainty, using validated detectors and manual audit rather than researcher survey rates as direct paper rates.
3. **Researcher-Life-Years (RLY)** — researcher time directly spent producing, following up, correcting, or redoing severely flawed research.
4. **Scientific Contamination Footprint (SCF)** — downstream works that materially depend on problematic evidence, stratified by direct citations, evidence syntheses, guidelines/policies, and higher-order propagation.
5. **Epistemic Reproduction Number (R_E)** and **Knowledge Ghost Half-Life** — whether a problematic claim continues to reproduce through dependent works and how quickly propagation decays after correction.
6. **Innovation Delay Years (IDY)** — counterfactual delay imposed on legitimate alternatives, topic entry, or discovery trajectories.
7. **Participant Sacrifice Without Knowledge Gain** — participant-hours / participant-risk in the clinical subset when research fails to yield usable public knowledge.
8. **Integrity Maintenance Debt** — reviewer, editor, investigator, institutional, and correction labor consumed by problematic research.

## Secondary estimands

- collateral career damage to uninvolved collaborators;
- Scientific Detour Years for fields redirected by unreliable foundations;
- funding and attention displacement;
- correction latency and post-retraction citation persistence.

## Exploratory estimands

- **Never-Woken Sleeping Beauties:** counterfactual number of high-potential delayed-recognition papers that may fail to awaken under attention/funding distortion;
- talent misallocation into unreliable research trajectories;
- the long-run scientific **Trust Tax** (extra verification, monitoring, and transaction costs induced by reduced trust).

These exploratory outcomes will never be presented as directly observed facts.

## Global publication universe

The denominator is versioned and plural by design.

Current anchors at project initialization (2026-09-18):

- Crossref status page (updated 2026-09-16): 187,832,048 total records; 125,897,384 journal DOIs.
- OpenAlex Works Help: ~327.2 million core scholarly works, where a `work` includes journal articles, conference papers, book chapters, datasets, dissertations, preprints, and more.
- Crossref 2026 public data file: ~180 million metadata records through part of March 2026.

Primary confirmatory publication window: **2000–2025**. 2026 remains incomplete and is used only for infrastructure/current-state descriptions.

Primary paper denominator: OpenAlex/Crossref-resolved **journal articles + reviews**, with conference papers handled in sensitivity analyses. All-work denominators are descriptive only.

## Anchor evidence already verified

- Xie, Wang & Kong (2021), *Science and Engineering Ethics*, DOI `10.1007/s11948-021-00314-9`: pooled researcher-level prevalence of at least one FFP-type research misconduct behavior 2.9% (95% CI 2.1–3.8%); QRP 12.5% (10.5–14.7%). These are researcher-level survey estimates, **not paper prevalence**.
- Gopalakrishna et al. (2022), *PLOS ONE*, DOI `10.1371/journal.pone.0263023`: randomized-response survey in the Netherlands; fabrication 4.3% and falsification 4.2% over the previous three years. Again, these are researcher-level estimates.
- Xu et al. (2025), *BMJ*, DOI `10.1136/bmj-2024-082068` (VITALITY Study I): 1,330 retracted trials and 847 systematic reviews that quantitatively synthesized retracted trials form an empirical template for measuring evidence contamination.
- Hussinger & Pellens (2019), *Research Policy*, DOI `10.1016/j.respol.2018.01.012`: uninvolved prior collaborators experienced an estimated 8–9% citation penalty after documented misconduct cases, motivating a distinct collateral-career outcome.
- Yilmaz et al. (2018), DOI `10.1016/j.trci.2018.03.005`: in an Alzheimer/MCI trial sample, 66,655 participants were enrolled in completed but unpublished trials and 18,246 in unpublished discontinued trials, demonstrating a measurable participant-sacrifice dimension of research waste (E3, not necessarily misconduct).
- Hamilton et al. (2020), *eLife*, DOI `10.7554/elife.62529`: cites an estimate of ~68.5 million reviewer-hours volunteered globally per year, motivating a reviewer/editor labor denominator.
- Miura, Asatani & Sakata (2021), DOI `10.1007/s41109-021-00389-0`: large-scale Sleeping Beauty/Prince extraction from a Scopus dataset of 73 million papers and 1.2 billion citation links, supplying an empirical basis for delayed-recognition modeling.
- Sandoval-Lentisco & Ioannidis (2026 preprint), DOI `10.64898/2026.07.04.26357187`: among 6,081 U.S.-affiliated retracted articles, 1,725 linked to NIH grants; attributed direct cost estimated at $440M in 2026 dollars, while $4.03B in investigator-held grants were associated with retracted papers. The authors explicitly warn that the latter is not equivalent to waste and that retractions capture only detected cases.

## Core statistical strategy

### 1. Detected lower bound

Join Retraction Watch/Crossref correction metadata to a versioned global publication universe. Classify reasons before counting severe integrity failures.

### 2. Latent article-state estimation

For paper `i`, define latent state:

```text
Z_i = 0 clean / no detected severe problem
      1 honest major error
      2 QRP / severe reporting distortion
      3 FFP / serious integrity failure
      4 organized or systematic publication fraud
```

Observed signals may include retraction/editorial notices, image anomalies, statistical consistency tests, paper-mill/tortured-phrase signals, duplicated text/data, and post-publication integrity flags.

Primary model: hierarchical Bayesian latent-class model with detector sensitivity/specificity estimated from a stratified manual-audit subset.

Secondary model: multi-list capture-recapture / log-linear models, treated as sensitivity analysis because detector independence is unlikely.

### 3. Propagation model

Build a temporal knowledge graph:

```text
problematic work
  -> citing work
  -> systematic review / meta-analysis
  -> guideline / policy / patent / downstream research
```

Citation edges are not automatically counted as contamination. Edge-level dependence must be classified as background mention, critique, methodological use, result dependence, or evidence-synthesis inclusion.

### 4. Counterfactual opportunity-cost model

Estimate delays/displacement using matched topic clusters, event studies, difference-in-differences, and synthetic controls around integrity shocks. The first confirmatory target is **delay**, not permanent nonexistence, because delay is more identifiable.

### 5. Sleeping Beauty extension

Train delayed-recognition models on observed Sleeping Beauty / Prince pairs, then estimate how integrity-related attention or funding distortions change awakening probabilities. Results remain exploratory counterfactual estimates.

## Reporting principle

There will be **no single Global Bad Science Score**. Heterogeneous harms keep their natural units:

```text
USD
researcher-years
participant-hours / participant-risk
reviewer/editor/correction hours
contaminated downstream works
years of innovation delay
career-impact measures
model-estimated unrealized discoveries
```

Every modeled quantity gets uncertainty intervals and sensitivity analysis.

## Research status

See [`process/STATUS.md`](process/STATUS.md).

The project is currently in **feasibility + pilot construction**, not at the stage where global latent-prevalence or opportunity-loss numbers can be presented as empirical estimates.

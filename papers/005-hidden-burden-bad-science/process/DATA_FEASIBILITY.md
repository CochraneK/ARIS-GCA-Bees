# DATA FEASIBILITY + ACQUISITION PLAN — ARIS4C005

## Status

Feasibility is **high for the detected lower bound and downstream citation/evidence-synthesis modules**, **moderate for calibrated latent article prevalence**, and **moderate-to-low for global opportunity-loss modules** until a manual audit and topic-level pilot are run.

The plan follows PuddingSkill-style evidence rules: definitions before numbers, versioned denominators, atomic numeric claims, explicit access/licensing, and no silent conversion between observed and modelled quantities.

---

# 1. Global publication universe

## OpenAlex — primary graph/universe source

**What it answers**

- yearly article/review counts;
- DOI resolution;
- authorship, source, institution, topic, citation graph;
- work types and dates;
- funder/award links where available.

**Current scale at initialization (2026-09-18)**

- Help Center Works count: `327,203,926` core works;
- core contains journal articles, conference papers, books/chapters, datasets, dissertations, preprints, etc.;
- expansion corpus is ~190M additional noisier/repository-heavy works; all corpus exceeds 510M.

**Acquisition**

- REST API for pilots and counts;
- free public quarterly snapshot for production-scale analysis;
- JSONL and Parquet available through public S3;
- use `corpus=core` for primary bibliometrics.

**Risks**

- work != paper;
- source/type changes across releases;
- author/institution disambiguation errors;
- citation coverage varies by field and time.

**Action**

Freeze a snapshot/retrieval date and build target universe for 2000–2025 with `type in {article, review}` (exact current OpenAlex type vocabulary to be checked at extraction time), DOI reconciliation, and field/topic metadata.

---

## Crossref — denominator reconciliation + correction metadata

**Current status page (updated 2026-09-16)**

- total records: `187,832,048`;
- journal DOIs: `125,897,384`;
- conference DOIs: `10,149,465`;
- cited-by links: `2,054,772,224`.

These are metadata-record counts, not a direct estimate of unique scholarly articles.

**Acquisition**

- REST API;
- annual public data files where useful;
- DOI-level metadata reconciliation.

**Action**

Use Crossref as an independent denominator/coverage check and to resolve update metadata. Do not average Crossref and OpenAlex counts.

---

# 2. Retractions / formal corrections

## Retraction Watch via Crossref — primary detected-correction source

**Access**

Crossref acquired the Retraction Watch database in 2023. It is available through:

- Crossref REST API (`update-to` / retraction filters);
- full CSV via `crossref/retraction-watch-data` GitLab repository.

Crossref documentation states the dataset is updated every working day by Retraction Watch. Expressions of concern/corrections are present but less comprehensive than retractions.

**Important data note**

The same event can appear from publisher and Retraction Watch sources. Deduplicate by DOI/event/record identifier rather than counting raw API update rows.

**Needed fields**

- retracted DOI / title / publication date;
- retraction date;
- Retraction Watch reason(s);
- publisher/journal;
- country/institution only after author identity resolution;
- retraction source and record ID;
- correction/notice DOI where available.

**Classification**

Map reasons to E1/E3 codebook with narrow/broad sensitivity definitions. Ambiguous notices remain ambiguous.

---

# 3. Biomedical citation / translation graph

## NIH iCite + NIH Open Citation Collection

**Access**

- bulk snapshot repository;
- `/api/pubs` API;
- PubMed-ID keyed article metrics.

**Use**

- biomedical citation network;
- field/year-normalized Relative Citation Ratio (RCR);
- Approximate Potential to Translate (APT) where appropriate;
- stable biomedical subset for propagation pilots.

**Version risk**

iCite release notes document calculation changes (including 2026 RCR benchmarking refinements), so snapshot/version must be frozen.

---

# 4. Funding linkage

## NIH RePORTER — first production funding pilot

**Access**

- public Project API v2;
- Publication Search API linking PMIDs to application/core project numbers;
- public bulk exports.

**Useful fields**

- award amount;
- direct/indirect costs;
- fiscal year;
- project/core project number;
- project period;
- PI/institution;
- linked PMID/publication.

**Rate/technical limits**

NIH recommends no more than one API request per second and exposes bulk data for large jobs.

**Primary use**

Replicate and extend the output-attribution logic used by Sandoval-Lentisco & Ioannidis (2026), while keeping associated grant dollars distinct from attributable wasted dollars.

**Global extension**

Potential later sources: Europe PMC grant links, UKRI Gateway to Research, Dimensions/OpenAlex funding metadata, NSF awards, Wellcome, EU CORDIS. Feasibility/licensing must be assessed source by source; do not promise a globally complete funding ledger in Paper 1.

---

# 5. Clinical trials / participant burden

## ClinicalTrials.gov / AACT — clinical subset

**Targets**

- enrollment;
- status and discontinuation;
- dates;
- sponsor;
- posted results;
- linked publications;
- adverse-event results where available.

**Join strategy**

NCT IDs in publications + registry publication links + DOI/PMID resolution.

**Primary participant analysis**

Separate:

- E1/E2: participants in trials later invalidated/seriously compromised;
- E3: participants in completed/discontinued trials without usable public results.

**Coverage boundary**

ClinicalTrials.gov is not a complete global history of all human studies, especially earlier decades and non-US registration ecosystems. WHO ICTRP can broaden coverage, subject to data-access terms.

---

# 6. Article-level integrity detectors

No single detector defines misconduct. Detectors are noisy measurement instruments.

## 6.1 Formal editorial signals

- Retraction Watch/Crossref retractions;
- expressions of concern;
- corrections;
- publisher notices.

High interpretability; low sensitivity to undetected problems.

## 6.2 Post-publication discussion

Potential sources:

- PubPeer where permitted;
- journal comments;
- public integrity investigations.

Use as candidate signals, not ground truth. Terms/API/redistribution constraints must be checked before bulk ingestion.

## 6.3 Text/paper-mill signals

Potential sources/tools:

- Problematic Paper Screener / tortured-phrase resources;
- duplicate/reference-anomaly detectors;
- paper-mill signature studies.

Validation sample is mandatory because false positives may be field/language dependent.

## 6.4 Image anomalies

Potential sources:

- public validated image-duplication datasets;
- detector outputs from published studies;
- own detector only if reproducibly benchmarked.

Do not infer intent from an image anomaly alone.

## 6.5 Statistical consistency

Possible tools/features:

- GRIM / GRIMMER-like checks where assumptions hold;
- baseline-characteristic consistency tests for RCTs;
- impossible sample-size/statistic combinations;
- duplicated numerical fingerprints.

These are field/design-specific and cannot be applied indiscriminately across the global literature.

---

# 7. Literature evidence sources

## Scite — currently available

Useful for:

- scientific literature discovery;
- DOI metadata;
- full-text passages where access permits;
- citation context and supporting/contrasting/mentioning labels;
- citation graph pilot;
- editorial notices.

Scite's fixed citation-intent classes are not equivalent to the project's custom material-dependence taxonomy. Human validation remains required.

## Elicit — currently blocked

Attempted during project initialization. The connected account returned `api_access_denied` because its plan does not include API access.

**Decision:** Elicit is optional, not a pipeline dependency. Do not stall the project or invent results. Scite + primary sources cover the current feasibility stage.

---

# 8. Evidence-synthesis / guideline contamination

## VITALITY-style seed dataset

Xu et al. (2025, BMJ; DOI `10.1136/bmj-2024-082068`) supplies a strong empirical template:

- 1,330 retracted randomized trials;
- 312 (23.5%) contaminated 4,095 meta-analyses from 847 systematic reviews;
- 218 substantially affected meta-analyses in 68 systematic reviews were used in 157 English-language clinical practice guidelines;
- excluding retracted trials changed pooled-effect direction in 8.4% of meta-analyses and P-value significance in 16.0% overall.

This is a clinical evidence-ecosystem result, not representative of all science.

**Action**

Reproduce the logic on an independently assembled subset before generalizing the SCF framework.

---

# 9. Career spillover data

## OpenAlex / ORCID / funding joins

Possible outcomes:

- citation trajectory;
- coauthor formation;
- publication rate;
- topic changes;
- institution changes;
- grant success where funder data resolve.

Anchor design: misconduct-event matched analyses such as Hussinger & Pellens (2019), which estimated an 8–9% citation penalty for uninvolved prior collaborators.

**Risk**

Author disambiguation and implication status are high-stakes. Build conservative identity matching and exclude uncertain identities from confirmatory analyses.

---

# 10. Sleeping Beauty / delayed-recognition data

## OpenAlex / Scite citation graph

Observed Sleeping Beauty models require long citation windows. Candidate training cohorts should end early enough to observe awakening (for example pre-2010/pre-2015 depending on definition).

Anchor literature:

- Miura, Asatani & Sakata (2021), DOI `10.1007/s41109-021-00389-0`, large-scale SB/Prince extraction;
- van Raan & Winnink (2019), DOI `10.1371/journal.pone.0223373`, medical SBs and patent relevance.

**First feasible test**

Estimate whether matched local integrity shocks are associated with longer sleep duration among papers that eventually awaken. Permanent non-awakening is a later structural counterfactual.

---

# 11. Manual audit — the bottleneck that makes the latent model credible

## Pilot

Suggested initial pilot:

- 5,000–10,000 works receive automated/metadata detectors;
- 750–1,500 works manually reviewed in a stratified adjudication sample;
- include random population sample plus enriched positive-signal strata;
- double-code severe-integrity labels on the highest-stakes subset.

The pilot determines actual sensitivity, specificity, prevalence, and audit burden before fixing confirmatory sample size.

## Confirmatory scale (conditional)

If the pilot supports feasibility:

- 30,000–50,000 automatically characterized works;
- 3,000–5,000 adjudicated gold-standard works or an adaptive equivalent;
- stratify by broad field, publication period, access modality, and article type.

These are planning targets, not fixed commitments; formal power/precision calculations follow pilot estimates.

---

# 12. Data acquisition order

1. Freeze OpenAlex/Crossref denominator definitions and extraction date.
2. Pull/deduplicate Retraction Watch/Crossref correction records.
3. Build DOI/PMID/OpenAlex-ID crosswalk.
4. Produce detected-rate and correction-latency baseline.
5. Build article-detector pilot sample and adjudication protocol.
6. Calibrate latent severe-integrity prevalence model.
7. Build citation/dependence classifier and direct SCF pilot.
8. Reproduce a clinical evidence-synthesis contamination subset.
9. Link NIH RePORTER for attributable-cost pilot.
10. Run collaborator spillover and Innovation Delay pilot designs.
11. Only after those survive diagnostics, run Sleeping Beauty counterfactual extension.

---

# 13. Licensing / redistribution discipline

- Store identifiers and derived features whenever source redistribution is restricted.
- Do not commit copyrighted full text or restricted third-party datasets into the public ARIS4C repository.
- Retain source/version/query provenance sufficient to rehydrate legally accessible data.
- Crossref metadata and OpenAlex-derived public metadata can support an open reproducibility layer; source-specific terms still govern full text and third-party annotations.

---

# 14. Current feasibility verdict

### Ready now

- global denominator definitions;
- detected retraction/correction lower bound;
- correction latency;
- citation propagation pilot;
- biomedical evidence-synthesis contamination replication;
- NIH funding linkage pilot;
- delayed-recognition model scaffolding.

### Requires pilot calibration

- article-level latent severe-integrity prevalence;
- Researcher-Life-Years;
- Integrity Maintenance Debt;
- material-dependence citation classifier;
- Knowledge Ghost Half-Life;
- Innovation Delay Years.

### Keep exploratory until stronger identification

- global Scientific Detour Years;
- permanent crowding-out of otherwise publishable work;
- Never-Woken Sleeping Beauties;
- Talent Misallocation;
- global Trust Tax.

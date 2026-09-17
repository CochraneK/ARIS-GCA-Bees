# DATA FEASIBILITY — ARIS4C004

Date: 2026-09-18

## Bottom line

**Science/mathematics: GO for continued identity/network pilot; not yet GO for exposure coding or confirmatory analysis.**  
**Philosophy/literature/intellectual history: CONDITIONAL GO.**  
**Visual arts/music: HIGH-RISK PILOT ONLY.**

The project is not blocked by lack of a general candidate universe or scientific graph data. The dominant feasibility risks are now:

1. historical person ↔ scholarly-author-cluster identity precision;
2. graph observability and its selection bias across eras/regions/subdomains;
3. reliable historical mental-health evidence after the network frame is frozen;
4. documentation imbalance;
5. reproducible influence edges outside bibliometrics;
6. realistic adaptive replacement rules.

---

## 1. Source matrix

| Source | Primary role | Access / reuse | Strengths | Main limitations | ARIS4C004 decision |
|---|---|---|---|---|---|
| OpenAlex | Scientific authors, works, references, citations, topics, institutions | Core OpenAlex data CC0; API + downloadable snapshot | Large open scholarly graph, stable work IDs, references/topics | Historical coverage incomplete; historical people may be split across multiple Author IDs; humanities weaker; full-text PDFs retain original licenses | **Primary science graph source, with person-level author-cluster audit** |
| Wikidata | Cross-domain IDs, occupations, dates, relationship leads | Structured data CC0; SPARQL/dumps | Cross-domain, many authority IDs | Claims have uneven sourcing; OpenAlex Author-ID linkage was near-absent in the first pilot; `medical condition` / `influenced by` cannot be confirmatory evidence | **Candidate/entity-resolution lead source, not clinical ground truth** |
| Crossref | DOI/publication/reference metadata supplement | Public REST API; bibliographic metadata/references generally reusable; abstracts may remain copyrighted | Publisher-deposited metadata, DOIs, references, ORCID/ROR | Sparse historical references in some fields; abstracts have separate rights | **Supplementary bibliographic identity evidence** |
| Laouenan et al. cross-verified notable people | Mental-health-independent cross-domain candidate frame | Public Sciences-Po Dataverse; cross-verified restricted dataset CC-BY-SA | ~2.2M cross-verified notable people; occupations, dates, geography, notability variables | Still a notability/Wikipedia-derived universe; strong European/Western skew remains; not a population census | **Primary candidate-frame option for feasibility** |
| Semantic Scholar | Citation/reference/context supplement | API/data licensing includes attribution and use restrictions; underlying third-party rights vary | Useful scholarly graph enrichments | Public redistribution less simple than OpenAlex; license compliance overhead | **Optional only; not required** |
| Wikipedia / biographies | Candidate discovery, identity context, historical narrative leads | Wikipedia text CC BY-SA; other biographies vary | Rich contextual information | Not clinical evidence by itself; celebrity documentation bias | **Lead/context source only** |
| Archival/medical records, scholarly pathographies, authoritative biographies | Mental-health evidence | Source-specific | Highest evidential value when contemporaneous and well sourced | Labour intensive; rights/access vary; retrospective inference risk | **Required exposure-verification layer after network-frame lock** |
| Domain catalogues / authority files | Identity resolution and humanities/arts works | Source-specific | Better coverage of books, art works, composers, movements | Heterogeneous licenses and schemas | **Use selectively; record provenance** |

---

## 2. Reproducibility policy

The public repository should prefer reconstruction scripts and derived codes over committing large or rights-restricted source files.

### Safe to commit when practical

- OpenAlex IDs and derived graph features;
- person ↔ verified OpenAlex author-cluster decisions with evidence provenance;
- Wikidata QIDs and derived structured fields;
- Crossref identifiers/derived bibliographic features;
- manually coded evidence tiers with source citations/provenance;
- network edges that are factual relationships with provenance;
- simulation code and seeds;
- small CC-compatible derived datasets with required attribution.

### Do not commit by default

- copyrighted biography text;
- licensed full-text PDFs;
- restricted API response dumps when redistribution is unclear;
- sensitive modern personal health records;
- long verbatim passages from archival/medical sources.

### Required per-source metadata

Every acquisition module should record:

- source name/version/date;
- URL/DOI/identifier;
- license/reuse status;
- query/filter;
- acquisition timestamp;
- checksum for local raw file when applicable;
- transformation script/commit.

---

## 3. Pilot sampling design

### Candidate count

Initial cross-domain feasibility target remains **150–300 total candidate people** if multiple domains survive. The science pilot currently uses a fixed **100-person mental-health-independent candidate frame**, with the first 30 used for resolver development.

This is a candidate-frame target, **not** a quota for people with mental-health conditions.

### Time

Default broad historical window remains operationally `1800–2000`; strict quantitative robustness window: **1900–2000**. The current OpenAlex work pull uses 1900–2000.

### Domain families

A. science / mathematics  
B. philosophy / literature / intellectual history  
C. visual arts / music

### Stratification

Within each domain, inspect and where justified stratify by:

- historical period;
- geography/language region;
- baseline prominence/visibility;
- subdiscipline/genre;
- gender where source coverage permits.

The current science pilot is balanced on cohort × visibility but remains Europe-heavy (68/100), so region/subdomain observability must be audited before freezing the analytic frame.

The network analytic frame is frozen before mental-health evidence coding.

---

## 4. Exposure-evidence pilot

### Evidence classes

- **A1:** contemporaneous clinical diagnosis/record with clear provenance.
- **A2:** hospitalization or treating-clinician documentation where exact modern diagnosis is uncertain.
- **B1:** multiple strong contemporaneous nonclinical sources documenting a clinically meaningful syndrome.
- **B2:** high-quality scholarly biographical/medical reconstruction with explicit uncertainty and source trail.
- **C:** later/speculative retrospective diagnosis without adequate primary support.
- **U:** unknown/insufficient evidence.

For analysis, A1/A2 can be collapsed to Tier A and B1/B2 to Tier B if needed.

### Negative/comparison status

Do **not** create a binary `healthy=1` variable from absence of evidence.

Comparison candidates can instead be classified as:

- documented no/low evidence after sufficient search;
- unknown with high documentation intensity;
- unknown with low documentation intensity.

Primary matching should prioritize defensible common support and model uncertainty explicitly.

Exposure coding does not begin until identity/network inclusion rules are frozen.

---

## 5. Documentation-intensity features

At minimum measure:

- number of independent biographies/reference works;
- number of language editions / cross-verified biographies where available;
- Wikipedia biography length/pageview variables only as noisy proxies, not truth;
- surviving correspondence/archives indicator;
- institutional archive/authority-record indicator;
- number of medical/biographical scholarly sources found;
- source recency and source type distribution.

Documentation intensity must enter common-support assessment and sensitivity analysis.

---

## 6. Network feasibility by domain

### A. Science / mathematics — GO FOR CONTINUED IDENTITY PILOT

Core layers:

- author/person → work;
- work → cited work;
- person ↔ coauthor;
- work → topic;
- person → institution over time;
- advisor → trainee where source quality permits.

Preferred source: OpenAlex, supplemented by Crossref/Wikidata and discipline-specific genealogy/authority data where licensed.

Primary advantage: citations and coauthorship provide relatively reproducible temporal edges.

Current empirical warning: **11/30 (36.7%)** of the first bounded historical-science pilot triggered possible OpenAlex Author-ID fragmentation. Therefore the person-level object must be an audited cluster of one or more Author IDs rather than an automatically selected single ID.

Main remaining danger: older books/theory contributions and pre-digital/historical works are underrepresented, and observability itself may depend on era, geography, visibility, gender and subdomain.

### B. Philosophy / literature — CONDITIONAL GO

Possible layers:

- person → work;
- work → references/citations where available;
- person/work → explicitly documented influence;
- teacher/student;
- intellectual movement/school;
- translations/editions/reception events.

Main danger: "influence" often rests on interpretive scholarship and cannot be reduced to a single objective edge.

Required safeguard: high-confidence influence edges must cite a source that explicitly documents the relationship; algorithmic semantic similarity is exploratory only.

### C. Visual arts / music — HIGH RISK

Possible layers:

- creator → work;
- teacher/student/workshop;
- movement/school;
- exhibition/performance/program connections;
- explicit influence documented by catalogues raisonnés or art/music scholarship;
- later creator acknowledgement.

Main danger: reception and influence are deeply interpretive; machine-readable coverage is selective.

Likely role: portability stress test or case-study extension unless pilot coverage is unexpectedly strong.

---

## 7. Prospective domain acceptance gates

These thresholds are pilot gates, not evidence of substantive effects.

### Gate A — broad-frame graph observability

Do **not** require an arbitrary 95% of all historical candidates to resolve in OpenAlex.

Instead:

- report the proportion with plausible/verified graph records;
- characterize missingness across cohort, visibility, geography, gender and subdomain;
- ensure enough verified observable candidates remain in retained strata to support exposed/comparison analysis;
- do not loosen identity rules to raise coverage after mental-health evidence is known.

Current first-30 science estimates:

- single-top-record work coverage: 15/30 = 50.0%;
- at least one plausible network lead after fragment review: 20/30 = 66.7%;
- neither is yet final verified coverage.

### Gate B — analytic-frame identity precision

Every confirmatory included person must be `VERIFIED_SINGLE` or `VERIFIED_CLUSTER` under `IDENTITY_CODEBOOK.md`.

Requirements:

- near-100% externally auditable identity decisions among included analytic persons;
- multiple plausible OpenAlex IDs require cluster review;
- name equality alone is insufficient to merge fragments;
- conflicting ORCID/authority evidence blocks blind merging;
- verified clusters must retain provenance and deduplicate duplicate works;
- identity status and network observability remain separate variables.

Precision is prioritized over broad-frame coverage.

### Gate C — output/network sufficiency

For people retained in the network analytic frame, enough verified domain-appropriate graph data must exist to calculate preregistered baseline and downstream features.

For focal exposed cases, the target remains >=70% with at least one high-confidence downstream path beyond direct output, subject to refinement after the verified identity pilot.

### Gate D — exposure yield

- At least **15 Tier-A/Tier-B exposed focal cases** in the pilot domain to justify continued domain-specific expansion.
- A confirmatory domain will likely require more; final N is determined by simulation-based precision/power.
- The network analytic frame must be frozen before this yield is measured.

### Gate E — comparison support

- >=3 plausible comparison candidates per exposed focal case before final matching;
- common support in era, domain, baseline impact/network position as appropriate, and documentation intensity.

### Gate F — documentation common support

After matching/weighting, key documentation-intensity standardized mean differences should generally be <=0.20; tighter targets preferred. Because documentation may be downstream of fame, this is an ascertainment/common-support diagnostic rather than a universal causal adjustment rule.

### Gate G — edge provenance

- all confirmatory non-bibliometric influence edges have source provenance;
- >=80% of edges used in primary focal subgraphs meet preregistered high/medium evidence criteria; low-confidence algorithmic edges cannot dominate.

### Gate H — simulation stability

- CPE estimates are numerically stable under repeated seeds and bootstrap/resampling;
- conclusions cannot depend on one arbitrary rewiring parameter;
- negative CPE remains reportable;
- no future-information substitution is allowed in primary models.

If a domain fails, downgrade it to exploratory/qualitative rather than changing gates after seeing preferred effects.

---

## 8. Science calibration opportunity

The science domain has a unique validation route: historical star-death studies provide observed benchmarks for collaborator loss, outsider entry, and network adaptation.

Relevant empirical anchors include:

- Azoulay et al. (2010), superstar death and collaborator productivity decline;
- Azoulay et al. (2019), collaborator decline plus outsider entry after 452 star deaths;
- Mohnen (2022), brokerage-dependent spillover losses;
- Khanna (2021), network moderators of coauthor productivity after star death;
- evolving collaboration-network work showing substantial topological robustness after eminent-node removal.

Use these results to define **plausibility bounds** for adaptive rewiring, not to assume one universal substitution coefficient.

A strong future validation would reproduce a known star-loss pattern using the chosen OpenAlex graph construction before applying the simulation to mental-health-related participation scenarios.

---

## 9. Counterfactual intervention timing

Do not assume removal from birth.

Candidate intervention schemes:

1. **career-wide attenuation:** reduce productive participation across the observed active career;
2. **early-career gate:** attenuate entry/early output, representing exclusion from training/hiring;
3. **episode-aligned attenuation:** where historically documented discrimination/institutional exclusion exists, intervene at that date;
4. **timing sensitivity:** test whether results are driven by intervention start.

Primary intervention timing must be frozen before outcome simulation.

---

## 10. Real pilot evidence

Canonical details are in `PILOT_RESULTS.md`.

Key current facts:

- 108,626 Discovery/Science candidates pass the source-frame eligibility filter;
- 100-person fixed-seed cohort × visibility frame created;
- Wikidata supplied 0/100 OpenAlex-ID leads and only 1/100 ORCID lead;
- repaired-name OpenAlex top-record pilot accepted 19/30, with 15/30 having acquired 1900–2000 works;
- explicit search-hit review found **11/30 possible fragmentation cases**, 9/30 single plausible records, 9/30 no search hit and 1/30 name collision/low similarity;
- 20/30 have at least one apparent network lead, but **0 are considered identity-verified automatically**.

This justifies continued identity work, not confirmatory analysis.

---

## 11. Feasibility verdict

### Data availability

**Not a blocker.** Open scientific graph and cross-domain candidate data exist with workable reuse terms.

### Person-level scientific identity

**Current primary technical bottleneck.** Historical OpenAlex Author-ID fragmentation is common enough to require a verified cluster protocol.

### Exposure verification

**Next major labour bottleneck, intentionally deferred** until a pre-exposure network frame is frozen.

### Cross-domain comparability

**Methodological bottleneck.** Raw outcomes cannot be pooled; use domain-specific estimands and hierarchical/meta-analytic synthesis only if multiple domains survive.

### Recommended next step

Do **not** simply expand the current resolver to 100 candidates. First generate bibliographic/coauthor/institution/topic evidence for every plausible fragment in the first-30 review queue, validate the person-level cluster protocol, estimate false-positive/missed-fragment rates, and only then scale the science identity pilot.

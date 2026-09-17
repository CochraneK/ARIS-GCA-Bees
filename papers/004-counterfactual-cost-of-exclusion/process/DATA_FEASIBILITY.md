# DATA FEASIBILITY — ARIS4C004

Date: 2026-09-18

## Bottom line

**Science/mathematics: GO for pilot.**  
**Philosophy/literature/intellectual history: CONDITIONAL GO.**  
**Visual arts/music: HIGH-RISK PILOT ONLY.**

The project is not blocked by lack of a general candidate universe or scientific graph data. The dominant feasibility risks are:

1. reliable historical mental-health evidence;
2. documentation imbalance;
3. reproducible influence edges outside bibliometrics;
4. realistic adaptive replacement rules.

---

## 1. Source matrix

| Source | Primary role | Access / reuse | Strengths | Main limitations | ARIS4C004 decision |
|---|---|---|---|---|---|
| OpenAlex | Scientific authors, works, references, citations, topics, institutions | Core OpenAlex data CC0; API + downloadable snapshot | Large open scholarly graph, stable IDs, author disambiguation, references/topics | Historical coverage and author disambiguation imperfect; humanities weaker; full-text PDFs retain original licenses | **Primary science graph source** |
| Wikidata | Cross-domain IDs, occupations, dates, relationship leads | Structured data CC0; SPARQL/dumps | Cross-domain, easy entity linking, many authority IDs | Claims have uneven sourcing; `medical condition` / `influenced by` cannot be treated as validated evidence | **Candidate/entity-resolution source, not clinical ground truth** |
| Crossref | DOI/publication/reference metadata supplement | Public REST API; bibliographic metadata/references generally reusable; abstracts may remain copyrighted | Publisher-deposited metadata, DOIs, references, ORCID/ROR | Sparse historical references in some fields; abstracts have separate rights | **Supplementary** |
| Laouenan et al. cross-verified notable people | Mental-health-independent cross-domain candidate frame | Public Sciences-Po Dataverse; cross-verified restricted dataset CC-BY-SA | ~2.2M cross-verified notable people; occupations, dates, geography, notability variables | Still a notability/Wikipedia-derived universe; residual Western/language bias; not a population census | **Primary candidate-frame option for humanities/arts** |
| Semantic Scholar | Citation/reference/context supplement | API/data licensing includes attribution and use restrictions; underlying third-party rights vary | Useful scholarly graph enrichments | Public redistribution less simple than OpenAlex; license compliance overhead | **Optional only; not required** |
| Wikipedia / biographies | Candidate discovery, historical narrative leads | Wikipedia text CC BY-SA; other biographies vary | Rich contextual information | Not clinical evidence by itself; text redistribution/licensing; celebrity documentation bias | **Lead generator only** |
| Archival/medical records, scholarly pathographies, authoritative biographies | Mental-health evidence | Source-specific | Highest evidential value when contemporaneous and well sourced | Labour intensive; rights/access vary; retrospective inference risk | **Required exposure-verification layer** |
| Domain catalogues / authority files | Humanities/arts entity resolution and works | Source-specific | Better coverage of books, art works, composers, movements | Heterogeneous licenses and schemas | **Use selectively; record provenance** |

---

## 2. Reproducibility policy

The public repository should prefer reconstruction scripts and derived codes over committing large or rights-restricted source files.

### Safe to commit when practical

- OpenAlex-derived IDs and numerical features;
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

Target **150–300 total candidate people** across three data environments, approximately 50–100 per domain family.

This is a candidate-frame target, **not** a quota for people with mental-health conditions.

### Time

Default: `1800 <= active/birth period <= 2000` as operationally appropriate.  
Strict robustness window: **1900–2000**.

### Domain families

A. science / mathematics  
B. philosophy / literature / intellectual history  
C. visual arts / music

### Stratification

Within each domain, sample across:

- historical period;
- geography/language region where feasible;
- baseline prominence/impact strata;
- subdiscipline/genre;
- gender where source coverage permits.

The frame is frozen before mental-health evidence coding.

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

Primary matching should prioritize the first two categories and model uncertainty explicitly.

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

Documentation intensity must enter matching/weighting and sensitivity analysis.

---

## 6. Network feasibility by domain

### A. Science / mathematics — GO

Core layers:

- author → work;
- work → cited work;
- author ↔ coauthor;
- author → topic;
- institution affiliation over time;
- advisor/trainee where external authority sources support it.

Preferred source: OpenAlex, supplemented by Crossref/Wikidata and discipline-specific genealogy data where licensed.

Primary advantage: citations and coauthorship provide relatively reproducible temporal edges.

Main danger: older books/theory contributions and pre-digital/historical works are underrepresented.

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

A domain can advance to confirmatory modeling only if all critical gates are met or an explicit downgrade is recorded.

### Identity gate

- >= 95% of sampled candidates resolve to stable canonical identities and dates.

### Output/network gate

- >= 80% of candidates have enough domain-appropriate output/network data to calculate preregistered baseline features.
- For focal exposed cases, >= 70% should have at least one high-confidence downstream path beyond direct output.

### Exposure-yield gate

- At least **15 Tier-A/Tier-B exposed focal cases** in the pilot domain to justify continued domain-specific development.
- A confirmatory domain will likely require more; final N is determined by simulation-based precision/power, not this minimum.

### Comparison-support gate

- >= 3 plausible comparison candidates per exposed focal case before final matching.
- Common support in era, domain, baseline impact/network position, and documentation intensity.

### Documentation gate

- After matching/weighting, key documentation-intensity standardized mean differences should generally be <= 0.20; tighter targets preferred.

### Edge-provenance gate

- All confirmatory non-bibliometric influence edges have source provenance.
- >= 80% of edges used in the primary focal subgraphs must meet the preregistered high/medium evidence definition; low-confidence algorithmic edges cannot dominate.

### Simulation-stability gate

- Replacement-adjusted focal loss estimates are numerically stable under repeated seeds and bootstrap/resampling.
- Conclusions cannot depend on one arbitrary rewiring parameter value.

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
4. **randomized timing sensitivity:** test whether results are driven by intervention timing.

Primary intervention timing must be frozen before outcome simulation.

---

## 10. Feasibility verdict

### Data availability

**Not a blocker.** Open scientific graph and cross-domain candidate data exist with workable reuse terms.

### Exposure verification

**Primary labour bottleneck.** Must be manually/semi-manually source audited.

### Cross-domain comparability

**Methodological bottleneck.** Raw outcomes cannot be pooled; use domain-specific estimands and hierarchical/meta-analytic synthesis if multiple domains survive.

### Recommended next step

Build the science pilot first because it provides the strongest graph and an external adaptation benchmark. In parallel, run a much smaller humanities/arts edge-audit to determine whether a cross-domain main study is realistic before scaling manual exposure coding.

# DATA SOURCES & LICENSING LEDGER — ARIS4C003

Last verified: 2026-09-18

This file separates **access**, **reuse/redistribution**, and **analytic role**. "Free to download" is not assumed to mean "safe to republish in this public repository."

## 1. OpenAlex — primary contemporary bibliometrics

**Role:** works, affiliations/countries, institutions, topics/fields, citations, normalized citation fields, coauthorship relations.

**Preferred acquisition:** free public Parquet snapshot rather than paid API.
The executable route supports either a local snapshot root or anonymous public-S3
reads through DuckDB/httpfs. The 2007–2025 filters and required-column projection
are placed at the first scan so Parquet pruning can reduce transferred data.

Official documentation currently states:
- the public snapshot is hosted in Amazon S3;
- it is free to download anonymously and needs no AWS account;
- JSONL and Parquet versions are available;
- individual entity prefixes such as `works` can be downloaded separately;
- the full snapshot is hundreds of GB, so the project should subset by format/entity and process out-of-core rather than blindly downloading both formats;
- OpenAlex data are released under CC0/public-domain terms.

**Repository policy:** derived analysis tables and scripts may be committed. Do not commit the enormous raw snapshot. Store source release/date/manifest/checksum and reconstruction instructions.

**API policy:** no paid OpenAlex API is required for the reproducible primary route.

**Current audit status:** PASS. A real public-S3 Works Parquet object was bound
outcome-blind on 2026-09-18. Required top-level fields and the frozen nested
paths `primary_topic.subfield.id`, `primary_topic.field.id`,
`authorships.countries`, and the Top-10% citation-percentile flag all bound
successfully. See `OPENALEX_SCHEMA_PROBE.json`. No country×discipline outcomes
were materialized during the probe.

## 2. Leiden Ranking Open Edition 2025 — institutional bibliometric robustness

**Role:** open university-level bibliometric indicators and an independent
processing/indicator validation layer for project calculations. It is **not an
independent bibliographic source**, because the Open Edition itself is based on
OpenAlex.

Official resources state:
- results spreadsheets are openly downloadable;
- underlying data are downloadable;
- results and underlying data are under CC0 public-domain dedication;
- source code is openly available under MIT;
- the 2025 edition is based on OpenAlex (August 2025 snapshot).

**Repository policy:** committing the CC0 results/derived subsets is legally much safer than proprietary rankings, but prefer scripts plus compact derived analytical tables rather than duplicating large source archives.

## 3. CEPII Gravity / GeoDist — dyadic geography and colonial ties

**Role:** geographic distance, language/cultural proximity, colonial-tie proxies, macro/gravity controls for country-pair collaboration models.

Current CEPII Gravity page:
- version shown: `202211`;
- coverage: country pairs, 1948–2020;
- provides distance, macro variables, trade-facilitation and cultural-proximity/colonial-tie variables;
- CSV/R/Stata downloads are available;
- licence: **Etalab 2.0**.

**Repository policy:** retain exact version and licence notice; prefer scripted
acquisition and derived dyadic columns. Do not silently mix current and archived
Gravity versions.

**Current audit status:** PASS for Gravity V202211. The official 206,707,748-byte
archive was downloaded and checksum-recorded; the frozen 159-country universe
collapses to the complete 12,561 unordered pairs, including 156 pairs with
`col_dep_ever=1`. See `data/manifests/CEPII_GRAVITY_V202211.json`.

## 4. ICOW Colonial History v1.1 — broader formal dependency history

**Role:** colonial/dependency ruler, independence information, broader formal dependency histories and dyadic historical relationships.

Official page states:
- coverage includes states that were members of the COW interstate system between 1816 and 2018;
- it codes colonies, dependencies, League of Nations mandates, UN trust territories, and related possession/secession/merger histories;
- the data may be downloaded freely;
- the maintainers explicitly request that users **do not redistribute ICOW data**, and instead direct others to the official site for the latest release.

**Repository policy:** **DO NOT COMMIT RAW ICOW DATA.** Commit acquisition instructions, transformation code, version, retrieval date, and derived model-ready variables only to the extent these do not amount to redistributing the source dataset.

## 5. COLDAT / Our World in Data processing — European overseas colonial duration

**Role:** transparent duration/intensity measures for European overseas colonization and the small-N European imperial-center profile.

OWID's current processed page based on COLDAT 3.0 states:
- only overseas colonies are included;
- contemporary independent states are the colony units;
- colonizers are Belgium, United Kingdom, France, Germany, Netherlands, Portugal, Spain, and Italy;
- the processed time span is 1462–2022;
- OWID provides direct CSV/ZIP downloads and identifies the original Harvard Dataverse source;
- OWID-authored data/visualization/code are CC BY, while third-party source data remain subject to the original provider's terms.

**Repository policy:** use OWID's processed series where it matches the
estimand and cite both OWID and COLDAT. The original COLDAT 3.0 file used here
was also checked at Harvard Dataverse and recorded as CC0 1.0 in the source
manifest. Raw source files remain gitignored by project convention.

**Scope warning:** COLDAT is not a complete global empire dataset. It excludes non-European and continental empire forms by construction.

## 6. QS Subject Rankings — prestige-heavy secondary layer

**Role:** prestige/institutional outcome only; never the sole measure of disciplinary strength.

**Acquisition policy:** use only publicly accessible/licensed values or
manually/reproducibly recorded public indicators consistent with terms of use.
The 2026 subject product covers 55 narrow subjects and exposes Excel-download
controls on subject pages, but public visibility/download controls are not
treated as blanket redistribution permission. Do not scrape or republish
proprietary bulk tables without verified permission.

**Repository policy:** prefer storing institution identifiers, source year, transformation code, and derived analytical summaries rather than copied ranking tables.

## 7. Times Higher Education Subject Rankings — secondary institutional composite

**Role:** secondary institutional-performance triangulation. THE 2026 subject
product uses 11 broad subject areas and 18 indicators across Teaching, Research
Environment, Research Quality, International Outlook, and Industry. It is
therefore a broad composite, not a narrow bibliometric outcome.

**Acquisition policy:** same caution as QS. Public visibility does not imply bulk redistribution rights.

## 8. ShanghaiRanking GRAS — secondary research-oriented ranking layer

**Role:** secondary ranking triangulation. GRAS 2026 covers 57 subjects and
uses research/faculty/output/impact/collaboration indicators, with bibliometric
components sourced from Web of Science/InCites. This makes it useful as an
external-source contrast to OpenAlex-based measures, while still remaining a
ranking product with eligibility thresholds.

**Acquisition policy:** verify exact public download/reuse permissions for the chosen year before committing source values. If redistribution rights are unclear, store extraction/reconstruction instructions and derived model coefficients only.

## 9. World Bank / UNESCO / OECD / OWID controls

**Role:** contemporary capacity and sensitivity analyses only, with estimand-specific justification.

Potential measures:
- population;
- GDP/GDP per capita;
- R&D expenditure;
- researchers per capita;
- tertiary enrollment/education;
- other science-system capacity variables.

**Policy:** source and licence each indicator independently. These variables are not automatically "controls" because some may mediate historical persistence.

---

# Reproducibility architecture

For each source create a machine-readable manifest entry containing:

- source name;
- version/release;
- retrieval date;
- official source URL;
- licence/reuse status;
- raw-file checksum if locally downloaded;
- whether raw data may be committed;
- transformation script;
- derived output path.

Recommended local-only layout:

```text
papers/003-colonial-disciplinary-advantage/
  data/
    raw/          # gitignored when large/restricted
    interim/
    derived/
    manifests/
```

Public repository should contain code/manifests and only those data artifacts that are both small and redistributable.

# Current acquisition decision

**No paid LLM API is needed.** GPTPage/web is used for ARIS reasoning/reviewer handoffs. For numerical scientific data, use official bulk downloads/snapshots/files rather than asking GPTPage to manufacture datasets.

Primary acquisition stack at this stage:

1. COLDAT/OWID + ICOW → historical exposure crosswalk;
2. CEPII → dyadic controls/ties;
3. OpenAlex public snapshot → primary bibliometrics;
4. Leiden Open Edition → open same-source processing/indicator validation;
5. QS/THE/Shanghai → secondary prestige/institutional triangulation only after terms are checked.

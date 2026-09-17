# ARIS4C006 · Data sources and feasibility

Last updated: 2026-09-18

## Design principle

No single data source can identify the target mechanism. The project requires a join between:

1. a **Chinese surname population baseline**;
2. bibliographic records that preserve **author order**;
3. longitudinal **author and affiliation histories**;
4. field/journal/year context from which actual alphabetization exposure can be estimated.

## Source matrix

| Source | Role | Unit | Time coverage | Primary use | Main limitation |
|---|---|---|---|---|---|
| ChineseNames 2025.8 | Population baseline | surname / given-name character | underlying DB 1930–2008 | expected surname-initial distribution, surname frequency, uniqueness | not a 2025 population census; mainly Han household-registration data represented in the source DB |
| Ministry of Public Security name reports | Contemporary validation | aggregated rankings/geography | mainly annual reports around 2019–2021 located so far | validate common surnames, name trends, geographic concentration | no open research-grade bulk individual table |
| OpenAlex | Main scholarly panel | work / authorship / author / institution | historical to current | author order, raw names, affiliations, fields, citations, corresponding-author flag | author disambiguation and name parsing are consequential for common Chinese names |
| CAS / transparent elite rosters | Secondary validation | person | roster-dependent | alternative elite outcome | selected population; must not define the primary success outcome |
| CCNC or other name corpora | Optional parser aid | name string | corpus-specific | name-form and sex/name-model auxiliary analysis | non-probability corpus; not a population denominator |

## 1. ChineseNames 2025.8

### Canonical role

Use as the **primary population denominator** for surname initials.

Current package facts:
- package version: `2025.8`;
- underlying database: `1930–2008`;
- 1,806 surnames;
- 2,614 given-name characters;
- approximately 1.2 billion Han Chinese represented in the source population database.

### `familyname` fields needed for 006

- `surname`
- `compound`
- `initial`
- `initial.rank`
- `n.1930_2008`
- `ppm.1930_2008`
- `surname.uniqueness`

The first rows already demonstrate why a uniform alphabet baseline is invalid: Wang (`W`), Li (`L`), Zhang (`Z`), Liu (`L`), Chen (`C`), Yang (`Y`), Huang (`H`), Zhao (`Z`), Wu (`W`), and Zhou (`Z`) place substantial population mass in a small set of initials.

### Derived baseline to freeze

Create `data/derived/chinesenames_initial_population_baseline.csv` with one row per initial and at least:

- `initial`
- `initial_rank`
- `surname_count`
- `population_n`
- `population_share`
- `population_ppm`
- `compound_surname_population_n`

Descriptive scholar over/under-representation can then use observed counts divided by counts expected from the Chinese population baseline, rather than an invalid `N/26` expectation.

### License / provenance

The R package is GPL-3. Its documentation should be cited. A convenient plain-CSV derivative repository exists for engineering tests, but the confirmatory data build should pin the canonical package version and produce our own exported snapshot.

## 2. Ministry of Public Security name reports

Use only for **external validation and temporal/geographic context**.

Potential checks:
- whether top surname rankings remain broadly compatible with the older ChineseNames baseline;
- which surnames are geographically concentrated;
- whether contemporary newborn-name patterns differ sharply from historical cohorts.

Do not:
- treat report rankings as a complete surname probability distribution;
- mass-query public same-name services as if they were a research API;
- silently mix newborn-name frequencies with adult scholar surname frequencies.

## 3. OpenAlex

### Why it is the main outcome source

OpenAlex authorships expose:
- resolved author ID and display name;
- `raw_author_name` preserved from the source record;
- raw affiliations and resolved institutions;
- countries attached to authorships;
- author order because authorships are embedded in work records in listed order;
- `is_corresponding` where source data provide it.

This is sufficient to estimate publication-order conventions and build longitudinal scholarly histories.

### Primary population definition

Avoid the phrase “Chinese person” when the data only identify affiliation.

**Primary estimand population:**

> scholars/authorships participating in the mainland-China scholarly system, operationalized using resolved `CN` institutional affiliations, whose surname can be parsed with a pre-specified high-confidence rule.

Preferred labels:
- `China-affiliated author-year`;
- `China-based scholar` when longitudinal criteria are satisfied;
- `Chinese-surname scholar` only when the surname classification itself is relevant.

Do not infer nationality, ethnicity, citizenship, or birthplace from the name.

### Candidate nested samples

**Sample A — authorship-level institutional sample**
- work contains an authorship with at least one `CN` institution;
- surname passes the high-confidence parser;
- suitable for estimating author-order exposure.

**Sample B — author-year China-based panel**
- author has qualifying China affiliation in year `t` based on works;
- outcomes measured at author-year level;
- suitable for longitudinal exposure/outcome models.

**Sample C — stable China-based career cohort**
- requires a pre-specified minimum share/number of early-career years with CN affiliations;
- useful for career analyses but must not be chosen after outcome inspection.

International mobility can be studied as transitions in observed affiliation geography without claiming citizenship.

## 4. Critical feasibility problem: Chinese surname parsing

OpenAlex does not provide a universally reliable `family_name` field for every author. A naive `last token = surname` rule is unsafe because Chinese names appear in both Western and Chinese order and may be romanized in multiple ways.

### Required parser tiers

**Tier 1 — high confidence**
- source/raw name contains Chinese characters and a surname can be matched directly to the frozen ChineseNames dictionary; or
- an independent structured source provides an explicit family-name field that can be linked reproducibly.

**Tier 2 — supported Romanized match**
- name token matches a Chinese-surname romanization dictionary;
- ordering is supported by multiple records / ORCID / consistent raw-name variants;
- ambiguous two-token cases receive an explicit confidence score.

**Tier 3 — heuristic only**
- e.g. final-token rule without corroboration;
- allowed for an engineering pilot, not confirmatory inference.

Polyphonic surnames and non-Mandarin/legacy romanizations require an explicit exception table.

### Validation target

Before confirmatory analysis, independently validate a stratified sample spanning:
- common vs rare surnames;
- two-token vs multi-token names;
- mainland-only vs internationally mobile authors;
- fields with high vs low alphabetization;
- compound surnames.

Report precision of surname identification and initial assignment. Pre-specify an acceptable threshold before viewing focal outcome effects.

## 5. Critical feasibility problem: author disambiguation

Chinese names have high collision rates. Common surnames and common given names may create merge/split errors that correlate with surname frequency and contaminate the focal predictor.

Mandatory diagnostics:
- outcome patterns by surname-frequency decile;
- repeat analysis among uncommon full-name strings;
- ORCID-linked subset where feasible;
- exclude authors with implausible simultaneous affiliations/publication volume;
- compare raw-name variation within OpenAlex author IDs;
- sensitivity to minimum career-consistency criteria.

If an effect strengthens mechanically with name commonness, treat that as a data-quality warning, not substantive evidence.

## 6. Measuring alphabetization exposure

For each eligible multi-author paper, derive whether surname order is lexicographically non-decreasing under the validated surname parser.

Because alphabetical ordering can happen by chance, especially with two authors, compute team-size-specific expected chance.

For `n` distinct surnames under random order:

`P(chance alphabetical) = 1 / n!`

Ties and repeated surnames require a permutation-count adjustment rather than blindly using `1/n!`.

### Context-level exposure candidates

Estimate an **excess alphabetization rate** for:
- journal × year;
- field × year;
- journal × field × rolling window where sample size permits.

Conceptually:

`excess_alpha = (observed_alpha_rate - expected_chance_rate) / (1 - expected_chance_rate)`

Use shrinkage/minimum-cell rules so small journals do not receive extreme exposure scores from a few papers.

For author-level analyses, construct cumulative exposure using contexts observed **before** or excluding the focal work/outcome window to reduce mechanical leakage.

## 7. Outcomes

### Mechanism-proximal first

- first-listed status in multi-author work;
- normalized listed position;
- corresponding-author status where available;
- team size / collaboration rate;
- selection into high- vs low-alphabetization journals;
- deliberate departures from alphabetical ordering.

### Distal outcomes second

- field/year-normalized citations;
- top-cited-paper shares;
- publication persistence;
- affiliation transitions;
- entry into high-prestige institutions using a separately frozen prestige metric;
- international mobility.

Cumulative metrics such as h-index are secondary because they strongly reflect career age and survival.

## 8. Data licensing and reproducibility

- Keep source URLs, access dates, package/API versions, and query parameters in machine-readable metadata.
- Do not commit unnecessary personally identifying raw profile pages.
- Pin the OpenAlex extraction date/version.
- Do not redistribute third-party data beyond its license.
- Store derived surname baselines and analysis-ready aggregate tables when redistribution is permitted.

## 9. Feasibility verdict

**Feasible with a major parser/disambiguation gate.**

The limiting factor is not the existence of surname or bibliometric data. It is whether surnames can be reconstructed from OpenAlex records with sufficiently high, non-differential accuracy and whether common-name disambiguation error can be bounded.

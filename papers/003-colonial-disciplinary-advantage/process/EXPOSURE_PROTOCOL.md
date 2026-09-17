# COLONIAL / IMPERIAL EXPOSURE PROTOCOL — ARIS4C003

## Key design correction

The "imperial-center" hypothesis has a **small effective N**. A duration-oriented source such as COLDAT covers eight European overseas colonial powers (Belgium, United Kingdom, France, Germany, Netherlands, Portugal, Spain, Italy). Repeating these countries across many disciplines does not create hundreds of independent treated countries.

Therefore ARIS4C003 must not present a conventional country×discipline panel regression as if the imperial-ruler treatment were supported by a large number of independent national treatment units.

The project will use **three distinct exposure families** with different inferential roles.

---

## Exposure family A — European overseas colonial duration (COLDAT)

Purpose:
- clean duration/intensity measures;
- high reproducibility;
- historical specialization analysis for European overseas empire;
- descriptive/limited-inference imperial-center analysis.

Current documentation:
- COLDAT aggregates the reach and duration of European overseas colonial empires from secondary historical sources;
- contemporary independent states are the colony units;
- overseas colonies only;
- eight European powers;
- OWID's processed series spans 1462–2022 and exposes years-colonized and colonizer-over-time summaries.

### Former-colony variables

Candidate primary variables:
- total years under European overseas colonial rule;
- last/primary European colonizer;
- number of distinct European colonizers;
- independence/end-of-rule period.

### Imperial-center variables

Candidate descriptive variables:
- cumulative colony-years ruled;
- number of overseas colonies per year / integrated empire exposure;
- peak number of colonies;
- duration of overseas colonial activity.

### Inference rule

For the eight European imperial centers:
- emphasize effect sizes, profile plots, rank/gradient consistency, and leave-one-empire-out analyses;
- use permutation/randomization-style inference across discipline labels or empire profiles where defensible;
- do not rely on naive cluster-robust asymptotics with only a handful of imperial treatment clusters;
- label conclusions as comparative/descriptive unless stronger design support is developed.

---

## Exposure family B — broader formal colonial/dependency history (ICOW)

Purpose:
- broader colonizer identities and dependency relationships;
- post-1816 state histories;
- dyadic former-colonizer links;
- capture relationships omitted by a Europe-only overseas-colony definition.

ICOW's public description includes colonies, dependencies, League of Nations mandates, UN trust territories, and related state/dependency histories. It is useful for primary colonial ruler, independence, and dyadic historical relationship coding.

### Strength

This family can represent non-European/formally distinct rulers (for example Japan or other non-European/continental powers where ICOW coding applies), which matters because ARIS4C003 should not equate "empire" with eight European states in all analyses.

### Limitation

ICOW is not interchangeable with COLDAT. Coverage rules, time range, and concept of dependency differ. Do not merge them without a documented crosswalk.

### Data policy

The ICOW site requests that users obtain the data from the official source rather than redistributing it. ARIS4C003 should therefore commit acquisition/cleaning instructions and derived non-reconstructive summaries only where permitted, not the raw ICOW archive.

---

## Exposure family C — dyadic colonial tie / common colonizer / language

Purpose:
- highest-powered test of persistence in modern scientific collaboration;
- country-pair analysis rather than country-level treatment;
- distinguish direct former colonizer–colony ties from common-colonizer affinity.

Candidate sources:
- ICOW colonial history;
- CEPII GeoDist/Gravity or other documented dyadic datasets for direct colonial relationship, common colonizer, language, distance, contiguity.

Primary dyadic distinctions:

1. `direct_former_colonial_tie_ij`
2. `common_colonizer_ij`
3. `common_language_ij`
4. `geographic_distance_ij`

Do not treat common language as merely a nuisance variable: it may be a persistence pathway created or reinforced by colonial history. Estimate models both before and after language adjustment and interpret attenuation mechanistically.

---

## Main inferential hierarchy after small-N review

### Tier 1 — large-sample confirmatory

**Former-colony / dependency disciplinary specialization**

Question:
> Among contemporary states, does the duration/type/identity of historical colonial exposure predict a systematic modern disciplinary profile as a function of field entanglement?

The sign is not prespecified as universally positive; colonizer identity and duration heterogeneity are central.

### Tier 1 — large-sample confirmatory

**Dyadic network persistence**

Question:
> Are direct former colonial pairs disproportionately connected in modern scientific collaboration, especially in more historically entangled fields, after standard gravity/network controls?

### Tier 2 — theory-critical but small-N

**Imperial-center specialization**

Question:
> Do historical imperial centers show the predicted disciplinary profile, and is the pattern monotonic with empire intensity across the small set of imperial powers?

Treat as comparative historical / exact-inference evidence, not a large-N causal regression.

### Tier 3 — exploratory extension

Broader empire forms not harmonized cleanly across datasets:
- continental empires;
- informal empire;
- protectorate/semi-colonial relations;
- US informal/global influence;
- historical scientific migration shocks.

These can motivate later papers or robustness analyses but should not destabilize the confirmatory core.

---

## Germany, Japan, and the United States

The motivating examples should be separated conceptually:

- **Germany:** included in European overseas-colonial exposure, though its formal overseas empire was shorter than Britain/France/etc.
- **Japan:** important non-European colonial empire; should be represented through broader colonial/dependency data rather than forced into COLDAT.
- **United States receiving German scientists:** this is **not a colonial-exposure measure**. It is a different historical-knowledge-capital mechanism (forced/scientist migration and postwar institutional transfer). Keep it as a theoretical analogy/future extension, not part of the primary colonial variable.

This separation prevents the paper from expanding into a generic "all history explains science" framework.

---

## Freeze decisions

1. Do not create one pooled `colonial_history_score` combining colonizer and colonized status.
2. Keep COLDAT and ICOW exposure concepts separate and triangulate them.
3. Treat imperial-center analysis as small-N.
4. Make former-colony and dyadic analyses the main scalable inferential layers.
5. Keep scientist migration/war shocks outside the primary 003 exposure definition.

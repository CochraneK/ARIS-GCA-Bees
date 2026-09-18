# ARIS4C006 · Closest prior work map

Last updated: 2026-09-18

## Decision rule

This file records work that could make ARIS4C006 redundant. Novelty is judged by overlap in **population + exposure + outcome + identification**, not by whether an earlier paper used the exact same database.

## High-danger precedents

| Work | Population | Exposure / mechanism | Outcome | Threat to 006 | Residual space |
|---|---|---|---|---|---|
| Einav & Yariv 2006, JEP, `10.1257/089533006776526085` | top U.S. economics + psychology faculty | surname rank × field alphabetical norm | tenure, honors, collaboration | establishes core alphabetical-discrimination mechanism and field comparison | measured local exposure + China-scale longitudinal panel |
| Efthyvoulou 2008, Journal of Socio-Economics, `10.1016/j.socec.2007.12.005` | economists | surname rank / alphabetic authorship | reputation, employment, views/downloads, strategic name behavior | already links surname position to reputation and strategic response | China-specific population calibration + longitudinal exposure |
| Liu & Fang 2014, Scientometrics, `10.1007/s11192-013-1219-x` | mainland-China publications across 25 categories with high alphabetization | Chinese publication share / intentional alphabetical authorship | trends in alphabetical authorship | directly studies mainland China and cross-field alphabetization; shows mainland authors generally do not prefer it | individual-level exposure and career consequences rather than aggregate publication trend |
| Huang 2015, Economic Inquiry, `10.1111/ecin.12125` | U.S.-based scientific journal articles | first-author surname initial / reference-list ordering | citations | already studies broad-science surname initials and citation mechanism | China-based longitudinal institutional-exposure design; citations cannot be sole endpoint |
| Kadel & Walter 2015, Finance Research Letters, `10.1016/j.frl.2015.05.015` | Economics + Finance scholars | alphabetical disadvantage | team-size/coauthoring strategy | already tests behavioral adaptation | broader exposure gradient and longitudinal mechanism tests |
| Yuret 2016, Scientometrics, `10.1007/s11192-016-2058-3` | full professors in 9 fields | alphabetic vs non-alphabetic fields | academic career/rank | tests field-level career effect and finds weak/null evidence | continuous measured exposure, China system, modern longitudinal records |
| Yuret 2019, Data and Information Management, `10.2478/dim-2019-0006` | 19,353 faculty over ~100 years | surname initials × alphabetic field | career progression/full professor | already longitudinal and career-focused | China + population calibration + work-level measured exposure |
| Fernandes & Cortez 2020, Scientometrics, `10.1007/s11192-020-03686-0` | 27 fields, two large bibliometric datasets | measured author-list alphabetization | field/time convention prevalence | already measures alphabetization empirically across many fields | link convention exposure to individual Chinese author trajectories rather than field description |
| Li & Yi 2021, Economic Journal, `10.1093/ej/ueaa049` | Chinese economists vs Chinese physicists/statisticians | surname rank × economics alphabetic norm | U.S./China job placement | **closest China-specific causal/identification predecessor** | all-field/local measured exposure, mechanism outcomes, broader longitudinal endpoints |
| Li & Li 2021, JEBO, *Alphabetic norm and research output* | 42 leading economics journals over 21 years | conformity/deviation from alphabetic norm | length, journal prestige, citations | shows norm conformity relates to output and asymmetric incentives | China-specific author-level exposure and population denominator |
| Wohlrabe & Bornmann 2022, Scientometrics, `10.1007/s11192-022-04322-9` | >120k economics multi-author papers | alphabetized coauthorship | citations | large-scale evidence finds little general citation effect after controls | argues strongly against citation-only headline; motivates mechanism-first design |
| Öz 2024, Scientometrics, `10.1007/s11192-024-05100-5` | 2,278 academics, 70,377 papers, 4 social-science fields | alphabetization + surname strategies | citation/behavior | recent multi-field strategic-response study | continuous journal/field/year exposure, China-scale longitudinal panel |
| Cai, Wong & Kwong 2025, Psychonomic Bulletin & Review, `10.3758/s13423-025-02727-0` | 446,755 articles across four disciplines + preregistered experiment | surname order × alphabetical-vs-numerical **citation system** | citation frequency / attention mechanism | recent causal/experimental evidence that alphabetical citation presentation can amplify surname-order citation bias; explicitly notes Chinese X/Y/Z concentration | distinct from byline-author-order exposure, but makes a citation-only surname headline substantially less novel |
| Donner & Korytkowski 2025, Scientometrics, `10.1007/s11192-025-05369-0` | mathematics coauthorship / Polish habilitation contribution statements | prevailing alphabetical byline convention | stated contribution vs author order | strengthens the claim that mathematics is a high-alphabetization comparison setting and shows alphabetical order may coexist with near-equal contributions | 006 must not equate later byline position with lower actual intellectual contribution in mathematics |
| Yuret 2026 preprint, `10.21203/rs.3.rs-8804379/v1` | 4,199 female academics in economics, mathematics, psychology | majority-alphabetical publication exposure × multiple surnames | strategic surname use/change | already uses researcher-level alphabetization exposure over long careers and finds greater use of earlier surnames in alphabetic contexts | 006 novelty must rest on China-specific population calibration, time-varying measured contexts, work-position mechanism, and prospective longitudinal architecture rather than generic person-level exposure |
| D'Angelo 2026, Journal of Informetrics, `10.1016/j.joi.2026.101841` | global top-2% scientists vs national expected surname distributions | surname rank + national expected distributions | c-score/top-scientist-list inclusion | **closest recent population-calibrated bibliometric predecessor** | directly measured institutional exposure and longitudinal mechanisms; elite lists only secondary |
| Crabtree, Holbein & Tsutsui, active R&R at Journal of Informetrics, *The Tyranny of Alphabetical Ordering: The Uneven Distribution of Authorship Credits by Authors' Country of Origin* | century of leading economics/political-science/sociology publications + ~0.5B name profiles across >100 countries | country-level surname-initial distributions under alphabetized bylines | cross-national position/credit disadvantage | **directly occupies the tempting “China's later surname distribution creates international alphabetical disadvantage” pivot** | individual China-based longitudinal exposure, within-author changes, behavioral mechanisms, Chinese name/identity measurement |

## Most dangerous combined prior-art facts

No single element below is novel on its own:

- surname rank and academic success — occupied;
- strategic response to alphabetical disadvantage — occupied;
- citations and surname initials — occupied;
- longitudinal academic careers — occupied;
- Chinese academics — occupied;
- mainland-China influence on alphabetization trends — occupied;
- many-field empirical alphabetization rates — occupied;
- population/expected surname distribution calibration — occupied by 2026 work;
- field heterogeneity — occupied;
- citation-system × surname-order causal/experimental mechanism — occupied by a 2025 preregistered archival/experimental study;
- researcher-level long-run alphabetization exposure and strategic surname choice — occupied by a 2026 preprint;
- international mobility of Chinese economists — occupied;
- **country-of-origin inequality caused by national surname distributions under alphabetical authorship — occupied by an active Journal of Informetrics R&R.**

## Candidate distinctive contribution after this sweep

The strongest remaining design is not a new correlation but a **linked exposure architecture**:

1. Select authorships through mainland-China institutional affiliation rather than presumed ethnicity.
2. Recover surname initials using a validated, outcome-blinded Chinese-name parser.
3. Calibrate initials against ChineseNames population frequencies.
4. Estimate journal/field/year/team-size-adjusted excess alphabetization directly from other papers/authors.
5. Assign each scholar a lagged longitudinal exposure history.
6. Test mechanism-proximal author-position/visibility outcomes first.
7. Test a small preregistered set of later career outcomes second.
8. Require attenuation in low-alphabetization, single-author, future-exposure, and randomized-rank controls.

## Potential sharper within-author contribution

A promising strengthening analysis is a **within-author exposure switch**:

- the same China-based scholar may publish across contexts with very different prior alphabetization norms (domestic/international journals, fields, collaborations, or convention periods);
- surname rank is fixed while institutional exposure changes;
- author fixed effects absorb all stable scholar-level traits, leaving identification in `surname-rank group × time-varying exposure` interactions.

This is not automatically causal because context switching is endogenous, but it is materially stronger than comparing different people with different surnames.

A domestic-vs-international framing should be retained only if exposure differences are empirically verified rather than assumed. It must not be reframed as a generic cross-country surname-distribution inequality claim because the Crabtree–Holbein–Tsutsui R&R now directly covers that territory.

## Search implication from Chinese authorship literature

Liu & Fang (2014) reports that mainland Chinese authors generally did not prefer alphabetical authorship and that growing mainland publication reduced intentional alphabetization in several natural-science/technology categories. This should be used as a prior hypothesis about heterogeneity, not hard-coded into the exposure score.

Li & Yi (2021) similarly relies on the fact that alphabetic name listing is unusual in Chinese settings outside international economics coauthorship. Again, ARIS4C006 should measure the convention rather than assign it categorically.

The Crabtree–Holbein–Tsutsui R&R reports that surname distributions differ sharply across countries and that late-surname countries appear systematically later in alphabetized bylines, with East/Central Asia among disadvantaged regions. This makes a simple “Chinese surnames are later, therefore Chinese authors lose credit internationally” paper redundant before it is even run.

## Novelty status

**NARROW / CONDITIONAL GO.**

The paper survives the novelty gate only as a measured-exposure, longitudinal, mechanism-first study inside the China-based scholarly system. If the actual analysis collapses to field dummies, raw surname rank, citations, elite-list representation, or country-of-origin comparisons, it should be stopped or reframed as a replication rather than presented as a new primary contribution.

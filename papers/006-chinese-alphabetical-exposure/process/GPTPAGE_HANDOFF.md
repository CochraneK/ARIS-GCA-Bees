# ARIS4C006 · GPTPage handoff

Last updated: 2026-09-18

## Purpose

Use this packet when an ARIS reviewer/research stage requires an external LLM/API that is unavailable in the current environment. Paste the relevant prompt into GPTPage and return the full response into the ARIS4C006 process record with model/date provenance.

Do not ask the reviewer to make the paper sound novel. Ask it to find reasons the paper is redundant, biased, or infeasible.

---

## Reviewer prompt A — closest-prior-work / novelty attack

You are an adversarial senior reviewer in scientometrics, sociology of science, economics of science, and bibliometrics.

Project: ARIS4C006, "Alphabetical Exposure and Academic Careers in Chinese Science."

Canonical question: Among scholars in the mainland-China scholarly system, does Pinyin surname alphabetical position predict authorship visibility or later career outcomes specifically under greater exposure to empirically measured alphabetical author-ordering regimes, after calibrating against the non-uniform population distribution of Chinese surnames?

Known closest prior work that MUST be treated as prior art:
- Einav & Yariv (2006), Journal of Economic Perspectives, surname initials and academic success in economics vs psychology, DOI 10.1257/089533006776526085.
- Li & Yi (2021), Economic Journal, Chinese economists vs physicists/statisticians and US/China job placement, DOI 10.1093/ej/ueaa049.
- Wohlrabe & Bornmann (2022), Scientometrics, >120k economics coauthored papers, DOI 10.1007/s11192-022-04322-9.
- Öz (2024), Scientometrics, economics/psychology/political science/sociology, DOI 10.1007/s11192-024-05100-5.
- D'Angelo (2026), Journal of Informetrics, expected national surname distributions and top-2%-scientist/c-score inclusion, DOI 10.1016/j.joi.2026.101841.

Planned contribution:
1. ChineseNames 1930–2008 surname population baseline;
2. China-affiliated OpenAlex scholarly population across many fields;
3. direct journal/field/year/team-size-adjusted measurement of excess alphabetization beyond random order;
4. longitudinal scholar-level cumulative exposure;
5. mechanism-proximal author-position/collaboration outcomes before distal career outcomes;
6. negative-control low-alphabetization and single-author contexts;
7. explicit Chinese-name parsing and OpenAlex disambiguation audits.

Tasks:
1. Search for the closest prior papers through 2026, especially anything already combining Chinese scholars, measured local alphabetization intensity, longitudinal careers, population surname baselines, or OpenAlex/Scopus all-field data.
2. Rank the top 10 most dangerous overlaps by conceptual proximity. For each, give exact citation/DOI/link, sample, exposure, outcomes, identification logic, and what 006 would still add.
3. State whether the project is: GO, NARROW, PIVOT, or STOP.
4. If GO/NARROW, write the narrowest defensible novelty claim in <=80 words.
5. Identify any claim currently presented as novel that is already occupied.
6. Do not reward sample size alone as novelty.

Output a table plus a blunt reviewer memo.

---

## Reviewer prompt B — surname-parser attack

Act as a bibliographic identity-resolution engineer and Chinese-name specialist.

We need to infer Chinese surname/family-name initials from OpenAlex `raw_author_name`, resolved display name, ORCID when present, and repeated publication records. Chinese names may appear in family-given or given-family order, in Chinese characters or Romanized form, with compound/polyphonic surnames and historical/regional Romanizations.

Current rule: confirmatory inference excludes heuristic-only “last token = surname” cases. We plan Tier 1 direct Chinese-character/structured-family-name evidence, Tier 2 corroborated Romanized evidence, Tier 3 heuristic-only excluded.

Tasks:
1. Attack this design: enumerate systematic error modes that could correlate with field, mobility, surname frequency, or alphabet rank.
2. Propose a robust parser architecture and confidence score.
3. Provide a curated starter list of polyphonic Chinese surnames and common non-Hanyu-Pinyin surname Romanizations, with authoritative sources where possible.
4. Design a blinded validation sample and minimum acceptance criteria.
5. Explain how to distinguish Chinese/Western name order without inferring ethnicity from the name.
6. Identify what evidence would force the study to narrow to Chinese-character-only names.

Do not suggest using an unvalidated generic Pinyin converter as sufficient evidence.

---

## Reviewer prompt C — causal identification attack

Act as an adversarial causal-inference reviewer.

Exposure of interest: interaction between stable surname initial rank `R_i` and lagged/cross-fitted local alphabetization intensity `E_it`, empirically estimated from journal/field/year author-order behavior after correcting for chance ordering by team size.

Primary population: China-affiliated authorships/authors, not nationality inferred from names.

Planned outcomes: listed author position, first-listed status, corresponding author, collaboration behavior, then field-normalized citations, publication persistence, institution transitions, and observed geographic mobility.

Known problems: surname geography/ancestry; endogenous field/journal/coauthor choice; common-name OpenAlex split/merge errors; internationalization affecting both name formatting and outcomes.

Tasks:
1. Draw the strongest plausible DAG(s), including measurement error.
2. Identify which covariates are confounders, mediators, colliders, or ambiguous.
3. Assess whether `R × E` is interpretable under any realistic assumptions.
4. Propose stronger within-author, event-study, instrumental-variable, regression-discontinuity, or natural-experiment opportunities ONLY where substantively plausible.
5. Design negative controls and future-exposure placebos.
6. Specify what evidence would justify causal language and what evidence permits only association/mechanism-consistency language.
7. Identify the single most dangerous source of false positive.

Return recommendations before any confirmatory outcome analysis.

---

## Reviewer prompt D — statistical specification / preregistration attack

Act as a senior statistical reviewer asked to prevent researcher degrees of freedom.

Given the design above, propose a preregistration-ready hierarchy with:
- one primary exposure interaction;
- no more than 4 confirmatory outcomes;
- exact sample/window/exclusion logic;
- context-level exposure estimator including ties and `1/n!` chance logic;
- cross-fitting/lagging strategy;
- fixed effects and clustering;
- multiplicity control;
- missing-data rules;
- parser-confidence rule;
- OpenAlex disambiguation sensitivity suite;
- stopping rules.

Explicitly reject specifications that are tautological because the focal paper contributes to its own exposure score.

Return: primary model, secondary models, falsification tests, exploratory-only analyses, and a preregistration checklist.

---

## Reviewer prompt E — final red-team decision

Read the canonical README, LITERATURE_SEED, DATA_SOURCES, RESEARCH_PLAN, SURNAME_PARSING_PROTOCOL, CAUSAL_MODEL, and AUTO_REVIEW for ARIS4C006.

Pretend you are reviewing for Journal of Informetrics / Scientometrics after seeing D'Angelo (2026).

Questions:
1. Is there enough novelty after the 2026 c-score paper?
2. Is the surname-population denominator scientifically appropriate, and what alternative denominator should be reported?
3. Is the local alphabetization-exposure measure genuinely independent of outcomes?
4. Could OpenAlex Chinese-name identity errors fully explain the proposed pattern?
5. What result pattern would be convincing evidence for the institutional mechanism?
6. What null result would still be publishable/useful?
7. Which analyses should be removed to prevent a sprawling paper?
8. Final verdict: GO / NARROW / PIVOT / STOP, with required changes.

Be skeptical. Do not infer quality from the sophistication of the plan.

---

## Return protocol

For every GPTPage run, save:
- date/time;
- model/product if shown;
- exact prompt label/version;
- full raw response;
- a separate ARIS adjudication note stating which reviewer suggestions are accepted/rejected and why.

External reviewer output is evidence for design decisions, not a replacement for source verification.

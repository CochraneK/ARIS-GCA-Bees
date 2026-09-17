# ARIS4C006 · Pilot 2: stratified exposure variation

Last updated: 2026-09-18

## Purpose

Test whether OpenAlex provides enough between-field variation in author-order conventions to support the planned `surname rank × measured alphabetization exposure` design.

**This is an engineering feasibility result only. The parser is `HEURISTIC_ONLY_LAST_LATIN_TOKEN`; no surname-effect inference is allowed.**

GitHub Actions run: `35275867080`

Artifact: `aris4c006-stratified-exposure-pilot`

## Sampling

Six fields were fixed prospectively for the pilot, 300 mainland-China (`CN`) affiliation works requested per field for 2024:

| OpenAlex field | ID | Eligible multi-author heuristic-parseable works |
|---|---:|---:|
| Economics, Econometrics and Finance | 20 | 294 |
| Mathematics | 26 | 280 |
| Business, Management and Accounting | 14 | 290 |
| Psychology | 32 | 294 |
| Medicine | 27 | 297 |
| Engineering | 22 | 300 |

## Main feasibility contrast: 3+ authors

Two-author lists are alphabetized by chance about half the time, so 3+ author teams are the more informative convention diagnostic.

| Field | N (3+) | Observed alphabetical* | Chance expectation | Excess alphabetical* | Mixed-international share |
|---|---:|---:|---:|---:|---:|
| Business/Management/Accounting | 244 | 10.25% | 6.60% | **+3.91%** | 59.84% |
| Economics | 262 | 9.54% | 6.66% | **+3.09%** | 54.58% |
| Mathematics | 251 | 7.97% | 5.69% | **+2.42%** | 54.58% |
| Engineering | 297 | 1.01% | 0.93% | **+0.08%** | 53.54% |
| Medicine | 289 | 1.04% | 1.39% | **−0.36%** | 57.44% |
| Psychology | 261 | 4.60% | 5.20% | **−0.64%** | 47.13% |

`*` heuristic surname parser; non-confirmatory.

## Interpretation

The goal was not to estimate a true alphabetization prevalence. It was to determine whether a preselected high/low field contrast can be extracted at adequate sample sizes and whether ordering above chance displays enough spread to justify building the real exposure estimator.

That gate passes.

The qualitative pattern is also directionally coherent with prior literature: Economics and Mathematics are established high-alphabetization fields, while contribution-order fields such as Medicine are much lower. This increases confidence that the extraction/classification pipeline is capturing meaningful convention heterogeneity rather than only noise.

## What this pilot does not establish

It does not establish:

- any causal surname effect;
- true field-specific alphabetization rates;
- whether a particular Chinese surname is advantaged/disadvantaged;
- career consequences;
- validity of the final-token surname heuristic;
- correctness of OpenAlex person-level author identities.

## Gate decision

**Moderator-variation feasibility: PASS.**

Next priority: validated Chinese surname parsing and OpenAlex author-identity error audit. Do not spend the next cycle merely scaling the heuristic pilot to more works.

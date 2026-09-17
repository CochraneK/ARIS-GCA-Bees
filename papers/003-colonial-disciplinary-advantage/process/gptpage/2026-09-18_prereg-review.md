# GPTPage preregistration adversary — 2026-09-18

Stage: researcher-degrees-of-freedom audit before contemporary outcome inspection

Execution mode: ChatGPT web/GPTPage handoff.

## Verdict

ARIS4C003 is conceptually mature enough to preregister, but **not yet safe to open the confirmatory outcome matrix**. The largest remaining analytic freedoms are the exact historical-exposure variable, the OpenAlex field crosswalk, the bibliometric time window, the specialization transformation, and low-volume handling.

The project should freeze one minimal primary specification and demote all alternative choices to named robustness analyses.

## Decision audit

| Decision point | Current ambiguity | Bias risk | Rule to freeze | Status |
|---|---|---|---|---|
| Former-colony exposure | duration vs ever-colonized vs colonizer identity | selecting exposure that fits outcome | choose one primary duration/relationship definition from one source family; others robustness | BLOCKING |
| Imperial-center exposure | several scale/intensity measures | specification search with only a few imperial centers | one descriptive primary intensity measure; small-N inference only | BLOCKING for Tier 2 |
| Continental/non-European empire scope | COLDAT excludes them; ICOW broader | changing sample after results | primary country-level duration analysis uses its source's explicit scope; broader empires separate prespecified extension | NEAR-FROZEN |
| Confirmatory disciplines | conceptual set now 21 fields | field cherry-picking | keep all 21 conceptual fields; no deletions because results are inconvenient | FROZEN |
| Discipline entanglement | 11 dimensions and 0–3 scale defined | outcome-informed scoring | complete blind evidence coding, second coding/adjudication before outcomes | BLOCKING |
| Database field mapping | conceptual fields may map to many OpenAlex topics | mapping can tune effect | freeze IDs/inclusion rules in crosswalk before country outcome extraction | BLOCKING |
| Main IKES aggregation | mean vs weighted/index variants | arbitrary weights | equal-weight mean is primary; median and leave-one-dimension-out only robustness | FROZEN |
| Publication counting | fractional vs full | internationally collaborative fields inflate countries | fractional attribution primary; full counting robustness | FROZEN |
| Bibliometric time window | many possible start/end years | select period with strongest legacy | choose one complete 4–5-year latest window plus prespecified earlier windows for persistence | BLOCKING |
| RCA transformation | raw RCA/log/symmetric RCA | skew/small denominators alter results | select one bounded symmetric/log transform based on metric properties before exposure merge | BLOCKING |
| Minimum output threshold | unspecified | small cells create extreme specialization | choose threshold from stability simulation/precision rule without exposure labels | BLOCKING |
| Citation outcome | MNCS/FWCI/top10/top1 | outcome shopping | one primary impact metric + top10 as secondary; top1 exploratory/robustness | BLOCKING |
| Network outcome | counts/share/centrality | many network metrics | normalized dyadic coauthorship intensity primary; centrality secondary | NEAR-FROZEN |
| Dyadic estimator | PPML vs NB/OLS | model shopping | choose based on prespecified count/zero structure diagnostics, without colonial coefficient inspection | BLOCKING |
| Common language | confounder vs mediator | coefficient interpretation changes | report nested models without and with language; do not select one based on significance | FROZEN |
| Country FE structure | country FE vs country-year FE | varying capacity can confound | repeated-window primary uses country-year FE + discipline-year FE where estimable | FROZEN |
| Small imperial-center inference | cluster SE/permutation/profile | pseudo-replication | no naive asymptotic cluster claims; effect/profile + leave-one-out + exact/permutation if justified | FROZEN |
| Ranking integration | three products differ | create supportive composite | never average into one master ranking; analyze separately | FROZEN |
| Small states | include/exclude | extreme ratios | threshold rule plus one prespecified small-state exclusion sensitivity | BLOCKING |
| Missing exposure/history | drop/impute | nonrandom missingness | no historical exposure imputation in primary analysis; report sample and missingness | RECOMMENDED FREEZE |
| Multiple testing | field-by-field results numerous | selective reporting | gradient interaction primary; full-field exploratory results all shown with FDR when p-values used | FROZEN |
| Leave-one-empire-out | which empires | selective robustness | run every eligible empire/colonizer systematically, not selected cases | FROZEN |
| Anglophone bias | many possible restrictions | post-hoc explanation | one predefined Anglophone/non-Anglophone split + coverage sensitivity | BLOCKING details |

## Minimal primary confirmatory specification recommended

### Analysis A — former-colony disciplinary specialization

- Sample: modern states with valid primary historical exposure and sufficient bibliometric coverage.
- Fields: all 21 frozen conceptual disciplines after fixed OpenAlex crosswalk.
- Exposure: one preregistered historical colonial-duration/dependency measure.
- Discipline moderator: adjudicated equal-weight IKES.
- Outcome: one prespecified transformed fractional-output specialization metric.
- Fixed effects: country×period and discipline×period.
- Main test: coefficient on `HistoricalExposure × IKES`.
- Uncertainty: cluster/multiway strategy must reflect country and field dependence; freeze after methods review/simulation.

### Analysis B — former-colonial dyadic collaboration

- Sample: country pairs with adequate publication mass.
- Exposure: direct former-colonial relationship.
- Moderator: IKES.
- Outcome: normalized fractional coauthorship intensity or count-offset formulation.
- Main model: gravity-style model with country-pair relevant fixed effects/controls; nested common-language specification.
- Main test: `FormerColonialTie × IKES`.

### Analysis C — imperial-center profile

- Small-N descriptive/exact corroboration only.
- No headline p-value based on treating every country×field observation as independent.

## Rules that prevent hindsight

1. The historical exposure table and discipline crosswalk receive version hashes before they are joined to contemporary outcome values.
2. IKES scores are committed before outcome extraction.
3. The first confirmatory model script is written to accept a synthetic/mock outcome dataset before real outcomes are loaded.
4. All deviations from preregistration receive a dated amendment with reason and whether any outcome was already viewed.
5. Exploratory full-field scans use separate files/output directories and are never silently promoted to confirmatory results.

## Recommended pre-analysis simulation

Before real OpenAlex outcomes, generate synthetic country×field×period data with realistic sparsity to choose:
- minimum publication threshold;
- transformation behavior;
- clustering/uncertainty strategy;
- estimator stability;
- ability to recover a planted exposure×IKES interaction.

Because synthetic data contain no real colonial effect, this step can safely resolve statistical engineering choices without outcome peeking.

## Gate result

**CONDITIONAL GO.**

The design can advance to historical IKES coding, database crosswalk, synthetic stability simulation, and source acquisition. The real confirmatory outcome matrix remains closed until the blocking decisions above are frozen.

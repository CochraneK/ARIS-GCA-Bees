# ARIS4C003 GATE-CLOSURE AUDIT

**Audit date:** 2026-09-18  
**Outcome state during audit:** contemporary confirmatory outcomes unopened.

This document does not replace `AUTO_REVIEW.md`. It records how the blocking
or material concerns raised there were handled before outcome inspection.

| Original concern | Closure / mitigation before outcomes | Residual limitation |
|---|---|---|
| Empire confounded with prior state/science capacity | Main estimand is within-country cross-disciplinary shape; country/period and discipline/period FE logic frozen in preregistration and model lock. | Associational path-dependence estimand; empire is not made exogenous. |
| Discipline selection can manufacture the result | D01–D21 set and OpenAlex crosswalk frozen; IKES rubric frozen; Coder A done; independent Coder B hard-gated. | Historical coding remains contestable and must be reported transparently. |
| Rankings reproduce prestige rather than capability | OpenAlex output/impact/network are the three headline outcomes; ranking products are secondary only. | Ranking layers retain provider/coverage/eligibility biases. |
| English/database coverage bias | Language/work-type/coverage diagnostics and prespecified language sensitivities are in the preregistration. | Indexed scholarship is not equivalent to all scholarship. |
| Colonial exposure is not one construct | Former-colony COLDAT duration, CEPII dyadic tie, and small-N imperial-center intensity are separated. COLDAT scope is explicitly European overseas colonialism. | Continental/informal empire is outside the primary estimand; ICOW remains robustness. |
| RCA instability / causal overinterpretation | PPML fractional counts with explicit zeros are primary; RCA/SRCA are descriptive. Small-output sensitivities are frozen. | Specialization remains a relative portfolio concept, not an economic structural parameter. |
| Strong FE changes estimand | Estimand explicitly stated as historical exposure covarying with contemporary disciplinary shape; no causal-treatment language from FE alone. | Discipline-specific omitted historical factors can remain. |
| Former-colony heterogeneity | No universal sign is hypothesized; pooled gradient is structural/descriptive and colonizer-specific analyses are secondary. | A single gradient can still mask heterogeneous pathways. |
| Post-treatment controls erase mechanisms | DAG/control review separates total historical association from capacity/mechanism analyses; modern GDP/R&D/language are not blindly added to the headline model. | Mechanism decomposition remains secondary and assumption-sensitive. |
| Novelty narrower than first assumed | Two targeted novelty sweeps explicitly identify RCA and colonial-collaboration precedents; claim narrowed to exposure × independently coded field-entanglement gradient across disciplines/outcomes. | Full systematic closest-prior-work search still required before submission. |
| Few discipline clusters | Two-way CRV1 is supplemented by 999 frozen IKES-label permutations and 21 leave-one-discipline-out fits. | Permutation is a falsification/sensitivity analysis, not randomized-treatment inference. |
| Small number of imperial centers | Imperial-center layer is explicitly N=8 corroboration with profile slopes, leave-one-empire-out and field-label permutation. | No large-N causal inference from metropoles. |
| Data/source drift | OpenAlex real S3 schema was probed outcome-blind; COLDAT and CEPII files are versioned/checksummed; source manifests are stored. | Public sources can change in future releases; provenance must be retained. |
| Temporal “persistence” not actually tested by a pooled coefficient | Amendment 003 freezes period-specific output/impact/dyad profiles for four mature windows plus 2023–25 output-only sensitivity. | Temporal profile remains observational and OpenAlex historical coverage changes over time. |
| IKES adjudication could become a hidden degree of freedom | Freeze code now forbids manual override of unflagged A/B cells; only missing or abs-difference >=2 cells can be adjudicated with notes. | Adjudication of flagged cells still requires historical judgment, so citations/reasons must be public. |

## Gate decision

### Design gate

**CLOSED / DESIGN_LOCKED.**

The model, field set, mapping, exposure definitions, outcome family, counting,
inference, time windows, and secondary temporal profile are fixed before
contemporary confirmatory outcomes.

### Historical/source gate

**CLOSED.**

- COLDAT country universe: 159 resolved current states.
- CEPII V202211: 12,561 complete unordered country pairs; 156 historical
  colonial/dependency ties.
- OpenAlex public-S3 schema: required frozen fields bind successfully.
- Raw/derived provenance and checksums are retained according to source terms.

### Independence gate

**OPEN / BLOCKING.**

A genuine fresh-context Coder B has not yet been supplied. This is deliberate:
the current ARIS context has seen Coder A and therefore cannot honestly serve as
the independent coder.

### Outcome gate

**LOCKED.**

No modern confirmatory country×discipline result may be materialized until the
independence gate is closed, adjudication is completed outcome-blind, and
`IKES_FROZEN.csv` plus provenance exist.

## No-rescue rule

After outcome unlock, null or inconvenient results do not permit:

- changing D01–D21 membership;
- changing primary OpenAlex selectors;
- reweighting IKES dimensions by observed fit;
- changing COLDAT/CEPII primary exposure definitions;
- selecting a different headline time period;
- promoting a QS/THE/Shanghai/Leiden result into the primary family;
- silently dropping failed period/permutation/LOO fits.

Any post-outcome change must be dated, labeled exploratory/sensitivity as
appropriate, and retain the original frozen analysis.

# GPTPage causal / DAG review — 2026-09-18

Stage: causal estimand and control-set review

Execution mode: ChatGPT web/GPTPage handoff.

## Core warning

ARIS4C003 is primarily a **historical path-dependence association study**, not a design that makes colonial exposure exogenous. Country and discipline fixed effects improve comparability but do not turn empire into a randomized treatment.

The paper should therefore separate three estimands rather than use one overloaded regression.

---

## Estimand A — total long-run historical association

Question:

> Is historical imperial/colonial exposure associated with the contemporary cross-disciplinary shape of national scientific specialization?

Conceptual DAG:

`pre-imperial state/scientific capacity → imperial expansion/exposure`

`pre-imperial state/scientific capacity → later universities/science → current outcomes`

`imperial expansion/exposure → institutions/networks/collections/languages → current outcomes`

For this estimand, modern GDP, R&D, university stock, English use, and international collaboration can be **mediators** rather than pure confounders. Controlling all of them would estimate a narrower direct association and may overcontrol the mechanism of interest.

Preferred design move: within-country cross-disciplinary interaction with country or country-year fixed effects, plus discipline or discipline-year fixed effects, rather than a giant covariate list.

Recommended language: "associated with persistent disciplinary specialization" / "consistent with long-run path dependence," not "caused by colonialism."

---

## Estimand B — association net of present-day scientific capacity

Question:

> Conditional on a country's present scientific resources and size, is historical exposure still associated with disproportionate strength in historically entangled fields?

Here modern variables such as total publication volume, R&D, tertiary education, or GDP may be useful descriptive controls, but they change the estimand. This should be presented as a robustness/decomposition analysis, not automatically as the "correct" model.

Recommended language: "the association is not fully explained by present-day aggregate scientific capacity."

---

## Estimand C — mechanism-specific persistence

### C1 prestige persistence

`historical exposure → reputation/institutional prestige → present ranking`

Control for contemporary bibliometric performance to ask whether prestige remains unusually high given current output/impact.

Potential outcome: ranking/reputation residual.

### C2 network persistence

`historical colonial tie → shared language/institutions/migration/funding → present coauthorship`

Shared language can be both a historical mediator and a modern proximity mechanism. Run models with and without language; interpret coefficient attenuation as decomposition, not as a universal confounding correction.

### C3 institution/human-capital pathway

`historical exposure → university/research-institute formation + specialist training → field-specific capacity → contemporary output`

Historical university/institute variables, if measured, should usually be treated as mediators/mechanism evidence rather than baseline confounders.

---

## Candidate variables by role

### Pre-exposure / historical confounding candidates

Hard to measure globally, but conceptually include:
- early modern state capacity;
- precolonial/early university/scientific institution stock;
- industrialization/printing/scientific society development;
- naval/military/commercial capacity;
- geography relevant to empire-building.

These are the hardest threat to causal interpretation and cannot be "solved" by modern GDP.

### Likely historical mediators

- colonial universities/research institutes;
- museums, collections, archives;
- field stations;
- professional societies/journals;
- language/education systems;
- researcher training traditions;
- migration/diaspora links;
- metropolitan funding relationships.

### Likely modern mediators / descendants

- R&D spending;
- university-system size;
- present international collaboration;
- English use in academia;
- funding ties;
- current research infrastructure.

### Outcomes

- relative output specialization;
- normalized citation/elite-paper performance;
- collaboration intensity/network structure;
- ranking/reputation/institutional position.

---

## Specific control recommendations

### GDP / GDP per capita
Do not mechanically include in every model. Use in a "net of contemporary capacity" specification and report how the historical interaction changes.

### R&D expenditure
Likely mediator of long-run institutional capacity; secondary decomposition/robustness control.

### University age / historic university stock
Potentially partly pre-exposure and partly a mediator depending date. Code temporally if used; do not collapse all universities into one modern stock variable.

### English/common language
For dyadic collaboration, run both without and with common-language controls. If colonial-tie coefficients shrink strongly, that is evidence that language is one persistence channel, not necessarily evidence against colonial legacy.

### Present international collaboration
Do not control for it when it is itself an outcome. It can be used in prestige decomposition only with clear temporal/conceptual justification.

### Region/geography
Reasonable robustness controls/dyadic gravity controls. Country fixed effects already absorb time-invariant country geography in the country×discipline model.

---

## Recommended model ladder

1. **Structural specialization model:** historical exposure × entanglement + country-year FE + discipline-year FE.
2. **Contemporary-capacity robustness:** add/select modern capacity interactions or stratifications, with changed estimand stated.
3. **Mechanism models:** network, prestige, historical-institution pathways analyzed separately.

Do not combine all three into one "fully controlled" regression and interpret the remaining coefficient as the only valid effect.

---

## Causal-language gate

Safe default manuscript language:

- predicts / is associated with;
- persistent pattern;
- consistent with historical path dependence;
- not fully explained by X (only when shown);
- evidence of network/prestige persistence.

Avoid without stronger identification:

- colonialism caused modern disciplinary advantage;
- empire increased field quality;
- colonization benefited/harmed scholarship by X units.

**Gate result:** GO after the manuscript explicitly distinguishes total association, net-of-current-capacity, and mechanism-specific estimands.

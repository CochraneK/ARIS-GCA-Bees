# SLEEPING BEAUTY / DELAYED RECOGNITION PROTOCOL — ARIS4C005

## Purpose

Study whether scientific-integrity failures can suppress or delay the recognition of legitimate high-potential research.

This module must not begin by counting hypothetical 'never-awakened discoveries.' It proceeds through identifiable layers.

---

## Layer SB0 — historical delayed recognition measurement

Use observed citation histories to compute:

- Beauty Coefficient B (Ke et al. 2015);
- citation-peak age t_m;
- awakening age t_a;
- awakening calendar year;
- complete observation-window length.

Ke et al. showed delayed recognition forms a continuous spectrum rather than a natural binary class. Therefore B is primary as a continuous variable.

Any top-x% Sleeping Beauty label is explicitly dataset-relative and exploratory.

---

## Beauty Coefficient

For annual citations c_t, t = 0 ... t_m, where t_m is the age at maximum annual citations:

l_t = ((c_tm - c_0) / t_m) * t + c_0

B = sum_{t=0}^{t_m} (l_t - c_t) / max(1, c_t)

If t_m = 0, define B = 0.

The implementation follows Ke, Ferrara, Radicchi & Flammini (PNAS 2015, DOI 10.1073/pnas.1424329112).

---

## Awakening time

Define perpendicular distance from annual citation point (t, c_t) to the reference line:

d_t = |(c_tm - c_0)t - t_m c_t + t_m c_0| / sqrt((c_tm - c_0)^2 + t_m^2)

Awakening age:

t_a = argmax_{t <= t_m} d_t

Ties must be resolved deterministically and documented.

---

## Layer SB1 — prospective awakening prediction

Goal:

> Using only information available by a frozen landmark age L, estimate the probability that a paper later enters a delayed-recognition state or awakens within horizon H.

Possible pre-landmark features:

- early citation trajectory;
- title/abstract semantic novelty;
- atypical concept combinations;
- interdisciplinarity/cognitive distance;
- author/network position;
- field growth;
- availability/open-access variables;
- independent semantic rediscovery signals measurable by the landmark.

Forbidden leakage:

- citations after landmark;
- future prince papers;
- future funding;
- future retraction/integrity outcomes;
- future network centrality;
- any final Beauty Coefficient computed using post-landmark citations as an input feature.

Historical awakened papers provide positives. Papers without enough follow-up are right-censored, not negatives.

---

## Layer SB2 — integrity exposure and awakening hazard

Once an awakening-risk model is calibrated, study whether pre-specified exposure to problematic science changes the hazard/probability of recognition.

Exposure examples:

- semantic proximity to adjudicated E1-S sources;
- attention competition from materially unreliable sources;
- funding/topic displacement around an integrity shock;
- citation-network paths through contaminated knowledge.

Primary comparison:

P(awakening | comparable pre-landmark features, high integrity exposure)

versus

P(awakening | comparable pre-landmark features, low integrity exposure).

Use matching/weighting/event-history methods with overlap and balance diagnostics.

---

## Layer SB3 — suppressed delayed-recognition opportunities

Only after SB1 + SB2 pass calibration/identification gates:

N_suppressed = sum_i [P_i(awake under low/no contamination) - P_i(awake observed exposure)]

Preferred label:

`estimated delayed-recognition opportunities suppressed`

Do not call this an observed count of 'true discoveries we lost.'

---

## Right censoring

A paper that has not awakened by the end of the database window may still awaken later.

Therefore:

- recent papers cannot be labelled never-awakened;
- awakening prediction/effect models must respect follow-up time;
- analyses should use landmarking, survival/event-history methods, or sufficiently mature cohorts.

---

## Corpus considerations

Historical precedent:

- Ke et al. applied B to more than 22 million WoS papers spanning over a century.
- Miura et al. later used ~73 million Scopus documents and ~1.2 billion citation links for large-scale Sleeping Beauty/Prince analysis.

ARIS4C005 can use OpenAlex for open reproducible implementation, but database-specific citation coverage and historical depth must be treated as measurement limitations.

---

## No-go rules

- Do not invent a natural B threshold; the distribution is continuous.
- Do not call recent dormant papers 'never-awakened.'
- Do not train on future information.
- Do not infer causal suppression from semantic proximity alone.
- Do not count all low-cited papers as lost discoveries.
- Do not add suppressed-opportunity counts to RLY or dollars.
- Do not claim a global buried-discovery count until calibration, censoring and causal exposure tests pass.

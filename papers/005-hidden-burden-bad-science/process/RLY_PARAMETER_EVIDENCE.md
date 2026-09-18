# RLY PARAMETER EVIDENCE — ARIS4C005

## Goal

Estimate Researcher-Life-Years (RLY) lost to severe scientific reliability failures without pretending that every dollar, review, citation, participant, or retracted paper can be converted into researcher time with one universal multiplier.

Primary decomposition:

RLY = production + downstream_misdirection + replication_correction + integrity_maintenance

Career spillover, participant sacrifice, funding exposure and innovation delay are reported separately unless a defensible time-conversion model is available.

---

## Component ontology

### RLY-P — production time

Researcher/staff time embedded in a scientifically unusable or severely unreliable work.

Do not automatically count the responsible actor's own time as 'victim youth.' Preferred reporting separates innocent coauthors/students/staff, intentional/culpable producer time, and unknown-role production time.

Current status: no defensible global hours-per-problematic-paper parameter. Keep uncalibrated.

### RLY-D — downstream misdirection

Time spent by later researchers because they materially depended on an unreliable source: failed follow-up experiments, invalid parameter choices, downstream analyses based on bad data/results, and avoidable replication attempts.

Requires semantic dependence (SCF), not raw citation count.

Current status: no global hours-per-material-dependence edge parameter. Keep uncalibrated.

### RLY-C — replication / correction

Time spent identifying, reproducing, investigating, correcting, retracting and repairing the scientific record.

Potential inputs include replication effort, institutional investigation effort, journal/editor correction effort, and post-publication forensic review.

Current status: component exists conceptually, but global time calibration is incomplete.

### RLY-I — integrity-maintenance labor

Peer-review/editorial/investigation time attributable to problematic submissions or published work.

Aczel et al. estimated over 100 million reviewer-hours globally in 2020, with the article discussion reporting over 130 million hours, roughly 15,000 researcher-years. This is a denominator for the size of the peer-review labor system, not the amount wasted on bad science.

Therefore global peer-review hours × bad-paper prevalence is forbidden unless the attributable fraction is independently estimated.

---

## Evidence anchors that must stay outside RLY totals unless converted validly

### Participant sacrifice

Yilmaz et al. found about 66,655 participants in completed but unpublished AD/MCI trials and 18,246 participants in unpublished discontinued trials.

This is E3 research waste, not fraud evidence. Report participant count, participant-hours if trial-level visit/time data are available, or risk-weighted participant exposure if a defensible clinical-risk metric is available. Do not convert participants into researcher-years.

### Career spillover

Hussinger & Pellens estimated an 8–9% citation penalty for uninvolved prior collaborators after a documented misconduct event.

This supports collateral career harm but does not directly equal years of lost career. Report separately as career-capital effects unless a validated citation-to-career-time model exists.

### Financial cost

Sandoval-Lentisco & Ioannidis (2026 preprint) attributed about $440M in 2026 dollars to 1,725 NIH-linked retracted articles, with a mean attributed cost around $255,087 per retracted NIH-funded article.

The same study reports $4.03B in associated investigator-held grants, but explicitly warns that associated grant totals are not equivalent to waste.

Money is not converted into RLY using salary division unless the grant/personnel structure is known.

### Historical misconduct-cost benchmark

Stern et al. (2014) estimated approximately $58M in direct NIH funding for retracted misconduct papers in their historical ORI/NIH cohort, with mean attributable direct cost around $392,582 per article in that sample.

Historical US biomedical context only.

---

## Primary RLY reporting rule

The dashboard/paper should show a vector:

(RLY-P, RLY-D, RLY-C, RLY-I)

with each component tagged EMPIRICALLY_CALIBRATED, PARTIALLY_CALIBRATED, SCENARIO_ONLY, or NOT_IDENTIFIED.

Do not collapse them into one empirical RLY total if overlap or calibration is unresolved.

---

## Scenario communication

If a component is scenario-only, it may be translated into intuitive equivalents such as 5-year PhD-equivalents or 40-year research-career equivalents.

The label must remain SCENARIO_NOT_EMPIRICAL_ESTIMATE.

Example: 1,000 RLY = 200 five-year PhD-equivalents is arithmetic communication, not a finding about actual PhD careers.

---

## Attribution rule

For every RLY component, the final model must identify:

1. exposure universe;
2. affected-unit count;
3. hours/years per affected unit;
4. attribution fraction to the integrity failure;
5. overlap with other components;
6. uncertainty distribution;
7. evidence source;
8. whether input is observed, modelled or scenario-only.

If any of items 1–6 are missing, the component cannot enter the empirical total.

---

## No-go rules

- Do not multiply total global R&D spending by a misconduct percentage.
- Do not multiply total peer-review hours by latent prevalence.
- Do not treat every citation as downstream wasted time.
- Do not count participant risk as researcher time.
- Do not convert citation penalties directly to career-years.
- Do not count whole associated grants as wasted.
- Do not add production time and grant-derived personnel time if they represent the same labor.

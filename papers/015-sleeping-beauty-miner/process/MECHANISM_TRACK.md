# ARIS4C015 Mechanism Track

Updated: 2026-09-18

## Core correction

A random historical cohort is appropriate for prospective evaluation, but it is
not guaranteed to contain any genuine Sleeping Beauty.

Therefore:

> A cohort-relative top-q delayed-recognition outcome is not itself a
> Sleeping Beauty diagnosis.

If a 20-paper random sample contains no genuine delayed-recognition event,
forcing the top 20% to be "positive" is useful only as a ranking smoke test. It
cannot support mechanism claims.

ARIS4C015 now separates three scientific tracks.

## Three-track architecture

### Track A — Retrospective identification

Question:

> Which papers show robust delayed-recognition trajectories?

Data:
- large retrospective citation corpus;
- complete annual citation histories;
- SciSciNet / SciSciNet-v2 / OpenAlex-derived trajectories.

Outputs:
- Beauty Coefficient;
- awakening time;
- van-Raan-style sleep/depth/wake criteria;
- source-calibrated B sensitivity;
- recognition floor;
- robust SB gate;
- candidate Prince papers.

Track A supplies cases to Track M.

### Track M — Mechanism discovery

Question:

> Why did some low-attention papers later awaken while otherwise comparable
> papers did not?

This track is case-enriched by design.

It starts from genuine/robust retrospective SB cases and builds matched controls.

It must never estimate prospective predictive accuracy from the enriched sample.

### Track B — Prospective rediscovery

Question:

> At historical cutoff T, could the system have surfaced papers before their
> later delayed recognition?

Data:
- random/reproducible historical cohorts;
- only evidence available at or before T.

Outputs:
- ranking metrics;
- calibration;
- lead time;
- human-review yield.

Track B is where prevalence and predictive claims are evaluated.

## Robust Sleeping Beauty gate

No single rule is treated as universally definitive.

The current mechanism gate requires converging evidence.

### Component 1 — Sleep / wake trajectory

Default mechanism settings:

- VARIABLE_SLEEP mode: scan admissible sleep lengths rather than forcing a
  single 5/10/15/20-year sleep;
- minimum sleep length: 5 years;
- primary sleep-depth profile: <= 2 citations/year, covering deep and
  less-deep literature variants;
- awakening window: 4 years immediately after the candidate sleep period;
- awakening intensity: > 5 citations/year;
- strict DEEP sensitivity: <= 1 citation/year;
- fixed s = 5/10/15/20 analyses remain available for literature replication.

The sleep length s is therefore an estimated/tunable trajectory dimension, not
a universal constant.

The original van Raan framework characterizes Sleeping Beauties by:

- depth of sleep;
- length of sleep;
- awakening intensity.

Different fields/studies have used different thresholds, so parameters must
always be reported.

### Component 2 — Beauty Coefficient

Use complete annual trajectories to calculate B.

For source-calibrated screening, SciSciNet v1 provides useful reference points:

- B > 33: approximately its top 2% SB group;
- B > 307.55: its top-10,000 high-B group.

These are SciSciNet-specific calibration values, not universal constants.

When another source is used, re-estimate the B distribution or report
cross-source sensitivity.

### Component 3 — Later recognition floor

A delayed trajectory that remains almost completely uncited is different from a
paper that later receives substantial scientific attention.

Current mechanism default:

- at least 50 total citations over the full observation window.

The primary gate includes both DEEP and LESS_DEEP profiles. A DEEP-only
(maximum 1 citation/year during sleep) subset is reported as a stricter
sensitivity analysis rather than treated as the only valid SB definition.

Sensitivity analyses should include:

- 30 / 50 / 100 total citations;
- field/cohort-normalized late citation percentile;
- top-q future uptake;
- Bcp / under-cited Sleeping Beauty alternatives.

### Default robust case

A paper enters the primary mechanism SB set only if all three default components
pass.

This strict gate is for mechanism enrichment, not for prospective candidate
ranking.

## Robust identity versus relative trajectory quadrant

ARIS4C015 treats these as two separate variables.

**Robust SB identity** is determined from the complete retrospective trajectory:
sleep depth/length, awakening intensity, B, and later-recognition floor.

**Relative trajectory quadrant** describes where the same paper sits compared
with its field × publication-year cohort on early and late attention.

The quadrant cannot veto a robust SB identity. This matters especially in old,
sparse cohorts: a paper can rank high on early citation percentile despite
having only a handful of early citations and then remaining dormant for
decades.

Both variables are retained for analysis.

## Four canonical trajectory states

Controls and descriptive quadrants are built from field × publication-year
normalized early/late attention.

### 1. SLEEPING_BEAUTY

- early attention <= 25th percentile, with exact zero attention always treated as low;
- late attention >= 75th percentile;
- robust retrospective SB gate passes.

### 2. FORGOTTEN

- early attention <= 25th percentile, with exact zero attention always treated as low;
- late attention <= 25th percentile, with exact zero attention always treated as low.

### 3. IMMEDIATE_HIT

- early attention >= 75th percentile;
- late attention >= 75th percentile.

### 4. FADING

- early attention >= 75th percentile;
- late attention <= 25th percentile.

Papers in the middle zones remain AMBIGUOUS and need not be forced into a
quadrant.

A low-early/high-late paper that fails the robust SB gate is explicitly labeled
LOW_EARLY_HIGH_LATE_UNCONFIRMED rather than automatically called a Sleeping
Beauty.

## Primary mechanism contrasts

### M1 — SB vs at-risk dormant control

Primary question:

> At the calendar time the SB awakens, what distinguishes it from a
> same-field/same-cohort paper that is still dormant at that time?

This is an event-time **risk-set comparison**.

For an SB with sleep length s:

- exact-match field and publication year;
- inspect each potential control only through age s for matching;
- require average citation rate through s to remain in the configured sleep
  regime;
- require no qualifying awakening burst at or before the case event time;
- allow the control to awaken later;
- match on sleep-rate distance, reference count and author count;
- do not use the control's post-event future outcome to select the match.

A paper that later becomes an SB is therefore allowed to serve as a control at
an earlier case's awakening time if it was still dormant then. This naturally
supports later survival / time-to-awakening analysis.

This is now the primary readiness contrast because it aligns the comparison
time and avoids defining controls as papers that must remain forgotten forever.

### M2 — SB vs Forgotten

Secondary/extreme contrast:

> Why did one later awaken while an extremely low-attention paper remained
> forgotten through the observation endpoint?

Forgotten controls remain useful for descriptive mechanism contrasts but are
often much more deeply uncited than robust SBs, so they are not required to be
the primary matched-control set.

### M3 — SB vs Immediate Hit

Both eventually receive high attention.

Question:

> Why was one recognized immediately while the other was delayed?

This comparison is useful for mechanisms of premature discovery / field
readiness / communication / network position.

Early citation level is intentionally not matched here because it is the
defining contrast.

### M4 — Immediate Hit vs Fading

Secondary comparison:

> What separates durable early attention from transient attention?

This helps distinguish delayed-recognition mechanisms from general citation
persistence.

## Mechanism families

### A. Premature-discovery / field-readiness mechanism

Test whether SB papers initially sit farther from the contemporaneous field but
become closer to a later-growing topic/community.

Candidate evidence:

- contemporaneous semantic distance;
- later semantic-neighborhood growth;
- required enabling technologies appearing later;
- emergence of terminology that makes the work searchable/relevant.

### B. Network-position mechanism

Compare early:

- bibliographic coupling;
- reference-network brokerage;
- core/periphery position;
- community membership;
- cross-community reference diversity.

Hypothesis:

Some SBs may contain useful knowledge while occupying weak diffusion pathways.

### C. Combination / novelty mechanism

Test:

- atypical reference combinations;
- previously rare concept/journal combinations;
- field-crossing references.

Important negative prior:

Existing large-scale SB–Prince work reports that delayed recognition is not
simply explained by rare cross-field combinations. Novelty must therefore be
tested, not assumed.

### D. Visibility / communication mechanism

Audit, rather than automatically reward:

- journal visibility;
- author network position;
- language/indexing coverage;
- abstract/title terminology;
- open availability.

Prestige is not intrinsic scientific value.

### E. Awakening-trigger mechanism

For each robust SB:

- identify candidate Prince papers around awakening;
- test direct citation;
- co-citation growth;
- semantic relation;
- community diffusion;
- technology/application events;
- review/guideline events where timestamped.

Do not force one Prince.

The literature supports first-citing-paper definitions, maximum co-citation
definitions, and multiple-Prince / no-single-Prince cases.

### F. Science-to-technology mechanism

Optional:

- patent citation preceding scientific awakening;
- clinical/standards use;
- software/method adoption.

This can reveal technology-first rediscovery.

## Matching architecture

The matching layer implements two related designs.

**Primary event-time risk set**
- exact field;
- exact publication year;
- control still dormant at the case awakening age;
- control may awaken later;
- nearest sleep-rate / reference-count / author-count matching;
- no use of post-event control outcomes during match selection.

**Secondary retrospective contrasts**
- SB vs Forgotten;
- SB vs Immediate Hit.

All matched designs report:
- match yield;
- unmatched cases;
- standardized mean differences for observed covariates;
- explicit balance failure.

A successful match is not automatically an acceptable mechanism comparison.
Hard calipers can be prespecified later as sensitivity analyses after empirical
support for a defensible threshold.

A later confirmatory analysis may use:

- propensity-score matching;
- coarsened exact matching;
- entropy balancing;
- risk-set matching for time-to-awakening.

But the first version remains transparent and auditable.

## Case enrichment is not prevalence estimation

The mechanism dataset intentionally contains many more SBs than a random sample.

Therefore do not report population prevalence or prospective predictive
performance from the mechanism cohort.

Those estimates belong to Track B or a separate population study.

## Large-corpus extraction strategy

### Preferred route: SciSciNet / SciSciNet-v2

SciSciNet provides precomputed Sleeping Beauty metrics for tens of millions of
papers and annual citation-derived B / awakening information.

Efficient two-stage extraction:

1. cheap prefilter using high SB_B, sufficient citations, and field/cohort;
2. reconstruct annual trajectories for candidates and controls;
3. apply robust SB gate;
4. construct four trajectory states within field/cohort;
5. match controls;
6. compute mechanism features.

This avoids reconstructing every expensive feature for hundreds of millions of
papers.

### OpenAlex route

OpenAlex is useful for identifiers, references, citing papers, metadata
enrichment, and bounded validation.

It is not the preferred method for repeatedly crawling the full citation graph
at global scale.

## Hard mechanism gate

The executable mechanism builder returns mechanism_ready = false if zero robust
SB cases are found.

When this occurs:

- do not estimate SB mechanisms;
- do not rename relative top-q cases as SBs;
- expand the corpus;
- inspect source coverage;
- run prespecified threshold sensitivity if scientifically justified.

This directly prevents a random no-SB sample from generating a fictional
mechanism analysis.

## Potential Sleeping Beauties

A fifth class may be used only prospectively:

POTENTIAL_SLEEPING_BEAUTY

This means:

- currently low attention;
- resembles historical pre-awakening SB evidence;
- has not yet demonstrated retrospective awakening.

It is never treated as ground-truth SB.

This is the final discovery target of the agent.

## End-to-end logic

LARGE RETROSPECTIVE CORPUS
-> ROBUST SB IDENTIFICATION
-> MATCHED FORGOTTEN / IMMEDIATE-HIT CONTROLS
-> MECHANISM / PRINCE ANALYSIS
-> HISTORICAL TIME-SAFE FEATURES
-> RANDOM PROSPECTIVE BACKTEST
-> NOT-YET-AWAKENED CANDIDATES

This separation is now a core ARIS4C015 invariant.

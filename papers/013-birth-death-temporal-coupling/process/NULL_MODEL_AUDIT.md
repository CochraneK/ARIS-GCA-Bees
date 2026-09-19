# Null-model audit · ARIS4C013 Pilot 1

## Audit question

Can the data-cleaning or null-model design itself create or erase an apparent birthday effect?

This audit was performed before any population-scale administrative coupling result was available.

## Finding 1 · exact-age boundary selection can manufacture a large effect

Suppose birth and death month/day are independently and uniformly distributed over a 365-day calendar, with a fixed year difference of 18.

If we then require attained age >=18, inclusion becomes:

- included when death month/day is on or after birth month/day;
- excluded when death month/day is before birth month/day.

So inclusion depends directly on the phase being tested.

Enumerating all 365 × 365 equally likely month/day pairs:

- observed eligible offset-0 pairs: 365;
- expected offset-0 under the marginals of the selected sample: about 122.33;
- artificial O/E: about **2.9837**.

No biological, psychological, or cultural birthday mechanism exists in this toy example.

### Correction

Use a year-gap range for which every month/day pairing is eligible. For the intended adult range, year gaps 19–110 imply attained ages 18–110 for every valid month/day pairing.

## Finding 2 · birth decade is unnecessarily coarse

A birth-decade × death-year × sex null preserves broad cohort composition but can mix:

- different exact birth cohorts;
- different attained-age mixtures;
- changing seasonal fertility patterns;
- secular changes in date recording.

With tens of millions of records, these small compositional differences matter.

### Correction

Primary null:

**exact birth year × death year × sex**

Sensitivity null:

**birth decade × death year × sex**

The coarse v1 null remains visible so robustness to stratification resolution can be assessed.

## Finding 3 · conditioning on exact attained age is not an acceptable “fix”

It might seem attractive to stratify or condition on exact age at death. But exact age is itself determined by whether death occurs before or after the birthday in the death year.

Conditioning on a variable partly defined by the tested birth–death phase can induce or distort the association.

Therefore Pilot 1 controls cohort using birth year and death year, not exact attained age.

## Finding 4 · the analytic marginal-independence expectation is directionally correct

For offset k, the expected count within a stratum is:

[
E_k = rac{1}{N}sum_d B_d D_{(d+k)mod365},
]

where B and D are the observed birth- and death-phase marginals.

The implementation uses the equivalent circular cross-correlation. Expected counts sum to N across all 365 offsets.

## Finding 5 · date heaping remains a separate threat

Even with a correct phase-safe sample and exact-year null, correlated imputation can create offset-0 spikes. Hence the prespecified raw/strict comparison remains necessary:

- birth heaping days: 1, 15;
- death heaping days: 1, 4, 15.

The Wikidata Pilot 0A already demonstrated that correlated low-precision dates can create enormous false coupling.

## Outcome

**Pilot 1 lock upgraded from v1 to v2 before administrative outcome access.**

The v2 design is less vulnerable to:
- boundary-selection artifacts;
- coarse cohort mixing;
- significance-only interpretation.

The untouched 1997–2005 holdout remains unopened.

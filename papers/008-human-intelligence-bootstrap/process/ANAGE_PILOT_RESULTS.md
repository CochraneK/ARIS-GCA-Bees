# AnAge pilot extraction · ARIS4C008

**Source:** AnAge stable bulk dataset (`dataset.zip`) from Human Ageing Genomic Resources, accessed 2026-09-18.

## Extraction

The bulk file contained **4,645 rows** in the fetched stable build. Matching against the 008 seed panel plus explicit genus/family exemplars produced **24 species rows**.

The normalized extract is stored at `data/anage_pilot_summary.csv`.

## What this adds

For matched taxa, AnAge contributes a source-curated life-history layer including some combination of:

- female and male maturity age;
- gestation/incubation;
- weaning;
- litter/clutch size;
- interbirth interval;
- adult weight;
- maximum longevity;
- metabolic rate/body mass where present;
- temperature;
- AnAge data-quality flag.

## Scope rules

Exact-species records are marked `exact_species`.

The following are retained only as explicit exemplars:
- `Pongo pygmaeus` for the pilot label `Pongo spp.`;
- `Gorilla gorilla` for `Gorilla spp.`;
- `Macaca fuscata` for `Macaca spp.`;
- `Callithrix jacchus` and `Leontopithecus rosalia` for `Callitrichidae`;
- `Tursiops aduncus` appears as a genus exemplar alongside an exact `T. truncatus` row.

No exemplar value should be promoted to an exact-species measurement in confirmatory analysis.

## Data-quality warning

The source's own `Data quality` field is retained. For example, the extracted Goffin's cockatoo entry is marked **questionable**, so its longevity/body-mass row should not be used uncritically.

## Immediate biological design implication

Life-history variation is large even among cognitively interesting taxa. The matrix now contains contrasts such as:

- very long maximum longevity and delayed maturity in whales, elephants and great apes;
- comparatively short life histories in social insects;
- socially complex/culturally interesting birds with intermediate-to-long recorded longevity;
- teaching in meerkats despite a much shorter life history than great apes.

These are exactly the dissociations needed to test whether a long learning window is necessary, merely enabling, or only useful in interaction with other modules.

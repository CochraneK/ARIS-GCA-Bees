# EltonTraits ecology layer · ARIS4C008

EltonTraits 1.0 was parsed from its original bird and mammal tab-separated files.

## Coverage

- birds in source file: ~9,995 rows in the retrieved table;
- mammals in source file: ~5,403 rows;
- current 008 species matched: **26 / 29**.

Mapping:
- 24 current names match directly;
- `Cebus libidinosus` is explicitly reconciled to `Sapajus libidinosus`;
- `Physeter catodon` is explicitly reconciled to `Physeter macrocephalus`.

The three uncovered v2 taxa are all outside EltonTraits' bird/mammal scope:
- Octopus vulgaris;
- Bombus terrestris;
- Apis mellifera.

## Module I contribution

The extract supplies cross-species ecological indicators including:
- proportional diet categories;
- foraging stratum;
- activity timing;
- body mass;
- source certainty fields.

These are **ecological challenge/opportunity variables**, not intelligence indicators.

A highly extractive or omnivorous diet may provide opportunities for cognition, but the direction and form of effect must be tested rather than assumed.

## Harmonization cautions

Bird and mammal source schemas differ:
- birds encode foraging strata as percentage allocations;
- mammals use categorical foraging-stratum codes;
- activity fields differ;
- source certainty conventions differ.

Therefore the raw source fields are preserved. Cross-clade derived indices require a documented transformation layer rather than direct column pooling.

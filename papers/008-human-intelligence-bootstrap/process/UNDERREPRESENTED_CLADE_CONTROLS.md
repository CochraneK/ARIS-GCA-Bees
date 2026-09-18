# AnimalTraits underrepresented-clade calibrations · ARIS4C008

AnimalTraits v1.0.7 was screened for species absent from the existing ACDB/ASNR/current-panel screening pool.

## Deterministic selection rule

For each underrepresented class available in this AnimalTraits release:

1. exclude every species already in the screening pool;
2. count observation records for body mass, brain size and metabolic rate;
3. rank first by the number of distinct measured trait axes;
4. then by bounded measurement-record abundance;
5. retain the top three species.

This yielded **15 calibration taxa**:
- Amphibia: 3;
- Reptilia: 3;
- Insecta: 3;
- Arachnida: 3;
- Malacostraca: 3.

The retrieved AnimalTraits table did not supply comparable Actinopterygii or Cephalopoda candidates under this rule, so those clades are not artificially filled from a different measurement system.

## Interpretation

These are **data-rich calibration taxa**, not low-intelligence animals and not biological negatives.

Their purpose is to:
- broaden clade coverage;
- make energetic/neural scaling contrasts less bird/mammal-centric;
- supply low-cost H/body-size constraints;
- provide potential counterexamples before expensive behavioral coding.

Any A–F behavioral state remains unknown until independently evidenced.

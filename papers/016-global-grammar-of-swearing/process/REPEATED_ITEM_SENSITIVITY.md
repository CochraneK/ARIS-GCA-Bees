# ARIS4C016 Repeated-Item Sensitivity and Filler Control

Updated: 2026-09-19

## Why this analysis matters

The primary repeated-item model found modest English-community effects after
lexical-item fixed effects:

- tabooness partial R² = .0265;
- offensiveness partial R² = .0361.

Two questions remain:

1. Are these results driven by the unbalanced pattern in which some lexical
   items occur in only 2–4 of the five English communities?
2. Are the community effects specific to taboo judgements, or do they also
   appear for ordinary filler words and general psycholinguistic ratings?

We therefore reran the same pure-Python FWL item-fixed-effects diagnostic on:
- the balanced subset of taboo items observed in **all five** English
  communities;
- shared **filler** items as a negative-control class.

## Balanced five-community taboo subset

Only 23 taboo items are present in all five English samples, yielding 115
item-community observations.

| Dimension | Community partial R² | Item-bootstrap 95% interval |
|---|---:|---:|
| Tabooness | .0537 | .0273–.1941 |
| Offensiveness | .0532 | .0128–.2373 |
| Valence | .0691 | .0258–.2418 |
| Arousal | .1293 | .0593–.2941 |
| Concreteness | .3591 | .2135–.5438 |
| Age of acquisition | .2515 | .1337–.4617 |

The taboo-specific effects remain non-zero and are somewhat larger than in the
139-item primary set, but the uncertainty intervals widen sharply because the
balanced subset is small.

Therefore the balanced analysis supports robustness of the qualitative result
but does not justify a more precise or larger-effect claim.

## Filler negative control

For non-taboo filler words, only 35 lexical items are shared by at least two
English communities, yielding 73 item-community observations. No filler item
is shared by all five communities.

| Dimension | Community partial R² | Item-bootstrap 95% interval |
|---|---:|---:|
| Tabooness rating | .2965 | .1192–.6154 |
| Offensiveness rating | .1583 | .0209–.4712 |
| Valence | .2021 | .0719–.4994 |
| Arousal | .2404 | .0940–.5431 |
| Concreteness | .2129 | .0682–.4600 |
| Age of acquisition | .1933 | .0561–.4785 |

These estimates are much larger than the primary taboo-word community effects,
but the filler control is sparse and its intervals are wide.

## Interpretation

This is an important **negative-control result**.

The observed community effect in taboo ratings cannot currently be interpreted
as a taboo-specific cultural signal, because community-associated differences
are at least as visible—and in this sparse control set substantially
larger—for filler words and general lexical ratings.

Plausible contributors include:
- participant composition;
- site-specific use of rating scales;
- procedural calibration;
- dialect/register;
- lexical sampling;
- aggregation/reliability differences;
- broader community differences in semantic judgements.

The result therefore strengthens the paper's measurement-first argument.

## What this does *not* show

It does not show that taboo culture is irrelevant.

The filler design is weaker than the taboo design:
- only 35 shared filler items;
- only 73 observations;
- no balanced all-five-community filler subset;
- filler words were not constructed as a purpose-built matched control sample
  for this analysis.

Therefore the correct conclusion is:

> A community main effect exists, but the current data do not establish that
> it is specific to taboo language.

## Consequence for the confirmatory design

The next repeated-item model should test a **difference-in-community-effect**
question rather than community effects in isolation.

Preferred future design:
1. matched taboo and neutral items;
2. identical community coverage;
3. comparable frequency, length and lexical class;
4. participant-level or reliability-weighted ratings;
5. explicit taboo-status × community interaction;
6. item and participant hierarchical effects.

Until then, the English repeated-item analysis is evidence for
**context-sensitive ratings**, not direct evidence for a cultural taboo effect.

## Reproducibility

Code:
`code/repeated_item_sensitivity.py`

The script:
- downloads the checksum-verified public Study-2 CSV;
- emits aggregate statistics only;
- never prints taboo lexical items.

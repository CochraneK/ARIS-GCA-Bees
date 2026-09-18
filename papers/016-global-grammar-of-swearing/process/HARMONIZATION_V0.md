# ARIS4C016 Harmonization v0

Updated: 2026-09-18

## Goal

Test how much of the source annotation can be harmonized **without** forcing
local/ambiguous labels into a global scheme.

The rule set is deliberately conservative and lives in
`code/harmonize_labels.py`.

## Overall coverage

Across Study 1:
- 10,918 non-empty category-label occurrences across category/category2/category3;
- 8,778 label occurrences mapped by high-confidence rules;
- **80.4% label-occurrence coverage**;
- 38 distinct normalized labels remain unresolved.

This does **not** mean 80.4% of lexical rows are globally comparable, because
some samples have many rows with no category annotation at all.

## Row-level mapped coverage by sample

Selected examples:
- Cantonese (CN): 98.4%;
- English (CA): 92.9%;
- Finnish (FI): 94.7%;
- Serbian (RS): 94.7%;
- Thai (TH): 92.9%;
- English (AU): 74.8%;
- Mandarin (CN): 76.8%;
- Setswana (BW): **32.4%**;
- Spanish (ES): **18.4%**.

The last two are low because large fractions of their Study-1 rows have no
primary category annotation.

## Why unresolved labels are retained

The most common unresolved label is `slur`.

This is intentional. A slur is not a semantic source comparable to "sexual"
or "scatological"; it usually encodes a socially targeted derogatory function
whose identity basis cannot safely be inferred from the label alone.

Other unresolved labels include broad judgements such as:
- negative condition;
- behavioral;
- abuse;
- slang;
- moral;
- bodypart;
- local abbreviations and community-specific labels.

These require native/context review or a more explicit mapping rule.

## Allowed automatic operations

v0 automation may:
- lowercase/trim labels;
- repair a very small set of obvious spelling variants;
- map unambiguous semantic-source labels;
- map a few unambiguous pragmatic labels;
- map explicit social-indexical labels;
- mark euphemism as a form property.

v0 automation may **not**:
- infer identity group from an English gloss;
- infer pragmatic function from a lexical form alone;
- classify `slur` into a protected/social group without evidence;
- fill missing category annotations;
- turn unresolved local labels into `OTHER` merely to increase coverage.

## Confirmatory-analysis rule

Semantic-domain prevalence comparisons must report, per sample:
1. mapped-row coverage;
2. unresolved-row share;
3. missing-category share;
4. sensitivity to excluding low-coverage samples.

No "country has more X taboo" claim is allowed when the apparent difference
could plausibly be explained by annotation coverage.

## Next gate

Construct a stratified human/native-speaker audit set that over-samples:
- unresolved high-frequency labels;
- samples with low row-level coverage;
- items with conflicting/multiple source labels;
- same-word English/Spanish items showing high cross-community rating
  disagreement.

The purpose is not to maximize automatic coverage, but to estimate mapping
error and identify which axes are actually comparable.

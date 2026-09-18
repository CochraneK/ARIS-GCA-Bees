# Pilot 0A Source Note · Wikidata biographies

## Snapshot
Third-party repository: `dalager/wikidata-incarnations`.

The repository documents a 2024-01-01 Wikidata dump extraction of 2,953,301 humans with:
`id,P569,P570,P27,label,sitelinks`.

Its extraction command keeps the first P569 and P570 claims after simplifying Wikidata entities.

## What this source can establish
- whether the ARIS4C013 circular-time pipeline works at multi-million-record scale;
- whether obvious date-heaping artifacts can create apparent birth–death coupling;
- whether a birthday-window signal is robust to simple precision safeguards.

## What this source cannot establish
- population-level mortality risk;
- causal effects of birth timing;
- Bazi validity;
- representative effects for any country or historical cohort.

## Precision limitation
The slim CSV does not retain Wikidata `timePrecision`. Therefore all day-level analyses are explicitly provisional. The pipeline requires valid month/day syntax and reports sensitivity analyses excluding day-of-month 1, but that cannot recover missing precision metadata.

## Confirmatory role
None. Pilot 0A is a methods/feasibility and artifact-detection exercise. Confirmatory analysis requires an administrative or registry dataset with explicit date precision and a sampling frame.

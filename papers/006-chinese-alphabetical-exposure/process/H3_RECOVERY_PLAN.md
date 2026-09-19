# H3 preoutcome recovery plan — ARIS4C006

Frozen recovery decision: 2026-09-19

## Trigger

Original outcome-blind H3 structural-cohort run:

- workflow run: `35424798137`
- head commit: `e60c1c4a9dcf897a43a8ed022f4a2817d62fe273`
- build shards requested: 64
- successful build shards: 53
- cancelled at the 50-minute job limit: **11**
- aggregate job itself completed, but the original run did not provide a complete 64-shard cohort.

Missing shard IDs are frozen from the GitHub Actions job record:

`7, 11, 14, 17, 35, 47, 49, 50, 57, 60, 63`

## Why recovery may use the current builder

After the original H3 run was launched, commit `29b162aa6f1a0223389b4796483b0887b53ec7e3` changed the H3 builder only to batch canonical-author metadata resolution. Sampling, entry-cohort, identity, exposure and structural-eligibility rules were explicitly unchanged.

Recovery therefore uses the current builder for **only the 11 missing shards**, while reusing the 53 immutable successful artifacts from run `35424798137`.

This is an engineering recovery, not a design amendment.

## Frozen recovery invariants

- source convention/primary-frame artifacts remain from run `35424125236`;
- shard count remains 64;
- author-to-shard hash rule remains unchanged;
- `author_batch_size=20` remains unchanged;
- entry years remain 2014–2020;
- no Persistence5 outcome may be opened during recovery;
- no H3 effect or p-value may be computed during recovery;
- all structural thresholds in the preregistration remain unchanged;
- the recovered aggregate must contain **exactly 64 H3 shard manifests** before structural PASS can be accepted.

## Structural gate

The existing frozen thresholds remain:

- validated entry authors >= 1,000;
- final H3 eligible preoutcome authors >= 750;
- all seven entry years 2014–2020;
- >=20 entry primary fields;
- >=100 ORCID-anchored final authors;
- >=500 low-identity-risk final authors.

If the complete 64-shard aggregate fails, H3 is removed from the confirmatory secondary family. Thresholds must not be relaxed.

## Next gate

Only if the complete 64/64 outcome-blind structural aggregate passes may `36_open_h3_persistence.py` open Persistence5 under the existing preregistration lock/unlock.

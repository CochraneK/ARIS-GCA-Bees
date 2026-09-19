# ARIS4C015 SQL

Executable query templates for the large-corpus Mechanism Track.

Run order:

1. `sciscinet_v2_schema_discovery.sql`
2. `sciscinet_v2_sb_candidate_counts.sql`
3. `sciscinet_v2_sb_prefilter.sql`

Do not skip schema discovery. SciSciNet-v2 is rebuilt on OpenAlex and v1 column
names must not be assumed to survive unchanged.

The B thresholds in these exploratory queries are source-calibration references,
not universal Sleeping Beauty definitions.

After export:
- reconstruct annual citation trajectories;
- run `mechanism_cohort_cli.py`;
- require robust SB cases;
- require SB-vs-Forgotten match yield and SMD balance before mechanism analysis.

Canonical design:
- `../process/MECHANISM_TRACK.md`
- `../process/SCISCINET_MECHANISM_QUERY.md`

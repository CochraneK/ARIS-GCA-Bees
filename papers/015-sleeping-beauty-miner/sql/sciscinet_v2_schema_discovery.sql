-- ARIS4C015 SciSciNet-v2 schema discovery
-- Run before assuming v1 metric names exist unchanged in v2.

SELECT
  table_name,
  column_name,
  data_type
FROM
  `ksm-rch-scisciturbo.sciscinet_v2.INFORMATION_SCHEMA.COLUMNS`
WHERE
  table_name IN (
    'sciscinet_papers',
    'sciscinet_paperreferences',
    'sciscinet_paperdetails'
  )
  AND LOWER(column_name) IN (
    'paperid',
    'year',
    'sb_b',
    'sb_t',
    'c3',
    'c5',
    'c10',
    'cited_by_count',
    'citation_count',
    'reference_count',
    'author_count'
  )
ORDER BY
  table_name,
  column_name;

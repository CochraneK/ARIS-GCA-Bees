-- ARIS4C015 retrospective mechanism-candidate count probe
--
-- IMPORTANT:
--   B > 33 is a SciSciNet-v1 calibration reference, not a universal v2
--   threshold. Use this query only after schema discovery confirms SB_B.
--   This is Track M retrospective enrichment, never a prospective feature.

SELECT
  year,
  COUNT(*) AS n_papers,
  COUNTIF(SB_B > 33) AS n_b_gt_33,
  COUNTIF(SB_B > 307.55) AS n_b_gt_307_55
FROM
  `ksm-rch-scisciturbo.sciscinet_v2.sciscinet_papers`
WHERE
  year BETWEEN 1970 AND 1995
GROUP BY
  year
ORDER BY
  year;

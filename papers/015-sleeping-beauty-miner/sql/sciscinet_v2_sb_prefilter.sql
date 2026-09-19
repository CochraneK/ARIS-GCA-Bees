-- ARIS4C015 cheap retrospective SB prefilter
--
-- Do NOT label output rows SLEEPING_BEAUTY yet.
-- The exported candidates must still pass complete trajectory reconstruction,
-- variable-sleep depth/wake gating, source-calibrated B sensitivity, and the
-- later-recognition floor.

SELECT
  paperid,
  year,
  SB_B,
  SB_T,
  C3,
  C5,
  C10
FROM
  `ksm-rch-scisciturbo.sciscinet_v2.sciscinet_papers`
WHERE
  year BETWEEN 1970 AND 1995
  AND SB_B > 33
ORDER BY
  SB_B DESC;

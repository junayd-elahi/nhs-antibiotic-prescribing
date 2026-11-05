SELECT COUNT(*)
FROM(
SELECT
  scores.PRACTICE_CODE,
  COUNT(*) AS high_months,
  AVG(ratio) AS avg_ratio
FROM scores
WHERE ratio > 1.5
GROUP BY scores.PRACTICE_CODE
)
WHERE high_months = 24
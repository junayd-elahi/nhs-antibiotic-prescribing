SELECT
  scores.PRACTICE_CODE,
  MAX(PRACTICE_NAME) AS practice_name,
  COUNT(*) AS high_months,
  AVG(ratio) AS avg_ratio
FROM scores
WHERE ratio > 1.5
GROUP BY scores.PRACTICE_CODE
HAVING COUNT(*) = 24
ORDER BY avg_ratio DESC
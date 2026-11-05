CREATE OR REPLACE VIEW scores AS
SELECT month,
       PRACTICE_CODE,
       PRACTICE_NAME,
       items_per_1000,
       AVG(items_per_1000) OVER (PARTITION BY month) AS month_avg,
       items_per_1000 / month_avg AS ratio
FROM rates
WHERE PRACTICE_CODE NOT LIKE 'Y%';
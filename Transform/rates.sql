CREATE OR REPLACE VIEW rates AS
SELECT a.month,
       a.PRACTICE_CODE,
       a.PRACTICE_NAME,
       a.ICB_CODE,
       a.items,
       l.list_size,
       a.items * 1000.0 / l.list_size AS items_per_1000
FROM raw.epd_antibiotics a
JOIN raw.practice_list_sizes l
  ON a.PRACTICE_CODE = l.PRACTICE_CODE
 AND a.month = l.month
WHERE l.list_size >= 1000;
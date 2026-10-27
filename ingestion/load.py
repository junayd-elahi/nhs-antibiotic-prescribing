import sys
from ingestion.nhsbsa import run_query
from ingestion.db import connect

def fetch_month(month: str):
    resource = f"EPD_SNOMED_{month}"
    sql = f"""
        SELECT YEAR_MONTH, PRACTICE_CODE, PRACTICE_NAME, ICB_CODE, ICB_NAME,
               SUM(ITEMS) AS items, SUM(ACTUAL_COST) AS actual_cost
        FROM `{resource}`
        WHERE BNF_PRESENTATION_CODE LIKE '0501%'
        GROUP BY YEAR_MONTH, PRACTICE_CODE, PRACTICE_NAME, ICB_CODE, ICB_NAME
    """
    df = run_query(resource, sql)
    if df.empty:
        raise RuntimeError(f"No rows returned for {month}")
    return df

def load_month(month: str) -> int:
    df = fetch_month(month)
    with connect() as con:
        con.execute("CREATE SCHEMA IF NOT EXISTS raw")
        con.execute("CREATE TABLE IF NOT EXISTS raw.epd_antibiotics AS SELECT * FROM df LIMIT 0")
        con.execute("DELETE FROM raw.epd_antibiotics WHERE YEAR_MONTH = ?", [int(month)])
        con.execute("INSERT INTO raw.epd_antibiotics SELECT * FROM df")
    return len(df)

if __name__ == "__main__":
    month = sys.argv[1]
    print(month, load_month(month), "rows")
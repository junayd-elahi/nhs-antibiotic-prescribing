import sys
from ingestion.nhsbsa import run_query
from ingestion.db import connect

def bnf_column(resource: str) -> str:
    columns = run_query(resource, f"SELECT * FROM `{resource}` LIMIT 1").columns
    for name in ["BNF_PRESENTATION_CODE", "BNF_CODE"]:
        if name in columns:
            return name
    raise RuntimeError(f"No BNF code column in {resource}")

def fetch_month(month: str):
    resource = f"EPD_SNOMED_{month}"
    bnf = bnf_column(resource)
    sql = f"""
        SELECT '{month}' AS month, PRACTICE_CODE, PRACTICE_NAME, ICB_CODE, ICB_NAME,
               SUM(CAST(ITEMS AS INT64)) AS items, SUM(CAST(ACTUAL_COST AS FLOAT64)) AS actual_cost
                       FROM `{resource}`
        WHERE {bnf} LIKE '0501%'
        GROUP BY PRACTICE_CODE, PRACTICE_NAME, ICB_CODE, ICB_NAME
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
        con.execute("DELETE FROM raw.epd_antibiotics WHERE month = ?", [month])
        con.execute("INSERT INTO raw.epd_antibiotics SELECT * FROM df")
    return len(df)

if __name__ == "__main__":
    month = sys.argv[1]
    print(month, load_month(month), "rows")
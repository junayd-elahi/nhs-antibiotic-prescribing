import requests
import pandas as pd

URL = "https://opendata.nhsbsa.net/api/3/action/datastore_search_sql"

def run_query(resource: str, sql: str) -> pd.DataFrame:
    response = requests.get(URL, params={"resource_id": resource, "sql": sql})
    response.raise_for_status()
    body = response.json()
    if not body["success"]:
        raise RuntimeError(body["error"])
    return pd.DataFrame(body["result"]["result"]["records"])

def icb_counts(month: str) -> pd.DataFrame:
    resource = f"EPD_SNOMED_{month}"
    sql = f"""
        SELECT , ______, COUNT(*) AS n_rows
        FROM `{resource}`
        WHERE BNF_PRESENTATION_CODE LIKE '0501%'
        GROUP BY ______, ______
        ORDER BY n_rows DESC
    """
    return run_query(resource, sql)


for month in ["202608", "202508"]:
    df = icb_counts(month)
    print(month, len(df), "ICBs")
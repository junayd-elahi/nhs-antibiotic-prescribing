import requests
import pandas as pd

URL = "https://opendata.nhsbsa.net/api/3/action/datastore_search_sql"

def run_query(resource: str, sql: str) -> pd.DataFrame:
    response = requests.get(URL, params={"resource_id": resource, "sql": sql})
    if not response.ok:
        raise RuntimeError(f"{response.status_code}: {response.text}")
    body = response.json()
    if not body["success"]:
        raise RuntimeError(body["error"])
    return pd.DataFrame(body["result"]["result"]["records"])
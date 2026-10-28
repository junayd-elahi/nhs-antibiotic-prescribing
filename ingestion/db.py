from pathlib import Path
import duckdb

DB_PATH = Path(__file__).resolve().parents[1] / "data" / "nhs.duckdb"

def connect() -> duckdb.DuckDBPyConnection:
    DB_PATH.parent.mkdir(exist_ok=True)
    return duckdb.connect(str(DB_PATH))

def replace_month(table: str, month: str, df: pd.DataFrame) -> None:
    with connect() as con:
        con.execute("CREATE SCHEMA IF NOT EXISTS raw")
        con.execute(f"CREATE TABLE IF NOT EXISTS {table} AS SELECT * FROM df LIMIT 0")
        con.execute(f"DELETE FROM {table} WHERE month = ?", [month])
        con.execute(f"INSERT INTO {table} SELECT * FROM df")

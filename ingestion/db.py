from pathlib import Path
import duckdb

DB_PATH = Path(__file__).resolve().parents[1] / "data" / "nhs.duckdb"

def connect() -> duckdb.DuckDBPyConnection:
    DB_PATH.parent.mkdir(exist_ok=True)
    return duckdb.connect(str(DB_PATH))
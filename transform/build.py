from pathlib import Path
from ingestion.db import connect

SQL_DIR = Path(__file__).parent
VIEWS = ["rates.sql", "scores.sql"]

if __name__ == "__main__":
    with connect() as con:
        for name in VIEWS:
            con.execute((SQL_DIR / name).read_text())
            print("built", name)
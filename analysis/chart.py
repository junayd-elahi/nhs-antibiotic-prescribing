from pathlib import Path
import matplotlib.pyplot as plt
import pandas as pd
from ingestion.db import connect

PRACTICE = "C83614"
OUT = Path(__file__).resolve().parents[1] / "docs" / "sutterton_vs_national.png"

def fetch() -> pd.DataFrame:
    with connect() as con:
        df = con.execute("""
            SELECT month, items_per_1000, month_avg
            FROM scores
            WHERE PRACTICE_CODE = ?
            ORDER BY month
        """, [PRACTICE]).df()
    if df.empty:
        raise RuntimeError(f"No rows for {PRACTICE}, run transform.build first")
    df["month"] = pd.to_datetime(df["month"], format="%Y%m")
    return df

def plot(df: pd.DataFrame) -> None:
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(df["month"], df["items_per_1000"], label="Sutterton Surgery")
    ax.plot(df["month"], df["month_avg"], label="National average")
    ax.set_ylabel("Antibiotic items per 1,000 patients")
    ax.set_title("Sutterton Surgery vs national average, Sept 2024 to Aug 2026")
    ax.legend()
    OUT.parent.mkdir(exist_ok=True)
    fig.savefig(OUT, dpi=150, bbox_inches="tight")

if __name__ == "__main__":
    plot(fetch())
    print("saved", OUT)
import sys
import pandas as pd
from ingestion import load, list_size

def months_between(start: str, end: str) -> list[str]:
    periods = pd.period_range(pd.Period(start, "M"), pd.Period(end, "M"), freq="M")
    if len(periods) == 0:
        raise ValueError(f"start {start} is after end {end}")
    return [p.strftime("%Y%m") for p in periods]

if __name__ == "__main__":
    start, end = sys.argv[1], sys.argv[2]
    for month in months_between(start, end):
        print(month, "prescribing", load.load_month(month), "rows")
        print(month, "list sizes", list_size.load_month(month), "rows")
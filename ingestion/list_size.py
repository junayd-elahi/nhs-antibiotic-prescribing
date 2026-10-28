import calendar
import io
import re
import sys
import pandas as pd
import requests
from ingestion.db import replace_month

PAGE = "https://digital.nhs.uk/data-and-information/publications/statistical/patients-registered-at-a-gp-practice/{slug}"
ZIP_LINK = re.compile(r'https://files\.digital\.nhs\.uk/[^"\']+/gp-reg-pat-prac-all\.(?:zip|csv)')

def download(url: str) -> requests.Response:
    response = requests.get(url)
    if not response.ok:
        raise RuntimeError(f"{response.status_code} for {url}")
    return response

def page_url(month: str) -> str:
    name = calendar.month_name[int(month[4:])].lower()
    return PAGE.format(slug=f"{name}-{month[:4]}")

def zip_url(month: str) -> str:
    links = set(ZIP_LINK.findall(download(page_url(month)).text))
    if len(links) != 1:
        raise RuntimeError(f"Expected 1 zip link for {month}, found {len(links)}")
    return links.pop()

def fetch_month(month: str) -> pd.DataFrame:
    url = zip_url(month)
    compression = "zip" if url.endswith(".zip") else None
    raw = pd.read_csv(io.BytesIO(download(url).content), compression=compression)
    if raw.empty:
        raise RuntimeError(f"No rows for {month}")
    return pd.DataFrame({
        "month": month,
        "PRACTICE_CODE": raw["CODE"],
        "list_size": raw["NUMBER_OF_PATIENTS"],
    })

def load_month(month: str) -> int:
    df = fetch_month(month)
    replace_month("raw.practice_list_sizes", month, df)
    return len(df)

if __name__ == "__main__":
    month = sys.argv[1]
    print(month, load_month(month), "rows")
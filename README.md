
- **DuckDB** as a local analytical database: free, embedded, no server
- Loads are idempotent: each month is deleted and reinserted, so reruns never duplicate

## Method

1. Join prescribing to list size on practice code and month, giving items per 1,000 patients
2. Compare each practice to the national average **for the same month**, since prescribing is strongly seasonal (about 44 per 1,000 in December vs 30 in August)
3. Flag a practice-month as high when its ratio exceeds 1.5
4. A practice is an outlier when it is high in all 24 months, which filters out one-off spikes

## Design decisions

- **Practice code, not ICB, as the anchor.** The 2026 restructure cut ICBs from 42 to 36 with redrawn boundaries, so ICB codes are not stable over the period
- **Excluded non-GP prescribers.** About a fifth of prescribing rows have no registered list: out-of-hours services, walk-in centres, community services (mostly Y-prefixed codes). A per-patient rate is meaningless for them
- **Excluded Y-coded services** from comparison. Care home practices reached 8x the national rate because their patients are frail and elderly, which would swamp the results
- **Excluded practices under 1,000 patients**, where a few prescriptions produce extreme rates
- **Grouped by practice code, not name.** Names are not unique, and 3 practices were renamed during the period. Grouping by name gave 36 or 37 outliers instead of 40

## Data quality issues found

The source data is not consistent across months, and each issue surfaced during the backfill:

- BNF code column renamed from `BNF_CODE` to `BNF_PRESENTATION_CODE`
- `YEAR_MONTH` changed from integer (`202409`) to string (`'2026-08'`), so the loader stamps its own month column
- Numeric columns stored as text in March 2025, requiring explicit casts
- List size files published as zip in some months and csv in others

## Limitations

- **No adjustment for population.** Age, deprivation and rurality all affect infection rates. The geographic clustering suggests some outliers reflect their patients rather than prescribing behaviour
- Items are a count of prescriptions, not doses or courses
- The 1.5x threshold is a judgement call, not a clinical standard

## Run it

```powershell
pip install -r requirements.txt
python -m ingestion.backfill 202409 202608
python -m transform.build
python -m analysis.chart
```

Then run `analysis/persistent_outliers.sql` in DuckDB.

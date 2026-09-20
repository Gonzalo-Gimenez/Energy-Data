# Argentina Energy Analytics (Data Analyst)

Exploratory analysis on **public** Argentine energy and fuel-price data. No proprietary YPF or field telemetry — only reproducible questions a sector analyst would ask with open datasets.

## Business questions

| # | Question | Where answered |
|---|----------|----------------|
| 1 | How did national average fuel prices move month over month? | `sql/01_price_trends.sql` |
| 2 | Which fuel type shows the widest price spread across provinces? | `sql/02_price_dispersion.sql` |
| 3 | Is there a seasonal pattern in diesel vs gasoline? | `sql/03_seasonality.sql` |
| 4 | Which regions concentrate the highest posted prices? | `sql/04_regional_rank.sql` |
| 5 | What would we monitor weekly if this were an operations desk? | `memo/ANALYST_MEMO.md` |

## Stack

- Python 3.12 + pandas (ingest / sanity checks)
- DuckDB (local analytic warehouse)
- SQL (versioned queries)
- CSV derived from public fuel-price series (documented in `data/README.md`)

## Quick start

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python scripts/build_duckdb.py
duckdb data/energy.duckdb -c ".read sql/01_price_trends.sql"
```

Or run all packaged queries:

```powershell
python scripts/run_all_sql.py
```

## Data limits

- Demo file `data/fuel_prices_public_sample.csv` is a **curated subset** shaped like Secretaría de Energía / Surtidor reports (dates, product, province, ARS/liter). Replace with your own export from [datos.gob.ar](https://datos.gob.ar) following `data/README.md`.
- Do not infer internal margins or production — this repo stops at public posted prices.

## Analyst memo

One-page narrative for a hiring manager: `memo/ANALYST_MEMO.md`.

## License

MIT — portfolio demonstration project.

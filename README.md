# Argentina Energy Analytics (Data Analyst)

Exploratory analysis on **public** Argentine fuel-price data: BigQuery warehouse, versioned SQL, Power BI desk, and a one-page analyst memo. No proprietary refinery or field telemetry.

![Overview dashboard](docs/powerbi-overview.png)

## Business questions

| # | Question | SQL |
|---|----------|-----|
| 1 | How did national average fuel prices move month over month? | `sql/01_price_trends.sql` |
| 2 | Which fuel type shows the widest price spread across provinces? | `sql/02_price_dispersion.sql` |
| 3 | Is there a seasonal pattern in diesel vs gasoline? | `sql/03_seasonality.sql` |
| 4 | Which regions concentrate the highest posted prices? | `sql/04_regional_rank.sql` |
| 5 | What would we monitor weekly on an operations desk? | `sql/05_weekly_watch.sql` |

## Stack

- Python 3.12 + pandas (CSV validation)
- **Google BigQuery** (`energy_ar.fuel_prices`)
- SQL (Standard SQL, `{{TABLE}}` placeholder for the fully qualified table)
- **Power BI** (`powerbi/EnergyFuelPrices.pbip`, CSV import; BigQuery connector in production)
- Analyst memo: `memo/ANALYST_MEMO.md`

## Quick start

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python scripts/generate_sample_csv.py   # optional: regenerate demo CSV
python scripts/validate_csv.py
```

### BigQuery (optional)

```powershell
$env:GCP_PROJECT = "your-gcp-project"
gcloud auth application-default login
python scripts/load_bigquery.py
python scripts/run_all_sql.py
```

Without GCP credentials, `run_all_sql.py` still writes `output/*.csv` using a local DuckDB engine with the same SQL logic.

### Power BI

Open `powerbi/EnergyFuelPrices.pbip` in Power BI Desktop. See `powerbi/README.md`. To refresh README screenshots:

```powershell
python scripts/export_powerbi_png.py
```

## Data limits

`data/fuel_prices_public_sample.csv` is a **curated demo** shaped like public surtidor exports. Replace with your own [datos.gob.ar](https://datos.gob.ar) export (see `data/README.md`). Do not infer refinery margin or real consumption from price alone.

## License

MIT — portfolio demonstration project.

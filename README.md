# Argentina Energy Analytics (Data Analyst)

Exploratory analysis on **public** Argentine fuel-price data: a local PostgreSQL warehouse (Docker), versioned SQL, a Power BI desk, and a one-page analyst memo. No cloud billing, no proprietary refinery telemetry.

![Overview dashboard](docs/powerbi-overview.png)

## What is “the database” in this repo

Companies do **not** keep the warehouse as an Excel on a laptop. They load tables into a SQL engine (BigQuery, Snowflake, or Postgres) and analysts query that.

Here the same job is **simulated locally** so anyone can clone and run it:

| In GitHub (source of truth) | At demo time |
|-----------------------------|--------------|
| `data/fuel_prices_public_sample.csv` + `sql/00_schema.sql` | `docker compose up -d` → Postgres on `:5435`, table `fuel_prices` |

We do **not** commit the Postgres volume (binary, machine-specific). The CSV + schema **are** the public database.

```
CSV (GitHub)  →  PostgreSQL warehouse (Docker :5435)  →  sql/01–05  →  output/
                          ↘
                       Power BI (imports the same CSV)
```

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
- **PostgreSQL 15** in Docker (`energy.fuel_prices`, port **5435**)
- SQL (Postgres, one file per business question)
- **Power BI** (`powerbi/EnergyFuelPrices.pbip`, CSV import; same grain as the warehouse table)
- Analyst memo: `memo/ANALYST_MEMO.md`

## Quick start

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python scripts/validate_csv.py
docker compose up -d
python scripts/load_warehouse.py   # if the volume already existed without data
python scripts/run_all_sql.py
```

First `docker compose up` runs `sql/00_schema.sql` and loads the CSV. If Postgres is not running, `run_all_sql.py` still writes `output/*.csv` with DuckDB (same SQL).

Query the warehouse:

```powershell
docker compose exec warehouse psql -U energy -d energy -c "SELECT producto, COUNT(*) FROM fuel_prices GROUP BY 1;"
```

### Power BI

Open `powerbi/EnergyFuelPrices.pbip` in Power BI Desktop. See `powerbi/README.md`.

```powershell
python scripts/export_powerbi_png.py
```

## Data limits

`data/fuel_prices_public_sample.csv` is a **curated demo** shaped like public surtidor exports. Replace with your own [datos.gob.ar](https://datos.gob.ar) export (see `data/README.md`). Do not infer refinery margin or real consumption from price alone.

## License

MIT — portfolio demonstration project.

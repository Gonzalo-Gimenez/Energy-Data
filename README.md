# Argentina Energy Analytics (Data Analyst)

Exploratory analysis on **public** Argentine fuel-price data: a local PostgreSQL warehouse (Docker), versioned SQL, a Power BI desk, and a one-page analyst memo. No cloud billing, no proprietary refinery telemetry.

![Overview dashboard](docs/powerbi-overview.png)

## What is “the database” in this repo

In a company the warehouse is a SQL engine (BigQuery, Snowflake, or Postgres). Analysts connect with a SQL client (DBeaver, DataGrip) or Power BI — they do not query the CSV by hand.

This exercise **simulates that warehouse with PostgreSQL in Docker**. Same job as BigQuery; local, free, and openable in DBeaver.

| On GitHub (source of truth) | On your machine (demo) |
|-----------------------------|-------------------------|
| `data/fuel_prices_public_sample.csv` + `sql/*.sql` | `docker compose up -d` → Postgres `:5435` → table `fuel_prices` |

The Postgres data directory is **not** committed (binary). The CSV and the SQL files **are** the public database.

```
CSV (GitHub)
    → PostgreSQL in Docker (warehouse, like BigQuery)
    → DBeaver / sql/01–05
    → Power BI (same CSV)
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
- **PostgreSQL 15** in Docker (`energy` / table `fuel_prices`, port **5435**)
- SQL files in `sql/` (open them in DBeaver)
- **Power BI** (`powerbi/EnergyFuelPrices.pbip`)
- Analyst memo: `memo/ANALYST_MEMO.md`

## Quick start

```powershell
cd Proyectos\energy-analytics-ar
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
docker compose up -d
python scripts/load_warehouse.py
python scripts/run_all_sql.py
```

## DBeaver (SQL client)

New connection → PostgreSQL:

| Field | Value |
|-------|--------|
| Host | `localhost` |
| Port | `5435` |
| Database | `energy` |
| Username | `energy` |
| Password | `energy` |

Then open `sql/01_price_trends.sql` (and the rest) against that connection. DBeaver is the desktop SQL IDE; it is **not** DuckDB. DuckDB is not part of this project.

## Power BI

Open `powerbi/EnergyFuelPrices.pbip` in Power BI Desktop. See `powerbi/README.md`.

## Data limits

`data/fuel_prices_public_sample.csv` is a **curated demo** shaped like public surtidor exports. Replace with your own [datos.gob.ar](https://datos.gob.ar) export (see `data/README.md`). Do not infer refinery margin or real consumption from price alone.

## License

MIT — portfolio demonstration project.

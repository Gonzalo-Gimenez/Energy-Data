# Data sources

Use open Argentine datasets, for example:

- Fuel prices and surtidor series on [datos.gob.ar](https://datos.gob.ar/dataset) (Secretaría de Energía).
- National energy statistics when the question is production/consumption — cite the dataset ID in your memo.

## Schema

| Column | Type | Description |
|--------|------|-------------|
| `fecha` | DATE | Observation date |
| `producto` | TEXT | e.g. Nafta Super, Gasoil Grado 2 |
| `provincia` | TEXT | Province name |
| `precio_ars_litro` | NUMERIC | Posted ARS per liter |

`fuel_prices_public_sample.csv` is **demo data** (~500 rows, Jan 2024 – Sep 2025). Regenerate with `python scripts/generate_sample_csv.py`.

This CSV **is** the public database in GitHub. Load it into DuckDB:

```powershell
python scripts/build_duckdb.py
```

That writes `data/energy.duckdb` (local, gitignored). Optional: `docker compose up -d` loads the same CSV into PostgreSQL on port 5435.

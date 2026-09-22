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

## BigQuery load

After replacing the CSV:

```powershell
$env:GCP_PROJECT = "your-project"
python scripts/load_bigquery.py
```

Target table: `energy_ar.fuel_prices` (dataset created if missing).

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

This CSV **is** the public database in GitHub. Docker Compose loads it into PostgreSQL (`fuel_prices`) on port 5435.

```powershell
docker compose up -d
python scripts/load_warehouse.py
```

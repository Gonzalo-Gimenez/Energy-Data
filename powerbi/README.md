# Power BI report (Energy Fuel Prices)

Open `EnergyFuelPrices.pbip` in **Power BI Desktop** (October 2024+ with PBIP support).

## Data source

The semantic model imports `../data/fuel_prices_public_sample.csv` — the same grain as DuckDB `fuel_prices`. In a company you would point Power BI at the warehouse instead of the file.

## DAX measures (in model)

- `Precio_promedio` — national average ARS/liter
- `Spread_max_min` — max minus min in the current filter context
- `Ultimo_mes` — average price in the latest month of the dataset

## Report pages (build in Desktop)

1. **Overview** — KPI cards (Nafta Super / Gasoil / Premium averages), line chart of monthly mean by product.
2. **Provinces** — bar chart of last-month average by province, slicer on `producto`.

Export PNGs to `docs/powerbi-overview.png` and `docs/powerbi-provinces.png` after layout, or run:

```powershell
.\.venv\Scripts\python scripts\export_powerbi_png.py
```

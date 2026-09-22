# Power BI report (Energy Fuel Prices)

Open `EnergyFuelPrices.pbip` in **Power BI Desktop**.

The PNGs in `docs/` are a **light office-style stand-in** (matplotlib) so GitHub and the portfolio have a cover. They are not screenshots of Desktop. Build the two pages here, then **File → Export → PNG** (or Snipping Tool) and replace `docs/powerbi-overview.png` / `docs/powerbi-provinces.png`.

## Data source

The semantic model imports `data/fuel_prices_public_sample.csv` (same grain as DuckDB `fuel_prices`). If Desktop asks to locate the file, point it at that CSV. In a company you would use the warehouse connector instead.

## DAX measures (in the model)

- `Precio_promedio` — national average ARS/liter
- `Spread_max_min` — max minus min in the current filter context
- `Ultimo_mes` — average price in the latest month

## Pages to build in Desktop (light theme)

View → Themes → **Office** or **Executive** (white canvas).

1. **Overview** — three cards (Nafta Super / Gasoil / Premium using `Precio_promedio` + slicer/filter on `producto`) and a line chart of monthly average.
2. **Provinces** — bar chart of last-month average by `provincia`, slicer on `producto`.

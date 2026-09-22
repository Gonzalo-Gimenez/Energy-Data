# Analyst memo (1 page)

**Audience:** energy retail / downstream analyst hiring manager  
**Data:** public posted fuel prices (demo CSV; replace with datos.gob.ar export)  
**Warehouse:** PostgreSQL `fuel_prices` (Docker, `localhost:5435`) — same grain as the CSV in GitHub  
**Desk:** Power BI report in `powerbi/EnergyFuelPrices.pbip`

## Snapshot (demo sample, Sep 2025)

- **Nafta Super** national mean ≈ **988 ARS/L**; **Gasoil Grado 2** ≈ **941 ARS/L**; **Nafta Premium** ≈ **1,043 ARS/L** (simple averages over all rows).
- **Widest provincial spread (full history):** Gasoil Grado 2 **~110 ARS/L** between min and max province; gasoline products ~106 ARS/L (`sql/02_price_dispersion.sql`).
- **Seasonality:** diesel shows a **Q2–Q3 uplift** in the demo generator (freight-heavy months); QoQ changes stay in the **0.8–2.4%** band in `sql/03_seasonality.sql` — watch trends, not single quarters.
- **Weekly control (`sql/05_weekly_watch.sql`):** flag **ALERTA** when national mean moves **≥2% WoW**; latest weeks in the sample stay **OK**.

## What I would watch weekly

1. **National basket** — average Nafta Super and Gasoil Grado 2 vs prior week; alert above 2% WoW on the national mean.
2. **Regional stress** — provinces with spread vs Buenos Aires widening; persistent gaps deserve a supply-planning call.
3. **Product mix** — diesel catching up to gasoline in % change over eight weeks; one week is noise.

## What this dataset cannot answer

- Refinery margin, crack spread, or internal cost — not in public surtidor prices.
- Real consumption — need volumes or ENARGAS/Secretaría series, not price alone.

## Next step with real data

Ingest the official CSV/API into `prices_raw`, snapshot into the warehouse table, point Power BI at Postgres (or BigQuery at work), and keep the five SQL files as the regression suite for schema changes.

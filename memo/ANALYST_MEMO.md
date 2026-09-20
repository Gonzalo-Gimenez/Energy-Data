# Analyst memo (1 page)

**Audience:** energy retail / downstream analyst hiring manager  
**Data:** public posted fuel prices (demo CSV; replace with datos.gob.ar export)

## What I would watch weekly

1. **National basket** — average Nafta Super and Gasoil Grado 2 vs prior week; flag moves above a simple control limit (e.g. 2% WoW on the national mean).
2. **Regional stress** — provinces with spread vs Buenos Aires widening; often logistics or local tax noise, but persistent gaps deserve a call with supply planning.
3. **Product mix** — diesel catching up to gasoline in % change terms can signal freight-heavy demand or import parity shifts; I would not act on one week, but I would chart eight weeks.

## What this dataset cannot answer

- Refinery margin, crack spread, or YPF-internal cost — not in public surtidor prices.
- Real consumption — need sales volumes or ENARGAS/Secretaría series, not price alone.

## Next step with real data

Ingest the official CSV/API, version snapshots in a `prices_raw` table, and keep these five SQL files as the regression suite for any schema change.

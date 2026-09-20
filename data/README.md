# Data sources

Use open Argentine datasets, for example:

- Fuel prices and surtidor series published on [datos.gob.ar](https://datos.gob.ar/dataset) (Secretaría de Energía).
- National energy statistics when the question is production/consumption — always cite the dataset ID in your memo.

`fuel_prices_public_sample.csv` is **demo data** for the portfolio: same schema you would expect from a public export (`fecha`, `producto`, `provincia`, `precio_ars_litro`). Swap the file and re-run `scripts/build_duckdb.py` without changing SQL.

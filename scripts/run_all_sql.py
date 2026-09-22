"""Run versioned SQL with DuckDB (pip) and write results to output/."""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

import duckdb

from warehouse import CSV_PATH, DUCKDB_PATH, OUTPUT_DIR, query_files


def connect() -> duckdb.DuckDBPyConnection:
    if DUCKDB_PATH.exists():
        return duckdb.connect(str(DUCKDB_PATH))
    con = duckdb.connect()
    con.execute(
        """
        CREATE TABLE fuel_prices AS
        SELECT
            CAST(fecha AS DATE) AS fecha,
            producto,
            provincia,
            CAST(precio_ars_litro AS DOUBLE) AS precio_ars_litro
        FROM read_csv_auto(?)
        """,
        [str(CSV_PATH)],
    )
    return con


def main() -> None:
    con = connect()
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    try:
        for path in query_files():
            df = con.sql(path.read_text(encoding="utf-8")).fetchdf()
            out = OUTPUT_DIR / f"{path.stem}.csv"
            df.to_csv(out, index=False)
            print(f"\n=== {path.name} -> {out.name} ({len(df)} rows) ===\n")
            print(df.head(12).to_string(index=False))
    finally:
        con.close()


if __name__ == "__main__":
    main()

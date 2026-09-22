"""Load the public sample CSV into a local DuckDB warehouse."""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

import duckdb

from validate_csv import validate_csv
from warehouse import CSV_PATH, DUCKDB_PATH


def main() -> None:
    n_csv = len(validate_csv())
    DUCKDB_PATH.parent.mkdir(parents=True, exist_ok=True)
    if DUCKDB_PATH.exists():
        DUCKDB_PATH.unlink()
    con = duckdb.connect(str(DUCKDB_PATH))
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
    n = con.execute("SELECT COUNT(*) FROM fuel_prices").fetchone()[0]
    con.close()
    print(f"Loaded {n} rows (CSV had {n_csv}) into {DUCKDB_PATH}")


if __name__ == "__main__":
    main()

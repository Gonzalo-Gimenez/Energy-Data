"""Load public-sample CSV into DuckDB for SQL analysis."""
from pathlib import Path

import duckdb

ROOT = Path(__file__).resolve().parents[1]
CSV = ROOT / "data" / "fuel_prices_public_sample.csv"
DB = ROOT / "data" / "energy.duckdb"


def main() -> None:
    DB.parent.mkdir(parents=True, exist_ok=True)
    con = duckdb.connect(str(DB))
    con.execute("DROP TABLE IF EXISTS fuel_prices")
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
        [str(CSV)],
    )
    n = con.execute("SELECT COUNT(*) FROM fuel_prices").fetchone()[0]
    con.close()
    print(f"Loaded {n} rows into {DB}")


if __name__ == "__main__":
    main()

"""Run versioned SQL against the warehouse and write results to output/."""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from warehouse import CSV_PATH, DATABASE_URL, OUTPUT_DIR, query_files


def run_postgres() -> None:
    import pandas as pd
    import psycopg2

    conn = psycopg2.connect(DATABASE_URL)
    try:
        OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
        for path in query_files():
            sql = path.read_text(encoding="utf-8")
            df = pd.read_sql_query(sql, conn)
            out = OUTPUT_DIR / f"{path.stem}.csv"
            df.to_csv(out, index=False)
            print(f"\n=== {path.name} -> {out.name} ({len(df)} rows) ===\n")
            print(df.head(12).to_string(index=False))
    finally:
        conn.close()


def run_duckdb() -> None:
    import duckdb

    con = duckdb.connect()
    con.execute(
        """
        CREATE OR REPLACE TABLE fuel_prices AS
        SELECT
            CAST(fecha AS DATE) AS fecha,
            producto,
            provincia,
            CAST(precio_ars_litro AS DOUBLE) AS precio_ars_litro
        FROM read_csv_auto(?)
        """,
        [str(CSV_PATH)],
    )
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    for path in query_files():
        sql = path.read_text(encoding="utf-8")
        df = con.sql(sql).fetchdf()
        out = OUTPUT_DIR / f"{path.stem}.csv"
        df.to_csv(out, index=False)
        print(f"\n=== {path.name} -> {out.name} ({len(df)} rows) ===\n")
        print(df.head(12).to_string(index=False))
    con.close()


def postgres_up() -> bool:
    try:
        import psycopg2

        conn = psycopg2.connect(DATABASE_URL, connect_timeout=3)
        conn.close()
        return True
    except Exception:
        return False


def main() -> None:
    if postgres_up():
        run_postgres()
        return
    print("PostgreSQL not reachable on :5435; running SQL locally with DuckDB.\n")
    run_duckdb()


if __name__ == "__main__":
    main()

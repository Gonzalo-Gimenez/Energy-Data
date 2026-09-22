"""Run versioned SQL against BigQuery and write results to output/."""
from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from bq_config import OUTPUT_DIR, SQL_DIR, gcp_project, substitute_table


def run_local_duckdb_fallback() -> bool:
    """When GCP is not configured, run queries with DuckDB (BQ-compatible SQL subset)."""
    try:
        import duckdb
    except ImportError:
        return False

    from bq_config import CSV_PATH

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
    for path in sorted(SQL_DIR.glob("*.sql")):
        sql = substitute_table(path.read_text(encoding="utf-8"), project="__local__")
        sql = sql.replace("`__local__.energy_ar.fuel_prices`", "fuel_prices")
        sql = sql.replace("DATE_TRUNC(fecha, WEEK(MONDAY))", "date_trunc('week', fecha)")
        sql = sql.replace("DATE_TRUNC(f.fecha, MONTH)", "date_trunc('month', f.fecha)")
        sql = sql.replace("DATE_TRUNC(l.max_fecha, MONTH)", "date_trunc('month', l.max_fecha)")
        sql = sql.replace("DATE_TRUNC(fecha, MONTH)", "date_trunc('month', fecha)")
        sql = sql.replace("DATE_TRUNC(fecha, QUARTER)", "date_trunc('quarter', fecha)")
        df = con.sql(sql).fetchdf()
        out = OUTPUT_DIR / f"{path.stem}.csv"
        df.to_csv(out, index=False)
        print(f"\n=== {path.name} -> {out.name} ({len(df)} rows) ===\n")
        print(df.head(12).to_string(index=False))
    con.close()
    return True


def run_bigquery() -> None:
    from google.cloud import bigquery

    project = gcp_project()
    if not project:
        raise ValueError("missing project")

    client = bigquery.Client(project=project)
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    for path in sorted(SQL_DIR.glob("*.sql")):
        sql = substitute_table(path.read_text(encoding="utf-8"), project=project)
        df = client.query(sql).to_dataframe()
        out = OUTPUT_DIR / f"{path.stem}.csv"
        df.to_csv(out, index=False)
        print(f"\n=== {path.name} -> {out.name} ({len(df)} rows) ===\n")
        print(df.head(12).to_string(index=False))


def main() -> None:
    if gcp_project():
        try:
            run_bigquery()
            return
        except Exception as exc:
            print(f"BigQuery run failed ({exc}); falling back to local DuckDB.\n")

    if not run_local_duckdb_fallback():
        raise SystemExit(
            "Set GCP_PROJECT for BigQuery, or install duckdb for local output generation."
        )


if __name__ == "__main__":
    main()

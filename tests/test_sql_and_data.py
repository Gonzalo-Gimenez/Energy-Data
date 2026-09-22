from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

import duckdb

from validate_csv import validate_csv
from warehouse import CSV_PATH, query_files


def test_csv_schema_and_volume():
    df = validate_csv()
    assert len(df) >= 500
    assert df["fecha"].min().year == 2024
    assert df["producto"].nunique() >= 3
    assert df["provincia"].nunique() >= 6


def test_sql_files_present_and_non_empty():
    files = query_files()
    assert len(files) == 5
    for path in files:
        body = path.read_text(encoding="utf-8")
        assert "fuel_prices" in body
        assert len(body.strip()) > 40


def test_queries_return_rows_in_duckdb():
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
    for path in query_files():
        df = con.sql(path.read_text(encoding="utf-8")).fetchdf()
        assert len(df) > 0
    con.close()

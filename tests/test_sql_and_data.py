from __future__ import annotations

import sys
from pathlib import Path

import psycopg2
import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from validate_csv import validate_csv
from warehouse import DATABASE_URL, query_files


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


def _postgres_available() -> bool:
    try:
        conn = psycopg2.connect(DATABASE_URL, connect_timeout=3)
        conn.close()
        return True
    except Exception:
        return False


@pytest.mark.skipif(not _postgres_available(), reason="docker compose warehouse not running")
def test_queries_return_rows_from_warehouse():
    conn = psycopg2.connect(DATABASE_URL)
    try:
        for path in query_files():
            with conn.cursor() as cur:
                cur.execute(path.read_text(encoding="utf-8"))
                rows = cur.fetchall()
            assert len(rows) > 0
    finally:
        conn.close()

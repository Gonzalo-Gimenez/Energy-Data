from __future__ import annotations

import os
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from bq_config import SQL_DIR, substitute_table
from validate_csv import validate_csv


def test_csv_schema_and_volume():
    df = validate_csv()
    assert len(df) >= 500
    assert df["fecha"].min().year == 2024
    assert df["producto"].nunique() >= 3
    assert df["provincia"].nunique() >= 6


def test_sql_files_present_and_non_empty():
    names = [f"0{i}_" for i in range(1, 6)] + ["05_"]
    files = sorted(SQL_DIR.glob("*.sql"))
    assert len(files) == 5
    for path in files:
        body = path.read_text(encoding="utf-8")
        assert "{{TABLE}}" in body
        assert len(body.strip()) > 40


@pytest.mark.skipif(
    not (os.environ.get("GCP_PROJECT") or os.environ.get("GOOGLE_CLOUD_PROJECT")),
    reason="BigQuery integration test needs GCP_PROJECT",
)
def test_bigquery_queries_return_rows():
    from google.cloud import bigquery

    from bq_config import gcp_project

    client = bigquery.Client(project=gcp_project())
    for path in sorted(SQL_DIR.glob("*.sql")):
        sql = substitute_table(path.read_text(encoding="utf-8"))
        df = client.query(sql).to_dataframe()
        assert len(df) > 0

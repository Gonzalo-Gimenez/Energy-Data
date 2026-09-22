"""BigQuery settings shared by load and query scripts."""
from __future__ import annotations

import os
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CSV_PATH = ROOT / "data" / "fuel_prices_public_sample.csv"
SQL_DIR = ROOT / "sql"
OUTPUT_DIR = ROOT / "output"

DATASET_ID = os.environ.get("BQ_DATASET", "energy_ar")
TABLE_ID = os.environ.get("BQ_TABLE", "fuel_prices")


def gcp_project() -> str | None:
    return os.environ.get("GCP_PROJECT") or os.environ.get("GOOGLE_CLOUD_PROJECT")


def table_fqn(project: str | None = None) -> str:
    proj = project or gcp_project()
    if not proj:
        raise ValueError("Set GCP_PROJECT (or GOOGLE_CLOUD_PROJECT) to run BigQuery scripts.")
    return f"`{proj}.{DATASET_ID}.{TABLE_ID}`"


def substitute_table(sql: str, project: str | None = None) -> str:
    fqn = table_fqn(project)
    return sql.replace("{{TABLE}}", fqn)

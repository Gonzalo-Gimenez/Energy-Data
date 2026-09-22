"""Local warehouse paths and connection (PostgreSQL in Docker)."""
from __future__ import annotations

import os
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CSV_PATH = ROOT / "data" / "fuel_prices_public_sample.csv"
SQL_DIR = ROOT / "sql"
OUTPUT_DIR = ROOT / "output"
SCHEMA_SQL = SQL_DIR / "00_schema.sql"

DATABASE_URL = os.environ.get(
    "ENERGY_DATABASE_URL",
    "postgresql://energy:energy@localhost:5435/energy",
)
TABLE = "fuel_prices"


def query_files() -> list[Path]:
    return sorted(p for p in SQL_DIR.glob("*.sql") if p.name != "00_schema.sql")

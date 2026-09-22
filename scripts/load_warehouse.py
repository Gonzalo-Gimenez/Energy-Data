"""Load the public sample CSV into the local PostgreSQL warehouse."""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

import psycopg2
from psycopg2 import sql

from validate_csv import validate_csv
from warehouse import CSV_PATH, DATABASE_URL, SCHEMA_SQL, TABLE


def main() -> None:
    validate_csv()
    conn = psycopg2.connect(DATABASE_URL)
    try:
        with conn.cursor() as cur:
            cur.execute(SCHEMA_SQL.read_text(encoding="utf-8"))
            cur.execute(sql.SQL("TRUNCATE {}").format(sql.Identifier(TABLE)))
        conn.commit()
        with conn.cursor() as cur, CSV_PATH.open("r", encoding="utf-8") as f:
            cur.copy_expert("COPY fuel_prices FROM STDIN WITH CSV HEADER", f)
        conn.commit()
        with conn.cursor() as cur:
            cur.execute(sql.SQL("SELECT COUNT(*) FROM {}").format(sql.Identifier(TABLE)))
            n = cur.fetchone()[0]
        print(f"Loaded {n} rows into {TABLE} ({DATABASE_URL})")
    finally:
        conn.close()


if __name__ == "__main__":
    main()

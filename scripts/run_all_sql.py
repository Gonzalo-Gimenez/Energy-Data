"""Run versioned SQL against PostgreSQL and write results to output/."""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from warehouse import DATABASE_URL, OUTPUT_DIR, query_files


def main() -> None:
    import pandas as pd
    import psycopg2

    try:
        conn = psycopg2.connect(DATABASE_URL, connect_timeout=5)
    except Exception as exc:
        raise SystemExit(
            "PostgreSQL is not running on localhost:5435.\n"
            "Start it with: docker compose up -d\n"
            f"Detail: {exc}"
        ) from exc

    try:
        OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
        for path in query_files():
            sql = path.read_text(encoding="utf-8")
            with conn.cursor() as cur:
                cur.execute(sql)
                cols = [d[0] for d in cur.description]
                df = pd.DataFrame(cur.fetchall(), columns=cols)
            out = OUTPUT_DIR / f"{path.stem}.csv"
            df.to_csv(out, index=False)
            print(f"\n=== {path.name} -> {out.name} ({len(df)} rows) ===\n")
            print(df.head(12).to_string(index=False))
    finally:
        conn.close()


if __name__ == "__main__":
    main()

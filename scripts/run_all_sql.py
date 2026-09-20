from pathlib import Path

import duckdb

ROOT = Path(__file__).resolve().parents[1]
DB = ROOT / "data" / "energy.duckdb"
SQL_DIR = ROOT / "sql"


def main() -> None:
    if not DB.exists():
        raise SystemExit("Run scripts/build_duckdb.py first")
    con = duckdb.connect(str(DB))
    for path in sorted(SQL_DIR.glob("*.sql")):
        print(f"\n=== {path.name} ===\n")
        sql = path.read_text(encoding="utf-8")
        result = con.sql(sql)
        try:
            print(result.fetchdf().to_string(index=False))
        except duckdb.Error:
            con.execute(sql)
    con.close()


if __name__ == "__main__":
    main()

"""Sanity checks on the public sample CSV (used before warehouse load)."""
from __future__ import annotations

import pandas as pd

from warehouse import CSV_PATH

REQUIRED = {"fecha", "producto", "provincia", "precio_ars_litro"}


def validate_csv() -> pd.DataFrame:
    df = pd.read_csv(CSV_PATH)
    missing = REQUIRED - set(df.columns)
    if missing:
        raise ValueError(f"CSV missing columns: {missing}")
    if df.empty:
        raise ValueError("CSV is empty")
    if df["precio_ars_litro"].isna().any():
        raise ValueError("Null prices found")
    if (df["precio_ars_litro"] <= 0).any():
        raise ValueError("Non-positive prices found")
    df["fecha"] = pd.to_datetime(df["fecha"])
    return df


if __name__ == "__main__":
    frame = validate_csv()
    print(
        f"OK: {len(frame)} rows, "
        f"{frame['fecha'].min().date()} .. {frame['fecha'].max().date()}"
    )

"""Regenerate demo fuel price sample (portfolio use only)."""
from __future__ import annotations

import csv
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "fuel_prices_public_sample.csv"

PRODUCTS = [
    "Nafta Super",
    "Gasoil Grado 2",
    "Nafta Premium",
]
PROVINCES = [
    "Buenos Aires",
    "Córdoba",
    "Mendoza",
    "Santa Fe",
    "Neuquén",
    "Chubut",
    "Tucumán",
    "Salta",
]

# Base ARS/liter anchors (Jan 2024) + gentle trend + seasonal diesel bump in Q2
BASE = {
    "Nafta Super": 890.0,
    "Gasoil Grado 2": 842.0,
    "Nafta Premium": 945.0,
}
PROVINCE_PREMIUM = {
    "Buenos Aires": 0.0,
    "Córdoba": 12.0,
    "Mendoza": 22.0,
    "Santa Fe": 8.0,
    "Neuquén": 18.0,
    "Chubut": 25.0,
    "Tucumán": 15.0,
    "Salta": 20.0,
}


def month_starts(start: date, end: date) -> list[date]:
    cur = date(start.year, start.month, 15)
    out: list[date] = []
    while cur <= end:
        out.append(cur)
        if cur.month == 12:
            cur = date(cur.year + 1, 1, 15)
        else:
            cur = date(cur.year, cur.month + 1, 15)
    return out


def price_for(product: str, provincia: str, d: date) -> float:
    months_from_start = (d.year - 2024) * 12 + (d.month - 1)
    trend = months_from_start * 4.2
    seasonal = 0.0
    if product == "Gasoil Grado 2" and d.month in (4, 5, 6, 7):
        seasonal = 8.0
    noise = (hash((product, provincia, d.isoformat())) % 17) - 8
    return round(
        BASE[product] + trend + PROVINCE_PREMIUM[provincia] + seasonal + noise * 0.35,
        1,
    )


def main() -> None:
    start = date(2024, 1, 15)
    end = date(2025, 9, 15)
    rows: list[tuple[str, str, str, float]] = []
    for d in month_starts(start, end):
        for product in PRODUCTS:
            for provincia in PROVINCES:
                rows.append(
                    (
                        d.isoformat(),
                        product,
                        provincia,
                        price_for(product, provincia, d),
                    )
                )
    OUT.parent.mkdir(parents=True, exist_ok=True)
    with OUT.open("w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["fecha", "producto", "provincia", "precio_ars_litro"])
        w.writerows(rows)
    print(f"Wrote {len(rows)} rows to {OUT}")


if __name__ == "__main__":
    main()

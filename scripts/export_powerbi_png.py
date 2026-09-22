"""Export Power-BI-style dashboard PNGs for README (metrics match DAX measures)."""
from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
CSV = ROOT / "data" / "fuel_prices_public_sample.csv"
DOCS = ROOT / "docs"
DOCS.mkdir(parents=True, exist_ok=True)

PBI_BG = "#1B1B1D"
PBI_CARD = "#252526"
PBI_ACCENT = "#118DFF"
PBI_TEXT = "#F3F2F1"


def load() -> pd.DataFrame:
    df = pd.read_csv(CSV, parse_dates=["fecha"])
    return df


def export_overview(df: pd.DataFrame) -> None:
    fig = plt.figure(figsize=(16, 9), facecolor=PBI_BG)
    gs = fig.add_gridspec(2, 3, height_ratios=[0.35, 0.65], hspace=0.35, wspace=0.25)

    products = ["Nafta Super", "Gasoil Grado 2", "Nafta Premium"]
    for i, product in enumerate(products):
        ax = fig.add_subplot(gs[0, i])
        ax.set_facecolor(PBI_CARD)
        val = df.loc[df["producto"] == product, "precio_ars_litro"].mean()
        ax.text(
            0.5,
            0.55,
            f"{val:,.1f}",
            ha="center",
            va="center",
            fontsize=28,
            color=PBI_TEXT,
            fontweight="bold",
        )
        ax.text(
            0.5,
            0.2,
            product,
            ha="center",
            va="center",
            fontsize=11,
            color="#B3B0AD",
        )
        ax.set_xticks([])
        ax.set_yticks([])
        for spine in ax.spines.values():
            spine.set_visible(False)

    ax_line = fig.add_subplot(gs[1, :])
    ax_line.set_facecolor(PBI_CARD)
    monthly = (
        df.assign(mes=df["fecha"].dt.to_period("M").dt.to_timestamp())
        .groupby(["mes", "producto"], as_index=False)["precio_ars_litro"]
        .mean()
    )
    for product in products:
        sub = monthly[monthly["producto"] == product]
        ax_line.plot(sub["mes"], sub["precio_ars_litro"], label=product, linewidth=2.2)
    ax_line.set_title(
        "Precio promedio mensual (ARS/l)",
        color=PBI_TEXT,
        loc="left",
        fontsize=14,
        pad=12,
    )
    ax_line.tick_params(colors=PBI_TEXT)
    ax_line.legend(facecolor=PBI_CARD, edgecolor=PBI_CARD, labelcolor=PBI_TEXT)
    ax_line.grid(color="#3B3A39", alpha=0.5)
    for spine in ax_line.spines.values():
        spine.set_color("#3B3A39")

    fig.suptitle(
        "Energy Fuel Prices — Overview",
        color=PBI_TEXT,
        fontsize=18,
        x=0.02,
        ha="left",
        y=0.98,
    )
    out = DOCS / "powerbi-overview.png"
    fig.savefig(out, dpi=150, facecolor=PBI_BG, bbox_inches="tight")
    plt.close(fig)
    print(f"Wrote {out}")


def export_provinces(df: pd.DataFrame) -> None:
    last_month = df["fecha"].max().to_period("M")
    sub = df[df["fecha"].dt.to_period("M") == last_month]
    product = "Nafta Super"
    prov = (
        sub[sub["producto"] == product]
        .groupby("provincia", as_index=False)["precio_ars_litro"]
        .mean()
        .sort_values("precio_ars_litro", ascending=True)
    )

    fig, ax = plt.subplots(figsize=(16, 9), facecolor=PBI_BG)
    ax.set_facecolor(PBI_CARD)
    ax.barh(prov["provincia"], prov["precio_ars_litro"], color=PBI_ACCENT)
    ax.set_title(
        f"{product} — último mes por provincia",
        color=PBI_TEXT,
        loc="left",
        fontsize=16,
        pad=16,
    )
    ax.tick_params(colors=PBI_TEXT)
    ax.grid(axis="x", color="#3B3A39", alpha=0.5)
    for spine in ax.spines.values():
        spine.set_color("#3B3A39")

    fig.suptitle(
        "Energy Fuel Prices — Provinces",
        color=PBI_TEXT,
        fontsize=18,
        x=0.02,
        ha="left",
        y=0.98,
    )
    out = DOCS / "powerbi-provinces.png"
    fig.savefig(out, dpi=150, facecolor=PBI_BG, bbox_inches="tight")
    plt.close(fig)
    print(f"Wrote {out}")


def main() -> None:
    df = load()
    export_overview(df)
    export_provinces(df)


if __name__ == "__main__":
    main()

"""Light corporate desk screenshots for README/cover (same metrics as the DAX model).

These PNGs are stand-ins until you export from Power BI Desktop.
Open powerbi/EnergyFuelPrices.pbip to build the real report.
"""
from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
CSV = ROOT / "data" / "fuel_prices_public_sample.csv"
DOCS = ROOT / "docs"
DOCS.mkdir(parents=True, exist_ok=True)

# Office / Power BI light report
PAGE = "#FFFFFF"
CANVAS = "#F3F2F1"
CARD = "#FFFFFF"
INK = "#201F1E"
MUTED = "#605E5C"
LINE = "#E1DFDD"
ACCENT = "#0078D4"
PRODUCT_COLORS = {
    "Nafta Super": "#0078D4",
    "Gasoil Grado 2": "#107C10",
    "Nafta Premium": "#5C2E91",
}

plt.rcParams.update(
    {
        "font.family": "sans-serif",
        "font.sans-serif": ["Segoe UI", "Calibri", "Arial"],
        "axes.unicode_minus": False,
    }
)


def load() -> pd.DataFrame:
    return pd.read_csv(CSV, parse_dates=["fecha"])


def _card(ax, face: str = CARD) -> None:
    ax.set_facecolor(face)
    ax.set_xticks([])
    ax.set_yticks([])
    for spine in ax.spines.values():
        spine.set_color(LINE)
        spine.set_linewidth(1)


def export_overview(df: pd.DataFrame) -> None:
    products = ["Nafta Super", "Gasoil Grado 2", "Nafta Premium"]
    fig = plt.figure(figsize=(16, 9), facecolor=PAGE)
    gs = GridSpec(
        3,
        3,
        figure=fig,
        height_ratios=[0.16, 0.28, 0.56],
        hspace=0.42,
        wspace=0.22,
        left=0.06,
        right=0.97,
        top=0.92,
        bottom=0.08,
    )

    ax_head = fig.add_subplot(gs[0, :])
    ax_head.set_facecolor(PAGE)
    ax_head.set_xlim(0, 1)
    ax_head.set_ylim(0, 1)
    ax_head.axis("off")
    ax_head.text(0, 0.62, "Precios de combustibles — Argentina", fontsize=22, color=INK, fontweight="bold")
    ax_head.text(
        0,
        0.18,
        "Escritorio de analista  ·  muestra pública ene 2024 – sep 2025  ·  ARS / litro",
        fontsize=11,
        color=MUTED,
    )

    for i, product in enumerate(products):
        ax = fig.add_subplot(gs[1, i])
        _card(ax)
        val = df.loc[df["producto"] == product, "precio_ars_litro"].mean()
        ax.set_xlim(0, 1)
        ax.set_ylim(0, 1)
        ax.plot([0.08, 0.22], [0.82, 0.82], color=PRODUCT_COLORS[product], linewidth=4, solid_capstyle="butt")
        ax.text(0.08, 0.22, product.upper(), fontsize=10, color=MUTED, ha="left")
        ax.text(0.08, 0.48, f"{val:,.1f}", fontsize=28, color=INK, fontweight="bold", ha="left")
        ax.text(0.08, 0.08, "ARS/l promedio", fontsize=9, color=MUTED, ha="left")

    ax_line = fig.add_subplot(gs[2, :])
    ax_line.set_facecolor(CARD)
    monthly = (
        df.assign(mes=df["fecha"].dt.to_period("M").dt.to_timestamp())
        .groupby(["mes", "producto"], as_index=False)["precio_ars_litro"]
        .mean()
    )
    for product in products:
        sub = monthly[monthly["producto"] == product]
        ax_line.plot(
            sub["mes"],
            sub["precio_ars_litro"],
            label=product,
            color=PRODUCT_COLORS[product],
            linewidth=2.4,
        )
    ax_line.set_title("Precio promedio mensual", loc="left", fontsize=13, color=INK, pad=10)
    ax_line.tick_params(colors=MUTED, labelsize=9)
    ax_line.grid(axis="y", color=LINE, linewidth=0.8)
    ax_line.set_axisbelow(True)
    for spine in ax_line.spines.values():
        spine.set_color(LINE)
    ax_line.spines["top"].set_visible(False)
    ax_line.spines["right"].set_visible(False)
    legend = ax_line.legend(
        frameon=True,
        facecolor=CARD,
        edgecolor=LINE,
        fontsize=9,
        loc="upper left",
    )
    for text in legend.get_texts():
        text.set_color(INK)

    out = DOCS / "powerbi-overview.png"
    fig.savefig(out, dpi=160, facecolor=PAGE)
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

    fig = plt.figure(figsize=(16, 9), facecolor=PAGE)
    gs = GridSpec(2, 1, figure=fig, height_ratios=[0.16, 0.84], hspace=0.15, left=0.16, right=0.94, top=0.92, bottom=0.1)
    ax_head = fig.add_subplot(gs[0, 0])
    ax_head.axis("off")
    ax_head.set_xlim(0, 1)
    ax_head.set_ylim(0, 1)
    ax_head.text(0, 0.55, "Ranking provincial — último mes", fontsize=22, color=INK, fontweight="bold")
    ax_head.text(0, 0.12, f"{product}  ·  {last_month.strftime('%b %Y')}  ·  ARS / litro", fontsize=11, color=MUTED)

    ax = fig.add_subplot(gs[1, 0])
    ax.set_facecolor(CARD)
    bars = ax.barh(prov["provincia"], prov["precio_ars_litro"], color=ACCENT, height=0.62)
    ax.bar_label(bars, fmt="%.1f", padding=6, color=MUTED, fontsize=9)
    ax.tick_params(colors=MUTED, labelsize=10)
    ax.grid(axis="x", color=LINE, linewidth=0.8)
    ax.set_axisbelow(True)
    ax.set_xlabel("ARS / litro", color=MUTED)
    for spine in ax.spines.values():
        spine.set_color(LINE)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)

    out = DOCS / "powerbi-provinces.png"
    fig.savefig(out, dpi=160, facecolor=PAGE)
    plt.close(fig)
    print(f"Wrote {out}")


def main() -> None:
    df = load()
    export_overview(df)
    export_provinces(df)


if __name__ == "__main__":
    main()

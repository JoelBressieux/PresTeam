"""Chart generation helpers for the EV population ETL pipeline."""

from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd


def save_top_10_ev_makes(summary: pd.DataFrame, output_path: Path) -> None:
    """Save a horizontal bar chart for the top 10 EV makes."""
    _require_columns(summary, {"make", "vehicle_count"}, "top EV makes chart")
    top_10 = summary.head(10).sort_values("vehicle_count")

    fig, ax = plt.subplots(figsize=(10, 6))
    ax.barh(top_10["make"], top_10["vehicle_count"], color="#2F6F73")
    ax.set_title("Top 10 EV Makes")
    ax.set_xlabel("Vehicle Count")
    ax.set_ylabel("Make")
    ax.grid(axis="x", alpha=0.25)
    _save_figure(fig, output_path)


def save_ev_count_by_model_year(summary: pd.DataFrame, output_path: Path) -> None:
    """Save a bar chart of EV counts by model year."""
    _require_columns(
        summary, {"model_year", "vehicle_count"}, "EV count by model year chart"
    )

    fig, ax = plt.subplots(figsize=(12, 6))
    ax.bar(summary["model_year"].astype(str), summary["vehicle_count"], color="#5B8DEF")
    ax.set_title("EV Count by Model Year")
    ax.set_xlabel("Model Year")
    ax.set_ylabel("Vehicle Count")
    ax.tick_params(axis="x", rotation=45)
    ax.grid(axis="y", alpha=0.25)
    _save_figure(fig, output_path)


def save_ev_type_split(summary: pd.DataFrame, output_path: Path) -> None:
    """Save a pie chart showing the split by EV type."""
    _require_columns(
        summary, {"electric_vehicle_type", "vehicle_count"}, "EV type split chart"
    )

    fig, ax = plt.subplots(figsize=(8, 8))
    ax.pie(
        summary["vehicle_count"],
        labels=summary["electric_vehicle_type"],
        autopct="%1.1f%%",
        startangle=90,
    )
    ax.set_title("EV Type Split")
    ax.axis("equal")
    _save_figure(fig, output_path)


def save_charts(summaries: dict[str, pd.DataFrame], charts_dir: Path) -> None:
    """Save all charts produced by the pipeline."""
    charts_dir.mkdir(parents=True, exist_ok=True)
    save_top_10_ev_makes(summaries["ev_by_make"], charts_dir / "top_10_ev_makes.png")
    save_ev_count_by_model_year(
        summaries["ev_by_model_year"], charts_dir / "ev_count_by_model_year.png"
    )
    save_ev_type_split(summaries["ev_by_ev_type"], charts_dir / "ev_type_split.png")


def _require_columns(df: pd.DataFrame, columns: set[str], chart_name: str) -> None:
    """Raise a clear error if a chart input table is missing expected columns."""
    missing = columns.difference(df.columns)
    if missing:
        raise ValueError(
            f"Cannot create {chart_name}; missing columns: {', '.join(sorted(missing))}."
        )


def _save_figure(fig: plt.Figure, output_path: Path) -> None:
    """Save a matplotlib figure and close it."""
    output_path.parent.mkdir(parents=True, exist_ok=True)
    fig.tight_layout()
    fig.savefig(output_path, dpi=150)
    plt.close(fig)

"""Runnable EV population ETL pipeline.

Run from the project root with:

    python -m src.pipeline
"""

from pathlib import Path

from src.clean import clean_ev_population
from src.load import load_ev_population
from src.transform import build_summary_tables
from src.visualize import save_charts


RAW_DATA_PATH = Path("data/raw/ev_population.csv")
PROCESSED_DATA_PATH = Path("data/processed/ev_clean.csv")
SUMMARY_TABLES_DIR = Path("outputs/summary_tables")
CHARTS_DIR = Path("outputs/charts")


def run_pipeline() -> None:
    """Run the full EV population ETL pipeline."""
    raw_df = load_ev_population(RAW_DATA_PATH)
    clean_df = clean_ev_population(raw_df)

    PROCESSED_DATA_PATH.parent.mkdir(parents=True, exist_ok=True)
    clean_df.to_csv(PROCESSED_DATA_PATH, index=False)

    summaries = build_summary_tables(clean_df)
    SUMMARY_TABLES_DIR.mkdir(parents=True, exist_ok=True)
    for name, summary_df in summaries.items():
        summary_df.to_csv(SUMMARY_TABLES_DIR / f"{name}.csv", index=False)

    save_charts(summaries, CHARTS_DIR)

    print("EV population ETL pipeline completed successfully.")
    print(f"Clean data: {PROCESSED_DATA_PATH}")
    print(f"Summary tables: {SUMMARY_TABLES_DIR}")
    print(f"Charts: {CHARTS_DIR}")


if __name__ == "__main__":
    run_pipeline()

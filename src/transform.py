"""Summary table transformations for the EV population ETL pipeline."""

import pandas as pd


def summarize_by_make(df: pd.DataFrame) -> pd.DataFrame:
    """Return EV counts by manufacturer, highest count first."""
    return _count_by(df, "make", "vehicle_count")


def summarize_by_model_year(df: pd.DataFrame) -> pd.DataFrame:
    """Return EV counts by model year in ascending year order."""
    summary = _count_by(df, "model_year", "vehicle_count")
    return summary.sort_values("model_year").reset_index(drop=True)


def summarize_by_ev_type(df: pd.DataFrame) -> pd.DataFrame:
    """Return EV counts by electric vehicle type, highest count first."""
    return _count_by(df, "electric_vehicle_type", "vehicle_count")


def build_summary_tables(df: pd.DataFrame) -> dict[str, pd.DataFrame]:
    """Build all summary tables produced by the pipeline."""
    return {
        "ev_by_make": summarize_by_make(df),
        "ev_by_model_year": summarize_by_model_year(df),
        "ev_by_ev_type": summarize_by_ev_type(df),
    }


def _count_by(df: pd.DataFrame, column: str, count_name: str) -> pd.DataFrame:
    """Count records by a column with a clear error for missing fields."""
    if column not in df.columns:
        raise ValueError(f"Cannot summarize EV data because '{column}' is missing.")

    return (
        df.groupby(column, dropna=False)
        .size()
        .reset_index(name=count_name)
        .sort_values(count_name, ascending=False)
        .reset_index(drop=True)
    )

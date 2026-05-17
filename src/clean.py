"""Cleaning helpers for the EV population ETL pipeline."""

from datetime import datetime
import re

import pandas as pd


REQUIRED_COLUMNS = {"make", "model", "model_year", "electric_vehicle_type"}


def standardize_column_names(df: pd.DataFrame) -> pd.DataFrame:
    """Return a DataFrame with columns converted to snake_case names."""
    cleaned = df.copy()
    cleaned.columns = [_to_snake_case(column) for column in cleaned.columns]
    return cleaned


def clean_ev_population(df: pd.DataFrame) -> pd.DataFrame:
    """Clean the raw EV population data for summary analysis.

    The cleaning is intentionally conservative: it standardizes column names,
    trims text fields, removes rows missing core analysis fields, handles
    invalid model years, and fills obvious optional text gaps with "Unknown".
    """
    cleaned = standardize_column_names(df)
    _validate_required_columns(cleaned)

    text_columns = cleaned.select_dtypes(include="object").columns
    for column in text_columns:
        cleaned[column] = cleaned[column].str.strip()
        cleaned[column] = cleaned[column].replace(
            {"": pd.NA, "nan": pd.NA, "None": pd.NA, "N/A": pd.NA}
        )

    cleaned["model_year"] = pd.to_numeric(cleaned["model_year"], errors="coerce")
    current_year = datetime.now().year
    valid_year = cleaned["model_year"].between(1990, current_year + 1)
    cleaned = cleaned.loc[valid_year].copy()
    cleaned["model_year"] = cleaned["model_year"].astype("int64")

    if "electric_range" in cleaned.columns:
        cleaned["electric_range"] = pd.to_numeric(
            cleaned["electric_range"], errors="coerce"
        )
        cleaned.loc[cleaned["electric_range"] < 0, "electric_range"] = pd.NA

    cleaned = cleaned.dropna(subset=sorted(REQUIRED_COLUMNS))

    optional_text_columns = [
        "county",
        "city",
        "state",
        "electric_utility",
        "clean_alternative_fuel_vehicle_cafv_eligibility",
    ]
    for column in optional_text_columns:
        if column in cleaned.columns:
            cleaned[column] = cleaned[column].fillna("Unknown")

    return cleaned.reset_index(drop=True)


def _to_snake_case(column: str) -> str:
    """Convert a column name to a readable snake_case string."""
    column = column.strip().lower()
    column = column.replace("&", "and")
    column = re.sub(r"[^a-z0-9]+", "_", column)
    return column.strip("_")


def _validate_required_columns(df: pd.DataFrame) -> None:
    """Raise a clear error if expected CSV columns are missing after cleanup."""
    missing = REQUIRED_COLUMNS.difference(df.columns)
    if missing:
        missing_list = ", ".join(sorted(missing))
        available = ", ".join(df.columns)
        raise ValueError(
            "Raw EV population CSV is missing required columns after "
            f"standardization: {missing_list}. Available columns: {available}"
        )

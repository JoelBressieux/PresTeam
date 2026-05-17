"""Data loading helpers for the EV population ETL pipeline."""

from pathlib import Path

import pandas as pd


def load_ev_population(csv_path: Path) -> pd.DataFrame:
    """Load the raw EV population CSV into a pandas DataFrame.

    Args:
        csv_path: Relative path to the source CSV from the project root.

    Returns:
        A DataFrame containing the raw EV population data.

    Raises:
        FileNotFoundError: If the CSV file does not exist.
        ValueError: If pandas cannot read the CSV or the file is empty.
    """
    if not csv_path.exists():
        raise FileNotFoundError(
            f"Raw EV population file not found at '{csv_path}'. "
            "Expected the CSV at data/raw/ev_population.csv."
        )

    try:
        df = pd.read_csv(csv_path)
    except pd.errors.EmptyDataError as exc:
        raise ValueError(f"Raw EV population file is empty: '{csv_path}'.") from exc
    except pd.errors.ParserError as exc:
        raise ValueError(f"Could not parse raw EV population CSV: '{csv_path}'.") from exc
    except OSError as exc:
        raise ValueError(f"Could not read raw EV population CSV: '{csv_path}'.") from exc

    if df.empty:
        raise ValueError(f"Raw EV population CSV has no rows: '{csv_path}'.")

    return df

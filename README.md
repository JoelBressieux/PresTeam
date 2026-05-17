# EV Population ETL Demo

This repository contains a small Python ETL pipeline for the raw EV population
CSV at `data/raw/ev_population.csv`.

## Project Structure

- `src/`: pipeline modules for loading, cleaning, transforming, visualizing, and running the ETL.
- `tests/`: future automated tests.
- `data/raw/`: source data files.
- `data/processed/`: cleaned datasets created by the pipeline.
- `outputs/summary_tables/`: CSV summary tables created by the pipeline.
- `outputs/charts/`: PNG charts created by the pipeline.

## Run

Install dependencies:

```bash
pip install -r requirements.txt
```

Run the pipeline from the project root:

```bash
python -m src.pipeline
```

"""Pull fresh IESO demand + Toronto weather and rebuild data/processed/dataset.parquet.

Usage:
    python scripts/update_data.py              # last 3 years + current year
    python scripts/update_data.py --years 2023 2024 2025 2026
"""
import argparse
import sys
from datetime import date
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from ieso_lab.data import fetch_ieso_demand, fetch_weather  # noqa: E402
from ieso_lab.features import build_dataset  # noqa: E402
from ieso_lab.paths import DATASET_FILE  # noqa: E402


def main():
    this_year = date.today().year
    ap = argparse.ArgumentParser()
    ap.add_argument("--years", nargs="+", type=int,
                    default=list(range(this_year - 3, this_year + 1)))
    years = sorted(ap.parse_args().years)

    print(f"Fetching IESO demand for {years} ...")
    demand = fetch_ieso_demand(years)
    print(f"  {len(demand):,} hourly rows")

    print("Fetching Toronto weather ...")
    weather = fetch_weather(date(years[0], 1, 1), date.today())
    print(f"  {len(weather):,} hourly rows")

    df = build_dataset(demand, weather)
    df.to_parquet(DATASET_FILE, index=False)
    print(f"Saved {len(df):,} rows x {df.shape[1]} cols -> {DATASET_FILE}")
    print(f"Range: {df.timestamp_utc.min()} -> {df.timestamp_utc.max()}")


if __name__ == "__main__":
    main()

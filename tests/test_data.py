"""Run with:  pytest
These run automatically on every Pull Request (GitHub Actions, Stage 7)."""
import pandas as pd

from ieso_lab.data import parse_ieso_demand
from ieso_lab.features import add_weather_features

SAMPLE = """\\\\Hourly Demand Report,,,
\\\\Created at 2026-11-11 07:30:14,,,
\\\\For 2026,,,
Date,Hour,Market Demand,Ontario Demand
2026-01-01,1,19489,16526
2026-01-01,24,19317,16374
"""


def test_parse_skips_comment_lines():
    df = parse_ieso_demand(SAMPLE)
    assert len(df) == 2
    assert list(df.columns) == ["timestamp_utc", "demand_mw", "market_demand_mw"]


def test_hour_1_est_is_05_utc():
    df = parse_ieso_demand(SAMPLE)
    assert df["timestamp_utc"].iloc[0] == pd.Timestamp("2026-01-01 05:00", tz="UTC")
    # hour 24 = 23:00 EST = 04:00 UTC next day
    assert df["timestamp_utc"].iloc[1] == pd.Timestamp("2026-01-02 04:00", tz="UTC")


def test_degree_days():
    df = add_weather_features(pd.DataFrame({"temperature_2m": [10.0, 18.0, 25.0]}))
    assert df["hdd"].tolist() == [8.0, 0.0, 0.0]
    assert df["cdd"].tolist() == [0.0, 0.0, 7.0]

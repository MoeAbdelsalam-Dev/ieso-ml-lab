"""Turn raw demand + weather into a model-ready table (one row = one hour)."""
from __future__ import annotations

import holidays
import numpy as np
import pandas as pd

BASE_TEMP_C = 18.0  # standard heating/cooling balance point


def add_calendar(df: pd.DataFrame) -> pd.DataFrame:
    # IESO operates on EST (UTC-5) all year, so use that for calendar features.
    est = df["timestamp_utc"].dt.tz_convert("Etc/GMT+5")
    df["date_est"] = est.dt.date
    df["hour"] = est.dt.hour
    df["dayofweek"] = est.dt.dayofweek  # 0 = Monday
    df["month"] = est.dt.month
    df["is_weekend"] = (df["dayofweek"] >= 5).astype(int)
    on_holidays = holidays.CA(subdiv="ON", years=sorted(est.dt.year.unique()))
    df["is_holiday"] = df["date_est"].map(lambda d: int(d in on_holidays))
    return df


def add_weather_features(df: pd.DataFrame) -> pd.DataFrame:
    t = df["temperature_2m"]
    df["hdd"] = np.maximum(0, BASE_TEMP_C - t)  # heating degree (cold)
    df["cdd"] = np.maximum(0, t - BASE_TEMP_C)  # cooling degree (hot)
    return df


def add_lags(df: pd.DataFrame) -> pd.DataFrame:
    """Demand at the same hour yesterday / last week. Only valid if you would
    actually know them at prediction time (you do, for day-ahead forecasts)."""
    s = df.set_index("timestamp_utc")["demand_mw"]
    df["demand_lag_24h"] = df["timestamp_utc"].map(s.shift(24, freq="h"))
    df["demand_lag_168h"] = df["timestamp_utc"].map(s.shift(168, freq="h"))
    return df


def build_dataset(demand: pd.DataFrame, weather: pd.DataFrame) -> pd.DataFrame:
    df = demand.merge(weather, on="timestamp_utc", how="inner")
    df = add_calendar(df)
    df = add_weather_features(df)
    df = add_lags(df)
    return df.sort_values("timestamp_utc").reset_index(drop=True)


def add_peak_label(df: pd.DataFrame, threshold_mw: float) -> pd.DataFrame:
    """Classification target: 1 if the hour is a 'peak' hour.
    Pick threshold_mw from the TRAINING data only (see Module 2 - leakage)."""
    df["is_peak"] = (df["demand_mw"] >= threshold_mw).astype(int)
    return df

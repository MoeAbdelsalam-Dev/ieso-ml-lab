"""Live data pulls: IESO hourly Ontario demand + Toronto weather (Open-Meteo).

Everything is stored and joined in UTC to avoid daylight-saving bugs:
- IESO reports use Eastern Standard Time all year (no DST), hours 1-24 = "hour ending".
- Open-Meteo is requested in GMT (UTC).
"""
from __future__ import annotations

import io
from datetime import date, timedelta

import pandas as pd
import requests

from .paths import RAW_DIR

IESO_DEMAND_URL = "https://reports-public.ieso.ca/public/Demand/PUB_Demand{suffix}.csv"
WEATHER_ARCHIVE_URL = "https://archive-api.open-meteo.com/v1/archive"
WEATHER_FORECAST_URL = "https://api.open-meteo.com/v1/forecast"
TORONTO = {"latitude": 43.65, "longitude": -79.38}
WEATHER_VARS = ["temperature_2m", "relative_humidity_2m", "wind_speed_10m", "cloud_cover"]


# ---------------------------------------------------------------- IESO demand
def parse_ieso_demand(csv_text: str) -> pd.DataFrame:
    """Parse an IESO PUB_Demand CSV (3 comment lines starting with '\\')."""
    lines = [ln for ln in csv_text.splitlines() if not ln.startswith("\\")]
    df = pd.read_csv(io.StringIO("\n".join(lines)))
    df.columns = [c.strip() for c in df.columns]
    # Hour 1 = 00:00-01:00 EST. EST = UTC-5 all year -> add 5h to get UTC.
    start_est = pd.to_datetime(df["Date"]) + pd.to_timedelta(df["Hour"] - 1, unit="h")
    df["timestamp_utc"] = (start_est + pd.Timedelta(hours=5)).dt.tz_localize("UTC")
    df = df.rename(columns={"Ontario Demand": "demand_mw", "Market Demand": "market_demand_mw"})
    return df[["timestamp_utc", "demand_mw", "market_demand_mw"]]


def fetch_ieso_demand(years: list[int]) -> pd.DataFrame:
    """Download hourly demand for the given years (current year = live file)."""
    this_year = date.today().year
    frames = []
    for y in years:
        suffix = "" if y == this_year else f"_{y}"
        resp = requests.get(IESO_DEMAND_URL.format(suffix=suffix), timeout=60)
        resp.raise_for_status()
        (RAW_DIR / f"ieso_demand_{y}.csv").write_text(resp.text)  # keep raw copy
        frames.append(parse_ieso_demand(resp.text))
    return pd.concat(frames).drop_duplicates("timestamp_utc").sort_values("timestamp_utc")


# ---------------------------------------------------------------- Weather
def _weather_json_to_df(js: dict) -> pd.DataFrame:
    h = js["hourly"]
    df = pd.DataFrame(h)
    df["timestamp_utc"] = pd.to_datetime(df.pop("time")).dt.tz_localize("UTC")
    return df


def fetch_weather(start: date, end: date) -> pd.DataFrame:
    """Hourly Toronto weather. Archive lags ~5 days, so recent days + tomorrow
    come from the forecast endpoint (past_days)."""
    params = {**TORONTO, "hourly": ",".join(WEATHER_VARS), "timezone": "GMT"}
    archive_end = min(end, date.today() - timedelta(days=6))
    frames = []
    if start <= archive_end:
        r = requests.get(WEATHER_ARCHIVE_URL, timeout=60,
                         params={**params, "start_date": start.isoformat(),
                                 "end_date": archive_end.isoformat()})
        r.raise_for_status()
        frames.append(_weather_json_to_df(r.json()))
    r = requests.get(WEATHER_FORECAST_URL, timeout=60,
                     params={**params, "past_days": 10, "forecast_days": 2})
    r.raise_for_status()
    frames.append(_weather_json_to_df(r.json()))
    df = pd.concat(frames).drop_duplicates("timestamp_utc", keep="first")
    df = df.sort_values("timestamp_utc")
    df.to_csv(RAW_DIR / "weather_toronto.csv", index=False)
    return df

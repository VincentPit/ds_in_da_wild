"""
Phase 4 data cleaning.

Reads cached inputs from data/ and writes two analysis-ready CSVs:
  - data/phase4_borough_day.csv : one row per BOROUGH x Date (used for H1)
  - data/phase4_city_day.csv    : one row per Date            (used for H2, H3)

Inputs (all already on disk):
  - data/atvc_daily.csv                         (ATVC city-wide daily totals)
  - data/atvc_boro_daily.csv                    (ATVC borough-day totals)
  - data/Motor_Vehicle_Collisions_-_Crashes_*.csv  (NYPD raw crashes)
  - data/era5_nyc_daily.csv                     (Open-Meteo ERA5, pre-fetched)

Run:
    python phase4_clean.py
"""

from pathlib import Path
import sys
import numpy as np
import pandas as pd

DATA = Path(__file__).resolve().parent / "data"

CRASH_COLS = [
    "CRASH DATE", "BOROUGH", "COLLISION_ID",
    "NUMBER OF PERSONS INJURED", "NUMBER OF PERSONS KILLED",
    "NUMBER OF PEDESTRIANS INJURED", "NUMBER OF CYCLIST INJURED",
    "NUMBER OF MOTORIST INJURED",
]
NUMERIC_CRASH_COLS = CRASH_COLS[3:]


def _find_crashes_csv() -> Path:
    matches = sorted(DATA.glob("Motor_Vehicle_Collisions_-_Crashes_*.csv"))
    if not matches:
        sys.exit(f"ERROR: no Motor_Vehicle_Collisions_-_Crashes_*.csv in {DATA}")
    return matches[0]


def load_atvc_city() -> pd.DataFrame:
    p = DATA / "atvc_daily.csv"
    df = pd.read_csv(p, parse_dates=["Date"])
    df["daily_vol"] = pd.to_numeric(df["daily_vol"], errors="coerce")
    df["n_segments"] = pd.to_numeric(df["n_segments"], errors="coerce")
    df = df.dropna(subset=["Date", "daily_vol"]).copy()
    df["vol_M"] = df["daily_vol"] / 1_000_000.0
    return df.rename(columns={
        "daily_vol": "city_daily_volume",
        "n_segments": "city_seg_count",
    })[["Date", "city_daily_volume", "city_seg_count", "vol_M"]]


def load_atvc_boro() -> pd.DataFrame:
    p = DATA / "atvc_boro_daily.csv"
    df = pd.read_csv(p, parse_dates=["Date"])
    df["daily_vol"] = pd.to_numeric(df["daily_vol"], errors="coerce")
    df["n_segments"] = pd.to_numeric(df["n_segments"], errors="coerce")
    df = df.dropna(subset=["Date", "boro", "daily_vol"]).copy()
    df["BOROUGH"] = (
        df["boro"].astype(str).str.strip().str.upper()
        .replace({"THE BRONX": "BRONX"})
    )
    df = df[df["BOROUGH"].isin(["BRONX", "BROOKLYN", "MANHATTAN", "QUEENS", "STATEN ISLAND"])]
    return df.groupby(["Date", "BOROUGH"], as_index=False).agg(
        boro_daily_volume=("daily_vol", "sum"),
        boro_seg_count=("n_segments", "sum"),
    )


def load_crashes() -> pd.DataFrame:
    p = _find_crashes_csv()
    df = pd.read_csv(p, low_memory=False, usecols=CRASH_COLS)
    df["CRASH DATE"] = pd.to_datetime(df["CRASH DATE"], errors="coerce")
    df = df.dropna(subset=["CRASH DATE"]).copy()
    for c in NUMERIC_CRASH_COLS:
        df[c] = pd.to_numeric(df[c], errors="coerce").fillna(0)
    df["BOROUGH"] = df["BOROUGH"].astype(str).str.strip().str.upper()
    df.loc[~df["BOROUGH"].isin(
        ["BRONX", "BROOKLYN", "MANHATTAN", "QUEENS", "STATEN ISLAND"]
    ), "BOROUGH"] = pd.NA
    return df.rename(columns={"CRASH DATE": "Date"})


def load_weather() -> pd.DataFrame:
    p = DATA / "era5_nyc_daily.csv"
    df = pd.read_csv(p, parse_dates=["Date"])
    return df[["Date", "temp_F", "precip_mm"]]


def add_calendar_features(df: pd.DataFrame) -> pd.DataFrame:
    out = df.copy()
    out["year"] = out["Date"].dt.year
    out["month"] = out["Date"].dt.month
    out["dow_num"] = out["Date"].dt.dayofweek
    out["day_of_week"] = out["Date"].dt.day_name()
    out["is_weekend"] = out["dow_num"].isin([5, 6]).astype(int)
    return out


def build_borough_day_panel(crashes: pd.DataFrame, atvc_city: pd.DataFrame,
                            atvc_boro: pd.DataFrame, weather: pd.DataFrame) -> pd.DataFrame:
    boro_crash = (
        crashes.dropna(subset=["BOROUGH"])
        .groupby(["Date", "BOROUGH"], as_index=False)
        .agg(
            daily_crashes=("COLLISION_ID", "count"),
            persons_injured=("NUMBER OF PERSONS INJURED", "sum"),
            persons_killed=("NUMBER OF PERSONS KILLED", "sum"),
            ped_injured=("NUMBER OF PEDESTRIANS INJURED", "sum"),
            cyc_injured=("NUMBER OF CYCLIST INJURED", "sum"),
            motorist_injured=("NUMBER OF MOTORIST INJURED", "sum"),
        )
    )

    # Inner-join on the set of dates that has city-wide ATVC AND crash data.
    panel = boro_crash.merge(atvc_city, on="Date", how="inner")
    panel = panel.merge(atvc_boro, on=["Date", "BOROUGH"], how="left")
    panel = panel.merge(weather, on="Date", how="left")
    panel = add_calendar_features(panel)

    panel = panel[[
        "Date", "BOROUGH",
        "daily_crashes", "persons_injured", "persons_killed",
        "ped_injured", "cyc_injured", "motorist_injured",
        "city_daily_volume", "city_seg_count", "vol_M",
        "boro_daily_volume", "boro_seg_count",
        "temp_F", "precip_mm",
        "year", "month", "dow_num", "day_of_week", "is_weekend",
    ]].sort_values(["Date", "BOROUGH"]).reset_index(drop=True)
    return panel


def build_city_day_panel(crashes: pd.DataFrame, atvc_city: pd.DataFrame,
                         weather: pd.DataFrame) -> pd.DataFrame:
    city_crash = (
        crashes.groupby("Date", as_index=False).agg(
            daily_crashes=("COLLISION_ID", "count"),
            persons_injured=("NUMBER OF PERSONS INJURED", "sum"),
            persons_killed=("NUMBER OF PERSONS KILLED", "sum"),
            ped_injured=("NUMBER OF PEDESTRIANS INJURED", "sum"),
            cyc_injured=("NUMBER OF CYCLIST INJURED", "sum"),
            motorist_injured=("NUMBER OF MOTORIST INJURED", "sum"),
        )
    )
    df = city_crash.merge(atvc_city, on="Date", how="inner")
    df = df.merge(weather, on="Date", how="left")
    df = add_calendar_features(df)
    df["injury_rate"] = np.where(
        df["daily_crashes"] > 0,
        df["persons_injured"] / df["daily_crashes"],
        np.nan,
    )
    df["total_inj_by_type"] = df["ped_injured"] + df["cyc_injured"] + df["motorist_injured"]
    return df.sort_values("Date").reset_index(drop=True)


def main() -> None:
    print("Loading inputs...")
    atvc_city = load_atvc_city()
    atvc_boro = load_atvc_boro()
    crashes = load_crashes()
    weather = load_weather()

    print(f"  ATVC city:    {len(atvc_city):,} days  ({atvc_city.Date.min().date()} -> {atvc_city.Date.max().date()})")
    print(f"  ATVC boro:    {len(atvc_boro):,} rows  ({atvc_boro.BOROUGH.nunique()} boroughs)")
    print(f"  Crashes raw:  {len(crashes):,} rows")
    print(f"  Weather ERA5: {len(weather):,} days")

    print("\nBuilding borough-day panel for H1 ...")
    boro_panel = build_borough_day_panel(crashes, atvc_city, atvc_boro, weather)
    print(f"  borough-day panel: {len(boro_panel):,} rows  "
          f"({boro_panel.Date.nunique()} dates x {boro_panel.BOROUGH.nunique()} boroughs)")
    print(f"  weather coverage:  temp {boro_panel.temp_F.notna().sum()}/{len(boro_panel)}  "
          f"precip {boro_panel.precip_mm.notna().sum()}/{len(boro_panel)}")

    print("\nBuilding city-day panel for H2 / H3 ...")
    city_panel = build_city_day_panel(crashes, atvc_city, weather)
    print(f"  city-day panel: {len(city_panel):,} rows  "
          f"({city_panel.Date.min().date()} -> {city_panel.Date.max().date()})")
    print(f"  weather coverage: temp {city_panel.temp_F.notna().sum()}/{len(city_panel)}  "
          f"precip {city_panel.precip_mm.notna().sum()}/{len(city_panel)}")
    print(f"  zero-crash days:  {(city_panel.daily_crashes == 0).sum()}")

    out_boro = DATA / "phase4_borough_day.csv"
    out_city = DATA / "phase4_city_day.csv"
    boro_panel.to_csv(out_boro, index=False)
    city_panel.to_csv(out_city, index=False)
    print(f"\nWrote {out_boro}")
    print(f"Wrote {out_city}")


if __name__ == "__main__":
    main()

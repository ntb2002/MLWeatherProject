"""Load and clean EPA AQS daily data for Los Angeles."""

from __future__ import annotations

from pathlib import Path

import pandas as pd


def load_epa_year(filepath):
    """Load one year of EPA AQS CSV and return daily max AQI for LA.

    Applies fixed filters (California, Los Angeles County, Los Angeles city,
    24-hour samples), then aggregates to one row per calendar day using the
    maximum AQI observed that day.

    Parameters
    ----------
    filepath : str or pathlib.Path
        Path to a daily EPA AQS CSV file (e.g. ``daily_88101_2023.csv``).

    Returns
    -------
    pandas.DataFrame
        Two columns: ``Date Local`` (parsed as datetime) and ``AQI`` (numeric).
        One row per day after filtering and aggregation.

    Notes
    -----
    We take the **maximum** AQI per day—not the mean—because the Air Quality
    Index is a regulatory health metric designed around the **worst** air
    quality experienced in that period. The mean would dilute peak pollution
    and understate exposure risk; the daily AQI summary is intended to reflect
    the most protective (i.e. highest) index value when multiple valid
    observations exist for the same day.

    """
    path = Path(filepath)
    df = pd.read_csv(path, low_memory=False)

    mask = (
        (df["State Name"] == "California")
        & (df["County Name"] == "Los Angeles")
        & (df["City Name"] == "Los Angeles")
        & (df["Sample Duration"] == "24 HOUR")
    )
    filtered = df.loc[mask]
    out = filtered.groupby("Date Local", as_index=False)["AQI"].max()
    out["Date Local"] = pd.to_datetime(out["Date Local"])
    return out


def load_all_years(data_folder):
    """Load every EPA CSV in a folder and merge into one time-ordered series.

    Parameters
    ----------
    data_folder : str or pathlib.Path
        Directory containing one or more daily EPA AQS ``*.csv`` files.

    Returns
    -------
    pandas.DataFrame
        Concatenation of :func:`load_epa_year` for each CSV, sorted by
        ``Date Local`` ascending. Columns are ``Date Local`` and ``AQI``.

    Notes
    -----
    Per-day aggregation uses **max** AQI for the same rationale as
    :func:`load_epa_year`: AQI communicates worst-case conditions for health
    guidance; averaging would not match that intent.

    """
    folder = Path(data_folder)
    paths = sorted(folder.glob("*.csv"))
    if not paths:
        return pd.DataFrame(columns=["Date Local", "AQI"])

    parts = [load_epa_year(p) for p in paths]
    combined = pd.concat(parts, ignore_index=True)
    combined = combined.sort_values("Date Local", kind="mergesort").reset_index(
        drop=True
    )
    return combined


def load_ozone_year(filepath):
    """Load one year of EPA AQS ozone data and return daily max AQI for LA.

    Parameters
    ----------
    filepath : str or pathlib.Path
        Path to a daily EPA AQS ozone CSV file (parameter ``44201``).

    Returns
    -------
    pandas.DataFrame
        Two columns: ``Date Local`` (datetime) and ``ozone_aqi`` (numeric),
        with one row per day after filtering and aggregation.
    """
    path = Path(filepath)
    df = pd.read_csv(path, low_memory=False)

    mask = (
        (df["State Name"] == "California")
        & (df["County Name"] == "Los Angeles")
        & (df["City Name"] == "Los Angeles")
        & (df["Sample Duration"] == "8-HR RUN AVG BEGIN HOUR")
    )
    filtered = df.loc[mask]
    out = filtered.groupby("Date Local", as_index=False)["AQI"].max()
    out = out.rename(columns={"AQI": "ozone_aqi"})
    out["Date Local"] = pd.to_datetime(out["Date Local"])
    return out


def load_all_ozone_years(data_folder):
    """Load all EPA AQS ozone CSVs in a folder and combine to one series.

    Parameters
    ----------
    data_folder : str or pathlib.Path
        Directory containing one or more daily EPA AQS ozone ``*.csv`` files.

    Returns
    -------
    pandas.DataFrame
        Concatenation of :func:`load_ozone_year` for each CSV, sorted by
        ``Date Local`` ascending. Columns are ``Date Local`` and ``ozone_aqi``.
    """
    folder = Path(data_folder)
    paths = sorted(folder.glob("*.csv"))
    if not paths:
        return pd.DataFrame(columns=["Date Local", "ozone_aqi"])

    parts = [load_ozone_year(p) for p in paths]
    combined = pd.concat(parts, ignore_index=True)
    combined = combined.sort_values("Date Local", kind="mergesort").reset_index(
        drop=True
    )
    return combined

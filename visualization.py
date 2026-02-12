"""Matplotlib visualizations for the CityBike platform."""

from __future__ import annotations

import matplotlib.pyplot as plt
import pandas as pd
from pathlib import Path

FIGURES_DIR = Path(__file__).resolve().parent / "output" / "figures"


def _save_figure(fig: plt.Figure, filename: str) -> None:
    FIGURES_DIR.mkdir(parents=True, exist_ok=True)
    filepath = FIGURES_DIR / filename
    fig.savefig(filepath, dpi=150, bbox_inches="tight")
    plt.close(fig)
    print(f"Saved: {filepath}")


def plot_trips_per_station(trips: pd.DataFrame, stations: pd.DataFrame) -> None:
    counts = (
        trips["start_station_id"]
        .value_counts()
        .head(10)
        .rename_axis("station_id")
        .reset_index(name="trip_count")
    )
    merged = counts.merge(
        stations[["station_id", "station_name"]],
        on="station_id",
        how="left",
    )
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.barh(merged["station_name"], merged["trip_count"])
    ax.set_xlabel("Number of Trips")
    ax.set_ylabel("Station")
    ax.set_title("Top 10 Start Stations by Trip Count")
    ax.invert_yaxis()
    _save_figure(fig, "trips_per_station.png")


def plot_monthly_trend(trips: pd.DataFrame) -> None:
    df = trips.copy()
    df["year_month"] = df["start_time"].dt.to_period("M").dt.to_timestamp()
    monthly = df.groupby("year_month")["trip_id"].count().sort_index()
    fig, ax = plt.subplots(figsize=(10, 4))
    ax.plot(monthly.index, monthly.values, marker="o")
    ax.set_title("Monthly Trip Volume Trend")
    ax.set_xlabel("Month")
    ax.set_ylabel("Trip count")
    ax.grid(True, linestyle="--", alpha=0.3)
    _save_figure(fig, "monthly_trend.png")


def plot_duration_histogram(trips: pd.DataFrame) -> None:
    durations = trips["duration_minutes"].dropna()
    fig, ax = plt.subplots(figsize=(8, 4))
    ax.hist(durations, bins=30)
    ax.set_title("Trip Duration Distribution")
    ax.set_xlabel("Duration (minutes)")
    ax.set_ylabel("Number of trips")
    _save_figure(fig, "duration_histogram.png")


def plot_duration_by_user_type(trips: pd.DataFrame) -> None:
    df = trips[["user_type", "duration_minutes"]].dropna()
    groups = [g["duration_minutes"].to_numpy() for _, g in df.groupby("user_type")]
    labels = [name for name, _ in df.groupby("user_type")]
    fig, ax = plt.subplots(figsize=(7, 4))
    ax.boxplot(groups, labels=labels, showfliers=True)
    ax.set_title("Trip Duration by User Type")
    ax.set_xlabel("User type")
    ax.set_ylabel("Duration (minutes)")
    _save_figure(fig, "duration_by_user_type.png")

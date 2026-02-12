"""Synthetic data generator for the CityBike project.

Run:
    python generate_data.py

Generates raw CSV files into citybike/data/:
    - stations.csv
    - trips.csv
    - maintenance.csv
"""

from __future__ import annotations

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from pathlib import Path

np.random.seed(42)

DATA_DIR = Path(__file__).resolve().parent / "data"
DATA_DIR.mkdir(parents=True, exist_ok=True)

station_names = [
    "Central Station", "University Campus", "City Hall",
    "Riverside Park", "Market Square", "Tech Hub",
    "Old Town", "Harbor View", "Sports Arena",
    "West End", "North Gate", "Museum Quarter",
    "Business District", "Lakeside", "Airport Terminal"
]

stations = []
for i, name in enumerate(station_names):
    stations.append({
        "station_id": f"ST{100 + i}",
        "station_name": name,
        "capacity": int(np.random.choice([10, 15, 20, 25, 30])),
        "latitude": round(48.75 + np.random.uniform(0, 0.15), 6),
        "longitude": round(9.15 + np.random.uniform(0, 0.15), 6),
    })

stations_df = pd.DataFrame(stations)
stations_df.to_csv(DATA_DIR / "stations.csv", index=False)

n_trips = 1500
user_ids = [f"USR{np.random.randint(1000, 1200)}" for _ in range(80)]
bike_ids = [f"BK{np.random.randint(200, 350)}" for _ in range(60)]
start_date = datetime(2024, 1, 1)

trips = []
for i in range(n_trips):
    user_type = np.random.choice(["casual", "member"], p=[0.35, 0.65])
    bike_type = np.random.choice(["classic", "electric"], p=[0.6, 0.4])
    start_st = np.random.choice(stations_df["station_id"])
    end_st = np.random.choice(stations_df["station_id"])
    start_time = start_date + timedelta(
        days=int(np.random.randint(0, 365)),
        hours=int(np.random.randint(6, 23)),
        minutes=int(np.random.randint(0, 60)),
    )
    duration = max(2, float(np.random.exponential(25)))
    end_time = start_time + timedelta(minutes=duration)
    distance = round(float(np.random.uniform(0.5, 15.0)), 2)
    status = np.random.choice(["completed", "cancelled", np.nan], p=[0.82, 0.12, 0.06])

    trips.append({
        "trip_id": f"TR{10000 + i}",
        "user_id": str(np.random.choice(user_ids)),
        "user_type": str(user_type),
        "bike_id": str(np.random.choice(bike_ids)),
        "bike_type": str(bike_type),
        "start_station_id": str(start_st),
        "end_station_id": str(end_st),
        "start_time": start_time.strftime("%Y-%m-%d %H:%M:%S"),
        "end_time": end_time.strftime("%Y-%m-%d %H:%M:%S"),
        "duration_minutes": round(duration, 1),
        "distance_km": distance,
        "status": status,
    })

trips_df = pd.DataFrame(trips)

# Inject messiness
idx = np.random.choice(n_trips, 30, replace=False)
trips_df.loc[idx[:10], "duration_minutes"] = np.nan
trips_df.loc[idx[10:20], "distance_km"] = np.nan
trips_df.loc[idx[20:25], "end_time"] = trips_df.loc[idx[20:25], "start_time"]

dup_rows = trips_df.sample(15, random_state=42)
trips_df = pd.concat([trips_df, dup_rows], ignore_index=True)
trips_df.to_csv(DATA_DIR / "trips.csv", index=False)

maint_types = [
    "tire_repair", "brake_adjustment",
    "battery_replacement", "chain_lubrication",
    "general_inspection"
]

records = []
for i in range(200):
    bike = str(np.random.choice(bike_ids))
    btype = str(np.random.choice(["classic", "electric"]))
    mtype = str(np.random.choice(maint_types))
    cost = round(float(np.random.uniform(10, 150)), 2)
    if mtype == "battery_replacement":
        cost = round(float(np.random.uniform(80, 250)), 2)
        btype = "electric"

    records.append({
        "record_id": f"MR{5000 + i}",
        "bike_id": bike,
        "bike_type": btype,
        "date": (start_date + timedelta(days=int(np.random.randint(0, 365)))).strftime("%Y-%m-%d"),
        "maintenance_type": mtype,
        "cost": cost,
        "description": f"{mtype.replace('_', ' ').title()} for bike {bike}",
    })

maint_df = pd.DataFrame(records)
maint_df.loc[np.random.choice(200, 8, replace=False), "cost"] = np.nan
maint_df.to_csv(DATA_DIR / "maintenance.csv", index=False)

print("Generated: data/stations.csv, data/trips.csv, data/maintenance.csv")

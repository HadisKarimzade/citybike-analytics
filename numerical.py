"""NumPy-based numerical computations for the CityBike platform."""

from __future__ import annotations

import numpy as np


def station_distance_matrix(latitudes: np.ndarray, longitudes: np.ndarray) -> np.ndarray:
    """Compute pairwise Euclidean distances between stations (flat-earth)."""
    lat = np.asarray(latitudes, dtype=float)
    lon = np.asarray(longitudes, dtype=float)
    lat_diff = lat[:, np.newaxis] - lat[np.newaxis, :]
    lon_diff = lon[:, np.newaxis] - lon[np.newaxis, :]
    return np.sqrt(lat_diff ** 2 + lon_diff ** 2)


def trip_duration_stats(durations: np.ndarray) -> dict[str, float]:
    """Compute summary stats for durations."""
    d = np.asarray(durations, dtype=float)
    return {
        "mean": float(np.mean(d)),
        "median": float(np.median(d)),
        "std": float(np.std(d)),
        "p25": float(np.percentile(d, 25)),
        "p75": float(np.percentile(d, 75)),
        "p90": float(np.percentile(d, 90)),
    }


def detect_outliers_zscore(values: np.ndarray, threshold: float = 3.0) -> np.ndarray:
    """Return boolean mask where |z| > threshold."""
    v = np.asarray(values, dtype=float)
    mean = float(np.mean(v))
    std = float(np.std(v))
    if std == 0.0:
        return np.zeros_like(v, dtype=bool)
    z = (v - mean) / std
    return np.abs(z) >= float(threshold)


def calculate_fares(
    durations: np.ndarray,
    distances: np.ndarray,
    per_minute: float,
    per_km: float,
    unlock_fee: float = 0.0,
) -> np.ndarray:
    """Vectorized fare calculation (no loops)."""
    durs = np.asarray(durations, dtype=float)
    dists = np.asarray(distances, dtype=float)
    return float(unlock_fee) + float(per_minute) * durs + float(per_km) * dists

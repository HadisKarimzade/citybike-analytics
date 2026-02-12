"""Utility helpers for the CityBike platform.

Pure helper functions for validation, parsing, and formatting.
"""

from __future__ import annotations  # باعث می‌شه type hintها به‌صورت رشته (lazy) تفسیر بشن.

import re
from datetime import datetime
from typing import Any

DATE_FORMAT = "%Y-%m-%d"
DATETIME_FORMAT = "%Y-%m-%d %H:%M:%S"

VALID_BIKE_TYPES = {"classic", "electric"}
VALID_USER_TYPES = {"casual", "member"}
VALID_TRIP_STATUSES = {"completed", "cancelled"}
VALID_MAINTENANCE_TYPES = {
    "tire_repair",
    "brake_adjustment",
    "battery_replacement",
    "chain_lubrication",
    "general_inspection",
}


def validate_positive(value: float, name: str = "value") -> float:
    """Ensure *value* is a positive number."""
    if value <= 0:
        raise ValueError(f"{name} must be positive, got {value}")
    return value


def validate_non_negative(value: float, name: str = "value") -> float:
    """Ensure *value* is >= 0."""
    if value < 0:
        raise ValueError(f"{name} must be non-negative, got {value}")
    return value


def validate_email(email: str) -> str:
    """Basic email validation."""
    if not isinstance(email, str) or "@" not in email:
        raise ValueError(f"Invalid email: {email!r}")
    return email


def validate_in(value: Any, allowed: set, name: str = "value") -> Any:
    """Ensure *value* is in *allowed*."""
    if value not in allowed:
        raise ValueError(f"{name} must be one of {allowed}, got {value!r}")
    return value


def parse_datetime(text: str) -> datetime:
    """Parse a datetime string in YYYY-MM-DD HH:MM:SS format."""
    return datetime.strptime(text, DATETIME_FORMAT)


def parse_date(text: str) -> datetime:
    """Parse a date string in YYYY-MM-DD format."""
    return datetime.strptime(text, DATE_FORMAT)


def fmt_duration(minutes: float) -> str:
    """Format minutes as 'Xh Ym'."""
    h = int(minutes // 60)
    m = int(minutes % 60)
    return f"{h}h {m}m"


def fmt_currency(amount: float) -> str:
    """Format euros with 2 decimals."""
    return f"€{amount:.2f}"


def slug(text: str) -> str:
    """Simple slugifier for filenames."""
    text = text.strip().lower()
    text = re.sub(r"[^a-z0-9]+", "_", text)
    return text.strip("_")

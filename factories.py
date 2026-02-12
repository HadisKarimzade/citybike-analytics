"""Factory Pattern — create domain objects from raw dictionaries."""

from __future__ import annotations

from datetime import datetime

from models import Bike, ClassicBike, ElectricBike, User, CasualUser, MemberUser


def create_bike(data: dict) -> Bike:
    bike_type = str(data.get("bike_type", "")).lower().strip()
    if bike_type == "classic":
        return ClassicBike(
            bike_id=data["bike_id"],
            gear_count=int(data.get("gear_count", 7)),
        )
    if bike_type == "electric":
        return ElectricBike(
            bike_id=data["bike_id"],
            battery_level=float(data.get("battery_level", 100.0)),
            max_range_km=float(data.get("max_range_km", 50.0)),
        )
    raise ValueError(f"Unknown bike_type: {bike_type!r}")


def create_user(data: dict) -> User:
    """Create a User (CasualUser or MemberUser) from a data dictionary."""
    user_type = str(data.get("user_type", "")).lower().strip()
    if user_type == "casual":
        return CasualUser(
            user_id=data["user_id"],
            name=data.get("name", f"User {data['user_id']}"),
            email=data.get("email", f"{data['user_id'].lower()}@example.com"),
            day_pass_count=int(data.get("day_pass_count", 0)),
        )
    if user_type == "member":
        start = data.get("membership_start")
        end = data.get("membership_end")
        tier = str(data.get("tier", "basic")).lower().strip() or "basic"

        if isinstance(start, str):
            start_dt = datetime.fromisoformat(start)
        elif start is None:
            start_dt = datetime.now()
        else:
            start_dt = start

        if isinstance(end, str):
            end_dt = datetime.fromisoformat(end)
        elif end is None:
            end_dt = start_dt.replace(year=start_dt.year + 1)
        else:
            end_dt = end

        return MemberUser(
            user_id=data["user_id"],
            name=data.get("name", f"User {data['user_id']}"),
            email=data.get("email", f"{data['user_id'].lower()}@example.com"),
            membership_start=start_dt,
            membership_end=end_dt,
            tier=tier,
        )
    raise ValueError(f"Unknown user_type: {user_type!r}")

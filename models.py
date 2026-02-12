"""Domain models for the CityBike Bike-Sharing Analytics platform."""

from __future__ import annotations

from abc import ABC, abstractmethod
from datetime import datetime
from typing import Optional

from utils import (
    VALID_BIKE_TYPES,
    VALID_TRIP_STATUSES,
    VALID_USER_TYPES,
    VALID_MAINTENANCE_TYPES,
    validate_email,
    validate_in,
    validate_non_negative,
    validate_positive,
)


class Entity(ABC):
    """Abstract base class for all domain entities."""

    def __init__(self, id: str, created_at: datetime | None = None) -> None:
        if not id or not isinstance(id, str):
            raise ValueError("id must be a non-empty string")
        self._id = id
        self._created_at = created_at or datetime.now()

    @property
    def id(self) -> str:
        return self._id

    @property
    def created_at(self) -> datetime:
        return self._created_at

    @abstractmethod
    def __str__(self) -> str: ...

    @abstractmethod
    def __repr__(self) -> str: ...


class Bike(Entity):
    """Represents a bike."""

    VALID_STATUSES = {"available", "in_use", "maintenance"}

    def __init__(self, bike_id: str, bike_type: str, status: str = "available") -> None:
        super().__init__(id=bike_id)
        validate_in(bike_type, VALID_BIKE_TYPES, "bike_type")
        validate_in(status, self.VALID_STATUSES, "status")
        self._bike_type = bike_type
        self._status = status

    @property
    def bike_type(self) -> str:
        return self._bike_type

    @property
    def status(self) -> str:
        return self._status

    @status.setter
    def status(self, value: str) -> None:
        validate_in(value, self.VALID_STATUSES, "status")
        self._status = value

    def __str__(self) -> str:
        return f"Bike({self.id}, {self.bike_type}, {self.status})"

    def __repr__(self) -> str:
        return f"Bike(bike_id={self.id!r}, bike_type={self.bike_type!r}, status={self.status!r})"


class ClassicBike(Bike):
    def __init__(self, bike_id: str, gear_count: int = 7, status: str = "available") -> None:
        super().__init__(bike_id=bike_id, bike_type="classic", status=status)
        if not isinstance(gear_count, int) or gear_count <= 0:
            raise ValueError("gear_count must be a positive int")
        self._gear_count = gear_count

    @property
    def gear_count(self) -> int:
        return self._gear_count

    def __str__(self) -> str:
        return f"ClassicBike({self.id}, gears={self.gear_count}, status={self.status})"

    def __repr__(self) -> str:
        return f"ClassicBike(bike_id={self.id!r}, gear_count={self.gear_count}, status={self.status!r})"


class ElectricBike(Bike):
    def __init__(
        self,
        bike_id: str,
        battery_level: float = 100.0,
        max_range_km: float = 50.0,
        status: str = "available",
    ) -> None:
        super().__init__(bike_id=bike_id, bike_type="electric", status=status)
        if not isinstance(battery_level, (int, float)) or not (0.0 <= float(battery_level) <= 100.0):
            raise ValueError("battery_level must be between 0 and 100")
        validate_positive(float(max_range_km), "max_range_km")
        self._battery_level = float(battery_level)
        self._max_range_km = float(max_range_km)

    @property
    def battery_level(self) -> float:
        return self._battery_level

    @battery_level.setter
    def battery_level(self, value: float) -> None:
        if not (0.0 <= float(value) <= 100.0):
            raise ValueError("battery_level must be between 0 and 100")
        self._battery_level = float(value)

    @property
    def max_range_km(self) -> float:
        return self._max_range_km

    def __str__(self) -> str:
        return (
            f"ElectricBike({self.id}, battery={self.battery_level:.1f}%, "
            f"range={self.max_range_km:.1f}km, status={self.status})"
        )

    def __repr__(self) -> str:
        return (
            f"ElectricBike(bike_id={self.id!r}, battery_level={self.battery_level}, "
            f"max_range_km={self.max_range_km}, status={self.status!r})"
        )


class Station(Entity):
    def __init__(self, station_id: str, name: str, capacity: int, latitude: float, longitude: float) -> None:
        super().__init__(id=station_id)
        if not isinstance(name, str) or not name.strip():
            raise ValueError("name must be a non-empty string")
        if not isinstance(capacity, int) or capacity <= 0:
            raise ValueError("capacity must be a positive int")
        lat = float(latitude)
        lon = float(longitude)
        if not (-90.0 <= lat <= 90.0):
            raise ValueError("latitude must be in [-90, 90]")
        if not (-180.0 <= lon <= 180.0):
            raise ValueError("longitude must be in [-180, 180]")
        self._name = name.strip()
        self._capacity = capacity
        self._latitude = lat
        self._longitude = lon

    @property
    def name(self) -> str:
        return self._name

    @property
    def capacity(self) -> int:
        return self._capacity

    @property
    def latitude(self) -> float:
        return self._latitude

    @property
    def longitude(self) -> float:
        return self._longitude

    def __str__(self) -> str:
        return f"Station({self.id}, {self.name}, cap={self.capacity})"

    def __repr__(self) -> str:
        return (
            f"Station(station_id={self.id!r}, name={self.name!r}, capacity={self.capacity}, "
            f"latitude={self.latitude}, longitude={self.longitude})"
        )


class User(Entity):
    def __init__(self, user_id: str, name: str, email: str, user_type: str) -> None:
        super().__init__(id=user_id)
        if not isinstance(name, str) or not name.strip():
            raise ValueError("name must be a non-empty string")
        validate_email(email)
        validate_in(user_type, VALID_USER_TYPES, "user_type")
        self._name = name.strip()
        self._email = email.strip()
        self._user_type = user_type

    @property
    def name(self) -> str:
        return self._name

    @property
    def email(self) -> str:
        return self._email

    @property
    def user_type(self) -> str:
        return self._user_type

    def __str__(self) -> str:
        return f"User({self.id}, {self.name}, {self.user_type})"

    def __repr__(self) -> str:
        return f"User(user_id={self.id!r}, name={self.name!r}, email={self.email!r}, user_type={self.user_type!r})"


class CasualUser(User):
    def __init__(self, user_id: str, name: str, email: str, day_pass_count: int = 0) -> None:
        super().__init__(user_id=user_id, name=name, email=email, user_type="casual")
        if not isinstance(day_pass_count, int) or day_pass_count < 0:
            raise ValueError("day_pass_count must be an int >= 0")
        self._day_pass_count = day_pass_count

    @property
    def day_pass_count(self) -> int:
        return self._day_pass_count

    def __str__(self) -> str:
        return f"CasualUser({self.id}, passes={self.day_pass_count})"

    def __repr__(self) -> str:
        return (
            f"CasualUser(user_id={self.id!r}, name={self.name!r}, email={self.email!r}, "
            f"day_pass_count={self.day_pass_count})"
        )


class MemberUser(User):
    def __init__(
        self,
        user_id: str,
        name: str,
        email: str,
        membership_start: datetime | None = None,
        membership_end: datetime | None = None,
        tier: str = "basic",
    ) -> None:
        super().__init__(user_id=user_id, name=name, email=email, user_type="member")
        if tier not in {"basic", "premium"}:
            raise ValueError("tier must be 'basic' or 'premium'")
        start = membership_start or datetime.now()
        end = membership_end or start.replace(year=start.year + 1)
        if end <= start:
            raise ValueError("membership_end must be after membership_start")
        self._membership_start = start
        self._membership_end = end
        self._tier = tier

    @property
    def membership_start(self) -> datetime:
        return self._membership_start

    @property
    def membership_end(self) -> datetime:
        return self._membership_end

    @property
    def tier(self) -> str:
        return self._tier

    def __str__(self) -> str:
        return f"MemberUser({self.id}, tier={self.tier})"

    def __repr__(self) -> str:
        return (
            f"MemberUser(user_id={self.id!r}, name={self.name!r}, email={self.email!r}, "
            f"membership_start={self.membership_start!r}, membership_end={self.membership_end!r}, tier={self.tier!r})"
        )


class Trip:
    def __init__(
        self,
        trip_id: str,
        user: User,
        bike: Bike,
        start_station: Station,
        end_station: Station,
        start_time: datetime,
        end_time: datetime,
        distance_km: float,
        status: str = "completed",
    ) -> None:
        if not trip_id or not isinstance(trip_id, str):
            raise ValueError("trip_id must be a non-empty string")
        if end_time < start_time:
            raise ValueError("end_time must be >= start_time")
        validate_non_negative(float(distance_km), "distance_km")
        validate_in(status, VALID_TRIP_STATUSES, "status")
        self.trip_id = trip_id
        self.user = user
        self.bike = bike
        self.start_station = start_station
        self.end_station = end_station
        self.start_time = start_time
        self.end_time = end_time
        self.distance_km = float(distance_km)
        self.status = status

    @property
    def duration_minutes(self) -> float:
        delta = self.end_time - self.start_time
        return delta.total_seconds() / 60.0

    def __str__(self) -> str:
        return f"Trip({self.trip_id}, {self.user.id}->{self.start_station.id}->{self.end_station.id}, {self.duration_minutes:.1f}min)"

    def __repr__(self) -> str:
        return (
            f"Trip(trip_id={self.trip_id!r}, user={self.user!r}, bike={self.bike!r}, "
            f"start_station={self.start_station!r}, end_station={self.end_station!r}, "
            f"start_time={self.start_time!r}, end_time={self.end_time!r}, distance_km={self.distance_km}, status={self.status!r})"
        )


class MaintenanceRecord:
    VALID_TYPES = VALID_MAINTENANCE_TYPES

    def __init__(
        self,
        record_id: str,
        bike: Bike,
        date: datetime,
        maintenance_type: str,
        cost: float,
        description: str = "",
    ) -> None:
        if not record_id or not isinstance(record_id, str):
            raise ValueError("record_id must be a non-empty string")
        validate_in(maintenance_type, self.VALID_TYPES, "maintenance_type")
        validate_non_negative(float(cost), "cost")
        self.record_id = record_id
        self.bike = bike
        self.date = date
        self.maintenance_type = maintenance_type
        self.cost = float(cost)
        self.description = str(description or "")

    def __str__(self) -> str:
        return f"MaintenanceRecord({self.record_id}, bike={self.bike.id}, type={self.maintenance_type}, cost={self.cost:.2f})"

    def __repr__(self) -> str:
        return (
            f"MaintenanceRecord(record_id={self.record_id!r}, bike={self.bike!r}, date={self.date!r}, "
            f"maintenance_type={self.maintenance_type!r}, cost={self.cost}, description={self.description!r})"
        )

"""Pricing strategies for trip cost calculation (Strategy Pattern)."""

from __future__ import annotations

from abc import ABC, abstractmethod


class PricingStrategy(ABC):
    """Abstract pricing strategy — computes the cost of a trip."""

    @abstractmethod
    def calculate_cost(self, duration_minutes: float, distance_km: float) -> float:
        ...


class CasualPricing(PricingStrategy):
    """Pricing for casual users."""
    UNLOCK_FEE = 1.00
    PER_MINUTE = 0.15
    PER_KM = 0.10

    def calculate_cost(self, duration_minutes: float, distance_km: float) -> float:
        return self.UNLOCK_FEE + self.PER_MINUTE * duration_minutes + self.PER_KM * distance_km


class MemberPricing(PricingStrategy):
    """Pricing for member users — discounted rates."""
    PER_MINUTE = 0.08
    PER_KM = 0.05

    def calculate_cost(self, duration_minutes: float, distance_km: float) -> float:
        return self.PER_MINUTE * duration_minutes + self.PER_KM * distance_km


class PeakHourPricing(PricingStrategy):
    """Peak-hour pricing (surcharge multiplier on top of casual cost)."""
    MULTIPLIER = 1.5

    def __init__(self) -> None:
        self._base = CasualPricing()

    def calculate_cost(self, duration_minutes: float, distance_km: float) -> float:
        return self.MULTIPLIER * self._base.calculate_cost(duration_minutes, distance_km)

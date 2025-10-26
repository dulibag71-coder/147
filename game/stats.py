from __future__ import annotations

from dataclasses import dataclass
from typing import Dict

from . import settings


@dataclass
class SurvivalStats:
    oxygen: float = settings.STAT_MAX
    energy: float = settings.STAT_MAX
    temperature: float = settings.STAT_MAX
    nutrition: float = settings.STAT_MAX

    def as_dict(self) -> Dict[str, float]:
        return {
            "oxygen": self.oxygen,
            "energy": self.energy,
            "temperature": self.temperature,
            "nutrition": self.nutrition,
        }

    def tick(self, dt: float) -> Dict[str, float]:
        depleted: Dict[str, float] = {}
        for stat, rate in settings.STAT_DECAY_PER_MINUTE.items():
            change = rate * dt / 60.0
            depleted[stat] = self.consume(stat, change)
        return depleted

    def restore(self, stat: str, amount: float) -> float:
        return self._apply(stat, amount)

    def consume(self, stat: str, amount: float) -> float:
        return -self._apply(stat, -amount)

    def _apply(self, stat: str, delta: float) -> float:
        current = getattr(self, stat)
        new_value = max(0.0, min(settings.STAT_MAX, current + delta))
        setattr(self, stat, new_value)
        return new_value - current

    def is_critical(self, stat: str) -> bool:
        return getattr(self, stat) <= settings.STAT_CRITICAL_THRESHOLD

    def refill_all(self) -> None:
        for stat in self.as_dict().keys():
            setattr(self, stat, settings.STAT_MAX)

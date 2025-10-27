from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, Iterable, Optional

from . import settings

MISSION_LABELS = {
    "scrap": "스크랩",
    "enemies_defeated": "격추 수",
}


@dataclass
class Mission:
    id: str
    title: str
    description: str
    requirements: Dict[str, int]
    reward: Dict[str, int]
    completed: bool = False

    def progress(self, state: Dict[str, int]) -> float:
        complete_count = 0
        for key, target in self.requirements.items():
            if state.get(key, 0) >= target:
                complete_count += 1
        return complete_count / len(self.requirements)

    def is_ready(self, state: Dict[str, int]) -> bool:
        return all(state.get(key, 0) >= value for key, value in self.requirements.items())


@dataclass
class MissionLog:
    missions: Dict[str, Mission] = field(default_factory=dict)
    active: Optional[str] = None

    def __post_init__(self) -> None:
        if not self.missions:
            for data in settings.MISSIONS:
                mission = Mission(**data)
                self.missions[mission.id] = mission
            if self.missions:
                self.active = next(iter(self.missions))

    def active_mission(self) -> Optional[Mission]:
        if self.active:
            return self.missions.get(self.active)
        return None

    def complete_active(self, state: Dict[str, int]) -> Optional[Dict[str, int]]:
        mission = self.active_mission()
        if mission and not mission.completed and mission.is_ready(state):
            mission.completed = True
            rewards = mission.reward
            self.active = self._next_incomplete()
            return rewards
        return None

    def _next_incomplete(self) -> Optional[str]:
        for mission in self.missions.values():
            if not mission.completed:
                return mission.id
        return None

    def as_lines(self, state: Dict[str, int]) -> Iterable[str]:
        mission = self.active_mission()
        if not mission:
            yield "모든 임무 완료"
            return
        progress = mission.progress(state)
        yield f"{mission.title} ({progress * 100:0.0f}%)"
        yield mission.description
        for key, target in mission.requirements.items():
            label = MISSION_LABELS.get(key, key)
            yield f"- {label}: {state.get(key, 0)}/{target}"

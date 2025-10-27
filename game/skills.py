from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict

from . import settings


@dataclass
class Skill:
    name: str
    description: str
    stat: str
    value: float
    unlocked: bool = False


@dataclass
class SkillTree:
    skills: Dict[str, Skill] = field(default_factory=dict)
    points: int = 0
    level: int = 1
    experience: float = 0.0

    def __post_init__(self) -> None:
        if not self.skills:
            for name, data in settings.SKILL_TREE.items():
                self.skills[name] = Skill(name, data["description"], data["stat"], data["value"])

    def add_experience(self, amount: float) -> list[str]:
        self.experience += amount
        leveled = []
        while self.experience >= settings.EXPERIENCE_PER_LEVEL:
            self.experience -= settings.EXPERIENCE_PER_LEVEL
            self.level += 1
            self.points += settings.SKILL_POINTS_PER_LEVEL
            leveled.append(f"레벨 {self.level}")
        return leveled

    def unlock(self, name: str) -> str:
        skill = self.skills.get(name)
        if not skill:
            return "스킬을 찾을 수 없습니다"
        if skill.unlocked:
            return "이미 해금된 스킬입니다"
        if self.points <= 0:
            return "스킬 포인트가 부족합니다"
        skill.unlocked = True
        self.points -= 1
        return f"{name} 스킬 해금"

    def active_modifiers(self) -> Dict[str, float]:
        modifiers: Dict[str, float] = {}
        for skill in self.skills.values():
            if skill.unlocked:
                modifiers[skill.stat] = modifiers.get(skill.stat, 0.0) + skill.value
        return modifiers

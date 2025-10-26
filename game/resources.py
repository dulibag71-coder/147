from __future__ import annotations

import random
from typing import Dict

from ursina import Entity, Vec3

from . import settings
from .player import Player


class ResourceNode(Entity):
    def __init__(self, kind: str, position: Vec3) -> None:
        data = settings.RESOURCE_KINDS[kind]
        super().__init__(
            model="cube",
            color=data["color"],
            scale=(1.2, 0.6, 1.2),
            collider="box",
            position=position + Vec3(0, 0.4, 0),
        )
        self.kind = kind

    @classmethod
    def random(cls) -> "ResourceNode":
        kind = random.choice(list(settings.RESOURCE_KINDS.keys()))
        pos = Vec3(
            random.uniform(-settings.ARENA_SIZE, settings.ARENA_SIZE),
            0,
            random.uniform(-settings.ARENA_SIZE, settings.ARENA_SIZE),
        )
        return cls(kind, pos)

    def gather(self, player: Player) -> str:
        data = settings.RESOURCE_KINDS[self.kind]
        if "value" in data:
            player.add_resource(self.kind, data["value"])
            return f"{self.kind} +{data['value']}"
        if "restore" in data:
            restored: Dict[str, float] = data["restore"]
            for stat, amount in restored.items():
                player.stats.restore(stat, amount)
            return f"{self.kind} 자원 사용"
        return "획득"

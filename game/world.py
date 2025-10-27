from __future__ import annotations

import random
from typing import List

from ursina import Entity, Vec3, color

from . import settings
from .assets import ASSETS


class RuinWorld:
    def __init__(self) -> None:
        self.ground = ASSETS.spawn(
            "structure",
            model="plane",
            scale=settings.ARENA_SIZE * 2,
            texture="white_cube",
            texture_scale=(settings.ARENA_SIZE, settings.ARENA_SIZE),
            color=color.rgb(35, 38, 50),
        )
        self.structures: List[Entity] = []
        for _ in range(12):
            size = random.uniform(2.0, 4.5)
            height = random.uniform(3.0, 6.0)
            block = ASSETS.spawn(
                "structure",
                scale=(size, height, size),
                position=Vec3(
                    random.uniform(-settings.ARENA_SIZE + 4, settings.ARENA_SIZE - 4),
                    height / 2.0,
                    random.uniform(-settings.ARENA_SIZE + 4, settings.ARENA_SIZE - 4),
                ),
                collider="box",
                color=color.rgb(70, 80, 100),
            )
            self.structures.append(block)
        self.landing_pad = ASSETS.spawn(
            "landing_pad",
            model="cube",
            color=color.rgb(120, 150, 200),
            scale=(4, 0.3, 4),
            position=Vec3(0, 0.2, 0),
        )

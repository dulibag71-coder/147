from __future__ import annotations

from ursina import Entity, Vec3, color

from . import settings
from .enemy import PurgeDrone, find_closest_enemy


class Safer(Entity):
    def __init__(self, player: "Player") -> None:
        super().__init__(
            model="cube",
            color=color.rgb(240, 220, 120),
            scale=(0.8, 0.4, 0.8),
        )
        self.player = player
        self.shot_timer = settings.SAFER_ATTACK_INTERVAL
        self.support_timer = settings.SAFER_SUPPORT_INTERVAL

    def update(self, dt: float, enemies: list[PurgeDrone]) -> None:
        orbit_target = self.player.position + self.player.right * settings.SAFER_ORBIT_DISTANCE
        orbit_target += Vec3(0, settings.SAFER_VERTICAL_OFFSET, 0)
        self.position = self.position.lerp(orbit_target, min(1, dt * 2.5))
        self.look_at(self.player.position)
        self.shot_timer -= dt
        self.support_timer -= dt
        if self.shot_timer <= 0:
            target = find_closest_enemy(enemies, self.position, settings.SAFER_ATTACK_RANGE)
            if target:
                target.take_damage(settings.SAFER_SHOT_DAMAGE)
                self.shot_timer = settings.SAFER_ATTACK_INTERVAL
        if self.support_timer <= 0:
            self.player.stats.restore("energy", settings.SAFER_SUPPORT_AMOUNT)
            self.support_timer = settings.SAFER_SUPPORT_INTERVAL


from typing import TYPE_CHECKING

if TYPE_CHECKING:  # pragma: no cover
    from .player import Player

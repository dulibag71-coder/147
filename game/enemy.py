from __future__ import annotations

import random
from typing import Iterable, Optional

from ursina import Entity, Vec3, color

from . import settings


class PurgeDrone(Entity):
    def __init__(self, position: Vec3) -> None:
        super().__init__(
            model="sphere",
            color=color.rgb(230, 90, 90),
            scale=1.4,
            collider="box",
            position=position,
        )
        self.health = 50.0
        self.speed = 3.5
        self.attack_range = 1.8
        self.attack_cooldown = 1.4
        self._cooldown_timer = 0.0

    @classmethod
    def random_spawn(cls) -> "PurgeDrone":
        edge = random.choice([-1, 1])
        if random.random() < 0.5:
            pos = Vec3(edge * settings.ARENA_SIZE, 0.7, random.uniform(-settings.ARENA_SIZE, settings.ARENA_SIZE))
        else:
            pos = Vec3(random.uniform(-settings.ARENA_SIZE, settings.ARENA_SIZE), 0.7, edge * settings.ARENA_SIZE)
        return cls(pos)

    def update(self, dt: float, player: "Player") -> None:
        if not player.is_alive():
            return
        to_player = player.position - self.position
        to_player.y = 0
        distance = to_player.length()
        if distance > 0.1:
            direction = to_player.normalized()
            self.position += direction * self.speed * dt
            self.look_at(player.position + Vec3(0, 1.5, 0))
        self._cooldown_timer = max(0.0, self._cooldown_timer - dt)
        if distance <= self.attack_range and self._cooldown_timer == 0.0:
            player.take_damage(7.0)
            self._cooldown_timer = self.attack_cooldown

    def take_damage(self, amount: float) -> None:
        self.health = max(0.0, self.health - amount)

    def is_alive(self) -> bool:
        return self.health > 0


def find_closest_enemy(enemies: Iterable[PurgeDrone], position: Vec3, max_range: float) -> Optional[PurgeDrone]:
    best: Optional[PurgeDrone] = None
    best_distance = max_range
    for enemy in enemies:
        distance = (enemy.position - position).length()
        if distance <= best_distance:
            best_distance = distance
            best = enemy
    return best


from typing import TYPE_CHECKING

if TYPE_CHECKING:  # pragma: no cover
    from .player import Player

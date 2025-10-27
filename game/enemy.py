from __future__ import annotations

import random
from typing import Iterable, Optional

from ursina import Entity, Vec3, color

from . import settings
from .assets import ASSETS


class EnemyBase(Entity):
    def __init__(self, model_key: str, position: Vec3, color_tint=color.rgb(230, 90, 90)) -> None:
        model = ASSETS.resolve_model(model_key)
        super().__init__(
            model=model or "cube",
            color=color_tint if not model else color.white,
            scale=1.4,
            collider="box",
            position=position,
        )
        self.health = 60.0
        self.speed = 3.5
        self.attack_range = 2.0
        self.attack_cooldown = 1.3
        self._cooldown_timer = 0.0
        self.damage = 8.0
        self.state = "patrol"
        self.patrol_target = self.position

    def update(self, dt: float, player: "Player") -> None:
        if not player.is_alive():
            return
        to_player = player.position - self.position
        distance = to_player.length()
        if distance < 8.0:
            self.state = "engage"
        elif distance > 20.0 and self.state == "engage":
            self.state = "patrol"
        if self.state == "patrol":
            self._patrol(dt)
        else:
            self._engage(dt, player, to_player, distance)

    def _patrol(self, dt: float) -> None:
        if (self.patrol_target - self.position).length() < 1.0:
            self.patrol_target = Vec3(
                random.uniform(-settings.ARENA_SIZE, settings.ARENA_SIZE),
                self.y,
                random.uniform(-settings.ARENA_SIZE, settings.ARENA_SIZE),
            )
        direction = (self.patrol_target - self.position).normalized()
        self.position += direction * self.speed * dt * 0.5

    def _engage(self, dt: float, player: "Player", to_player: Vec3, distance: float) -> None:
        if distance > 0.5:
            self.position += to_player.normalized() * self.speed * dt
            self.look_at(player.position + Vec3(0, 1.5, 0))
        self._cooldown_timer = max(0.0, self._cooldown_timer - dt)
        if distance <= self.attack_range and self._cooldown_timer == 0.0:
            player.take_damage(self.damage)
            self._cooldown_timer = self.attack_cooldown

    def take_damage(self, amount: float) -> None:
        self.health = max(0.0, self.health - amount)

    def is_alive(self) -> bool:
        return self.health > 0

    def loot_table(self) -> dict[str, int]:
        return {"scrap": random.randint(1, 3)}


class PurgeDrone(EnemyBase):
    def __init__(self, position: Vec3) -> None:
        super().__init__("purge_drone", position)
        self.health = 70.0
        self.speed = 3.8
        self.damage = 10.0
        self.attack_range = 2.2
        self.attack_cooldown = 1.2

    @classmethod
    def random_spawn(cls) -> "PurgeDrone":
        edge = random.choice([-1, 1])
        if random.random() < 0.5:
            pos = Vec3(edge * settings.ARENA_SIZE, 0.7, random.uniform(-settings.ARENA_SIZE, settings.ARENA_SIZE))
        else:
            pos = Vec3(random.uniform(-settings.ARENA_SIZE, settings.ARENA_SIZE), 0.7, edge * settings.ARENA_SIZE)
        return cls(pos)

    def loot_table(self) -> dict[str, int]:
        loot = super().loot_table()
        if random.random() < 0.25:
            loot["data_chip"] = loot.get("data_chip", 0) + 1
        return loot


class WardenSentinel(EnemyBase):
    def __init__(self, position: Vec3) -> None:
        super().__init__("warden", position, color.rgb(200, 70, 200))
        self.health = 220.0
        self.speed = 2.5
        self.damage = 18.0
        self.attack_range = 3.5
        self.attack_cooldown = 2.4

    def loot_table(self) -> dict[str, int]:
        loot = super().loot_table()
        loot["data_chip"] = loot.get("data_chip", 0) + 2
        loot["scrap"] += 4
        return loot


def find_closest_enemy(enemies: Iterable[EnemyBase], position: Vec3, max_range: float) -> Optional[EnemyBase]:
    best: Optional[EnemyBase] = None
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

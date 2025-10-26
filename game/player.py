from __future__ import annotations

from collections import defaultdict
from typing import Dict, Iterable, Optional

from ursina import Entity, Vec3, color, held_keys

from . import settings
from .stats import SurvivalStats


class Player(Entity):
    def __init__(self) -> None:
        super().__init__(
            model="cube",
            color=color.rgb(90, 150, 255),
            scale=(1.0, 2.0, 1.0),
            collider="box",
        )
        self.health = settings.PLAYER_MAX_HEALTH
        self.stats = SurvivalStats()
        self.inventory: Dict[str, int] = defaultdict(int)
        self.attack_cooldown = 0.0
        self._attack_trigger = False

    def update(self, dt: float) -> None:
        move_input = Vec3(held_keys["d"] - held_keys["a"], 0, held_keys["w"] - held_keys["s"])
        if move_input.length():
            move_input = move_input.normalized()
        displacement = (self.forward * move_input.z + self.right * move_input.x) * settings.PLAYER_SPEED * dt
        sprinting = held_keys["shift"] and self.stats.energy > 0
        if sprinting:
            displacement *= settings.SPRINT_MULTIPLIER
            self.stats.consume("energy", 12.0 * dt)
        self.position += displacement
        self.rotation_y += (held_keys["q"] - held_keys["e"]) * settings.PLAYER_ROTATION_SPEED * dt
        self.position = Vec3(
            max(-settings.ARENA_SIZE, min(settings.ARENA_SIZE, self.x)),
            self.y,
            max(-settings.ARENA_SIZE, min(settings.ARENA_SIZE, self.z)),
        )
        self.attack_cooldown = max(0.0, self.attack_cooldown - dt)
        self.stats.tick(dt)

    def trigger_attack(self) -> None:
        self._attack_trigger = True

    def perform_attack(self, enemies: Iterable["Enemy"]) -> Optional["Enemy"]:
        if self.attack_cooldown > 0 or not self._attack_trigger:
            self._attack_trigger = False
            return None
        self._attack_trigger = False
        self.attack_cooldown = settings.PLAYER_ATTACK_COOLDOWN
        best_target: Optional["Enemy"] = None
        best_distance = settings.PLAYER_ATTACK_RANGE + 1
        forward = self.forward.normalized()
        for enemy in enemies:
            to_enemy = enemy.position - self.position
            distance = to_enemy.length()
            if distance > settings.PLAYER_ATTACK_RANGE:
                continue
            if distance <= 0:
                continue
            if forward.dot(to_enemy.normalized()) < settings.PLAYER_ATTACK_ARC:
                continue
            if distance < best_distance:
                best_distance = distance
                best_target = enemy
        if best_target:
            best_target.take_damage(settings.PLAYER_MELEE_DAMAGE)
        return best_target

    def take_damage(self, amount: float) -> None:
        self.health = max(0.0, self.health - amount)

    def is_alive(self) -> bool:
        return self.health > 0

    def add_resource(self, kind: str, amount: int) -> None:
        self.inventory[kind] += amount

    def consume_scrap(self, amount: int) -> bool:
        if self.inventory["scrap"] < amount:
            return False
        self.inventory["scrap"] -= amount
        return True

    def refill_survival(self) -> None:
        self.stats.refill_all()


from typing import TYPE_CHECKING

if TYPE_CHECKING:  # pragma: no cover
    from .enemy import Enemy

from __future__ import annotations

from typing import Iterable, Optional

from ursina import Audio, Entity, Vec3, color, held_keys, mouse

from . import settings
from .assets import ASSETS
from .inventory import Inventory
from .skills import SkillTree
from .stats import SurvivalStats


class Player(Entity):
    def __init__(self) -> None:
        model = ASSETS.resolve_model("player")
        super().__init__(
            model=model or "cube",
            color=color.rgb(90, 150, 255) if not model else color.white,
            scale=(1.0, 1.8, 1.0),
            collider="capsule",
        )
        self.velocity = Vec3(0, 0, 0)
        self.health = settings.PLAYER_MAX_HEALTH
        self.shield = settings.PLAYER_SHIELD_MAX
        self.stats = SurvivalStats()
        self.inventory = Inventory()
        self.skills = SkillTree()
        self.attack_cooldown = 0.0
        self.ranged_cooldown = 0.0
        self._attack_trigger = False
        self._dash_cooldown = 0.0
        self._audio_swipe = None
        try:
            self._audio_swipe = Audio("assets/audio/swing.wav", autoplay=False)
        except Exception:  # pragma: no cover - optional asset
            self._audio_swipe = None

    # --- Lifecycle ---
    def update(self, dt: float) -> None:
        move_input = Vec3(held_keys["d"] - held_keys["a"], 0, held_keys["w"] - held_keys["s"])
        if move_input.length():
            move_input = move_input.normalized()
        forward = self.forward
        right = self.right
        desired_velocity = (forward * move_input.z + right * move_input.x) * settings.PLAYER_SPEED
        sprinting = held_keys["shift"] and self.stats.energy > 0
        if sprinting:
            desired_velocity *= settings.SPRINT_MULTIPLIER
            self.stats.consume("energy", 18.0 * dt)
        if desired_velocity.length() > 0:
            blend = min(1.0, settings.PLAYER_ACCELERATION * dt)
            self.velocity = self.velocity.lerp(desired_velocity, blend)
        else:
            blend = min(1.0, settings.PLAYER_DECELERATION * dt)
            self.velocity = self.velocity.lerp(Vec3(0, 0, 0), blend)
        self.position += self.velocity * dt
        self.rotation_y += mouse.velocity[0] * settings.PLAYER_AIM_SENSITIVITY * dt
        self.rotation_y += (held_keys["q"] - held_keys["e"]) * settings.PLAYER_ROTATION_SPEED * dt
        self.position = Vec3(
            max(-settings.ARENA_SIZE, min(settings.ARENA_SIZE, self.x)),
            self.y,
            max(-settings.ARENA_SIZE, min(settings.ARENA_SIZE, self.z)),
        )
        self.attack_cooldown = max(0.0, self.attack_cooldown - dt)
        self.ranged_cooldown = max(0.0, self.ranged_cooldown - dt)
        self._dash_cooldown = max(0.0, self._dash_cooldown - dt)
        self.stats.tick(dt)
        if self.shield < settings.PLAYER_SHIELD_MAX:
            self.shield = min(settings.PLAYER_SHIELD_MAX, self.shield + settings.PLAYER_SHIELD_RECHARGE_RATE * dt)

    # --- Combat ---
    def trigger_attack(self) -> None:
        self._attack_trigger = True

    def perform_attack(self, enemies: Iterable["Enemy"]) -> Optional["Enemy"]:
        if self.attack_cooldown > 0 or not self._attack_trigger:
            self._attack_trigger = False
            return None
        self._attack_trigger = False
        modifiers = self.skills.active_modifiers()
        self.attack_cooldown = settings.PLAYER_ATTACK_COOLDOWN
        best_target: Optional["Enemy"] = None
        best_distance = settings.PLAYER_ATTACK_RANGE + 1
        forward = self.forward.normalized()
        for enemy in enemies:
            to_enemy = enemy.position - self.position
            distance = to_enemy.length()
            if distance > settings.PLAYER_ATTACK_RANGE or distance <= 0:
                continue
            if forward.dot(to_enemy.normalized()) < settings.PLAYER_ATTACK_ARC:
                continue
            if distance < best_distance:
                best_distance = distance
                best_target = enemy
        if best_target:
            damage = settings.PLAYER_MELEE_DAMAGE
            melee_bonus = modifiers.get("melee_bonus", 0.0)
            damage *= 1.0 + melee_bonus
            best_target.take_damage(damage)
            if self._audio_swipe:
                self._audio_swipe.play()
        return best_target

    def perform_ranged(self, enemies: Iterable["Enemy"]) -> Optional["Enemy"]:
        if self.ranged_cooldown > 0:
            return None
        target = min(
            (enemy for enemy in enemies if (enemy.position - self.position).length() <= settings.SAFER_ATTACK_RANGE),
            default=None,
            key=lambda e: (e.position - self.position).length(),
        )
        if not target:
            return None
        target.take_damage(settings.PLAYER_RANGED_DAMAGE)
        self.ranged_cooldown = settings.PLAYER_RANGED_INTERVAL
        return target

    def dash(self) -> bool:
        dash_modifier = self.skills.active_modifiers().get("dash_cooldown", 0.0)
        cooldown = max(0.3, 1.0 + dash_modifier)
        if self._dash_cooldown > 0:
            return False
        direction = self.forward
        self.position += direction.normalized() * 6.0
        self.position = Vec3(
            max(-settings.ARENA_SIZE, min(settings.ARENA_SIZE, self.x)),
            self.y,
            max(-settings.ARENA_SIZE, min(settings.ARENA_SIZE, self.z)),
        )
        self._dash_cooldown = cooldown
        return True

    # --- Health & stats ---
    def take_damage(self, amount: float) -> None:
        if self.shield > 0:
            absorbed = min(self.shield, amount)
            self.shield -= absorbed
            amount -= absorbed
        if amount > 0:
            self.health = max(0.0, self.health - amount)

    def restore_health(self, amount: float) -> None:
        self.health = min(settings.PLAYER_MAX_HEALTH, self.health + amount)

    def restore_shield(self, amount: float) -> None:
        self.shield = min(settings.PLAYER_SHIELD_MAX, self.shield + amount)

    def is_alive(self) -> bool:
        return self.health > 0

    # --- Inventory helpers ---
    def add_resource(self, kind: str, amount: int) -> None:
        self.inventory.add(kind, amount)

    def consume_resource(self, kind: str, amount: int) -> bool:
        return self.inventory.remove(kind, amount)

    def consume_scrap(self, amount: int) -> bool:
        return self.consume_resource("scrap", amount)

    def refill_survival(self) -> None:
        self.stats.refill_all()

    def gain_experience(self, amount: float) -> list[str]:
        return self.skills.add_experience(amount)

    def apply_item_heal(self) -> None:
        heal = self.skills.active_modifiers().get("item_heal", 0.0)
        if heal:
            self.restore_health(heal)


from typing import TYPE_CHECKING

if TYPE_CHECKING:  # pragma: no cover
    from .enemy import Enemy

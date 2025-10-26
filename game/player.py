from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Tuple

import pygame

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

    def update(self, delta: float) -> Dict[str, float]:
        depleted = {}
        for key, rate in settings.STAT_DEPLETION_RATES.items():
            value = max(0, getattr(self, key) - rate * (delta / 60.0))
            if value != getattr(self, key):
                depleted[key] = getattr(self, key) - value
            setattr(self, key, value)
        return depleted

    def restore(self, key: str, amount: float) -> None:
        setattr(self, key, min(settings.STAT_MAX, getattr(self, key) + amount))


class Player(pygame.sprite.Sprite):
    def __init__(self, position: Tuple[int, int]) -> None:
        super().__init__()
        self.image = pygame.Surface((32, 32))
        self.image.fill((80, 160, 255))
        self.rect = self.image.get_rect(center=position)
        self.velocity = pygame.Vector2(0, 0)
        self.stats = SurvivalStats()
        self.health = float(settings.PLAYER_MAX_HEALTH)
        self.attack_cooldown = 0.0
        self.inventory: Dict[str, int] = {
            "scrap": 0,
        }

    def update(self, dt: float, keys: pygame.key.ScancodeWrapper) -> None:
        self.velocity.xy = 0, 0
        if keys[pygame.K_w]:
            self.velocity.y = -1
        if keys[pygame.K_s]:
            self.velocity.y += 1
        if keys[pygame.K_a]:
            self.velocity.x = -1
        if keys[pygame.K_d]:
            self.velocity.x += 1
        if self.velocity.length_squared() > 0:
            self.velocity = self.velocity.normalize() * settings.PLAYER_SPEED
        self.rect.centerx += int(self.velocity.x * dt)
        self.rect.centery += int(self.velocity.y * dt)
        self.rect.clamp_ip(pygame.Rect(0, 0, settings.WINDOW_WIDTH, settings.WINDOW_HEIGHT))
        self.stats.update(dt)
        self.attack_cooldown = max(0.0, self.attack_cooldown - dt)

    def can_attack(self) -> bool:
        return self.attack_cooldown <= 0.0

    def perform_attack(self) -> None:
        self.attack_cooldown = settings.PLAYER_ATTACK_COOLDOWN

    def take_damage(self, amount: float) -> None:
        self.health = max(0.0, self.health - amount)

    def is_alive(self) -> bool:
        return self.health > 0

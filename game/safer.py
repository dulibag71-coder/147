from __future__ import annotations

import math
from typing import Optional

import pygame

from . import settings
from .enemy import Enemy


class Safer(pygame.sprite.Sprite):
    def __init__(self, position):
        super().__init__()
        self.image = pygame.Surface((24, 24))
        self.image.fill((180, 255, 200))
        self.rect = self.image.get_rect(center=position)
        self.support_timer = settings.SAFER_SUPPORT_INTERVAL
        self.shot_cooldown = 0.0

    def update(self, dt: float, player_rect: pygame.Rect, enemies: pygame.sprite.Group) -> Optional[Enemy]:
        # Follow the player with a small offset
        target = pygame.Vector2(player_rect.center)
        current = pygame.Vector2(self.rect.center)
        direction = target - current
        if direction.length_squared() > 4:
            move = direction.normalize() * settings.SAFER_SPEED
            self.rect.centerx += int(move.x * dt)
            self.rect.centery += int(move.y * dt)

        self.support_timer -= dt
        self.shot_cooldown = max(0.0, self.shot_cooldown - dt)

        # Find enemy in range
        target_enemy = None
        closest_distance = math.inf
        for enemy in enemies:
            distance = pygame.Vector2(enemy.rect.center).distance_to(current)
            if distance <= settings.SAFER_SHOT_RANGE and distance < closest_distance:
                closest_distance = distance
                target_enemy = enemy
        return target_enemy

    def can_support(self) -> bool:
        return self.support_timer <= 0

    def reset_support(self) -> None:
        self.support_timer = settings.SAFER_SUPPORT_INTERVAL

    def can_shoot(self) -> bool:
        return self.shot_cooldown <= 0

    def reset_shot(self) -> None:
        self.shot_cooldown = settings.SAFER_SHOT_COOLDOWN

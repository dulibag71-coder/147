from __future__ import annotations

import random
from typing import Tuple

import pygame

from . import settings


class Enemy(pygame.sprite.Sprite):
    def __init__(self, position: Tuple[int, int]) -> None:
        super().__init__()
        self.image = pygame.Surface((28, 28))
        self.image.fill((200, 80, 80))
        self.rect = self.image.get_rect(center=position)
        self.health = float(settings.ENEMY_HEALTH)
        self.attack_cooldown = 0.0

    def update(self, dt: float, player_rect: pygame.Rect) -> None:
        direction = pygame.Vector2(player_rect.center) - pygame.Vector2(self.rect.center)
        if direction.length_squared() > 0:
            direction = direction.normalize() * settings.ENEMY_SPEED
            self.rect.centerx += int(direction.x * dt)
            self.rect.centery += int(direction.y * dt)
        self.attack_cooldown = max(0.0, self.attack_cooldown - dt)

    def attack(self, player) -> None:
        if self.attack_cooldown > 0:
            return
        player.take_damage(settings.ENEMY_DAMAGE)
        self.attack_cooldown = settings.ENEMY_ATTACK_COOLDOWN

    def take_damage(self, amount: float) -> None:
        self.health = max(0.0, self.health - amount)

    def is_alive(self) -> bool:
        return self.health > 0

    @staticmethod
    def spawn_position() -> Tuple[int, int]:
        margin = 40
        side = random.choice(["top", "bottom", "left", "right"])
        if side == "top":
            return random.randint(margin, settings.WINDOW_WIDTH - margin), -margin
        if side == "bottom":
            return random.randint(margin, settings.WINDOW_WIDTH - margin), settings.WINDOW_HEIGHT + margin
        if side == "left":
            return -margin, random.randint(margin, settings.WINDOW_HEIGHT - margin)
        return settings.WINDOW_WIDTH + margin, random.randint(margin, settings.WINDOW_HEIGHT - margin)

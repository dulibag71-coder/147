from __future__ import annotations

from collections import deque
from typing import Deque

import pygame

from . import settings
from .crafting import CraftingSystem
from .enemy import Enemy
from .hud import HUD
from .player import Player
from .resources import ResourceNode, gather_resource
from .safer import Safer


class GameState:
    def __init__(self, screen: pygame.Surface) -> None:
        self.screen = screen
        self.player = Player((settings.WINDOW_WIDTH // 2, settings.WINDOW_HEIGHT // 2))
        self.player_group = pygame.sprite.GroupSingle(self.player)
        self.enemies = pygame.sprite.Group()
        self.resources = pygame.sprite.Group()
        self.safer = Safer((self.player.rect.centerx + 40, self.player.rect.centery))
        self.safer_group = pygame.sprite.GroupSingle(self.safer)
        self.hud = HUD(screen)
        self.crafting = CraftingSystem(self.player)
        self.messages: Deque[str] = deque(maxlen=4)
        self.spawn_timer = settings.ENEMY_SPAWN_INTERVAL
        self.resource_timer = settings.RESOURCE_RESPAWN_INTERVAL
        self.elapsed_time = 0.0
        self.survival_damage: dict[str, float] = {}
        for _ in range(3):
            self.spawn_resource()

    def update(self, dt: float, keys: pygame.key.ScancodeWrapper) -> None:
        if not self.player.is_alive():
            return
        self.elapsed_time += dt
        self.player.update(dt, keys)
        target_enemy = self.safer.update(dt, self.player.rect, self.enemies)
        for enemy in list(self.enemies):
            enemy.update(dt, self.player.rect)
            if enemy.rect.colliderect(self.player.rect):
                enemy.attack(self.player)
            if not enemy.is_alive():
                self.enemies.remove(enemy)
        self.spawn_timer -= dt
        if self.spawn_timer <= 0:
            self.spawn_enemy()
            self.spawn_timer = settings.ENEMY_SPAWN_INTERVAL
        self.resource_timer -= dt
        if self.resource_timer <= 0:
            self.spawn_resource()
            self.resource_timer = settings.RESOURCE_RESPAWN_INTERVAL
        # Survival damage if stats critical
        self.survival_damage = {}
        for stat, value in self.player.stats.as_dict().items():
            if value <= 0:
                self.player.take_damage(settings.STAT_DAMAGE_PER_SECOND * dt)
                self.survival_damage[stat] = settings.STAT_DAMAGE_PER_SECOND * dt
        # Safer support
        if target_enemy and self.safer.can_shoot():
            target_enemy.take_damage(settings.SAFER_SHOT_DAMAGE)
            self.safer.reset_shot()
            if not target_enemy.is_alive():
                self.enemies.remove(target_enemy)
                self.messages.append("세이퍼가 위협을 제거했습니다")
        if self.safer.can_support():
            self.player.stats.restore("energy", settings.SAFER_HEAL_AMOUNT)
            self.safer.reset_support()
            self.messages.append("세이퍼 버프로 에너지 회복")

    def draw(self) -> None:
        self.screen.fill(settings.BACKGROUND_COLOR)
        # Background grid for structure
        for x in range(0, settings.WINDOW_WIDTH, 40):
            pygame.draw.line(self.screen, settings.GRID_COLOR, (x, 0), (x, settings.WINDOW_HEIGHT))
        for y in range(0, settings.WINDOW_HEIGHT, 40):
            pygame.draw.line(self.screen, settings.GRID_COLOR, (0, y), (settings.WINDOW_WIDTH, y))
        self.resources.draw(self.screen)
        self.enemies.draw(self.screen)
        self.player_group.draw(self.screen)
        self.safer_group.draw(self.screen)
        self.hud.draw_stats(self.player, self.survival_damage)
        self.hud.draw_messages(tuple(self.messages))
        if self.crafting.active:
            self.hud.draw_crafting(self.crafting.available_recipes())
        if not self.player.is_alive():
            self.hud.draw_game_over()

    def spawn_enemy(self) -> None:
        position = Enemy.spawn_position()
        self.enemies.add(Enemy(position))
        self.messages.append("경보: 정화 드론 접근")

    def spawn_resource(self) -> None:
        node = ResourceNode(ResourceNode.random_kind(), ResourceNode.random_position())
        self.resources.add(node)
        self.messages.append("스캔: 잔해 자원 감지")

    def handle_attack(self) -> None:
        if not self.player.can_attack():
            return
        self.player.perform_attack()
        attack_rect = pygame.Rect(0, 0, settings.PLAYER_ATTACK_RANGE, settings.PLAYER_ATTACK_RANGE)
        attack_rect.center = self.player.rect.center
        hit_any = False
        for enemy in list(self.enemies):
            if attack_rect.colliderect(enemy.rect):
                enemy.take_damage(settings.PLAYER_ATTACK_DAMAGE)
                hit_any = True
                if not enemy.is_alive():
                    self.enemies.remove(enemy)
                    self.messages.append("적 제압")
        if not hit_any:
            self.messages.append("공격 빗나감")

    def handle_resource_pickup(self) -> None:
        for node in list(self.resources):
            if self.player.rect.colliderect(node.rect.inflate(10, 10)):
                updates = gather_resource(self.player, node)
                self.resources.remove(node)
                if "scrap" in updates:
                    self.messages.append(f"스크랩 +{updates['scrap']}")
                else:
                    for stat, amount in updates.items():
                        self.messages.append(f"{stat} +{amount}")

    def handle_crafting(self, selection_index: int) -> None:
        available = list(self.crafting.available_recipes().keys())
        if 0 <= selection_index < len(available):
            recipe_name = available[selection_index]
            result = self.crafting.craft(recipe_name)
            self.messages.append(result)

    def is_game_over(self) -> bool:
        return not self.player.is_alive()

    def reset(self) -> None:
        self.__init__(self.screen)

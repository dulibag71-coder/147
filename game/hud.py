from __future__ import annotations

from typing import Dict, Tuple

import pygame

from . import settings


class HUD:
    def __init__(self, screen: pygame.Surface) -> None:
        self.font = pygame.font.Font(settings.FONT_NAME, 16)
        self.small_font = pygame.font.Font(settings.FONT_NAME, 12)
        self.screen = screen

    def draw_stats(self, player, survival_damage: Dict[str, float]) -> None:
        x = 10
        y = 10
        for key, value in player.stats.as_dict().items():
            color = (200, 200, 200)
            if value <= settings.STAT_CRITICAL_THRESHOLD:
                color = (255, 120, 120)
            text = self.font.render(f"{key.capitalize()}: {value:05.1f}", True, color)
            self.screen.blit(text, (x, y))
            y += 22
        health = self.font.render(f"Health: {player.health:05.1f}", True, (255, 200, 200))
        self.screen.blit(health, (x, y))
        y += 22
        scrap = self.font.render(f"Scrap: {player.inventory.get('scrap', 0)}", True, (180, 180, 180))
        self.screen.blit(scrap, (x, y))
        y += 22
        if survival_damage:
            warning = self.small_font.render(
                ", ".join(f"-{key}" for key in survival_damage.keys()), True, (255, 150, 100)
            )
            self.screen.blit(warning, (x, y))

    def draw_messages(self, messages: Tuple[str, ...]) -> None:
        y = settings.WINDOW_HEIGHT - 60
        for message in messages:
            text = self.small_font.render(message, True, (200, 220, 240))
            self.screen.blit(text, (10, y))
            y += 16

    def draw_crafting(self, available_recipes: Dict[str, Tuple[int, str]]) -> None:
        panel = pygame.Surface((250, 140), pygame.SRCALPHA)
        panel.fill((10, 10, 10, 200))
        title = self.font.render("Crafting", True, (255, 255, 255))
        panel.blit(title, (10, 10))
        y = 40
        for idx, (recipe, data) in enumerate(available_recipes.items(), start=1):
            cost, description = data
            text = self.small_font.render(f"[{idx}] {recipe}: {description} (Scrap {cost})", True, (220, 220, 220))
            panel.blit(text, (10, y))
            y += 18
        self.screen.blit(panel, (settings.WINDOW_WIDTH - 260, 10))

    def draw_game_over(self) -> None:
        overlay = pygame.Surface(self.screen.get_size(), pygame.SRCALPHA)
        overlay.fill((5, 5, 5, 210))
        self.screen.blit(overlay, (0, 0))
        text = self.font.render("MISSION FAILED", True, (255, 120, 120))
        rect = text.get_rect(center=(settings.WINDOW_WIDTH // 2, settings.WINDOW_HEIGHT // 2))
        self.screen.blit(text, rect)

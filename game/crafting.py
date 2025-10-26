from __future__ import annotations

from typing import Dict

from . import settings
from .player import Player


class CraftingSystem:
    def __init__(self, player: Player) -> None:
        self.player = player
        self.active = False

    def toggle(self) -> bool:
        self.active = not self.active
        return self.active

    def available_recipes(self) -> Dict[str, dict]:
        affordable = {}
        for name, recipe in settings.CRAFTING_RECIPES.items():
            if all(self.player.inventory.get(resource, 0) >= amount for resource, amount in recipe["requirements"].items()):
                affordable[name] = recipe
        return affordable

    def craft(self, recipe_name: str) -> str:
        recipe = settings.CRAFTING_RECIPES[recipe_name]
        if not all(self.player.inventory.get(resource, 0) >= amount for resource, amount in recipe["requirements"].items()):
            return "자원이 부족합니다"
        for resource, amount in recipe["requirements"].items():
            if resource == "scrap":
                if not self.player.consume_scrap(amount):
                    return "스크랩이 부족합니다"
            else:
                self.player.inventory[resource] -= amount
        for stat, amount in recipe["effects"].items():
            self.player.stats.restore(stat, amount)
        return f"{recipe_name} 제작 완료"

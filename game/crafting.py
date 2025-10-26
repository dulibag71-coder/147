from __future__ import annotations

from typing import Dict

from . import settings


CRAFTING_RECIPES = {
    "Oxygen Tank": {
        "cost": 3,
        "effect": ("oxygen", 35),
        "description": "응급 산소 보충",
    },
    "Energy Cell": {
        "cost": 4,
        "effect": ("energy", 40),
        "description": "기어 전력 회복",
    },
    "Thermal Patch": {
        "cost": 2,
        "effect": ("temperature", 30),
        "description": "체온 안정화",
    },
    "Nutrient Pack": {
        "cost": 2,
        "effect": ("nutrition", 30),
        "description": "영양 보급",
    },
}


class CraftingSystem:
    def __init__(self, player) -> None:
        self.player = player
        self.active = False

    def toggle(self) -> None:
        self.active = not self.active

    def available_recipes(self) -> Dict[str, tuple]:
        return {
            name: (recipe["cost"], recipe["description"])
            for name, recipe in CRAFTING_RECIPES.items()
            if self.player.inventory.get("scrap", 0) >= recipe["cost"]
        }

    def craft(self, recipe_key: str) -> str:
        recipe = CRAFTING_RECIPES[recipe_key]
        cost = recipe["cost"]
        if self.player.inventory.get("scrap", 0) < cost:
            return "스크랩 부족"
        self.player.inventory["scrap"] -= cost
        stat, amount = recipe["effect"]
        self.player.stats.restore(stat, amount)
        return f"{recipe_key} 제작 완료 (+{amount} {stat})"

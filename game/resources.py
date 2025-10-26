from __future__ import annotations

import random
from typing import Dict, Tuple

import pygame

from . import settings


class ResourceNode(pygame.sprite.Sprite):
    def __init__(self, kind: str, position: Tuple[int, int]):
        super().__init__()
        self.kind = kind
        self.amount = settings.RESOURCE_TYPES[kind]["amount"]
        self.image = pygame.Surface((20, 20))
        self.image.fill(settings.RESOURCE_TYPES[kind]["color"])
        self.rect = self.image.get_rect(center=position)

    @staticmethod
    def random_kind() -> str:
        return random.choice(list(settings.RESOURCE_TYPES.keys()))

    @staticmethod
    def random_position() -> Tuple[int, int]:
        margin = 40
        return (
            random.randint(margin, settings.WINDOW_WIDTH - margin),
            random.randint(margin, settings.WINDOW_HEIGHT - margin),
        )


def gather_resource(player, node: ResourceNode) -> Dict[str, int]:
    inventory_updates: Dict[str, int] = {}
    if node.kind == "scrap":
        player.inventory["scrap"] = player.inventory.get("scrap", 0) + node.amount
        inventory_updates["scrap"] = node.amount
    else:
        player.stats.restore(node.kind, node.amount)
        inventory_updates[node.kind] = node.amount
    return inventory_updates

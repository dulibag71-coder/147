from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, Iterable


@dataclass
class InventoryItem:
    name: str
    count: int = 0
    description: str = ""


@dataclass
class Inventory:
    items: Dict[str, InventoryItem] = field(default_factory=dict)

    def add(self, name: str, amount: int = 1, description: str = "") -> None:
        item = self.items.get(name)
        if item is None:
            item = InventoryItem(name=name, count=amount, description=description)
            self.items[name] = item
        else:
            item.count += amount
        if description and not item.description:
            item.description = description

    def remove(self, name: str, amount: int = 1) -> bool:
        item = self.items.get(name)
        if not item or item.count < amount:
            return False
        item.count -= amount
        if item.count == 0:
            self.items.pop(name)
        return True

    def has(self, name: str, amount: int = 1) -> bool:
        item = self.items.get(name)
        return bool(item and item.count >= amount)

    def stack_count(self, name: str) -> int:
        item = self.items.get(name)
        return item.count if item else 0

    def get(self, name: str, default: int = 0) -> int:
        return self.stack_count(name) if name in self.items else default

    def as_lines(self) -> Iterable[str]:
        for item in self.items.values():
            yield f"{item.name} x{item.count}"

    def clear(self) -> None:
        self.items.clear()

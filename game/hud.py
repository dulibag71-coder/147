from __future__ import annotations

from collections import deque
from typing import Deque, Iterable

from ursina import Text, color

from . import settings
from .player import Player


class HUD:
    def __init__(self, player: Player) -> None:
        self.player = player
        self.stat_labels = {
            "oxygen": Text(text="", origin=(-0.5, 0.5), position=(-0.85, 0.45), scale=1.1, color=color.azure),
            "energy": Text(text="", origin=(-0.5, 0.5), position=(-0.85, 0.35), scale=1.1, color=color.orange),
            "temperature": Text(text="", origin=(-0.5, 0.5), position=(-0.85, 0.25), scale=1.1, color=color.cyan),
            "nutrition": Text(text="", origin=(-0.5, 0.5), position=(-0.85, 0.15), scale=1.1, color=color.lime),
        }
        self.health_label = Text(text="", origin=(-0.5, 0.5), position=(-0.85, 0.55), scale=1.2, color=color.red)
        self.inventory_label = Text(text="", origin=(-0.5, 0.5), position=(-0.85, -0.35), scale=1.0, color=color.white)
        self.messages: Deque[tuple[str, float]] = deque(maxlen=5)
        self.message_widgets: list[Text] = [
            Text(text="", origin=(-0.5, 0.5), position=(-0.65, -0.05 - i * 0.07), scale=1.0, color=color.white)
            for i in range(4)
        ]
        self.crafting_label = Text(text="", origin=(-0.5, 0.5), position=(0.7, 0.3), scale=1.05, color=color.white)
        self.objective_label = Text(
            text="탈출 모듈을 찾고 생존하라",
            origin=(-0.5, 0.5),
            position=(0, 0.45),
            scale=1.2,
            color=color.rgb(220, 220, 240),
        )

    def update(self, dt: float) -> None:
        self.health_label.text = f"HP {int(self.player.health)}"
        inventory_text = "스크랩: " + str(self.player.inventory.get("scrap", 0))
        self.inventory_label.text = inventory_text
        stats = self.player.stats.as_dict()
        for stat, label in self.stat_labels.items():
            value = stats[stat]
            warning = "!" if self.player.stats.is_critical(stat) else ""
            label.text = f"{stat.upper():<9} {int(value):>3}{warning}"
        self._refresh_messages(dt)

    def add_message(self, message: str) -> None:
        self.messages.append((message, settings.HUD_MESSAGE_DURATION))

    def _refresh_messages(self, dt: float) -> None:
        remaining = deque(maxlen=self.messages.maxlen)
        for index, (message, timer) in enumerate(self.messages):
            timer -= dt
            if timer > 0:
                remaining.append((message, timer))
                if index < len(self.message_widgets):
                    self.message_widgets[index].text = message
            elif index < len(self.message_widgets):
                self.message_widgets[index].text = ""
        for i in range(len(remaining), len(self.message_widgets)):
            self.message_widgets[i].text = ""
        self.messages = remaining

    def show_crafting(self, recipes: Iterable[str]) -> None:
        if not recipes:
            self.crafting_label.text = "사용 가능한 제작이 없습니다"
        else:
            lines = ["[C] 제작 모드"]
            for index, recipe in enumerate(recipes, start=1):
                lines.append(f"{index}. {recipe}")
            self.crafting_label.text = "\n".join(lines)

    def hide_crafting(self) -> None:
        self.crafting_label.text = ""

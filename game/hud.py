from __future__ import annotations

from collections import deque
from typing import Deque, Iterable

from ursina import Text, color

from . import settings
from .missions import MissionLog
from .player import Player


class HUD:
    def __init__(self, player: Player, missions: MissionLog) -> None:
        self.player = player
        self.missions = missions
        self.stat_labels = {
            "oxygen": Text(text="", origin=(-0.5, 0.5), position=(-0.85, 0.45), scale=1.1, color=color.azure),
            "energy": Text(text="", origin=(-0.5, 0.5), position=(-0.85, 0.35), scale=1.1, color=color.orange),
            "temperature": Text(text="", origin=(-0.5, 0.5), position=(-0.85, 0.25), scale=1.1, color=color.cyan),
            "nutrition": Text(text="", origin=(-0.5, 0.5), position=(-0.85, 0.15), scale=1.1, color=color.lime),
        }
        self.health_label = Text(text="", origin=(-0.5, 0.5), position=(-0.85, 0.58), scale=1.2, color=color.red)
        self.shield_label = Text(text="", origin=(-0.5, 0.5), position=(-0.85, 0.51), scale=1.0, color=color.azure)
        self.inventory_label = Text(text="", origin=(-0.5, 0.5), position=(-0.85, -0.35), scale=1.0, color=color.white)
        self.messages: Deque[tuple[str, float]] = deque(maxlen=5)
        self.message_widgets: list[Text] = [
            Text(text="", origin=(-0.5, 0.5), position=(-0.65, -0.05 - i * 0.07), scale=1.0, color=color.white)
            for i in range(4)
        ]
        self.crafting_label = Text(text="", origin=(-0.5, 0.5), position=(0.7, 0.3), scale=1.05, color=color.white)
        self.objective_lines: list[Text] = [
            Text(text="", origin=(-0.5, 0.5), position=(0.0, 0.45 - i * 0.05), scale=1.05, color=color.rgb(220, 220, 240))
            for i in range(4)
        ]
        self.environment_label = Text(text="", origin=(-0.5, 0.5), position=(0.7, 0.45), scale=1.0, color=color.rgb(200, 200, 220))
        self.progress_label = Text(text="", origin=(-0.5, 0.5), position=(0.7, 0.4), scale=1.0, color=color.rgb(200, 200, 220))

    def update(self, dt: float, mission_state: dict[str, int], environment_text: str = "") -> None:
        self.health_label.text = f"HP {int(self.player.health)}"
        self.shield_label.text = f"SH {int(self.player.shield)}"
        inventory_text = "스크랩: " + str(self.player.inventory.stack_count("scrap"))
        extra = [line for line in self.player.inventory.as_lines() if not line.lower().startswith("scrap")]
        if extra:
            inventory_text += " | " + ", ".join(extra)
        self.inventory_label.text = inventory_text
        stats = self.player.stats.as_dict()
        for stat, label in self.stat_labels.items():
            value = stats[stat]
            warning = "!" if self.player.stats.is_critical(stat) else ""
            label.text = f"{stat.upper():<9} {int(value):>3}{warning}"
        self._refresh_messages(dt)
        mission_lines = list(self.missions.as_lines(mission_state))
        for index, widget in enumerate(self.objective_lines):
            widget.text = mission_lines[index] if index < len(mission_lines) else ""
        self.environment_label.text = environment_text
        self.progress_label.text = f"LV {self.player.skills.level} | XP {int(self.player.skills.experience)}/{settings.EXPERIENCE_PER_LEVEL} | SP {self.player.skills.points}"

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

    def destroy(self) -> None:
        for label in self.stat_labels.values():
            label.disable()
        self.health_label.disable()
        self.shield_label.disable()
        self.inventory_label.disable()
        self.crafting_label.disable()
        self.environment_label.disable()
        self.progress_label.disable()
        for widget in self.message_widgets:
            widget.disable()
        for widget in self.objective_lines:
            widget.disable()

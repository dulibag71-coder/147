from __future__ import annotations

from ursina import Ursina, application, time

from game import settings
from game.game_state import GameState


def main() -> None:
    app = Ursina()
    application.window.size = settings.WINDOW_SIZE
    application.window.color = (0, 0, 0, 1)
    game_state = GameState()

    def update() -> None:  # type: ignore[override]
        dt = time.dt
        game_state.update(dt)

    def input(key: str) -> None:  # type: ignore[override]
        if key == "left mouse down":
            game_state.player.trigger_attack()
            game_state.handle_attack()
        elif key == "g":
            game_state.handle_resource_gather()
        elif key == "c":
            game_state.handle_crafting_toggle()
        elif key in {"1", "2", "3", "4"} and game_state.crafting.active:
            game_state.handle_craft_selection(int(key) - 1)
        elif key == "r":
            game_state.reset()

    app.run()


if __name__ == "__main__":
    main()

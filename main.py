from __future__ import annotations

import pygame

from game import settings
from game.game_state import GameState


def main() -> int:
    pygame.init()
    pygame.font.init()
    clock = pygame.time.Clock()
    screen = pygame.display.set_mode((settings.WINDOW_WIDTH, settings.WINDOW_HEIGHT))
    pygame.display.set_caption("잔해의 노래: 더미 스테이션")
    state = GameState(screen)

    while True:
        dt = clock.tick(settings.FPS) / 1000.0
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return 0
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return 0
                if event.key == pygame.K_r and state.is_game_over():
                    state.reset()
                if event.key == pygame.K_SPACE:
                    state.handle_attack()
                if event.key == pygame.K_e:
                    state.handle_resource_pickup()
                if event.key == pygame.K_c:
                    state.crafting.toggle()
                if state.crafting.active and pygame.K_1 <= event.key <= pygame.K_9:
                    selection = event.key - pygame.K_1
                    state.handle_crafting(selection)
        keys = pygame.key.get_pressed()
        state.update(dt, keys)
        state.draw()
        pygame.display.flip()


if __name__ == "__main__":
    raise SystemExit(main())

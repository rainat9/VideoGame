# main.py
from __future__ import annotations

import pygame

from settings import SCREEN_W, SCREEN_H, FPS, CAPTION
from states.title_state import TitleState


def main() -> None:
    pygame.init()
    pygame.display.set_caption(CAPTION)
    screen = pygame.display.set_mode((SCREEN_W, SCREEN_H))
    clock = pygame.time.Clock()
    print(SCREEN_W, SCREEN_H)
    # Start state (instructions/title)
    state = TitleState()

    running = True
    while running:
        dt = clock.tick(FPS) / 1000.0  # seconds

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                break

            state.handle_event(event)

        if not running:
            break

        state.update(dt)

        # Handle state transitions
        nxt = state.next_state()
        if nxt is not None:
            state = nxt

        state.draw(screen)
        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    main()

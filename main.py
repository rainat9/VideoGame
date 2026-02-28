# main.py
from __future__ import annotations

import asyncio
import pygame

from settings import SCREEN_W, SCREEN_H, FPS, CAPTION
from states.title_state import TitleState


async def main() -> None:
    pygame.init()
    pygame.display.set_caption(CAPTION)
    screen = pygame.display.set_mode((SCREEN_W, SCREEN_H))
    clock = pygame.time.Clock()
    print(SCREEN_W, SCREEN_H)

    state = TitleState()
    running = True

    while running:
        # Pump events first (important for browser responsiveness)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                break
            state.handle_event(event)

        if not running:
            break

        # Limit FPS and compute dt
        dt = clock.tick(FPS) / 1000.0

        state.update(dt)

        nxt = state.next_state()
        if nxt is not None:
            state = nxt

        state.draw(screen)
        pygame.display.flip()

        # ✅ KEY: yield to the browser so the page stays responsive
        await asyncio.sleep(0)

    pygame.quit()


if __name__ == "__main__":
    asyncio.run(main())
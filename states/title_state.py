
from __future__ import annotations

import pygame

from states.base_state import BaseState
from settings import SCREEN_W, SCREEN_H, TITLE_BG, FONTS_DIR
from assets import load_image, load_font


class TitleState(BaseState):
    def __init__(self) -> None:
        self._next: BaseState | None = None

        self.bg: pygame.Surface | None = None
        try:
            self.bg = load_image(TITLE_BG, scale_to=(SCREEN_W, SCREEN_H))
        except Exception:
            self.bg = None

        self.font_big = load_font(f"{FONTS_DIR}/pixel_font.ttf", 36)
        self.font_med = load_font(f"{FONTS_DIR}/pixel_font.ttf", 20)
        self.font_small = load_font(f"{FONTS_DIR}/pixel_font.ttf", 16)

        self.blink_t = 0.0
        self.show_press = True

    def handle_event(self, event: pygame.event.Event) -> None:
        if event.type != pygame.KEYDOWN:
            return

        if event.key == pygame.K_RETURN:
            from states.level_state import LevelState
            self._next = LevelState(level_id=1)

        elif event.key == pygame.K_ESCAPE:
            pygame.event.post(pygame.event.Event(pygame.QUIT))

    def update(self, dt: float) -> None:
        self.blink_t += dt
        if self.blink_t >= 0.5:
            self.blink_t = 0.0
            self.show_press = not self.show_press

    def draw(self, screen: pygame.Surface) -> None:
        if self.bg:
            screen.blit(self.bg, (0, 0))
        else:
            screen.fill((10, 10, 20)) 

    def next_state(self) -> BaseState | None:
        return self._next

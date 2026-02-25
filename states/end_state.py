# states/end_state.py
from __future__ import annotations

import pygame

from states.base_state import BaseState
from settings import SCREEN_W, SCREEN_H, END_BG, FONTS_DIR
from assets import load_image, load_font


class EndState(BaseState):
    def __init__(self) -> None:
        self._next: BaseState | None = None

        self.bg: pygame.Surface | None = None
        try:
            self.bg = load_image(END_BG, scale_to=(SCREEN_W, SCREEN_H))
        except Exception:
            self.bg = None

        self.font_big = load_font(f"{FONTS_DIR}/pixel_font.ttf", 34)
        self.font_med = load_font(f"{FONTS_DIR}/pixel_font.ttf", 18)

    def handle_event(self, event: pygame.event.Event) -> None:
        if event.type != pygame.KEYDOWN:
            return

        if event.key == pygame.K_r:
            from states.title_state import TitleState
            self._next = TitleState()

        elif event.key == pygame.K_ESCAPE:
            pygame.event.post(pygame.event.Event(pygame.QUIT))

    def update(self, dt: float) -> None:
        pass

    def draw(self, screen: pygame.Surface) -> None:
        if self.bg:
            screen.blit(self.bg, (0, 0))
        else:
            screen.fill((8, 18, 10))

        msg = self.font_big.render("AIR QUALITY RESTORED!", True, (235, 235, 235))
        screen.blit(msg, msg.get_rect(center=(SCREEN_W // 2, 140)))

        sub = self.font_med.render("You cleaned every area of the town.", True, (220, 220, 220))
        screen.blit(sub, sub.get_rect(center=(SCREEN_W // 2, 190)))

        hint1 = self.font_med.render("Press R to play again", True, (255, 255, 140))
        screen.blit(hint1, hint1.get_rect(center=(SCREEN_W // 2, SCREEN_H - 90)))

        hint2 = self.font_med.render("Press ESC to quit", True, (190, 190, 190))
        screen.blit(hint2, hint2.get_rect(center=(SCREEN_W // 2, SCREEN_H - 60)))

    def next_state(self) -> BaseState | None:
        return self._next

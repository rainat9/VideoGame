# states/title_state.py
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
            screen.fill((10, 10, 20))  # fallback background

        # Title
        title = self.font_big.render("RETRO REVIVAL: ECO QUEST", True, (230, 230, 230))
        screen.blit(title, title.get_rect(center=(SCREEN_W // 2, 110)))

        # Instructions
        lines = [
            "WASD or Arrow Keys: Move",
            "SPACE: Pick up nearby trash",
            "",
            "Clean up the area to improve Air Quality.",
            "Low Air Quality creates fog (reduced visibility).",
            "Reach the target Air Quality to unlock the next map.",
        ]

        y = 190
        for line in lines:
            surf = self.font_med.render(line, True, (220, 220, 220))
            screen.blit(surf, (SCREEN_W // 2 - surf.get_width() // 2, y))
            y += 28

        # Blinking start prompt
        if self.show_press:
            press = self.font_small.render("Press ENTER to start", True, (255, 255, 120))
            screen.blit(press, press.get_rect(center=(SCREEN_W // 2, SCREEN_H - 90)))

        quit_txt = self.font_small.render("Press ESC to quit", True, (180, 180, 180))
        screen.blit(quit_txt, quit_txt.get_rect(center=(SCREEN_W // 2, SCREEN_H - 60)))

    def next_state(self) -> BaseState | None:
        return self._next
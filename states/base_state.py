# states/base_state.py
from __future__ import annotations

import pygame


class BaseState:

    def handle_event(self, event: pygame.event.Event) -> None:
        pass

    def update(self, dt: float) -> None:
        pass

    def draw(self, screen: pygame.Surface) -> None:
        pass

    def next_state(self) -> "BaseState | None":
        return None

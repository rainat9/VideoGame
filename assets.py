# assets.py
from __future__ import annotations

import os
import pygame

_IMAGE_CACHE: dict[tuple, pygame.Surface] = {}
_FONT_CACHE: dict[tuple, pygame.font.Font] = {}


def _assert_pygame_ready() -> None:
    if not pygame.get_init():
        raise RuntimeError("Pygame is not initialized. Call pygame.init() before loading assets.")


def load_image(path: str,
               scale_to: tuple[int, int] | None = None,
               convert_alpha: bool = True) -> pygame.Surface:
    """
    Loads an image from disk with caching.

    Args:
        path: relative/absolute path to image
        scale_to: (w,h) if you want to force a size
        convert_alpha: True preserves transparency nicely (PNG sprites)

    Returns:
        pygame.Surface
    """
    _assert_pygame_ready()

    key = (path, scale_to, convert_alpha)
    if key in _IMAGE_CACHE:
        return _IMAGE_CACHE[key]

    if not os.path.exists(path):
        raise FileNotFoundError(f"Missing image file: {path}")

    img = pygame.image.load(path)
    img = img.convert_alpha() if convert_alpha else img.convert()

    if scale_to is not None:
        img = pygame.transform.smoothscale(img, scale_to)

    _IMAGE_CACHE[key] = img
    return img


def load_font(path: str | None, size: int) -> pygame.font.Font:
    """
    Loads a TTF font with caching. If path is None or missing, falls back to pygame default.
    """
    _assert_pygame_ready()

    key = (path, size)
    if key in _FONT_CACHE:
        return _FONT_CACHE[key]

    if path is None or (isinstance(path, str) and not os.path.exists(path)):
        font = pygame.font.Font(None, size)
    else:
        font = pygame.font.Font(path, size)

    _FONT_CACHE[key] = font
    return font


def clear_asset_cache() -> None:
    """If you ever reload assets during dev."""
    _IMAGE_CACHE.clear()
    _FONT_CACHE.clear()

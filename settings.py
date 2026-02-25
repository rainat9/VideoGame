# settings.py
from __future__ import annotations

# ----------------------------
# Window / performance
# ----------------------------
SCREEN_W = 960
SCREEN_H = 540
FPS = 60
CAPTION = "Retro Revival: Eco Quest"

# ----------------------------
# Paths
# ----------------------------
ASSETS_DIR = "assets"
MAPS_DIR = f"{ASSETS_DIR}/maps"
SPRITES_DIR = f"{ASSETS_DIR}/sprites"
FONTS_DIR = f"{ASSETS_DIR}/fonts"

# ----------------------------
# Player
# ----------------------------
PLAYER_SPEED = 220  # pixels per second
PLAYER_SIZE = (32, 32)

# ----------------------------
# Air quality / fog
# ----------------------------
AIR_MIN = 0
AIR_MAX = 100
AIR_START = 50

# Fog alpha ranges from 0 (no fog) to ~180 (heavy fog)
FOG_MIN_ALPHA = 0
FOG_MAX_ALPHA = 180

# ----------------------------
# UI
# ----------------------------
UI_BAR_W = 260
UI_BAR_H = 18
UI_PADDING = 12

# ----------------------------
# Controls
# ----------------------------
# We support both WASD and arrow keys for movement.
# Pickup is SPACE.
KEY_PICKUP = "SPACE"

# ----------------------------
# Level progression (targets)
# ----------------------------
# We currently have three playable levels.
LAST_LEVEL = 3

# Per-level air-quality threshold to advance
LEVEL_TARGETS = {
    1: 70,
    2: 80,
    3: 90,
}

# ----------------------------
# Asset filenames (initial framework)
# ----------------------------
# You can change these names later as long as you keep paths consistent.
TITLE_BG = f"{MAPS_DIR}/title_screen.png"   # optional
END_BG = f"{MAPS_DIR}/end_screen.png"       # optional

LEVEL_MAPS = {
    1: f"{MAPS_DIR}/level1_forest.png",
    2: f"{MAPS_DIR}/level2_city.png",
    3: f"{MAPS_DIR}/level3_ocean.png",
}

PLAYER_SPRITES = {
    "idle": f"{SPRITES_DIR}/player_idle.png",
    "walk1": f"{SPRITES_DIR}/player_walk_1.png",  # optional
    "walk2": f"{SPRITES_DIR}/player_walk_2.png",  # optional
}

# Example item sprite names (optional; you can hook these up later)
ITEM_SPRITES = {
    "leaf": f"{SPRITES_DIR}/trash_leaf.png",
    "plastic": f"{SPRITES_DIR}/trash_plastic.png",
    "electronics": f"{SPRITES_DIR}/trash_electronics.png",
    "chemical": f"{SPRITES_DIR}/trash_chemical.png",
}

# You can change the player character image by editing PLAYER_SPRITES above,
# and you can change world object images by editing the "image" fields in game/level_data.py.
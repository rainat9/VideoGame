# game/level_data.py
from __future__ import annotations

from settings import LEVEL_MAPS, LEVEL_TARGETS, SCREEN_W, SCREEN_H


LEVELS: dict[int, dict] = {
    # ========== LEVEL 1: FOREST ==========
    # Trash spawns in river (flows). Trees/bushes block movement.
    # Collect: can (+3), water bottle (+3), electronics (+2), chemical (+1).
    # Hazard: touching leaf reduces air (-10). Start 50, reach 100.
    1: {
        "map_path": LEVEL_MAPS[1],
        "spawn": (80, SCREEN_H - 120),
        "target_air": LEVEL_TARGETS[1],

        "item_spawn": {
            "count": 28,
            "types": ["leaf", "can", "water_bottle", "electronics", "chemical"],
        },
        "max_items": 7,
        "flow_areas": [
            {"rect": [314, 313, 646, 162], "vel": [50, 0], "on_exit": "remove"},
            {"rect": [0, 301, 245, 172], "vel": [50, 0], "on_exit": "remove"},
        ],
        "item_assets": {
            "leaf": "assets/leaves.png",
            "can": "assets/can.png",
            "water_bottle": "assets/water_bottle.png",
            "electronics": "assets/electronics.png",
            "chemical": "assets/chemical_container.png",
        },
        "item_sizes": {
            "leaf": (38, 38),
            "can": (38, 38),
            "water_bottle": (38, 38),
            "electronics": (38, 38),
            "chemical": (38, 38),
        },
        "air_rules": {
            "pickup": {
                "can": 3,
                "water_bottle": 3,
                "electronics": 2,
                "chemical": 1,
            },
            "step_on": {"leaf": -10},
        },
        "spawn_blocked_areas": [
            [102, 1, 102, 64],
            [30, 202, 80, 71],
            [67, 486, 59, 46],
            [282, 112, 53, 35],
            [391, 154, 31, 24],
            [501, 18, 55, 38],
            [612, 146, 70, 53],
            [762, 24, 36, 30],
            [880, 45, 61, 40],
            [433, 263, 47, 34],
            [155, 193, 26, 13],
            [251, 296, 60, 184],
        ],
        "player_collision": [
            [102, 1, 102, 64],
            [30, 202, 80, 71],
            [67, 486, 59, 46],
            [282, 112, 53, 35],
            [391, 154, 31, 24],
            [501, 18, 55, 38],
            [612, 146, 70, 53],
            [762, 24, 36, 30],
            [880, 45, 61, 40],
            [433, 263, 47, 34],
            [155, 193, 26, 13],
        ],
        "intro": {
            "title": "Level 1: Forest",
            "lines": [
                "Trash in the river flows; collect it with SPACE.",
                "Collect: can (+3), water bottle (+3), electronics (+2), chemical (+1).",
                "Hazard: touching leaf reduces air (-10).",
                "Trees and bushes block movement. Reach 100 air to advance.",
            ],
            "dismiss": "Press ENTER to start",
        },
    },

    # ========== LEVEL 2: NEIGHBORHOOD ==========
    # Two cars move on roads; touching a car decreases air. Don’t walk on houses/trees.
    # Collect: water bottle (+3), cardboard box (+3), batteries (+1), electronics (+1),
    #          food waste (+4), chip bag (+2), trash (+2).
    2: {
        "map_path": LEVEL_MAPS[2],
        "spawn": (80, SCREEN_H - 120),
        "target_air": LEVEL_TARGETS[2],

        "item_spawn": {
            "count": 30,
            "types": [
                "water_bottle",
                "cardboard_box",
                "batteries",
                "electronics",
                "food_waste",
                "trash",
                "chip_bag",
            ],
        },
        "max_items": 7,
        "spawn_interval": 1.5,
        "spawn_blocked_areas": [
            [64, 197, 226, 26],
            [0, 213, 38, 99],
            [88, 333, 51, 82],
            [357, 352, 11, 68],
            [350, 205, 22, 53],
            [85, 250, 22, 12],
            [156, 338, 180, 72],
            [227, 281, 93, 58],
            [552, 314, 145, 105],
            [756, 323, 197, 90],
            [567, 63, 123, 105],
            [791, 72, 121, 90],
            [478, 110, 27, 61],
            [479, 360, 22, 64],
            [488, 20, 34, 18],
            [902, 0, 57, 80],
            [768, 12, 19, 13],
        ],
        "player_collision": [
            [64, 197, 226, 26],
            [0, 213, 38, 99],
            [88, 333, 51, 82],
            [357, 352, 11, 68],
            [350, 205, 22, 53],
            [156, 338, 180, 72],
            [227, 281, 93, 58],
            [552, 314, 145, 105],
            [756, 323, 197, 90],
            [567, 63, 123, 105],
            [791, 72, 121, 90],
            [478, 110, 27, 61],
            [479, 360, 22, 64],
            [488, 20, 34, 18],
            [902, 0, 57, 80],
            [768, 12, 19, 13],
        ],
        "item_assets": {
            "water_bottle": "assets/water_bottle.png",
            "cardboard_box": "assets/cardboard_box.png",
            "batteries": "assets/batteries.png",
            "electronics": "assets/electronics.png",
            "food_waste": "assets/food_waste.png",
            "trash": "assets/trash.png",
            "chip_bag": "assets/chip_bag.png",
        },
        "item_sizes": {
            "water_bottle": (40, 40),
            "cardboard_box": (40, 40),
            "batteries": (40, 40),
            "electronics": (40, 40),
            "food_waste": (40, 40),
            "trash": (40, 40),
            "chip_bag": (40, 40),
        },
        "moving_objects": [
            {
                "image": "assets/cars.png",
                "rect": (SCREEN_W // 2 - 70, 0, 50, 50),
                "vel": (0, 180),
                "bounds": (SCREEN_W // 2 - 70, 40, SCREEN_W // 2 - 20, SCREEN_H - 120),
            },
            {
                "image": "assets/carsrl.png",
                "rect": (SCREEN_H - 40, 0, 50, 50),
                "vel": (190, 0),
                "bounds": (SCREEN_H - 20, 0, SCREEN_W - 120, SCREEN_H),
            },
        ],
        "air_rules": {
            "pickup": {
                "water_bottle": 3,
                "cardboard_box": 3,
                "batteries": 1,
                "electronics": 1,
                "food_waste": 4,
                "trash": 2,
                "chip_bag": 2,
            },
        },
        "intro": {
            "title": "Level 2: Neighborhood",
            "lines": [
                "Two cars move on the road; don’t touch them (air drops).",
                "Collect: water bottle (+3), cardboard box (+3), batteries (+1),",
                "electronics (+1), food waste (+4), chip bag (+2), trash (+2).",
                "Don’t walk on houses or trees. Reach 100 air to advance.",
            ],
            "dismiss": "Press ENTER to start",
        },
    },

    # ========== LEVEL 3: OCEAN ==========
    # All trash is moving (flow left/right); items leave screen at edge.
    # Collect: can (+3), electronics (+1), water bottle (+3), trash (+2).
    # Hazards when touching: oil slicks (-8), fishing nets (-8).
    3: {
        "map_path": LEVEL_MAPS[3],
        "spawn": (80, SCREEN_H - 120),
        "target_air": LEVEL_TARGETS[3],

        "item_spawn": {
            "count": 32,
            "types": ["can", "electronics", "water_bottle", "trash", "oil_slick", "fishing_net"],
        },
        "max_items": 6,
        "flow_areas": [
            {
                "rect": [0, 72, 960, 467],
                "speed": 40,
                "on_exit": "remove",
            },
        ],
        "spawn_blocked_areas": [[0, 0, 960, 72]],
        "item_assets": {
            "can": "assets/can.png",
            "electronics": "assets/electronics.png",
            "water_bottle": "assets/water_bottle.png",
            "trash": "assets/trash.png",
            "oil_slick": "assets/oil_slicks.png",
            "fishing_net": "assets/fishing_net.png",
        },
        "item_sizes": {
            "can": (35, 35),
            "electronics": (35, 35),
            "water_bottle": (35, 35),
            "trash": (35, 35),
            "oil_slick": (45, 45),
            "fishing_net": (45, 45),
        },
        "air_rules": {
            "pickup": {
                "can": 3,
                "electronics": 1,
                "water_bottle": 3,
                "trash": 2,
            },
            "step_on": {"oil_slick": -8, "fishing_net": -8},
        },
        "moving_objects": [],
        "intro": {
            "title": "Level 3: Ocean",
            "lines": [
                "All trash is moving; it leaves the screen at the edge.",
                "Collect: can (+3), electronics (+1), water bottle (+3), trash (+2).",
                "Hazards: touching oil slicks or fishing nets reduces air (-8).",
                "Reach 100 air to win.",
            ],
            "dismiss": "Press ENTER to start",
        },
    },
}

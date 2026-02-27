# game/level_data.py
from __future__ import annotations

from settings import LEVEL_MAPS, LEVEL_TARGETS, SCREEN_W, SCREEN_H

LEVELS: dict[int, dict] = {
    1: {
        "map_path": LEVEL_MAPS[1],
        "spawn": (80, SCREEN_H - 120),
        "target_air": LEVEL_TARGETS[1],

        # Items: forest trash & hazards
        # - Leaves
        # - Plastic bags
        # - Water bottles
        # - Electronics
        # - Chemical containers (hazard: stepping on reduces air)
        "item_spawn": {
            "count": 28,
            "types": [
                "leaf",
                "can",
                "water_bottle",
                "electronics",
                "chemical",
            ],
        },
        "max_items": 7,                 # optional – default 5 if omitted
        "flow_areas": [
        {
            "rect": [314, 313, 646, 162],   # x, y, width, height (covers the river band)
            "vel": [50, 0]                  # horizontal drift speed (pixels per second)
        },
        {
            "rect": [0, 301, 245, 172],   # x, y, width, height (covers the river band)
            "vel": [50, 0]                  # horizontal drift speed (pixels per second)
        }
        ],
# Item sprites spawned around the map (visible + collectible).
# These MUST cover every kind listed in item_spawn["types"].
"item_assets": {
    "leaf": "assets/leaves.png",
    "can": "assets/can.png",
    "water_bottle": "assets/water_bottles.png",
    "electronics": "assets/electronics.png",
    "chemical": "assets/chemical.png",
},
# Bigger = easier to see.
"item_sizes": {
    "leaf": (38, 38),
    "can": (38, 38),
    "water_bottle": (38, 38),
    "electronics": (38, 38),
    "chemical": (38, 38),
},
# Level intro popup (shown before play starts)
"intro": {
    "title": "Level 1: Forest Cleanup",
    "lines": [
        "Collect trash to improve air quality (SPACE while touching).",
        "+ Leaf, Plastic Bag, Water Bottle, Electronics = points",
        "- Chemical Containers = hazard (avoid stepping on / picking up)",
    ],
    "dismiss": "Press ENTER to start",
},

        # Trash floating down the river (can use a trash/log sprite).
        # Format:
        #   {"image": "assets/sprites/river_trash.png",
        #    "rect": (x,y,w,h), "vel": (vx,vy), "bounds": (minx, miny, maxx, maxy)}
        # MOVEMENT OF RIVER_TRASH HERE
        #   - Starts near (300, 430), moves horizontally between x=260 and x=700.
        # Rect here is also doubled in size for visibility.
       

        # Air-quality rules
        # Pickups: SPACE while touching item.
        "air_rules": {
            "pickup": {
                "leaf": 1,
                "can": 2,
                "water_bottle": 2,
                "electronics": 3,
            },
            # Hazards applied while standing on the item.
            # Chemical containers reduce the air bar when stepped on.
            "step_on": {
                "chemical": -10,
            },
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
            [251, 296, 60, 184], #bridge
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
        # (bridge omitted)
        ],
    },

    # ===== HERE IS LEVEL 2 (CITY) =====
    2: {
        "map_path": LEVEL_MAPS[2],
        "spawn": (80, SCREEN_H - 120),
        "target_air": LEVEL_TARGETS[2],

        # City items grouped conceptually as:
        # - Recycling: water bottles, cardboard boxes
        # - Hazardous: batteries, electronics
        # - Organic: food waste
        # - Trash: trash bags, chip bags
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
        "max_items": 7,                 # optional – default 5 if omitted
        "spawn_interval": 1.5,          # optional – default 2.0 if omitted
        "spawn_blocked_areas": [
        # Prevent items from spawning in the middle of roads
       # [200, 300, 600, 80],        # example horizontal road
        #[500, 150, 80, 300],         # example vertical road
        # Also block under moving cars if needed (though cars themselves are not items)
        [64, 197, 226, 26],
        [0, 213, 38, 99],
        [88, 333, 51, 82],
        [357, 352, 11, 68],
        [350, 205, 22, 53],
        [85, 250, 22, 12],
        [156, 338, 180, 72], #playground
        [227, 281, 93, 58], #playground
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
        [156, 338, 180, 72], #playground
        [227, 281, 93, 58], #playground
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
"intro": {
    "title": "Level 2: City Recycling Run",
    "lines": [
        "Collect recyclables + trash to raise air quality.",
        "+ Water Bottles, Cardboard Boxes, Trash, Chip Bags = points",
        "- Batteries/Electronics are hazardous (still count, but less safe)",
        "Avoid cars (they are obstacles, not collectibles).",
    ],
    "dismiss": "Press ENTER to start",
},
        # Moving obstacles: traffic lanes with car sprites.
        #   {"image": "assets/sprites/car_red.png",
        #    "rect": (x,y,w,h), "vel": (vx,vy), "bounds": (minx, miny, maxx, maxy)}
        # MOVEMENT OF CAR_LANE_1 HERE
        #   - Starts at x=0, y=400, moves right, bounces between x=0 and x=880.
        # MOVEMENT OF CAR_LANE_2 HERE
        #   - Starts at x=880, y=260, moves left, bounces between x=80 and x=880.
        # Car rect sizes are doubled for visibility.
# ===== HERE IS LEVEL 2 (CITY) =====
# Moving obstacles: traffic lanes with car sprites.
# Cars are obstacles (not collectible).
"moving_objects": [
    # Middle vertical road car (up/down)
    {
        "image": "assets/cars.png",
        "pickupable": False,
        "rect": (SCREEN_W // 2 - 70, 0, 50, 50),
        "vel": (0, 180),
        "bounds": (SCREEN_W // 2 - 70, 40, SCREEN_W // 2 - 60, SCREEN_H - 120),
    },
    # Bottom road car (left/right)
    {
        "image": "assets/carsrl.png",
        "pickupable": False,
        "rect": (0, SCREEN_H - 60, 50, 50),
        "vel": (190, 0),
        "bounds": (0, SCREEN_H - 60, SCREEN_W - 120, SCREEN_H - 80),
    },
],

        "air_rules": {
            "pickup": {
                "water_bottle": 3,     # recycling
                "cardboard_box": 3,    # recycling
                "batteries": 5,          # hazardous
                "electronics": 5,      # hazardous
                "food_waste": 2,       # organic
                "trash": 3,            # general trash
                "chip_bag": 3,
            },
            "step_on": {
                # You can add step-on penalties for specific kinds here if you like.
            },
        },
    },

    # ===== HERE IS LEVEL 3 (OCEAN) =====
    3: {
        "map_path": LEVEL_MAPS[3],
        "spawn": (80, SCREEN_H - 120),
        "target_air": LEVEL_TARGETS[3],

        # Ocean debris & hazards:
        # - Plastic Bags (Common)      -> float near surface
        # - Fishing Nets/Gear (Hazard) -> can entangle player / reduce air
        # - Sunken Electronics         -> rest on seabed
        # - Microplastics (Challenge)  -> many tiny moving pieces
        # - Oil Slicks (Hazard)        -> drifting patches that reduce visibility / air
        "item_spawn": {
            "count": 32,
            "types": [
                "can",
                "chip_bag",
                "water_bottle",
                "fishing_net",
                "sunken_electronics",
                "microplastic",
                "oil_slick",
            ],
        },

        "flow_areas": [
        {
        "rect": [0, 72, 960, 467],      # x, y, width, height (almost whole screen)
        "speed": 40, 
        "on_exit": "remove"                # disappear when completely outside this rect
        }
        ],
        "max_items": 6,
        "spawn_blocked_areas": [
        [0, 0, 960, 72],   #air
        ],
"item_assets": {
    "can": "assets/can.png",
    "chip_bag": "assets/chip_bag.png",
    "water_bottle": "assets/water_bottle.png",
    "fishing_net": "assets/fishing_net.png",
    "sunken_electronics": "assets/electronics.png",
    "microplastic": "assets/trash.png",
    "oil_slick": "assets/oil_slicks.png",
},
"item_sizes": {
    "can": (35, 35),
    "chip_bag": (35, 35),
    "water_bottle": (35, 35),
    "fishing_net": (45, 45),
    "sunken_electronics": (35, 35),
    "microplastic": (35, 35),
    "oil_slick": (45, 45),
},
"intro": {
    "title": "Level 3: Ocean Rescue",
    "lines": [
        "Collect ocean debris to restore air/visibility.",
        "+ Plastic Bags, Microplastics, Sunken Electronics = points",
        "- Fishing Nets and Oil Slicks are hazards (avoid stepping on them)",
    ],
    "dismiss": "Press ENTER to start",
},

        # Moving obstacles to represent currents of microplastics and drifting oil slicks.
        #   {"image": "assets/sprites/microplastics_band.png",
        #    "rect": (x,y,w,h), "vel": (vx,vy), "bounds": (minx, miny, maxx, maxy)}
        # MOVEMENT OF MICROPLASTICS_CURRENT HERE
        #   - Horizontal band near surface: starts at (200, 140), moves between x=160 and x=760.
        # MOVEMENT OF OIL_SLICK_HERE
        #   - Mid-depth patch: starts at (300, 320), moves vertically between y=220 and y=440.
        # Rect sizes here are doubled for clearer visibility.
        "moving_objects": [
            
        ],

        "air_rules": {
            "pickup": {
                "can": 3,
                "chip_bag": 2,
                "water_bottle": 1, 
                "sunken_electronics": 4,
                "microplastic": 3,
            },
            "step_on": {
                # Oil slicks and nets act as hazards when you stand on them.
                "fishing_net": -8,
                "oil_slick": -8,
            },
        },
    },
}

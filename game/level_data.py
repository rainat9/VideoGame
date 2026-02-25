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
                "plastic_bag",
                "water_bottle",
                "electronics",
                "chemical",
            ],
        },
# Item sprites spawned around the map (visible + collectible).
# These MUST cover every kind listed in item_spawn["types"].
"item_assets": {
    "leaf": "assets/leaves.png",
    "plastic_bag": "assets/plastic_bags.png",
    "water_bottle": "assets/water_bottles.png",
    "electronics": "assets/electronics.png",
    "chemical": "assets/chemical.png",
},
# Bigger = easier to see.
"item_sizes": {
    "leaf": (52, 52),
    "plastic_bag": (56, 56),
    "water_bottle": (52, 52),
    "electronics": (60, 60),
    "chemical": (64, 64),
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


        # Static objects with assets (trees, rocks, etc.)
        # Each line connects directly to an asset path in the folder.
        # Format:
        #   {"image": "assets/sprites/<your_forest_asset>.png", "rect": (x, y, w, h)}
        # Rect sizes here are already doubled for clearer visibility.
        "static_objects": [
            {"image": "assets/leaves.png", "rect": (200, 130, 180, 120)},
            {"image": "assets/plastic_bags.png", "rect": (420, 300, 220, 140)},
            {"image": "assets/water_bottles.png", "rect": (680, 160, 240, 120)},
            {"image": "assets/electronics.png", "rect": (840, 220, 200, 160)},
            {"image": "assets/chemical.png", "rect": (1000, 280, 240, 200)},
        ],

        # Trash floating down the river (can use a trash/log sprite).
        # Format:
        #   {"image": "assets/sprites/river_trash.png",
        #    "rect": (x,y,w,h), "vel": (vx,vy), "bounds": (minx, miny, maxx, maxy)}
        # MOVEMENT OF RIVER_TRASH HERE
        #   - Starts near (300, 430), moves horizontally between x=260 and x=700.
        # Rect here is also doubled in size for visibility.
        "moving_objects": [
            {
                "image": "assets/trash.png",
                "rect": (300, 430, 140, 80),
                "vel": (140, 0),
                "bounds": (260, 430, 700, 430),
            },
        ],

        # Air-quality rules
        # Pickups: SPACE while touching item.
        "air_rules": {
            "pickup": {
                "leaf": 1,
                "plastic_bag": 3,
                "water_bottle": 3,
                "electronics": 5,
                "chemical": 6,
            },
            # Hazards applied while standing on the item.
            # Chemical containers reduce the air bar when stepped on.
            "step_on": {
                "chemical": -10,
            },
        },
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
                "battery",
                "electronics",
                "food_waste",
                "trash",
                "chip_bag",
            ],
        },
"item_assets": {
    "water_bottle": "assets/water_bottle.png",
    "cardboard_box": "assets/cardboard_box.png",
    "battery": "assets/battery.png",
    "electronics": "assets/electronics.png",
    "food_waste": "assets/food_waste.png",
    "trash": "assets/trash.png",
    "chip_bag": "assets/chip_bag.png",
},
"item_sizes": {
    "water_bottle": (52, 52),
    "cardboard_box": (64, 64),
    "battery": (52, 52),
    "electronics": (60, 60),
    "food_waste": (60, 60),
    "trash": (60, 60),
    "chip_bag": (56, 56),
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


        # Static city objects (buildings, fences, etc.)
        # Each line points at one image in assets.
        #   {"image": "assets/sprites/city_building_1.png", "rect": (x, y, w, h)}
        # Rect sizes here are doubled for clearer visibility.
        "static_objects": [
            {"image": "assets/water_bottle.png", "rect": (240, 220, 240, 160)},
            {"image": "assets/cardboard_box.png", "rect": (540, 160, 280, 200)},
            {"image": "assets/battery.png", "rect": (840, 220, 200, 160)},
            {"image": "assets/electronics.png", "rect": (1000, 280, 240, 200)},
            {"image": "assets/food_waste.png", "rect": (1160, 340, 280, 240)},
            {"image": "assets/trash.png", "rect": (1320, 400, 320, 280)},
            {"image": "assets/chip_bag.png", "rect": (1480, 460, 360, 320)},
        ],

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
        "image": "assets/car.png",
        "pickupable": False,
        "rect": (SCREEN_W // 2 - 40, 40, 80, 40),
        "vel": (0, 220),
        "bounds": (SCREEN_W // 2 - 40, 40, SCREEN_W // 2 - 40, SCREEN_H - 120),
    },
    # Bottom road car (left/right)
    {
        "image": "assets/car.png",
        "pickupable": False,
        "rect": (40, SCREEN_H - 80, 80, 40),
        "vel": (260, 0),
        "bounds": (40, SCREEN_H - 80, SCREEN_W - 120, SCREEN_H - 80),
    },
],

        "air_rules": {
            "pickup": {
                "water_bottle": 3,     # recycling
                "cardboard_box": 3,    # recycling
                "battery": 5,          # hazardous
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
                "plastic_bag",
                "fishing_net",
                "sunken_electronics",
                "microplastic",
                "oil_slick",
            ],
        },
"item_assets": {
    "plastic_bag": "assets/plastic_bags.png",
    "fishing_net": "assets/fishing_net.png",
    "sunken_electronics": "assets/sunken_electronics.png",
    "microplastic": "assets/microplastic.png",
    "oil_slick": "assets/oil_slicks.png",
},
"item_sizes": {
    "plastic_bag": (56, 56),
    "fishing_net": (72, 72),
    "sunken_electronics": (72, 72),
    "microplastic": (44, 44),
    "oil_slick": (72, 56),
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


        # Static obstacles (rocks, reef structures)
        #   {"image": "assets/sprites/reef_rock.png", "rect": (x, y, w, h)}
        # Rect sizes here are doubled for clearer visibility.
        "static_objects": [
            {"image": "assets/fishing_net.png", "rect": (520, 250, 320, 200)},
            {"image": "assets/sunken_electronics.png", "rect": (780, 310, 360, 240)},
            {"image": "assets/microplastic.png", "rect": (1040, 370, 400, 280)},
            {"image": "assets/oil_slicks.png", "rect": (1300, 430, 440, 320)},
        ],

        # Moving obstacles to represent currents of microplastics and drifting oil slicks.
        #   {"image": "assets/sprites/microplastics_band.png",
        #    "rect": (x,y,w,h), "vel": (vx,vy), "bounds": (minx, miny, maxx, maxy)}
        # MOVEMENT OF MICROPLASTICS_CURRENT HERE
        #   - Horizontal band near surface: starts at (200, 140), moves between x=160 and x=760.
        # MOVEMENT OF OIL_SLICK_HERE
        #   - Mid-depth patch: starts at (300, 320), moves vertically between y=220 and y=440.
        # Rect sizes here are doubled for clearer visibility.
        "moving_objects": [
            {
                "image": "assets/plastic_bags.png",
                "rect": (200, 140, 240, 60),
                "vel": (150, 0),
                "bounds": (160, 140, 760, 140),
            },
        ],

        "air_rules": {
            "pickup": {
                "plastic_bag": 3,
                "fishing_net": 5,
                "sunken_electronics": 5,
                "microplastic": 4,
                "oil_slick": 6,
            },
            "step_on": {
                # Oil slicks and nets act as hazards when you stand on them.
                "fishing_net": -8,
                "oil_slick": -8,
            },
        },
    },
}

# states/level_state.py
from __future__ import annotations

import math
import random
import pygame

from states.base_state import BaseState
from assets import load_image
from settings import (
    SCREEN_W, SCREEN_H,
    PLAYER_SPEED,
    PLAYER_SIZE,
    AIR_MIN, AIR_MAX, AIR_START,
    FOG_MIN_ALPHA, FOG_MAX_ALPHA,
    UI_PADDING, UI_BAR_W, UI_BAR_H,
    LAST_LEVEL,
    PLAYER_SPRITES,
)
from game.level_data import LEVELS


# ---------- helpers ----------

def clamp(v: int, lo: int, hi: int) -> int:
    return max(lo, min(hi, v))


def _wrap_into_screen(rect: pygame.Rect, margin: int = 16) -> pygame.Rect:
    """
    If level_data has coordinates larger than the screen (common when maps were designed
    for a bigger canvas), wrap them back into the visible 960x540 playfield so the game
    stays playable without adding a camera system.
    """
    r = rect.copy()
    if r.w >= SCREEN_W - 2 * margin:
        r.w = max(8, SCREEN_W - 2 * margin)
    if r.h >= SCREEN_H - 2 * margin:
        r.h = max(8, SCREEN_H - 2 * margin)

    # Wrap X/Y into [margin, SCREEN - margin - size]
    max_x = max(margin, SCREEN_W - margin - r.w)
    max_y = max(margin, SCREEN_H - margin - r.h)

    if r.x < margin or r.x > max_x:
        r.x = margin + (r.x - margin) % (max_x - margin + 1)
    if r.y < margin or r.y > max_y:
        r.y = margin + (r.y - margin) % (max_y - margin + 1)
    return r


def _scale_rect(rect: pygame.Rect, scale: float, anchor: str = "center") -> pygame.Rect:
    if scale == 1.0:
        return rect.copy()
    r = rect.copy()
    cx, cy = r.center
    r.w = max(1, int(round(r.w * scale)))
    r.h = max(1, int(round(r.h * scale)))
    if anchor == "topleft":
        # keep top-left fixed
        return pygame.Rect(rect.x, rect.y, r.w, r.h)
    r.center = (cx, cy)
    return r


# ---------- game objects ----------

class Player:
    def __init__(self, pos: tuple[int, int]) -> None:
        self.rect = pygame.Rect(pos[0], pos[1], PLAYER_SIZE[0], PLAYER_SIZE[1])
        self.speed = PLAYER_SPEED

    def update(self, dt: float, keys: pygame.key.ScancodeWrapper) -> pygame.Rect:
        dx = dy = 0.0
        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            dx -= 1
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            dx += 1
        if keys[pygame.K_w] or keys[pygame.K_UP]:
            dy -= 1
        if keys[pygame.K_s] or keys[pygame.K_DOWN]:
            dy += 1

        if dx != 0 and dy != 0:
            inv = 0.70710678
            dx *= inv
            dy *= inv

        old = self.rect.copy()
        self.rect.x += int(dx * self.speed * dt)
        self.rect.y += int(dy * self.speed * dt)

        # keep in bounds of screen
        self.rect.x = max(0, min(SCREEN_W - self.rect.w, self.rect.x))
        self.rect.y = max(0, min(SCREEN_H - self.rect.h, self.rect.y))

        return old


class StaticObject:
    """World object with an image and a collision rect (can be collectible)."""
    def __init__(self, image_path: str, rect: pygame.Rect) -> None:
        self.image_path = image_path
        self.rect = rect
        try:
            self.image = load_image(image_path, scale_to=(rect.w, rect.h))
        except Exception:
            self.image = None


class Item:
    def __init__(self, kind: str, rect: pygame.Rect, image: pygame.Surface | None,
                 spawn_time: float, lifetime: float,
                 moving: bool = False, vx: float = 0, vy: float = 0,
                 bounds: pygame.Rect | None = None,
                 on_exit: str = "bounce"):          # new parameter
        self.kind = kind
        self.rect = rect
        self.image = image
        self.spawn_time = spawn_time
        self.lifetime = lifetime
        self.moving = moving
        self.vx = vx
        self.vy = vy
        self.bounds = bounds
        self.on_exit = on_exit


class MovingObstacle:
    """Moving world object with an image and patrol bounds."""
    def __init__(
        self,
        image_path: str,
        rect: pygame.Rect,
        vel: tuple[float, float],
        bounds: pygame.Rect,
    ) -> None:
        self.image_path = image_path
        self.rect = rect
        self.vx, self.vy = vel
        self.bounds = bounds

        try:
            self.image = load_image(image_path, scale_to=(rect.w, rect.h))
        except Exception:
            self.image = None

    def update(self, dt: float) -> None:
        self.rect.x += int(self.vx * dt)
        self.rect.y += int(self.vy * dt)

        if self.rect.left < self.bounds.left or self.rect.right > self.bounds.right:
            self.vx *= -1
        if self.rect.top < self.bounds.top or self.rect.bottom > self.bounds.bottom:
            self.vy *= -1

        self.rect.left = max(self.bounds.left, self.rect.left)
        self.rect.right = min(self.bounds.right, self.rect.right)
        self.rect.top = max(self.bounds.top, self.rect.top)
        self.rect.bottom = min(self.bounds.bottom, self.rect.bottom)


# ---------- level state ----------

class LevelState(BaseState):
    """
    Keeps original gameplay flow (player movement, fog, air target, SPACE pickup),
    and adds:
      - bigger/more visible items/collectibles
      - enough spawns to realistically reach the target air
      - per-level intro popup explaining scoring + hazards
      - cars are NOT collectible; they are obstacles (small air penalty on hit)
    """
    # Default mapping from item kind -> asset path (adjust if your filenames differ).
    ITEM_ASSETS: dict[str, str] = {
        "leaf": "assets/leaves.png",
        "can": "assets/can.png",
        "water_bottle": "assets/water_bottle.png",
        "electronics": "assets/electronics.png",
        "chemical": "assets/chemical_container.png",
        "cardboard_box": "assets/cardboard_box.png",
        "batteries": "assets/batteries.png",
        "food_waste": "assets/food_waste.png",
        "trash": "assets/trash.png",
        "chip_bag": "assets/chip_bag.png",
        "fishing_net": "assets/fishing_net.png",
        "sunken_electronics": "assets/electronics.png",
        "microplastic": "assets/trash.png",
        "oil_slick": "assets/oil_slicks.png",
    }

    # Bigger by default, but still reasonable for a 960x540 screen.
    DEFAULT_ITEM_SIZE = (84, 84)
    def __init__(self, level_id: int) -> None:
        self.level_id = level_id
        self.cfg = LEVELS[level_id]
        self._next: BaseState | None = None
        
        # Background (static map image)
        self.bg = load_image(self.cfg["map_path"], scale_to=(SCREEN_W, SCREEN_H))

        # Player
        self.player = Player(self.cfg["spawn"])

        # Player sprite
        self.player_image: pygame.Surface | None = None
        try:
            idle_path = PLAYER_SPRITES.get("idle")
            if idle_path:
                self.player_image = load_image(idle_path, scale_to=(self.player.rect.w, self.player.rect.h))
        except Exception:
            self.player_image = None

        # Rules
        self.air_pickup: dict[str, int] = dict(self.cfg["air_rules"].get("pickup", {}))
        self.air_step_on: dict[str, int] = dict(self.cfg["air_rules"].get("step_on", {}))

        # Air + fog
        self.air = AIR_START
        self.target_air = int(self.cfg["target_air"])

        # Load collision rectangles (player cannot enter)
        self.collision_rects = []
        for rect_data in self.cfg.get("player_collision", []):
            self.collision_rects.append(pygame.Rect(*rect_data))

         # Max items on screen at once (default 5, can be set per level later)
        self.max_items = self.cfg.get("max_items", 5)

        # Spawn timer (seconds)
        self.spawn_interval = 2.0          # spawn a new item every 2 seconds
        self.spawn_timer = random.uniform(0, self.spawn_interval)  # random start

        # Blocked areas for spawning (from level data)
        self.spawn_blocked = []
        for rect_data in self.cfg.get("spawn_blocked_areas", []):
            self.spawn_blocked.append(pygame.Rect(*rect_data))

         # --- NEW: load flow areas (for drifting items) ---
        self.flow_areas = []
        for fa in self.cfg.get("flow_areas", []):
            area = {
                "rect": pygame.Rect(*fa["rect"]),
                "on_exit": fa.get("on_exit", "bounce")
            }
            if "vel" in fa:
                area["vel"] = fa["vel"]          # fixed (vx, vy)
            if "speed" in fa:
                area["speed"] = fa["speed"]      # constant horizontal speed, random direction
            self.flow_areas.append(area)

        
        self.fog_surface = pygame.Surface((SCREEN_W, SCREEN_H))
        self.fog_surface.fill((0, 0, 0))
        self.fog_alpha = 0

        # UI font
        self.font = pygame.font.Font(None, 22)
        self.big_font = pygame.font.Font(None, 34)

        self.t = 0.0  # time accumulator for pulsing

        # Intro popup
        self.level_intro_active = True

        # World objects (static + moving)
        self.static_objects: list[StaticObject] = []
        self.moving_obstacles: list[MovingObstacle] = []
        self._load_world_objects()

        # Items (random-spawned collectibles)
        self.items: list[Item] = []
        self._spawn_items()  # IMPORTANT: actually spawn them

        # Car collision penalty cooldown (prevents draining every frame)
        self._car_hit_cooldown = 0.0
        
    # ---------- world loading ----------

    def _load_world_objects(self) -> None:
        # Only affects non-car moving objects and all static objects.
        static_scale = float(self.cfg.get("static_scale", 1.25))
        moving_scale = float(self.cfg.get("moving_scale", 1.25))

        # Static objects
        for so in self.cfg.get("static_objects", []):
            r = pygame.Rect(*so["rect"])
            r = _scale_rect(r, static_scale, anchor="center")
            r = _wrap_into_screen(r, margin=16)
            self.static_objects.append(StaticObject(so["image"], r))

        # Moving objects
        for mo in self.cfg.get("moving_objects", []):
            r = pygame.Rect(*mo["rect"])
            bminx, bminy, bmaxx, bmaxy = mo["bounds"]
            bounds_rect = pygame.Rect(bminx, bminy, bmaxx - bminx, bmaxy - bminy)

            # Wrap/scaling so patrol stays visible
            is_car = ("car" in mo["image"].lower())
            if not is_car:
                r = _scale_rect(r, moving_scale, anchor="center")
            r = _wrap_into_screen(r, margin=16)

            # bounds rect: if it was "line bounds" (same min/max on one axis), preserve that behavior
            bounds_rect = _wrap_into_screen(bounds_rect, margin=16)
            self.moving_obstacles.append(MovingObstacle(mo["image"], r, mo["vel"], bounds_rect))

    # ---------- item spawning / assets ----------

    def _item_size_for_kind(self, kind: str) -> tuple[int, int]:
        sizes = self.cfg.get("item_sizes", {})
        if isinstance(sizes, dict) and kind in sizes:
            w, h = sizes[kind]
            return int(w), int(h)
        return self.DEFAULT_ITEM_SIZE

    def _load_item_image(self, kind: str, size: tuple[int, int]) -> pygame.Surface | None:
        path = self.ITEM_ASSETS.get(kind)
        if not path:
            # try a simple fallback
            path = f"assets/{kind}.png"
        try:
            return load_image(path, scale_to=size)
        except Exception:
            return None

    def _spawn_items(self) -> None:
        self.items = []
        for _ in range(self.max_items):
            self._spawn_one_item()

    def _spawn_one_item(self) -> None:
    # Gather all possible kinds from level config and rules
        kinds = list(self.cfg.get("item_spawn", {}).get("types", []))
        for k in list(self.air_pickup.keys()) + list(self.air_step_on.keys()):
            if k not in kinds:
                kinds.append(k)
        if not kinds:
            return

        kind = random.choice(kinds)
        w, h = self._item_size_for_kind(kind)

        # Occupied rectangles: static objects + player + existing items
        blocked = [o.rect.copy() for o in self.static_objects]
        blocked.append(self.player.rect.copy())
        blocked.extend(it.rect for it in self.items)

        rect = self._random_free_rect(blocked, w, h)
        img = self._load_item_image(kind, (w, h))

        if self.level_id == 3:
            lifetime = 1e9   
        else:
            lifetime = random.uniform(8.0, 15.0)

        # Determine if this item should flow
        moving = False
        
        vx = vy = 0
        bounds = None
        on_exit = "bounce"
        for fa in self.flow_areas:
            if rect.colliderect(fa["rect"]):
                moving = True
                bounds = fa["rect"]
                on_exit = fa["on_exit"]
                if "vel" in fa:
                    vx, vy = fa["vel"]
                elif "speed" in fa:
                    # constant speed, random horizontal direction
                    direction = random.choice([-1, 1])
                    vx = fa["speed"] * direction
                    vy = 0
                else:
                    # fallback – no movement
                    vx = vy = 0
                break

        self.items.append(Item(kind, rect, img, self.t, lifetime,
                               moving=moving, vx=vx, vy=vy, bounds=bounds,
                               on_exit=on_exit))  

    def _random_free_rect(self, blocked: list[pygame.Rect], w: int, h: int) -> pygame.Rect:
        # Keep away from edges so items are visible
        margin_x = 24
        margin_y = 10
        max_x = max(margin_x, SCREEN_W - margin_x - w)
        max_y = max(margin_y, SCREEN_H - margin_y - h)

        for _ in range(800):
            x = random.randint(margin_x, max_x)
            y = random.randint(margin_y, max_y)
            r = pygame.Rect(x, y, w, h)
            if any(r.colliderect(b) for b in blocked):
                continue
            if any(r.colliderect(area) for area in self.spawn_blocked):
                continue
            return r
        # fallback
        return pygame.Rect(margin_x, margin_y, w, h)

    # ---------- input ----------

    def handle_event(self, event: pygame.event.Event) -> None:
        if event.type != pygame.KEYDOWN:
            return

        if event.key == pygame.K_ESCAPE:
            pygame.event.post(pygame.event.Event(pygame.QUIT))

        # Level intro gating
        if self.level_intro_active:
            if event.key in (pygame.K_RETURN, pygame.K_KP_ENTER):
                self.level_intro_active = False
            return

        if event.key == pygame.K_SPACE:
            self._try_pickup()

        # dev shortcut: skip level
        if event.key == pygame.K_n:
            self.air = self.target_air

    # ---------- gameplay rules ----------

    def _is_collectible_moving(self, image_path: str) -> bool:
        # Cars are obstacles, not collectible.
        return ("car" not in image_path.lower())

    def _try_pickup(self) -> None:
        # Only check random items (self.items)
        for i, it in enumerate(self.items):
            if self.player.rect.colliderect(it.rect):
                gain = int(self.air_pickup.get(it.kind, 1))
                self.air += gain
                self.air = clamp(self.air, AIR_MIN, AIR_MAX)
                self.items.pop(i)
                return

        # Moving objects: collectible if not a car
        for i, mo in enumerate(self.moving_obstacles):
            if self.player.rect.colliderect(mo.rect):
                if not self._is_collectible_moving(mo.image_path):
                    return
                delta = self._delta_for_asset_path(mo.image_path)
                if delta != 0:
                    self.air += delta
                    self.air = clamp(self.air, AIR_MIN, AIR_MAX)
                    self.moving_obstacles.pop(i)
                return

    def _delta_for_asset_path(self, image_path: str) -> int:
        """
        Convert a static/moving asset into an air delta, based on whether it looks like
        a hazardous item. Keeps original feel (SPACE to interact) but avoids breaking
        when filenames differ slightly.
        """
        p = image_path.lower()

        # Hazards
        if "chemical" in p or "oil" in p or "batteries" in p or "net" in p:
            return -abs(int(self.air_step_on.get("chemical", -8)))  # negative

        # Cars not collectible
        if "car" in p:
            return 0

        return 6

    # ---------- update/draw ----------

    def update(self, dt: float) -> None:
        self.t += dt
        if self.level_intro_active:
            # freeze gameplay until player acknowledges the popup
            return

        keys = pygame.key.get_pressed()
        old_rect = self.player.rect.copy()
        self.player.update(dt, keys)

        # --- NEW: collision with solid objects ---
        for rect in self.collision_rects:
            if self.player.rect.colliderect(rect):
                self.player.rect = old_rect
                break

        # Update moving obstacles
        for mo in self.moving_obstacles:
            mo.update(dt)

        # Step-on hazards from random items
        for i, it in enumerate(self.items):
            if it.kind in self.air_step_on and self.player.rect.colliderect(it.rect):
                self.air += int(self.air_step_on[it.kind])  # should be negative
                self.items.pop(i)
                break

        # Car collisions (non-collectible moving obstacles)
        if self._car_hit_cooldown > 0:
            self._car_hit_cooldown = max(0.0, self._car_hit_cooldown - dt)
        else:
            for mo in self.moving_obstacles:
                if ("car" in mo.image_path.lower()) and self.player.rect.colliderect(mo.rect):
                    self.air -= 6
                    self._car_hit_cooldown = 0.6
                    break
        # Move flowing items – bounce or remove on exit
        new_items = []
        for it in self.items:
            if it.moving and it.bounds is not None:
                it.rect.x += it.vx * dt
                it.rect.y += it.vy * dt

                if it.on_exit == "bounce":
                    # Bounce inside bounds
                    if it.rect.left < it.bounds.left:
                        it.rect.left = it.bounds.left
                        it.vx = -it.vx
                    if it.rect.right > it.bounds.right:
                        it.rect.right = it.bounds.right
                        it.vx = -it.vx
                    if it.rect.top < it.bounds.top:
                        it.rect.top = it.bounds.top
                        it.vy = -it.vy
                    if it.rect.bottom > it.bounds.bottom:
                        it.rect.bottom = it.bounds.bottom
                        it.vy = -it.vy
                    new_items.append(it)

                elif it.on_exit == "remove":
                    # If completely outside bounds, discard
                    if (it.rect.right < it.bounds.left or
                        it.rect.left > it.bounds.right or
                        it.rect.bottom < it.bounds.top or
                        it.rect.top > it.bounds.bottom):
                        continue          # skip → item disappears
                    new_items.append(it)

            else:
                # Non‑moving items are always kept
                new_items.append(it)

        self.items = new_items

        if not self.level_intro_active:
            self.spawn_timer -= dt
            while self.spawn_timer <= 0 and len(self.items) < self.max_items:
                self.spawn_timer += self.spawn_interval
                self._spawn_one_item()

        self.air = clamp(self.air, AIR_MIN, AIR_MAX)

        # Remove items that have expired
        current_time = self.t
        self.items = [it for it in self.items if current_time - it.spawn_time < it.lifetime]

        # Fog: low air => higher alpha
        self.fog_alpha = int(FOG_MAX_ALPHA - (self.air / AIR_MAX) * (FOG_MAX_ALPHA - FOG_MIN_ALPHA))
        self.fog_alpha = clamp(self.fog_alpha, FOG_MIN_ALPHA, FOG_MAX_ALPHA)
        self.fog_surface.set_alpha(self.fog_alpha)

        # Transition
        if self.air >= self.target_air:
            self._advance()

    def _advance(self) -> None:
        if self.level_id < LAST_LEVEL:
            self._next = LevelState(self.level_id + 1)
        else:
            from states.end_state import EndState
            self._next = EndState()

    def draw(self, screen: pygame.Surface) -> None:
        screen.blit(self.bg, (0, 0))

        # Static objects
        for obj in self.static_objects:
            if obj.image is not None:
                screen.blit(obj.image, obj.rect)
            else:
                pygame.draw.rect(screen, (110, 110, 110), obj.rect, 2)

        # Moving objects
        for mo in self.moving_obstacles:
            if mo.image is not None:
                screen.blit(mo.image, mo.rect)
            else:
                pygame.draw.rect(screen, (200, 80, 80), mo.rect, 2)

        # Random items (collectibles) — make them obvious
        for it in self.items:
            # Soft pulsing "halo" behind items to make them obvious (no borders)
            pulse = 0.65 + 0.35 * (0.5 + 0.5 * math.sin(self.t * 4.0))  # 0.65..1.0
            glow_w = int(it.rect.w * (1.15 + 0.10 * pulse))
            glow_h = int(it.rect.h * (1.15 + 0.10 * pulse))

            glow = pygame.Surface((glow_w, glow_h), pygame.SRCALPHA)
            # subtle minty/blue-ish glow; not a border
            glow.fill((60, 220, 200, int(70 * pulse)))
            glow_rect = glow.get_rect(center=it.rect.center)
            screen.blit(glow, glow_rect)

            if it.image is not None:
                screen.blit(it.image, it.rect)
            else:
                # fallback: readable box without border
                box = pygame.Surface((it.rect.w, it.rect.h), pygame.SRCALPHA)
                box.fill((240, 240, 0, 220))
                screen.blit(box, it.rect)
                label = self.font.render(it.kind.replace("_", " "), True, (0, 0, 0))
                screen.blit(label, (it.rect.x + 6, it.rect.y + 6))

        # Player
        if self.player_image is not None:
            screen.blit(self.player_image, self.player.rect)
        else:
            pygame.draw.rect(screen, (240, 240, 240), self.player.rect)

        # Fog overlay (only after intro)
        if not self.level_intro_active:
            screen.blit(self.fog_surface, (0, 0))

        # UI
        self._draw_ui(screen)

        # Level intro popup
        if self.level_intro_active:
            self._draw_level_intro(screen)

    def _draw_ui(self, screen: pygame.Surface) -> None:
        x = UI_PADDING
        y = UI_PADDING
        pygame.draw.rect(screen, (20, 20, 20), (x - 2, y - 2, UI_BAR_W + 4, UI_BAR_H + 4))
        pygame.draw.rect(screen, (60, 60, 60), (x, y, UI_BAR_W, UI_BAR_H))
        fill = int((self.air / AIR_MAX) * UI_BAR_W)
        pygame.draw.rect(screen, (120, 220, 120), (x, y, fill, UI_BAR_H))

        txt = self.font.render(f"Air: {self.air}/{AIR_MAX}  Target: {self.target_air}", True, (255, 255, 255))
        screen.blit(txt, (x, y + UI_BAR_H + 6))

        lvl = self.font.render(f"Level {self.level_id}", True, (255, 255, 255))
        screen.blit(lvl, (SCREEN_W - lvl.get_width() - UI_PADDING, UI_PADDING))

        hint = self.font.render("SPACE: pick up   N: skip (dev)", True, (230, 230, 230))
        screen.blit(hint, (UI_PADDING, SCREEN_H - 26))

    def _draw_level_intro(self, screen: pygame.Surface) -> None:
        overlay = pygame.Surface((SCREEN_W, SCREEN_H), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))
        screen.blit(overlay, (0, 0))

        pad = 24
        box_w = SCREEN_W - 2 * pad
        box_h = SCREEN_H - 2 * pad
        box = pygame.Rect(pad, pad, box_w, box_h)
        pygame.draw.rect(screen, (30, 30, 30), box)
        pygame.draw.rect(screen, (255, 255, 255), box, 2)

        title = self.big_font.render(f"Level {self.level_id}", True, (255, 255, 255))
        screen.blit(title, (box.x + 18, box.y + 16))

        # Build explanation from rules
        pickups = sorted(self.air_pickup.items(), key=lambda kv: -int(kv[1]))
        hazards = sorted(self.air_step_on.items(), key=lambda kv: int(kv[1]))  # negative first

        lines: list[str] = []
        lines.append("Goal: collect items to raise Air until you reach the target.")
        lines.append("SPACE while touching an item/object to collect it.")
        lines.append("")
        lines.append("Counts for points (Air increases):")
        if pickups:
            lines.append("  " + ", ".join([f"{k} (+{v})" for k, v in pickups]))
        else:
            lines.append("  (none configured)")
        lines.append("")
        lines.append("Hazards (Air decreases if you step on them):")
        if hazards:
            lines.append("  " + ", ".join([f"{k} ({v})" for k, v in hazards]))
        else:
            lines.append("  (none configured)")
        lines.append("")
        lines.append("Traffic cars do NOT give points (avoid them).")
        lines.append("")
        lines.append("Press ENTER to start.")

        y = box.y + 70
        for s in lines:
            surf = self.font.render(s, True, (240, 240, 240))
            screen.blit(surf, (box.x + 18, y))
            y += 24

    def next_state(self) -> BaseState | None:
        return self._next

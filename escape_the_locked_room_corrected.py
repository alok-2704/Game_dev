import pygame
import sys
import math
import random

pygame.init()

# ============================================================
# ESCAPE: THE LOCKED ROOM
# ============================================================

WIDTH, HEIGHT = 1200, 720
FPS = 60
GAME_TIME = 150

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Escape: The Locked Room")
clock = pygame.time.Clock()

# ---------------- COLORS ----------------
BG = (12, 14, 20)
WALL = (43, 46, 57)
WALL_LIGHT = (58, 62, 74)
WALL_DARK = (31, 33, 42)
FLOOR = (77, 56, 43)
FLOOR_LINE = (98, 72, 53)
PANEL = (20, 23, 31)
PANEL_2 = (29, 33, 43)
WHITE = (239, 242, 246)
MUTED = (158, 165, 177)
GOLD = (224, 178, 76)
GOLD_BRIGHT = (250, 210, 105)
BLUE = (75, 145, 225)
BLUE_LIGHT = (118, 184, 245)
GREEN = (71, 190, 119)
RED = (220, 78, 84)
WOOD = (101, 62, 39)
WOOD_LIGHT = (139, 88, 53)
BLACK = (5, 7, 10)
SKIN = (240, 190, 150)
HAIR = (45, 30, 20)
SHIRT = (45, 100, 185)
PANTS = (35, 45, 60)

# ---------------- FONTS ----------------
def font(size, bold=False):
    return pygame.font.SysFont("arial", size, bold=bold)

F_TITLE = font(58, True)
F_H1 = font(34, True)
F_H2 = font(24, True)
F_BODY = font(19)
F_SMALL = font(15)
F_TINY = font(12)

# ============================================================
# HELPERS
# ============================================================

def text(surface, value, pos, color=WHITE, f=F_BODY, center=False):
    img = f.render(str(value), True, color)
    rect = img.get_rect()
    if center:
        rect.center = pos
    else:
        rect.topleft = pos
    surface.blit(img, rect)
    return rect

def rounded(surface, rect, color, radius=10, border=None, width=1):
    pygame.draw.rect(surface, color, rect, border_radius=radius)
    if border:
        pygame.draw.rect(surface, border, rect, width=width, border_radius=radius)

def clamp(value, low, high):
    return max(low, min(high, value))

# ============================================================
# PARTICLES / ATMOSPHERE
# ============================================================

class Particle:
    def __init__(self):
        self.x = random.randint(0, WIDTH)
        self.y = random.randint(0, HEIGHT)
        self.r = random.choice([1, 1, 2])
        self.speed = random.uniform(0.08, 0.25)
        self.alpha = random.randint(25, 60)

    def update(self):
        self.y -= self.speed
        if self.y < 70:
            self.y = HEIGHT
            self.x = random.randint(0, WIDTH)

    def draw(self, surf):
        p = pygame.Surface((self.r * 2, self.r * 2), pygame.SRCALPHA)
        pygame.draw.circle(p, (220, 200, 160, self.alpha), (self.r, self.r), self.r)
        surf.blit(p, (int(self.x), int(self.y)))

particles = [Particle() for _ in range(70)]

# ============================================================
# HUMAN PLAYER CHARACTER (ENLARGED & ANIMATED)
# ============================================================

class Player:
    def __init__(self):
        # Increased size hitbox: 38x64 px
        self.rect = pygame.Rect(580, 560, 38, 64)
        self.speed = 220
        self.walk_time = 0
        self.idle_time = 0
        self.facing = "down"
        self.is_moving = False

    def reset(self):
        self.rect.topleft = (580, 560)
        self.walk_time = 0
        self.idle_time = 0
        self.facing = "down"
        self.is_moving = False

    def move(self, dt, obstacles):
        keys = pygame.key.get_pressed()
        dx = int(keys[pygame.K_d] or keys[pygame.K_RIGHT]) - int(keys[pygame.K_a] or keys[pygame.K_LEFT])
        dy = int(keys[pygame.K_s] or keys[pygame.K_DOWN]) - int(keys[pygame.K_w] or keys[pygame.K_UP])

        self.is_moving = (dx != 0 or dy != 0)

        if self.is_moving:
            length = math.hypot(dx, dy)
            dx = dx / length * self.speed * dt
            dy = dy / length * self.speed * dt

            if abs(dx) > abs(dy):
                self.facing = "right" if dx > 0 else "left"
            elif abs(dy) > 0:
                self.facing = "down" if dy > 0 else "up"

            self._move_axis(dx, 0, obstacles)
            self._move_axis(0, dy, obstacles)
            self.walk_time += dt * 10
        else:
            self.walk_time = 0
            self.idle_time += dt * 3

        self.rect.left = clamp(self.rect.left, 25, WIDTH - 25 - self.rect.width)
        self.rect.top = clamp(self.rect.top, 105, HEIGHT - 35 - self.rect.height)

    def _move_axis(self, dx, dy, obstacles):
        self.rect.x += int(dx)
        self.rect.y += int(dy)
        for obstacle in obstacles:
            if self.rect.colliderect(obstacle):
                if dx > 0:
                    self.rect.right = obstacle.left
                elif dx < 0:
                    self.rect.left = obstacle.right
                if dy > 0:
                    self.rect.bottom = obstacle.top
                elif dy < 0:
                    self.rect.top = obstacle.bottom

    def draw(self, surf):
        cx = self.rect.centerx
        cy = self.rect.centery

        # Walking bob and subtle breathing idle animation
        if self.is_moving:
            bob = int(math.sin(self.walk_time) * 2)
            stride_l = int(math.sin(self.walk_time) * 3)
            stride_r = -stride_l
            arm_swing = int(math.cos(self.walk_time) * 4)
        else:
            bob = int(math.sin(self.idle_time) * 1.2)
            stride_l, stride_r, arm_swing = 0, 0, 0

        # Ground Shadow
        pygame.draw.ellipse(surf, (8, 9, 12, 170), (cx - 20, self.rect.bottom - 5, 40, 12))

        # Legs & Shoes (Enlarged)
        pygame.draw.rect(surf, PANTS, (cx - 9, self.rect.bottom - 22 + stride_l, 7, 16), border_radius=2)
        pygame.draw.rect(surf, PANTS, (cx + 2, self.rect.bottom - 22 + stride_r, 7, 16), border_radius=2)
        pygame.draw.rect(surf, (28, 18, 14), (cx - 10, self.rect.bottom - 7 + stride_l, 8, 6), border_radius=2)
        pygame.draw.rect(surf, (28, 18, 14), (cx + 2, self.rect.bottom - 7 + stride_r, 8, 6), border_radius=2)

        # Torso / Shirt
        torso_rect = pygame.Rect(cx - 11, cy - 12 + bob, 22, 24)
        pygame.draw.rect(surf, SHIRT, torso_rect, border_radius=4)
        # Collar accent
        pygame.draw.polygon(surf, WHITE, [(cx - 4, cy - 12 + bob), (cx + 4, cy - 12 + bob), (cx, cy - 7 + bob)])

        # Arms & Hands
        pygame.draw.rect(surf, SHIRT, (cx - 15, cy - 10 + bob + arm_swing, 4, 15), border_radius=2)
        pygame.draw.rect(surf, SHIRT, (cx + 11, cy - 10 + bob - arm_swing, 4, 15), border_radius=2)
        pygame.draw.circle(surf, SKIN, (cx - 13, cy + 7 + bob + arm_swing), 3)
        pygame.draw.circle(surf, SKIN, (cx + 13, cy + 7 + bob - arm_swing), 3)

        # Neck & Head
        pygame.draw.rect(surf, SKIN, (cx - 3, cy - 16 + bob, 6, 6))
        head_center = (cx, cy - 24 + bob)
        pygame.draw.circle(surf, SKIN, head_center, 12)

        # Hair
        pygame.draw.circle(surf, HAIR, (cx, cy - 26 + bob), 12)
        pygame.draw.rect(surf, HAIR, (cx - 11, cy - 32 + bob, 22, 9), border_radius=3)

        # Expressive Eyes based on facing direction
        if self.facing == "down":
            pygame.draw.circle(surf, BLACK, (cx - 4, cy - 23 + bob), 2)
            pygame.draw.circle(surf, BLACK, (cx + 4, cy - 23 + bob), 2)
        elif self.facing == "left":
            pygame.draw.circle(surf, BLACK, (cx - 7, cy - 23 + bob), 2)
        elif self.facing == "right":
            pygame.draw.circle(surf, BLACK, (cx + 7, cy - 23 + bob), 2)

# ============================================================
# GAME OBJECTS & LOGIC
# ============================================================

class RoomObject:
    def __init__(self, name, rect, description):
        self.name = name
        self.rect = pygame.Rect(rect)
        self.description = description

    def nearby(self, player_rect):
        return player_rect.colliderect(self.rect.inflate(50, 50))

class Game:
    def __init__(self):
        self.state = "menu"
        self.player = Player()

        self.painting = RoomObject("Painting", (480, 110, 240, 130), "A strange landscape. A tiny number is scratched behind the frame.")
        self.bookshelf = RoomObject("Bookshelf", (50, 380, 180, 230), "Several books are dusty. One red book looks recently moved.")
        self.desk = RoomObject("Desk", (360, 440, 240, 100), "A clean wooden study desk with drawers.")
        self.box = RoomObject("Safe", (720, 440, 130, 95), "A secure metal safe on a wooden pedestal.")
        self.door = RoomObject("Exit Door", (1040, 200, 100, 245), "A heavy wooden door requiring a key.")

        self.objects = [self.painting, self.bookshelf, self.desk, self.box, self.door]

        self.inventory_items = []
        self.inventory_clues = {}
        self.has_key = False
        self.drawer_open = False
        self.box_open = False
        self.code_attempts = 3
        self.code_input = ""
        self.code = "543"  # Clue 1 = 5, Clue 2 = 4, Clue 3 = 3

        self.start_ticks = 0
        self.score = 0
        self.message = ""
        self.message_until = 0
        self.popup_title = ""
        self.popup_text = ""
        self.nearby = None
        self.flash = 0
        self.victory_time = 0

    def start(self):
        self.state = "playing"
        self.player.reset()
        self.inventory_items.clear()
        self.inventory_clues.clear()
        self.has_key = False
        self.drawer_open = False
        self.box_open = False
        self.code_attempts = 3
        self.code_input = ""
        self.score = 0
        self.message = ""
        self.start_ticks = pygame.time.get_ticks()

    def elapsed(self):
        return (pygame.time.get_ticks() - self.start_ticks) / 1000

    def remaining(self):
        return max(0, GAME_TIME - int(self.elapsed()))

    def show_message(self, msg, seconds=3):
        self.message = msg
        self.message_until = pygame.time.get_ticks() + seconds * 1000

    def open_popup(self, title, body):
        self.state = "popup"
        self.popup_title = title
        self.popup_text = body

    def interact(self):
        if not self.nearby:
            return

        name = self.nearby.name

        # CLUE 1: PAINTING
        if name == "Painting":
            if "Painting Inscription" not in self.inventory_clues:
                body = (
                    "\"The first number is hidden among the stories.\"\n\n"
                    "\"Look where books stand, from top to bottom.\""
                )
                self.inventory_clues["Painting Inscription"] = body
                self.score += 100
                self.open_popup("A HIDDEN INSCRIPTION", body)
            else:
                self.open_popup("PAINTING", self.inventory_clues["Painting Inscription"])

        # CLUE 2: BOOKSHELF
        elif name == "Bookshelf":
            if "The Red Book" not in self.inventory_clues:
                body = (
                    "\"The last number is kept where things are stored.\"\n\n"
                )
                self.inventory_clues["The Red Book"] = body
                self.score += 100
                self.open_popup("THE RED BOOK", body)
            else:
                self.open_popup("BOOKSHELF", self.inventory_clues["The Red Book"])

        # CLUE 3: DESK
        elif name == "Desk":
            if not self.drawer_open:
                self.drawer_open = True
                if "Desk Note" not in self.inventory_clues:
                    body = (
                        "\"The second number belongs to the night.\"\n\n"
                        "\"Look beyond the glass, the little lights in the sky\""
                    )
                    self.inventory_clues["Desk Note"] = body
                    self.score += 100
                    self.open_popup("THE DESK NOTE", body)
            else:
                self.open_popup("DESK", self.inventory_clues.get("Desk Note", "The drawer is empty now."))

        # SAFE
        elif name == "Safe":
            if self.box_open:
                self.open_popup("SAFE", "The safe is unlocked and empty. You already took the Brass Key.")
            elif len(self.inventory_clues) < 3:
                self.open_popup(
                    "LOCKED SAFE",
                    "A 3-digit combination lock guards this safe.\n\n"
                    "You should investigate all 3 clues around the room before guessing!"
                )
            else:
                self.code_input = ""
                self.state = "code"

        # EXIT DOOR
        elif name == "Exit Door":
            if self.has_key:
                self.score += self.remaining() * 10
                self.victory_time = self.remaining()
                self.state = "win"
            else:
                self.open_popup(
                    "LOCKED DOOR",
                    "The exit door is bolted shut.\n\n"
                    "A brass key is needed to open it."
                )

    def submit_code(self):
        if self.code_input == self.code:
            self.box_open = True
            self.has_key = True
            self.inventory_items.append("Brass Key")
            self.score += 300
            self.state = "playing"
            self.show_message("ACCESS GRANTED • BRASS KEY ADDED TO INVENTORY", 4)
        else:
            self.code_attempts -= 1
            self.code_input = ""
            if self.code_attempts <= 0:
                self.state = "gameover"
            else:
                self.show_message(f"ACCESS DENIED • {self.code_attempts} ATTEMPT(S) LEFT", 3)
                self.state = "playing"

    def update(self, dt):
        for p in particles:
            p.update()

        if self.state != "playing":
            return

        if self.remaining() <= 0:
            self.state = "gameover"
            return

        obstacles = [self.bookshelf.rect, self.desk.rect, self.box.rect, self.door.rect]
        self.player.move(dt, obstacles)

        self.nearby = None
        for obj in self.objects:
            if obj.nearby(self.player.rect):
                self.nearby = obj
                break

        if self.remaining() <= 20:
            self.flash += dt

    # ========================================================
    # DRAWING
    # ========================================================

    def draw_room(self):
        screen.fill(BG)

        # Walls & Floor
        pygame.draw.rect(screen, WALL, (0, 0, WIDTH, 380))
        pygame.draw.rect(screen, WALL_DARK, (0, 0, WIDTH, 78))

        for x in range(0, WIDTH, 100):
            pygame.draw.line(screen, WALL_LIGHT, (x, 80), (x, 380), 1)

        pygame.draw.rect(screen, FLOOR, (0, 380, WIDTH, HEIGHT - 380))
        for y in range(410, HEIGHT, 45):
            pygame.draw.line(screen, FLOOR_LINE, (0, y), (WIDTH, y), 2)
        for x in range(-500, WIDTH + 500, 100):
            pygame.draw.line(screen, (83, 61, 46), (WIDTH // 2, 380), (x, HEIGHT), 1)

        # 1. WINDOW (4 Stars)
        win_x, win_y, win_w, win_h = 95, 110, 160, 210
        pygame.draw.rect(screen, (20, 25, 38), (win_x - 6, win_y - 6, win_w + 12, win_h + 12), border_radius=10)
        pygame.draw.rect(screen, (10, 16, 28), (win_x, win_y, win_w, win_h), border_radius=8)

        pygame.draw.circle(screen, (240, 240, 210), (win_x + 40, win_y + 55), 26)
        pygame.draw.circle(screen, (10, 16, 28), (win_x + 50, win_y + 52), 22)

        stars = [
            (win_x + 115, win_y + 45),
            (win_x + 130, win_y + 110),
            (win_x + 45, win_y + 145),
            (win_x + 105, win_y + 165)
        ]
        for sx, sy in stars:
            pygame.draw.circle(screen, (255, 255, 255), (sx, sy), 4)
            pygame.draw.line(screen, GOLD_BRIGHT, (sx - 7, sy), (sx + 7, sy), 1)
            pygame.draw.line(screen, GOLD_BRIGHT, (sx, sy - 7), (sx, sy + 7), 1)

        pygame.draw.line(screen, WOOD, (win_x + win_w // 2, win_y), (win_x + win_w // 2, win_y + win_h), 4)
        pygame.draw.line(screen, WOOD, (win_x, win_y + win_h // 2), (win_x + win_w, win_y + win_h // 2), 4)
        pygame.draw.rect(screen, WOOD_LIGHT, (win_x, win_y, win_w, win_h), 4, border_radius=8)
        text(screen, "NIGHT SKY", (win_x + 35, win_y + win_h + 8), MUTED, F_SMALL)

        # 2. PAINTING
        pygame.draw.rect(screen, BLACK, self.painting.rect.inflate(8, 8), border_radius=6)
        pygame.draw.rect(screen, GOLD, self.painting.rect, border_radius=5)
        inner = self.painting.rect.inflate(-16, -16)
        pygame.draw.rect(screen, (25, 30, 40), inner, border_radius=3)
        pygame.draw.circle(screen, GOLD_BRIGHT, (inner.centerx, inner.centery - 10), 24)
        pygame.draw.polygon(
            screen, BLUE,
            [(inner.left + 10, inner.bottom - 5),
             (inner.left + 60, inner.top + 30),
             (inner.left + 110, inner.bottom - 20),
             (inner.right - 20, inner.top + 15),
             (inner.right - 5, inner.bottom - 5)]
        )
        text(screen, "PAINTING", (self.painting.rect.centerx - 35, self.painting.rect.bottom + 8), MUTED, F_SMALL)

        # 3. BOOKSHELF (5 Books in 1st Column)
        pygame.draw.rect(screen, BLACK, self.bookshelf.rect.inflate(8, 8), border_radius=8)
        pygame.draw.rect(screen, WOOD, self.bookshelf.rect, border_radius=6)

        for y in [435, 480, 525, 570]:
            pygame.draw.rect(screen, WOOD_LIGHT, (self.bookshelf.rect.left + 10, y, self.bookshelf.rect.width - 20, 6))

        book_colors = [(180, 60, 60), (60, 110, 180), (200, 150, 50), (60, 160, 90), (140, 80, 160)]
        first_col_rects = [
            (self.bookshelf.rect.left + 20, 395, 20, 38),
            (self.bookshelf.rect.left + 20, 442, 20, 36),
            (self.bookshelf.rect.left + 20, 487, 20, 36),
            (self.bookshelf.rect.left + 20, 532, 20, 36),
            (self.bookshelf.rect.left + 20, 577, 20, 31),
        ]
        for i, r in enumerate(first_col_rects):
            pygame.draw.rect(screen, book_colors[i], r, border_radius=2)

        other_books = [
            (self.bookshelf.rect.left + 50, 400, 16, 33), (self.bookshelf.rect.left + 72, 395, 18, 38),
            (self.bookshelf.rect.left + 50, 445, 18, 33), (self.bookshelf.rect.left + 74, 443, 16, 35),
            (self.bookshelf.rect.left + 50, 490, 17, 33), (self.bookshelf.rect.left + 73, 489, 19, 34),
            (self.bookshelf.rect.left + 50, 535, 16, 33), (self.bookshelf.rect.left + 72, 534, 18, 34),
        ]
        for i, r in enumerate(other_books):
            pygame.draw.rect(screen, book_colors[(i + 1) % len(book_colors)], r, border_radius=2)

        text(screen, "BOOKSHELF", (self.bookshelf.rect.centerx - 45, self.bookshelf.rect.bottom + 8), MUTED, F_SMALL)

        # 4. DESK (Clean 3 Drawers)
        pygame.draw.rect(screen, BLACK, self.desk.rect.inflate(8, 8), border_radius=8)
        pygame.draw.rect(screen, WOOD, self.desk.rect, border_radius=7)

        for i in range(3):
            drawer_rect = pygame.Rect(self.desk.rect.left + 16, self.desk.rect.top + 14 + i * 26, self.desk.rect.width - 32, 20)
            pygame.draw.rect(screen, WOOD_LIGHT, drawer_rect, border_radius=3)
            pygame.draw.circle(screen, GOLD_BRIGHT, (drawer_rect.centerx, drawer_rect.centery), 3)

        pygame.draw.rect(screen, WOOD, (self.desk.rect.left + 14, self.desk.rect.bottom, 14, 30))
        pygame.draw.rect(screen, WOOD, (self.desk.rect.right - 28, self.desk.rect.bottom, 14, 30))
        text(screen, "DESK", (self.desk.rect.centerx - 20, self.desk.rect.bottom + 34), MUTED, F_SMALL)

        # 5. SAFE
        stand_rect = pygame.Rect(self.box.rect.left - 8, self.box.rect.top - 8, self.box.rect.width + 16, self.box.rect.height + 16)
        pygame.draw.rect(screen, BLACK, stand_rect.inflate(6, 6), border_radius=8)
        pygame.draw.rect(screen, WOOD, stand_rect, border_radius=8)
        pygame.draw.rect(screen, WOOD_LIGHT, (stand_rect.left + 4, stand_rect.top + 4, stand_rect.width - 8, 6))
        pygame.draw.rect(screen, WOOD, (stand_rect.centerx - 12, stand_rect.bottom, 24, 35))

        box_color = GREEN if self.box_open else (52, 58, 69)
        pygame.draw.rect(screen, box_color, self.box.rect, border_radius=6)
        pygame.draw.rect(screen, (75, 84, 98), self.box.rect.inflate(-8, -8), border_radius=4)
        
        if not self.box_open:
            pygame.draw.rect(screen, GOLD, (self.box.rect.centerx - 12, self.box.rect.centery - 10, 24, 20), border_radius=3)
            pygame.draw.circle(screen, BLACK, (self.box.rect.centerx, self.box.rect.centery), 4)
        else:
            pygame.draw.circle(screen, WHITE, (self.box.rect.centerx, self.box.rect.centery), 6)

        text(screen, "SAFE", (self.box.rect.centerx - 18, stand_rect.bottom + 38), MUTED, F_SMALL)

        # 6. EXIT DOOR
        pygame.draw.rect(screen, BLACK, self.door.rect.inflate(8, 8), border_radius=8)
        pygame.draw.rect(screen, WOOD, self.door.rect, border_radius=7)
        pygame.draw.rect(screen, WOOD_LIGHT, (self.door.rect.left + 18, self.door.rect.top + 20, 64, 80), 3)
        pygame.draw.rect(screen, WOOD_LIGHT, (self.door.rect.left + 18, self.door.rect.top + 120, 64, 80), 3)
        pygame.draw.circle(screen, GOLD, (self.door.rect.right - 20, self.door.rect.centery), 6)
        text(screen, "EXIT", (self.door.rect.centerx - 16, self.door.rect.bottom + 8), GOLD_BRIGHT, F_SMALL)

        # 7. LAMP
        lamp_x = 940
        pygame.draw.rect(screen, WOOD, (lamp_x, 390, 8, 80))
        pygame.draw.circle(screen, GOLD_BRIGHT, (lamp_x + 4, 380), 22)
        pygame.draw.polygon(screen, GOLD, [(lamp_x - 24, 390), (lamp_x + 32, 390), (lamp_x + 20, 360), (lamp_x - 12, 360)])
        glow = pygame.Surface((180, 180), pygame.SRCALPHA)
        for r in range(80, 5, -8):
            alpha = max(0, 2 * (80 - r))
            pygame.draw.circle(glow, (250, 205, 90, alpha), (90, 90), r)
        screen.blit(glow, (lamp_x - 86, 290))

        # Player & Particles
        self.player.draw(screen)

        for p in particles:
            p.draw(screen)

        self.draw_hud()
        self.draw_interaction()
        self.draw_message()

        if self.remaining() <= 20:
            alpha = int(35 + 25 * (0.5 + 0.5 * math.sin(self.flash * 6)))
            overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
            pygame.draw.rect(overlay, (180, 20, 25, alpha), (0, 0, WIDTH, HEIGHT), width=8)
            screen.blit(overlay, (0, 0))

    def draw_hud(self):
        pygame.draw.rect(screen, (17, 19, 26), (0, 0, WIDTH, 78))
        pygame.draw.line(screen, GOLD, (0, 77), (WIDTH, 77), 1)

        text(screen, "ESCAPE", (28, 19), GOLD_BRIGHT, F_H2)
        text(screen, "THE LOCKED ROOM", (137, 24), MUTED, F_SMALL)

        remaining = self.remaining()
        mins = remaining // 60
        secs = remaining % 60
        timer_color = RED if remaining <= 20 else WHITE
        text(screen, f"TIME: {mins:02d}:{secs:02d}", (460, 25), timer_color, F_H2)
        text(screen, f"SCORE  {self.score}", (660, 28), GOLD_BRIGHT, F_SMALL)

        # INVENTORY BUTTON AT TOP RIGHT
        panel = pygame.Rect(WIDTH - 330, 10, 310, 58)
        rounded(screen, panel, PANEL, 8, GOLD if self.inventory_clues else PANEL_2)
        text(screen, "INVENTORY [Press I to open]", (WIDTH - 315, 14), GOLD_BRIGHT, F_TINY)

        total_items = len(self.inventory_clues) + len(self.inventory_items)
        if total_items == 0:
            text(screen, "No clues or items found yet", (WIDTH - 315, 34), MUTED, F_TINY)
        else:
            summary = f"{len(self.inventory_clues)} Clue(s) Found"
            if self.has_key:
                summary += " • Brass Key"
            text(screen, summary, (WIDTH - 315, 34), WHITE, F_TINY)

    def draw_interaction(self):
        if not self.nearby:
            return

        label = f"[ E ]  INVESTIGATE  •  {self.nearby.name.upper()}"
        img = F_SMALL.render(label, True, WHITE)
        rect = img.get_rect(center=(WIDTH // 2, 660))
        outer = rect.inflate(32, 20)
        rounded(screen, outer, PANEL, 10, GOLD)
        screen.blit(img, rect)

    def draw_message(self):
        if self.message_until > pygame.time.get_ticks():
            r = pygame.Rect(310, 585, 580, 48)
            rounded(screen, r, PANEL, 10, GOLD)
            text(screen, self.message, r.center, WHITE, F_SMALL, center=True)

    def draw_menu(self):
        screen.fill((9, 11, 17))
        for p in particles:
            p.draw(screen)

        pygame.draw.line(screen, GOLD, (170, 150), (1030, 150), 1)
        pygame.draw.line(screen, GOLD, (170, 590), (1030, 590), 1)

        text(screen, "ESCAPE", (WIDTH // 2, 235), GOLD_BRIGHT, F_TITLE, center=True)
        text(screen, "THE LOCKED ROOM", (WIDTH // 2, 300), WHITE, F_H2, center=True)
        text(screen, "A short mystery. Three clues. One way out.", (WIDTH // 2, 355), MUTED, F_BODY, center=True)

        button = pygame.Rect(410, 410, 380, 68)
        rounded(screen, button, GOLD, 14)
        text(screen, "PRESS ENTER TO BEGIN", button.center, BLACK, F_H2, center=True)

        text(screen, "WASD / ARROW KEYS   •   E TO INVESTIGATE   •   I FOR INVENTORY",
             (WIDTH // 2, 530), MUTED, F_SMALL, center=True)

    def draw_inventory(self):
        self.draw_room()
        overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 175))
        screen.blit(overlay, (0, 0))

        modal = pygame.Rect(260, 110, 680, 500)
        rounded(screen, modal, PANEL, 16, GOLD, 2)

        text(screen, "INVENTORY & CLUES", (WIDTH // 2, 155), GOLD_BRIGHT, F_H1, center=True)

        y = 210
        if self.inventory_items:
            text(screen, "ITEMS:", (300, y), GOLD, F_SMALL)
            y += 26
            for itm in self.inventory_items:
                r = pygame.Rect(300, y, 160, 30)
                rounded(screen, r, PANEL_2, 6, GREEN)
                text(screen, f"• {itm}", (315, y + 6), WHITE, F_SMALL)
            y += 45

        text(screen, "DISCOVERED CLUES:", (300, y), GOLD, F_SMALL)
        y += 30

        if not self.inventory_clues:
            text(screen, "No clues found yet. Investigate the room!", (300, y), MUTED, F_BODY)
        else:
            for title, clue_text in self.inventory_clues.items():
                card = pygame.Rect(300, y, 600, 70)
                rounded(screen, card, PANEL_2, 8)
                text(screen, f"[{title}]", (315, y + 8), GOLD_BRIGHT, F_SMALL)
                first_line = clue_text.replace("\n\n", " ").replace("\n", " ")
                if len(first_line) > 75:
                    first_line = first_line[:75] + "..."
                text(screen, first_line, (315, y + 36), WHITE, F_TINY)
                y += 82

        text(screen, "[ I / ESC / ENTER ]  Close Inventory", (WIDTH // 2, 575), MUTED, F_SMALL, center=True)

    def draw_code(self):
        self.draw_room()
        overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))
        screen.blit(overlay, (0, 0))

        modal = pygame.Rect(330, 135, 540, 440)
        rounded(screen, modal, PANEL, 18, GOLD, 2)

        text(screen, "COMBINATION SAFE", (WIDTH // 2, 185), GOLD_BRIGHT, F_H1, center=True)
        text(screen, "Enter the three numbers discovered in the room.",
             (WIDTH // 2, 235), MUTED, F_SMALL, center=True)

        display = pygame.Rect(425, 285, 350, 82)
        rounded(screen, display, BLACK, 12)
        shown = self.code_input if self.code_input else "_ _ _"
        text(screen, shown, display.center, WHITE, F_TITLE, center=True)

        color = RED if self.code_attempts == 1 else MUTED
        text(screen, f"ATTEMPTS REMAINING: {self.code_attempts}",
             (WIDTH // 2, 410), color, F_SMALL, center=True)

        text(screen, "ENTER  Submit     •     BACKSPACE  Delete     •     ESC  Cancel",
             (WIDTH // 2, 490), MUTED, F_TINY, center=True)

    def draw_popup(self):
        self.draw_room()
        overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 165))
        screen.blit(overlay, (0, 0))

        modal = pygame.Rect(300, 160, 600, 390)
        rounded(screen, modal, PANEL, 18, GOLD, 2)

        text(screen, self.popup_title, (WIDTH // 2, 215), GOLD_BRIGHT, F_H1, center=True)

        y = 275
        for line in self.popup_text.split("\n"):
            text(screen, line, (WIDTH // 2, y), WHITE if line.strip() else MUTED, F_BODY, center=True)
            y += 32

        text(screen, "[ E / ENTER / ESC ]  Close & Save to Inventory", (WIDTH // 2, 505), MUTED, F_SMALL, center=True)

    def draw_win(self):
        screen.fill((8, 27, 19))
        for p in particles:
            p.draw(screen)

        text(screen, "ESCAPED", (WIDTH // 2, 165), GREEN, F_TITLE, center=True)
        text(screen, "THE DOOR IS OPEN", (WIDTH // 2, 230), WHITE, F_H2, center=True)
        text(screen, "You solved the room and found your way out.", (WIDTH // 2, 280), MUTED, F_BODY, center=True)

        card = pygame.Rect(355, 340, 490, 160)
        rounded(screen, card, PANEL, 16, GREEN, 2)

        text(screen, f"SCORE     {self.score}", (WIDTH // 2, 380), GOLD_BRIGHT, F_H2, center=True)
        text(screen, f"TIME LEFT     {self.victory_time:02d}s", (WIDTH // 2, 425), WHITE, F_BODY, center=True)
        text(screen, f"CLUES FOUND     {len(self.inventory_clues)} / 3", (WIDTH // 2, 465), MUTED, F_SMALL, center=True)

        text(screen, "[ R ]  PLAY AGAIN        [ ESC ]  EXIT",
             (WIDTH // 2, 570), WHITE, F_SMALL, center=True)

    def draw_gameover(self):
        screen.fill((30, 10, 14))
        for p in particles:
            p.draw(screen)

        text(screen, "TIME RAN OUT", (WIDTH // 2, 175), RED, F_TITLE, center=True)
        text(screen, "The room remains locked.", (WIDTH // 2, 250), WHITE, F_H2, center=True)

        card = pygame.Rect(380, 325, 440, 135)
        rounded(screen, card, PANEL, 16, RED, 2)
        text(screen, f"FINAL SCORE     {self.score}", (WIDTH // 2, 365), GOLD_BRIGHT, F_H2, center=True)
        text(screen, f"CLUES FOUND     {len(self.inventory_clues)} / 3", (WIDTH // 2, 415), MUTED, F_SMALL, center=True)

        text(screen, "[ R ]  TRY AGAIN        [ ESC ]  EXIT",
             (WIDTH // 2, 540), WHITE, F_SMALL, center=True)

    def handle_event(self, event):
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if self.state == "menu":
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    self.start()
                elif event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()

        elif self.state == "playing":
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_e:
                    self.interact()
                elif event.key == pygame.K_i:
                    self.state = "inventory"
                elif event.key == pygame.K_ESCAPE:
                    self.state = "menu"

        elif self.state == "popup":
            if event.type == pygame.KEYDOWN and event.key in (pygame.K_e, pygame.K_RETURN, pygame.K_ESCAPE, pygame.K_SPACE):
                self.state = "playing"

        elif self.state == "inventory":
            if event.type == pygame.KEYDOWN and event.key in (pygame.K_i, pygame.K_ESCAPE, pygame.K_RETURN):
                self.state = "playing"

        elif self.state == "code":
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.code_input = ""
                    self.state = "playing"
                elif event.key == pygame.K_BACKSPACE:
                    self.code_input = self.code_input[:-1]
                elif event.key == pygame.K_RETURN:
                    self.submit_code()
                elif event.unicode.isdigit() and len(self.code_input) < 3:
                    self.code_input += event.unicode

        elif self.state in ("win", "gameover"):
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    self.start()
                elif event.key == pygame.K_ESCAPE:
                    self.state = "menu"

    def draw(self):
        if self.state == "menu":
            self.draw_menu()
        elif self.state == "playing":
            self.draw_room()
        elif self.state == "popup":
            self.draw_popup()
        elif self.state == "inventory":
            self.draw_inventory()
        elif self.state == "code":
            self.draw_code()
        elif self.state == "win":
            self.draw_win()
        elif self.state == "gameover":
            self.draw_gameover()

# ============================================================
# MAIN LOOP
# ============================================================

game = Game()

while True:
    dt = clock.tick(FPS) / 1000.0

    for event in pygame.event.get():
        game.handle_event(event)

    game.update(dt)
    game.draw()

    pygame.display.flip()
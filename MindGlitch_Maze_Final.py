import pygame
import sys
import random
import os
import sys
import os

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

# ------------------ SETUP ------------------
pygame.init()
WIDTH, HEIGHT = 900, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("MindGlitch")
clock = pygame.time.Clock()
FPS = 60

# ------------------ LOAD IMAGES ------------------
player_img = pygame.image.load(resource_path("assets/alien.png")).convert_alpha()
planet_img = pygame.image.load(resource_path("assets/planet.png")).convert_alpha()
earth_img = pygame.image.load(resource_path("assets/earth.png")).convert_alpha()
bg_img = pygame.image.load(resource_path("assets/space_bg.png")).convert()
bg_img = pygame.transform.scale(bg_img, (WIDTH, HEIGHT))

player_img = pygame.transform.scale(player_img, (82, 72))
planet_img = pygame.transform.scale(planet_img, (37, 37))
earth_img = pygame.transform.scale(earth_img, (40, 40))

# ------------------ COLORS ------------------
wall_color = (255, 60, 180)

# ------------------ FONTS ------------------
font_big = pygame.font.SysFont("Verdana", 72, bold=True)
font_medium = pygame.font.SysFont("Verdana", 40, bold=True)
font_small = pygame.font.SysFont("Verdana", 28, bold=True)

# ------------------ BACKGROUND ------------------
stars = [[random.randint(0,WIDTH), random.randint(0,HEIGHT), random.randint(1,3)] for _ in range(120)]

def draw_background():
    screen.blit(bg_img, (0, 0))
    for s in stars:
        pygame.draw.circle(screen, (100,100,255), (s[0],s[1]), s[2])
        s[1]+=s[2]*0.5
        if s[1]>HEIGHT:
            s[1]=0
            s[0]=random.randint(0,WIDTH)

# ------------------ UI ------------------
def draw_ui_frame():
    pygame.draw.line(screen, (255, 60, 180), (80, 120), (WIDTH-80, 120), 2)
    pygame.draw.line(screen, (0, 220, 255), (80, HEIGHT-120), (WIDTH-80, HEIGHT-120), 2)

def draw_title(text, y):
    t = font_big.render(text, True, (255, 60, 180))
    screen.blit(t, (WIDTH//2 - t.get_width()//2, y))

def draw_subtitle(text, y):
    t = font_medium.render(text, True, (0, 220, 255))
    screen.blit(t, (WIDTH//2 - t.get_width()//2, y))

def draw_hint(text, y):
    t = font_small.render(text, True, (180, 80, 255))
    screen.blit(t, (WIDTH//2 - t.get_width()//2, y))

# ✅ ADDITION (TOP INFO)
def draw_top_info(level, score):
    t = font_small.render(f"LEVEL: {level+1}   SCORE: {score}", True, (0,220,255))
    screen.blit(t, (WIDTH//2 - t.get_width()//2, 20))

# ------------------ SCREENS ------------------
def start_screen():
    while True:
        clock.tick(FPS)
        draw_background()
        draw_ui_frame()
        draw_title("MINDGLITCH", 180)
        draw_subtitle("NEON MAZE", 260)
        draw_hint("Press SPACE to start", 360)
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()

        if pygame.key.get_pressed()[pygame.K_SPACE]:
            return

def game_over_screen(score, high_score):
    while True:
        clock.tick(FPS)
        draw_background()
        draw_ui_frame()
        draw_title("GAME OVER", 180)
        draw_subtitle(f"Score: {score}", 260)
        draw_subtitle(f"Highest Score: {high_score}", 310)
        draw_hint("SPACE = Restart   ESC = Quit", 400)
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()

        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            return
        if keys[pygame.K_ESCAPE]:
            pygame.quit(); sys.exit()

def level_screen(level_num):
    while True:
        clock.tick(FPS)
        draw_background()
        draw_ui_frame()
        draw_title(f"LEVEL {level_num+1}", 220)
        draw_hint("Press SPACE to start", 340)
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()

        if pygame.key.get_pressed()[pygame.K_SPACE]:
            return

# ------------------ DRAW FUNCTIONS ------------------
def draw_player(x, y):
    screen.blit(player_img, (
        x - player_img.get_width()//2,
        y - player_img.get_height()//2
    ))

def draw_obstacle(obs):
    rect = obs["rect"]
    screen.blit(planet_img, (
        rect.x + rect.width//2 - planet_img.get_width()//2,
        rect.y + rect.height//2 - planet_img.get_height()//2
    ))

# ------------------ LEVELS ------------------
levels = [
[
"WWWWWWWWWWWWWWWWWWWW",
"W   W       W      W",
"W W W WWWWW W WWWW W",
"W W W     W W W    W",
"W WWW WWW W W W WW W",
"W     W   W   W W  W",
"WWW W WWWWW WWW W WW",
"W   W     W     W  W",
"W WWWWW WWW WWWWW WW",
"W       W         GW",
"WWWWWWWWWWWWWWWWWWWW"
],
[
"WWWWWWWWWWWWWWWWWWWW",
"W   W W         W  W",
"W W W W WWWWW W W WW",
"W W   W W   W W W  W",
"W WWWWW W W W W WW W",
"W       W W   W W  W",
"W WWWWWWW WWWWW W WW",
"W       W         W ",
"W WWWWW WWWWWWWWW WW",
"W     W       W   GW",
"WWWWWWWWWWWWWWWWWWWW"
],
[
"WWWWWWWWWWWWWWWWWWWW",
"W       W       W  W",
"W WWWWW W WWWWW W  W",
"W W   W W W   W W  W",
"W W W W   W W W W WW",
"W   W   W   W   W  W",
"WWW WWWWW WWWWWWW WW",
"W       W           W",
"W WWWWW WWWWWWWWW WW",
"W   W       W     GW",
"WWWWWWWWWWWWWWWWWWWW"
]
]

# ------------------ MAIN ------------------
player_size = 20
player_start_x, player_start_y = 50,50
player_speed = 4
high_score = 0

while True:
    start_screen()
    player_alive = True

    for level_index, layout in enumerate(levels):
        if not player_alive:
            break

        level_screen(level_index)

        tile_size = 40
        maze_width = len(layout[0]) * tile_size
        maze_height = len(layout) * tile_size
        offset_x = (WIDTH - maze_width) // 2
        offset_y = (HEIGHT - maze_height) // 2

        walls = []
        goal_rect = None

        for row_index, row in enumerate(layout):
            for col_index, cell in enumerate(row):
                x = col_index * 40 + offset_x
                y = row_index * 40 + offset_y
                if cell == "W":
                    walls.append(pygame.Rect(x,y,40,40))
                elif cell == "G":
                    goal_rect = pygame.Rect(x+5,y+5,30,30)

        player_x = player_start_x + offset_x
        player_y = player_start_y + offset_y

        obstacles = []
        for _ in range(level_index+2):
            obs_x = offset_x + random.randint(1, len(layout[0])-2)*40
            obs_y = offset_y + random.randint(1, len(layout)-2)*40
            obstacles.append({
                "rect": pygame.Rect(obs_x, obs_y, 30,30),
                "dir": random.choice([-1,1]),
                "speed": 2+level_index
            })

        running = True
        score = 0
        earth_angle = 0

        while running:
            clock.tick(FPS)
            draw_background()

            # ✅ SHOW LEVEL + SCORE
            draw_top_info(level_index, score)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit(); sys.exit()

            keys = pygame.key.get_pressed()
            dx = dy = 0
            if keys[pygame.K_LEFT]: dx = -player_speed
            if keys[pygame.K_RIGHT]: dx = player_speed
            if keys[pygame.K_UP]: dy = -player_speed
            if keys[pygame.K_DOWN]: dy = player_speed

            new_rect = pygame.Rect(player_x+dx, player_y+dy, player_size, player_size)

            if not any(new_rect.colliderect(w) for w in walls):
                player_x += dx
                player_y += dy

            player_rect = pygame.Rect(player_x, player_y, player_size, player_size)

            for wall in walls:
                glow = pygame.Surface((40,40), pygame.SRCALPHA)
                pygame.draw.rect(glow, (*wall_color,150), glow.get_rect())
                screen.blit(glow, (wall.x, wall.y))
                pygame.draw.rect(screen, wall_color, wall, 2)

            for obs in obstacles:
                obs["rect"].x += obs["dir"] * obs["speed"]

                if obs["rect"].x < offset_x + 40 or obs["rect"].x > offset_x + maze_width - 80:
                    obs["dir"] *= -1

                draw_obstacle(obs)

                if player_rect.colliderect(obs["rect"]):
                    player_alive = False
                    running = False
                    break

            earth_angle += 1
            rotated_earth = pygame.transform.rotate(earth_img, earth_angle)

            rect = rotated_earth.get_rect(center=(
                goal_rect.x + goal_rect.width//2,
                goal_rect.y + goal_rect.height//2
            ))

            glow = pygame.Surface((60,60), pygame.SRCALPHA)
            pygame.draw.circle(glow, (0,200,255,80), (30,30), 25)
            screen.blit(glow, (rect.x - 10, rect.y - 10))

            screen.blit(rotated_earth, rect)

            draw_player(player_x + player_size//2, player_y + player_size//2)

            score += 1

            if player_rect.colliderect(goal_rect):
                high_score = max(high_score, score)
                running = False

            pygame.display.flip()

        if not player_alive:
            game_over_screen(score, high_score)
            break

    # ✅ FINAL CONGRATS SCREEN
    if player_alive:
        while True:
            clock.tick(FPS)
            draw_background()
            draw_ui_frame()
            draw_title("CONGRATS", 180)
            draw_subtitle(f"Highest Score: {high_score}", 280)
            draw_hint("SPACE = Restart   ESC = Quit", 380)
            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit(); sys.exit()

            keys = pygame.key.get_pressed()
            if keys[pygame.K_SPACE]:
                break
            if keys[pygame.K_ESCAPE]:
                pygame.quit(); sys.exit()
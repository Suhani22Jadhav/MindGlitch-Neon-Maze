import pygame
import sys
import random

# ------------------ SETUP ------------------
pygame.init()
WIDTH, HEIGHT = 900, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("MindGlitch")
clock = pygame.time.Clock()
FPS = 60

# ------------------ COLORS ------------------
bg_color = (10, 10, 30)
player_color = (0, 220, 255)
wall_color = (255, 60, 180)
goal_color = (255, 255, 102)
obstacle_color = (180, 80, 255)

# ------------------ FONTS ------------------
font_big = pygame.font.SysFont("Verdana", 72, bold=True)
font_medium = pygame.font.SysFont("Verdana", 40, bold=True)
font_small = pygame.font.SysFont("Verdana", 28, bold=True)

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

# ------------------ PARTICLES ------------------
particles = []
def create_particles(x, y, color, count=20):
    for _ in range(count):
        particles.append({
            "x": x,
            "y": y,
            "vx": random.uniform(-3,3),
            "vy": random.uniform(-3,3),
            "size": random.randint(4,8),
            "color": color,
            "life": random.randint(20,35)
        })

def draw_particles():
    for p in particles[:]:
        pygame.draw.circle(screen, p["color"], (int(p["x"]), int(p["y"])), p["size"])
        p["x"] += p["vx"]
        p["y"] += p["vy"]
        p["life"] -= 1
        if p["life"] <= 0:
            particles.remove(p)

# ------------------ TRAIL ------------------
trail = []
def draw_trail():
    for i, pos in enumerate(trail):
        alpha = max(0, 150 - i*7)
        glow = pygame.Surface((50,50), pygame.SRCALPHA)
        pygame.draw.circle(glow, (*player_color, alpha), (25,25), 25 - i//2)
        screen.blit(glow, (pos[0]-25, pos[1]-25))

# ------------------ BACKGROUND ------------------
stars = [[random.randint(0,WIDTH), random.randint(0,HEIGHT)] for _ in range(50)]
def draw_background():
    screen.fill(bg_color)
    for s in stars:
        pygame.draw.circle(screen, (100,100,255), (s[0],s[1]),2)
        s[1]+=0.5
        if s[1]>HEIGHT:
            s[1]=0
            s[0]=random.randint(0,WIDTH)

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

# ------------------ SCREENS ------------------
def start_screen():
    waiting = True
    while waiting:
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
            waiting = False

def game_over_screen(score, high_score):
    waiting = True
    while waiting:
        clock.tick(FPS)
        draw_background()
        draw_ui_frame()

        draw_title("GAME OVER", 180)
        draw_subtitle(f"Score: {score}", 260)
        draw_subtitle(f"High Score: {high_score}", 310)
        draw_hint("SPACE = Restart   ESC = Quit", 400)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()

        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            waiting = False
        if keys[pygame.K_ESCAPE]:
            pygame.quit(); sys.exit()

def level_screen(level_num):
    waiting = True
    while waiting:
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
            waiting = False

# ------------------ PLAYER & OBSTACLE ------------------
def draw_player(x, y):
    for i in range(5,0,-1):
        glow = pygame.Surface((50,50), pygame.SRCALPHA)
        pygame.draw.circle(glow, (0,220,255,i*40), (25,25), 10+i*5)
        screen.blit(glow, (x-25, y-25))
    pygame.draw.circle(screen, player_color, (x,y), 10)

def draw_obstacle(obs):
    rect = obs["rect"]
    glow = pygame.Surface((rect.width, rect.height), pygame.SRCALPHA)
    pygame.draw.rect(glow, (*obstacle_color,120), glow.get_rect(), border_radius=5)
    screen.blit(glow, (rect.x, rect.y))
    pygame.draw.rect(screen, obstacle_color, rect, 2, border_radius=5)

# ------------------ MAIN GAME LOOP ------------------
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

        walls = []
        goal_rect = None
        for row_index, row in enumerate(layout):
            for col_index, cell in enumerate(row):
                x = col_index * 40
                y = row_index * 40
                if cell=="W": walls.append(pygame.Rect(x,y,40,40))
                elif cell=="G": goal_rect = pygame.Rect(x+5,y+5,30,30)

        player_x, player_y = player_start_x, player_start_y
        trail.clear()
        particles.clear()

        obstacles = []
        for _ in range(level_index+2):
            obs_x = random.randint(1,18)*40
            obs_y = random.randint(1,9)*40
            obs_dir = random.choice([-1,1])
            obstacles.append({"rect":pygame.Rect(obs_x, obs_y, 30,30),"dir":obs_dir,"speed":2+level_index})

        score = 0
        running=True

        while running:
            clock.tick(FPS)
            draw_background()
            draw_particles()

            for event in pygame.event.get():
                if event.type==pygame.QUIT:
                    pygame.quit(); sys.exit()

            keys=pygame.key.get_pressed()
            dx=dy=0
            if keys[pygame.K_LEFT]: dx=-player_speed
            if keys[pygame.K_RIGHT]: dx=player_speed
            if keys[pygame.K_UP]: dy=-player_speed
            if keys[pygame.K_DOWN]: dy=player_speed

            new_rect = pygame.Rect(player_x+dx,player_y+dy,player_size,player_size)
            if not any(new_rect.colliderect(w) for w in walls):
                player_x+=dx
                player_y+=dy

            player_rect = pygame.Rect(player_x,player_y,player_size,player_size)

            for wall in walls:
                glow = pygame.Surface((40,40), pygame.SRCALPHA)
                pygame.draw.rect(glow, (*wall_color,150), glow.get_rect())
                screen.blit(glow, (wall.x, wall.y))
                pygame.draw.rect(screen, wall_color, wall, 2)

            for obs in obstacles:
                obs["rect"].x += obs["dir"]*obs["speed"]
                if obs["rect"].x<40 or obs["rect"].x>WIDTH-80: obs["dir"]*=-1
                draw_obstacle(obs)
                if player_rect.colliderect(obs["rect"]):
                    player_alive = False
                    running = False
                    break

            pygame.draw.rect(screen, goal_color, goal_rect)

            trail.append((player_x+player_size//2, player_y+player_size//2))
            if len(trail)>20: trail.pop(0)
            draw_trail()

            draw_player(player_x+player_size//2, player_y+player_size//2)

            score+=1

            if player_rect.colliderect(goal_rect):
                create_particles(player_x+player_size//2, player_y+player_size//2, goal_color,50)
                score += 100
                high_score = max(high_score, score)
                break

            pygame.display.flip()

        if player_alive and player_rect.colliderect(goal_rect):
            for _ in range(80):
                clock.tick(FPS)
                draw_background()
                draw_ui_frame()
                draw_title(f"LEVEL {level_index+1} COMPLETE", 250)
                pygame.display.flip()

        elif not player_alive:
            game_over_screen(score, high_score)
            break

    if player_alive:
        waiting=True
        while waiting:
            clock.tick(FPS)
            draw_background()
            draw_ui_frame()

            draw_title("CONGRATS", 180)
            draw_subtitle(f"High Score: {high_score}", 280)
            draw_hint("SPACE = Restart   ESC = Quit", 380)

            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit(); sys.exit()

            keys = pygame.key.get_pressed()
            if keys[pygame.K_SPACE]: waiting=False
            if keys[pygame.K_ESCAPE]: pygame.quit(); sys.exit()
import pygame

# Initialize Pygame
pygame.init()

# Screen dimensions
WIDTH = 800
HEIGHT = 600

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 70, 70)
GREEN = (0, 255, 120)
CYAN = (80, 220, 255)
YELLOW = (255, 230, 90)
BLUE = (80, 140, 255)

# Player settings
PLAYER_SIZE = 32
PLAYER_HEIGHT = 22
PLAYER_SPEED = 5
player_pos = [WIDTH // 2, HEIGHT - 2 * PLAYER_SIZE]

# Bullet settings
BULLET_SIZE = 6
BULLET_SPEED = 8
bullets = []

# Invader settings
INVADER_SIZE = 28
INVADER_X_GAP = 56
INVADER_Y_GAP = 34
INVADER_START_Y = 80
LEVEL_SPEED_STEP = 0.3
level = 1
invader_speed = 1.0


def create_invaders(current_level):
    rows = min(3 + (current_level - 1) // 2, 7)
    x_gap = max(38, INVADER_X_GAP - (current_level - 1))
    return [
        [x, y]
        for x in range(30, WIDTH - INVADER_SIZE, x_gap)
        for y in range(
            INVADER_START_Y, INVADER_START_Y + rows * INVADER_Y_GAP, INVADER_Y_GAP
        )
    ]


invaders = create_invaders(level)

# Score
score = 0
font = pygame.font.SysFont(None, 32)

# Set up the display
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space Invaders")

# Clock to control frame rate
clock = pygame.time.Clock()


def draw_player(pos):
    body = pygame.Rect(pos[0], pos[1] + 7, PLAYER_SIZE, PLAYER_HEIGHT - 7)
    cockpit = pygame.Rect(pos[0] + 11, pos[1], 10, 9)
    left_wing = [(pos[0], pos[1] + PLAYER_HEIGHT), (pos[0] + 8, pos[1] + 10), (pos[0] + 13, pos[1] + PLAYER_HEIGHT)]
    right_wing = [
        (pos[0] + PLAYER_SIZE, pos[1] + PLAYER_HEIGHT),
        (pos[0] + PLAYER_SIZE - 8, pos[1] + 10),
        (pos[0] + PLAYER_SIZE - 13, pos[1] + PLAYER_HEIGHT),
    ]
    pygame.draw.rect(screen, BLUE, body)
    pygame.draw.rect(screen, CYAN, cockpit)
    pygame.draw.polygon(screen, BLUE, left_wing)
    pygame.draw.polygon(screen, BLUE, right_wing)
    pygame.draw.rect(screen, YELLOW, (pos[0] + 14, pos[1] + PLAYER_HEIGHT, 4, 5))


def draw_bullets(items):
    for bullet in items:
        pygame.draw.rect(screen, YELLOW, (bullet[0], bullet[1], BULLET_SIZE, BULLET_SIZE))


def draw_invaders(items):
    for invader in items:
        x = invader[0]
        y = invader[1]
        hull = pygame.Rect(x + 2, y + 8, INVADER_SIZE - 4, INVADER_SIZE - 10)
        dome = pygame.Rect(x + 7, y + 2, INVADER_SIZE - 14, 10)
        pygame.draw.ellipse(screen, GREEN, hull)
        pygame.draw.ellipse(screen, CYAN, dome)
        pygame.draw.rect(screen, GREEN, (x + 6, y + INVADER_SIZE - 4, 4, 4))
        pygame.draw.rect(screen, GREEN, (x + INVADER_SIZE - 10, y + INVADER_SIZE - 4, 4, 4))


def draw_hud(current_score, current_level):
    text = font.render(f"Score: {current_score}   Level: {current_level}", True, WHITE)
    screen.blit(text, (10, 10))


def move_bullets(items):
    for bullet in items:
        bullet[1] -= BULLET_SPEED
    return [bullet for bullet in items if bullet[1] > -BULLET_SIZE]


def move_invaders(items, speed):
    for invader in items:
        invader[0] += speed

    hit_wall = any(
        invader[0] + INVADER_SIZE >= WIDTH or invader[0] <= 0 for invader in items
    )
    if hit_wall:
        speed *= -1
        for invader in items:
            invader[1] += INVADER_SIZE // 2

    return speed


def check_collision(current_bullets, current_invaders):
    gained = 0
    kept_bullets = []
    kept_invaders = current_invaders[:]

    for bullet in current_bullets:
        bullet_rect = pygame.Rect(bullet[0], bullet[1], BULLET_SIZE, BULLET_SIZE)
        hit_index = None

        for i, invader in enumerate(kept_invaders):
            invader_rect = pygame.Rect(
                invader[0], invader[1], INVADER_SIZE, INVADER_SIZE
            )
            if bullet_rect.colliderect(invader_rect):
                hit_index = i
                break

        if hit_index is None:
            kept_bullets.append(bullet)
        else:
            gained += 1
            kept_invaders.pop(hit_index)

    return kept_bullets, kept_invaders, gained


# Main game loop
running = True
while running:
    screen.fill(BLACK)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            bullets.append(
                [player_pos[0] + PLAYER_SIZE // 2 - BULLET_SIZE // 2, player_pos[1]]
            )

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and player_pos[0] > 0:
        player_pos[0] -= PLAYER_SPEED
    if keys[pygame.K_RIGHT] and player_pos[0] < WIDTH - PLAYER_SIZE:
        player_pos[0] += PLAYER_SPEED

    bullets = move_bullets(bullets)
    invader_speed = move_invaders(invaders, invader_speed)
    bullets, invaders, gained = check_collision(bullets, invaders)
    score += gained
    # Start a fresh wave when all invaders are gone or they move off-screen.
    if not invaders or min(inv[1] for inv in invaders) > HEIGHT:
        level += 1
        invaders = create_invaders(level)
        next_speed = 1.0 + (level - 1) * LEVEL_SPEED_STEP
        invader_speed = next_speed if invader_speed > 0 else -next_speed

    draw_player(player_pos)
    draw_bullets(bullets)
    draw_invaders(invaders)
    draw_hud(score, level)

    pygame.display.update()
    clock.tick(30)

pygame.quit()

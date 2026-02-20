import pygame
import random

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
ENEMY_BULLET_SIZE = 6
ENEMY_BULLET_SPEED = 5
enemy_bullets = []

# Invader settings
INVADER_SIZE = 28
INVADER_X_GAP = 56
INVADER_Y_GAP = 34
INVADER_START_Y = 80
INVADER_DROP = 10
LEVEL_SPEED_STEP = 0.18
MAX_INVADER_SPEED = 2.4
level = 1
invader_speed = 1.0
PLAYER_LIVES_START = 3
MAX_PLAYER_LIVES = 5
lives = PLAYER_LIVES_START
game_over = False
last_enemy_shot_at = 0


def create_invaders(current_level):
    rows = min(3 + (current_level - 1) // 3, 5)
    x_gap = max(44, INVADER_X_GAP - (current_level - 1) // 2)
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


def draw_enemy_bullets(items):
    for bullet in items:
        pygame.draw.rect(
            screen, RED, (bullet[0], bullet[1], ENEMY_BULLET_SIZE, ENEMY_BULLET_SIZE)
        )


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


def draw_hud(current_score, current_level, current_lives):
    text = font.render(
        f"Score: {current_score}   Level: {current_level}   Lives: {current_lives}",
        True,
        WHITE,
    )
    screen.blit(text, (10, 10))


def move_bullets(items):
    for bullet in items:
        bullet[1] -= BULLET_SPEED
    return [bullet for bullet in items if bullet[1] > -BULLET_SIZE]


def move_enemy_bullets(items):
    for bullet in items:
        bullet[1] += ENEMY_BULLET_SPEED
    return [bullet for bullet in items if bullet[1] < HEIGHT + ENEMY_BULLET_SIZE]


def move_invaders(items, speed):
    for invader in items:
        invader[0] += speed

    hit_wall = any(
        invader[0] + INVADER_SIZE >= WIDTH or invader[0] <= 0 for invader in items
    )
    if hit_wall:
        speed *= -1
        for invader in items:
            invader[1] += INVADER_DROP

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


def enemy_fire(current_invaders, current_level):
    if not current_invaders:
        return None

    # Let only front-line invaders shoot to keep patterns readable.
    front_by_column = {}
    for inv in current_invaders:
        column = inv[0]
        if column not in front_by_column or inv[1] > front_by_column[column][1]:
            front_by_column[column] = inv

    shooter = random.choice(list(front_by_column.values()))
    cooldown_ms = max(420, 950 - (current_level - 1) * 22)
    return shooter, cooldown_ms


def check_player_hit(current_enemy_bullets, pos):
    player_rect = pygame.Rect(pos[0], pos[1], PLAYER_SIZE, PLAYER_HEIGHT + 5)
    kept = []
    hit = False
    for bullet in current_enemy_bullets:
        rect = pygame.Rect(
            bullet[0], bullet[1], ENEMY_BULLET_SIZE, ENEMY_BULLET_SIZE
        )
        if rect.colliderect(player_rect):
            hit = True
        else:
            kept.append(bullet)
    return kept, hit


def check_invader_reach_player(current_invaders, pos):
    return any(inv[1] + INVADER_SIZE >= pos[1] for inv in current_invaders)


def draw_game_over():
    large = pygame.font.SysFont(None, 64)
    title = large.render("GAME OVER", True, RED)
    sub = font.render("Press R to restart", True, WHITE)
    screen.blit(title, (WIDTH // 2 - title.get_width() // 2, HEIGHT // 2 - 50))
    screen.blit(sub, (WIDTH // 2 - sub.get_width() // 2, HEIGHT // 2 + 10))


def reset_game():
    global player_pos, bullets, enemy_bullets, invaders, invader_speed
    global score, level, lives, game_over, last_enemy_shot_at
    player_pos = [WIDTH // 2, HEIGHT - 2 * PLAYER_SIZE]
    bullets = []
    enemy_bullets = []
    score = 0
    level = 1
    lives = PLAYER_LIVES_START
    invader_speed = 1.0
    invaders = create_invaders(level)
    game_over = False
    last_enemy_shot_at = pygame.time.get_ticks()


# Main game loop
running = True
last_enemy_shot_at = pygame.time.get_ticks()
while running:
    screen.fill(BLACK)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE and not game_over:
            bullets.append(
                [player_pos[0] + PLAYER_SIZE // 2 - BULLET_SIZE // 2, player_pos[1]]
            )
        if event.type == pygame.KEYDOWN and event.key == pygame.K_r and game_over:
            reset_game()

    keys = pygame.key.get_pressed()
    if not game_over:
        if keys[pygame.K_LEFT] and player_pos[0] > 0:
            player_pos[0] -= PLAYER_SPEED
        if keys[pygame.K_RIGHT] and player_pos[0] < WIDTH - PLAYER_SIZE:
            player_pos[0] += PLAYER_SPEED

        bullets = move_bullets(bullets)
        enemy_bullets = move_enemy_bullets(enemy_bullets)
        invader_speed = move_invaders(invaders, invader_speed)
        bullets, invaders, gained = check_collision(bullets, invaders)
        score += gained

        now = pygame.time.get_ticks()
        shooter_info = enemy_fire(invaders, level)
        if shooter_info is not None:
            shooter, cooldown_ms = shooter_info
            if now - last_enemy_shot_at >= cooldown_ms:
                enemy_bullets.append(
                    [
                        shooter[0] + INVADER_SIZE // 2 - ENEMY_BULLET_SIZE // 2,
                        shooter[1] + INVADER_SIZE,
                    ]
                )
                last_enemy_shot_at = now

        enemy_bullets, got_hit = check_player_hit(enemy_bullets, player_pos)
        if got_hit or check_invader_reach_player(invaders, player_pos):
            lives -= 1
            player_pos = [WIDTH // 2, HEIGHT - 2 * PLAYER_SIZE]
            enemy_bullets = []
            if lives <= 0:
                game_over = True

        # Start a fresh wave when all invaders are gone or they move off-screen.
        if not invaders or min(inv[1] for inv in invaders) > HEIGHT:
            level += 1
            invaders = create_invaders(level)
            next_speed = min(MAX_INVADER_SPEED, 1.0 + (level - 1) * LEVEL_SPEED_STEP)
            invader_speed = next_speed if invader_speed > 0 else -next_speed
            enemy_bullets = []
            if level % 3 == 0 and lives < MAX_PLAYER_LIVES:
                lives += 1

    draw_player(player_pos)
    draw_bullets(bullets)
    draw_enemy_bullets(enemy_bullets)
    draw_invaders(invaders)
    draw_hud(score, level, lives)
    if game_over:
        draw_game_over()

    pygame.display.update()
    clock.tick(30)

pygame.quit()

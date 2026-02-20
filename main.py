import pygame

# Initialize Pygame
pygame.init()

# Screen dimensions
WIDTH = 800
HEIGHT = 600

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

# Player settings
PLAYER_SIZE = 50
PLAYER_SPEED = 6
player_pos = [WIDTH // 2, HEIGHT - 2 * PLAYER_SIZE]

# Bullet settings
BULLET_SIZE = 10
BULLET_SPEED = 10
bullets = []

# Invader settings
INVADER_SIZE = 50
invaders = [
    [x, y]
    for x in range(30, WIDTH - INVADER_SIZE, 60)
    for y in range(50, HEIGHT // 2 - INVADER_SIZE * 2, 40)
]
invader_speed = 1

# Score
score = 0
font = pygame.font.SysFont(None, 32)

# Set up the display
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space Invaders")

# Clock to control frame rate
clock = pygame.time.Clock()


def draw_player(pos):
    pygame.draw.rect(screen, RED, (pos[0], pos[1], PLAYER_SIZE, PLAYER_SIZE))


def draw_bullets(items):
    for bullet in items:
        pygame.draw.rect(screen, WHITE, (bullet[0], bullet[1], BULLET_SIZE, BULLET_SIZE))


def draw_invaders(items):
    for invader in items:
        pygame.draw.rect(
            screen, WHITE, (invader[0], invader[1], INVADER_SIZE, INVADER_SIZE)
        )


def draw_score(value):
    text = font.render(f"Score: {value}", True, WHITE)
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

    draw_player(player_pos)
    draw_bullets(bullets)
    draw_invaders(invaders)
    draw_score(score)

    pygame.display.update()
    clock.tick(30)

pygame.quit()

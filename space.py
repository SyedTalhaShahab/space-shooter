import subprocess
import sys

def install_pygame():
    try:
        import pygame
    except ImportError:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pygame"])
    finally:
        import pygame

# Call the function to ensure Pygame is installed
install_pygame()

# Your game code follows here...
import pygame
import random

# Initialize Pygame
pygame.init()

# Constants
TILE_SIZE = 32
ROWS = 16
COLUMNS = 16
BOARD_WIDTH = TILE_SIZE * COLUMNS
BOARD_HEIGHT = TILE_SIZE * ROWS
SHIP_WIDTH = TILE_SIZE * 2
SHIP_HEIGHT = TILE_SIZE
SHIP_X = TILE_SIZE * COLUMNS // 2 - TILE_SIZE
SHIP_Y = TILE_SIZE * ROWS - TILE_SIZE * 2
SHIP_VELOCITY_X = TILE_SIZE
ALIEN_WIDTH = TILE_SIZE * 2
ALIEN_HEIGHT = TILE_SIZE
ALIEN_X = TILE_SIZE
ALIEN_Y = TILE_SIZE
ALIEN_ROWS = 2
ALIEN_COLUMNS = 3
ALIEN_VELOCITY_X = 1
BULLET_VELOCITY_Y = -10
WHITE = (255, 255, 255)

# Setup the game screen
screen = pygame.display.set_mode((BOARD_WIDTH, BOARD_HEIGHT))
pygame.display.set_caption("Space Invaders")

# Load images
ship_img = pygame.image.load("ship.png")
alien_img = pygame.image.load("alien.png")

alien_img = pygame.transform.scale(alien_img, (ALIEN_WIDTH * (0.3), ALIEN_HEIGHT * (0.3)))
ship_img = pygame.transform.scale(ship_img, (ALIEN_WIDTH * (0.3), ALIEN_HEIGHT * (0.3)))


# Ship object
ship = {
    'x': SHIP_X,
    'y': SHIP_Y,
    'width': SHIP_WIDTH,
    'height': SHIP_HEIGHT,
    'velocity_x': SHIP_VELOCITY_X
}

# Alien setup
alien_array = []
alien_count = 0
alien_velocity_x = ALIEN_VELOCITY_X

def create_aliens():
    global alien_count
    alien_array.clear()
    for c in range(ALIEN_COLUMNS):
        for r in range(ALIEN_ROWS):
            alien = {
                'x': ALIEN_X + c * ALIEN_WIDTH,
                'y': ALIEN_Y + r * ALIEN_HEIGHT,
                'width': ALIEN_WIDTH,
                'height': ALIEN_HEIGHT,
                'alive': True
            }
            alien_array.append(alien)
    alien_count = len(alien_array)

create_aliens()

# Bullets setup
bullet_array = []
score = 0
game_over = False

def detect_collision(a, b):
    return a['x'] < b['x'] + b['width'] and \
           a['x'] + a['width'] > b['x'] and \
           a['y'] < b['y'] + b['height'] and \
           a['y'] + a['height'] > b['y']

# Main game loop
running = True
clock = pygame.time.Clock()

while running:
    screen.fill((0, 0, 0))  # Clear screen

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT and ship['x'] - ship['velocity_x'] >= 0:
                ship['x'] -= ship['velocity_x']
            elif event.key == pygame.K_RIGHT and ship['x'] + ship['velocity_x'] + ship['width'] <= BOARD_WIDTH:
                ship['x'] += ship['velocity_x']
            elif event.key == pygame.K_SPACE:
                bullet = {
                    'x': ship['x'] + ship['width'] * 15 // 32,
                    'y': ship['y'],
                    'width': TILE_SIZE // 8,
                    'height': TILE_SIZE // 2,
                    'used': False
                }
                bullet_array.append(bullet)

    if game_over:
        continue

    # Draw ship
    screen.blit(ship_img, (ship['x'], ship['y']))

    # Draw aliens
    for alien in alien_array:
        if alien['alive']:
            alien['x'] += alien_velocity_x

            if alien['x'] + alien['width'] >= BOARD_WIDTH or alien['x'] <= 0:
                alien_velocity_x *= -1
                alien['x'] += alien_velocity_x * 2
                for a in alien_array:
                    a['y'] += ALIEN_HEIGHT

            screen.blit(alien_img, (alien['x'], alien['y']))

            if alien['y'] >= ship['y']:
                game_over = True

    # Move and draw bullets
    for bullet in bullet_array:
        bullet['y'] += BULLET_VELOCITY_Y
        pygame.draw.rect(screen, WHITE, (bullet['x'] * (0.922), bullet['y'], bullet['width'], bullet['height']))

        for alien in alien_array:
            if not bullet['used'] and alien['alive'] and detect_collision(bullet, alien):
                bullet['used'] = True
                alien['alive'] = False
                alien_count -= 1
                score += 100

    # Remove used or off-screen bullets
    bullet_array = [b for b in bullet_array if not b['used'] and b['y'] > 0]

    # Check for next level
    if alien_count == 0:
        score += ALIEN_COLUMNS * ALIEN_ROWS * 100
        ALIEN_COLUMNS = min(ALIEN_COLUMNS + 1, COLUMNS // 2 - 2)
        ALIEN_ROWS = min(ALIEN_ROWS + 1, ROWS - 4)
        if alien_velocity_x > 0:
            alien_velocity_x += 0.2
        else:
            alien_velocity_x -= 0.2
        create_aliens()
        bullet_array.clear()

    # Display score
    font = pygame.font.SysFont("courier", 16)
    score_text = font.render(str(score), True, WHITE)
    screen.blit(score_text, (5, 20))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()

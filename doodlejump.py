import pygame
import random

# Initialize Pygame
pygame.init()

# Screen dimensions and colors
WIDTH, HEIGHT = 400, 600
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

# Set up the screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Enhanced Doodle Jump")

# Player attributes
player_width, player_height = 50, 50
player_x = WIDTH // 2 - player_width // 2
player_y = HEIGHT - player_height - 10
player_vel_y = 0
jump_strength = -10
gravity = 0.5

# Platform attributes
platforms = [[WIDTH // 2 - 50, HEIGHT - 50, 100, 10]]
platform_count = 6
platform_width, platform_height = 100, 10
platform_spacing = 100

# Game variables
score = 0
font = pygame.font.SysFont(None, 30)
game_over = False

# Power-up attributes
power_ups = []
power_up_chance = 0.1  # 10% chance to spawn power-up on a new platform
jetpack_boost = -20
spring_boost = -15
has_jetpack = False

# Enemy attributes
enemies = []
enemy_chance = 0.1  # 10% chance to spawn an enemy on a new platform

# Create initial platforms
def create_platforms():
    for i in range(platform_count):
        x = random.randint(0, WIDTH - platform_width)
        y = HEIGHT - (i * platform_spacing)
        platforms.append([x, y, platform_width, platform_height])

# Draw text on screen
def draw_text(text, font, color, x, y):
    img = font.render(text, True, color)
    screen.blit(img, (x, y))

# Game loop
running = True
create_platforms()
while running:
    pygame.time.delay(30)
    screen.fill(WHITE)

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Player movement
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and player_x > 0:
        player_x -= 5
    if keys[pygame.K_RIGHT] and player_x < WIDTH - player_width:
        player_x += 5

    # Apply gravity and jump
    player_y += player_vel_y
    player_vel_y += gravity

    # Check for platform collision and jumping
    for platform in platforms:
        if (player_x + player_width > platform[0] and player_x < platform[0] + platform_width and
                player_y + player_height > platform[1] and player_y + player_height < platform[1] + platform_height and
                player_vel_y > 0):
            player_vel_y = jump_strength
            score += 10  # Increase score each jump

    # Scroll platforms down
    if player_y < HEIGHT // 2:
        player_y += abs(player_vel_y)
        for platform in platforms:
            platform[1] += abs(player_vel_y)
            if platform[1] > HEIGHT:
                platform[1] = 0
                platform[0] = random.randint(0, WIDTH - platform_width)

                # Spawn power-ups and enemies
                if random.random() < power_up_chance:
                    power_ups.append([platform[0] + 20, platform[1] - 20, "jetpack" if random.random() < 0.5 else "spring"])
                if random.random() < enemy_chance:
                    enemies.append([platform[0] + 30, platform[1] - 30])

    # Check for power-up collision
    for power_up in power_ups:
        if (player_x + player_width > power_up[0] and player_x < power_up[0] + 20 and
                player_y + player_height > power_up[1] and player_y + player_height < power_up[1] + 20):
            if power_up[2] == "jetpack":
                player_vel_y = jetpack_boost
            elif power_up[2] == "spring":
                player_vel_y = spring_boost
            power_ups.remove(power_up)

    # Check for enemy collision (game over)
    for enemy in enemies:
        if (player_x + player_width > enemy[0] and player_x < enemy[0] + 20 and
                player_y + player_height > enemy[1] and player_y < enemy[1] + 20):
            game_over = True

    # Game over if player falls off screen
    if player_y > HEIGHT:
        game_over = True

    # Draw platforms
    for platform in platforms:
        pygame.draw.rect(screen, GREEN, platform)

    # Draw power-ups
    for power_up in power_ups:
        color = BLUE if power_up[2] == "jetpack" else RED
        pygame.draw.rect(screen, color, (power_up[0], power_up[1], 20, 20))

    # Draw enemies
    for enemy in enemies:
        pygame.draw.circle(screen, BLACK, (enemy[0], enemy[1]), 10)

    # Draw player
    pygame.draw.rect(screen, BLACK, (player_x, player_y, player_width, player_height))

    # Draw score
    draw_text(f"Score: {score}", font, BLACK, 10, 10)

    # Check for game over
    if game_over:
        draw_text("Game Over!", font, BLACK, WIDTH // 2 - 60, HEIGHT // 2)
        pygame.display.update()
        pygame.time.delay(2000)
        break

    # Update the display
    pygame.display.update()

# Quit Pygame
pygame.quit()

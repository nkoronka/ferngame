import pygame
import sys
import random

# Initialize Pygame
pygame.init()

# Set up some constants
WIDTH, HEIGHT = 800, 600
FPS = 60
OBSTACLE_WIDTH, OBSTACLE_HEIGHT = 50, 50
SCROLL_SPEED = 5
LEVEL_UP_TIME = 8000  # Level up every 8 seconds
OBSTACLE_SPAWN_TIME = LEVEL_UP_TIME // 4  # Spawn obstacles every 2 seconds within 8 seconds interval

# Set up assets: colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

# Create the game window
screen = pygame.display.set_mode((WIDTH, HEIGHT))

# Create player
player_pos = [WIDTH / 2, HEIGHT / 2]
player_speed = 5
player_size = (50, 50)

# Create obstacles
obstacles = []

# Level and obstacle spawn tracking
level = 1
obstacles_spawned = 0

# Level up and obstacle spawn events
LEVEL_UP = pygame.USEREVENT + 1
pygame.time.set_timer(LEVEL_UP, LEVEL_UP_TIME)
SPAWN_OBSTACLE = pygame.USEREVENT + 2

# Font for level display
font = pygame.font.Font(None, 36)

# Main game loop
while True:
    # Event loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == LEVEL_UP:
            SCROLL_SPEED += 1  # Increase scroll speed
            level += 1  # Increase level
            obstacles_spawned = 0
            pygame.time.set_timer(SPAWN_OBSTACLE, OBSTACLE_SPAWN_TIME)
        elif event.type == SPAWN_OBSTACLE:
            if obstacles_spawned < 4:
                obstacles.append([WIDTH, random.randint(0, HEIGHT - OBSTACLE_HEIGHT)])
                obstacles_spawned += 1
            else:
                pygame.time.set_timer(SPAWN_OBSTACLE, 0)  # Stop spawning obstacles

    # Check for key presses
    keys = pygame.key.get_pressed()
    if keys[pygame.K_a]:
        player_pos[0] -= player_speed
    if keys[pygame.K_d]:
        player_pos[0] += player_speed
    if keys[pygame.K_w]:
        player_pos[1] -= player_speed
    if keys[pygame.K_s]:
        player_pos[1] += player_speed

    # Keep player on the screen
    player_pos[0] = max(0, min(player_pos[0], WIDTH - player_size[0]))
    player_pos[1] = max(0, min(player_pos[1], HEIGHT - player_size[1]))

    # Update obstacle positions and remove if off screen
    obstacles = [[pos[0] - SCROLL_SPEED, pos[1]] for pos in obstacles if pos[0] > -OBSTACLE_WIDTH]

    # Check for collisions
    player_rect = pygame.Rect(player_pos[0], player_pos[1], *player_size)
    if any(pygame.Rect(obstacle[0], obstacle[1], OBSTACLE_WIDTH, OBSTACLE_HEIGHT).colliderect(player_rect) for obstacle in obstacles):
        print("Game Over!")
        pygame.quit()
        sys.exit()

    # Draw everything
    screen.fill(WHITE)
    pygame.draw.rect(screen, BLACK, (player_pos[0], player_pos[1], *player_size))

    for obstacle in obstacles:
        pygame.draw.rect(screen, RED, (obstacle[0], obstacle[1], OBSTACLE_WIDTH, OBSTACLE_HEIGHT))

    level_text = font.render(f"Level: {level}", True, BLACK)
    screen.blit(level_text, (WIDTH - level_text.get_width() - 10, 10))

    pygame.display.flip()
    pygame.time.Clock().tick(FPS)
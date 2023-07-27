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
OBSTACLES_PER_LEVEL = 6
OBSTACLE_SPAWN_TIME = LEVEL_UP_TIME // OBSTACLES_PER_LEVEL  # Spawn obstacles every 2 seconds within 8 seconds interval

# Set up assets: colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

# Game states
MENU = 0
GAME = 1
GAME_OVER = 2

# Create the game window
pygame.display.set_caption("My Game")
screen = pygame.display.set_mode((WIDTH, HEIGHT))

# Level up and obstacle spawn events
LEVEL_UP = pygame.USEREVENT + 1
pygame.time.set_timer(LEVEL_UP, LEVEL_UP_TIME)
SPAWN_OBSTACLE = pygame.USEREVENT + 2

# Font for level display
font = pygame.font.Font(None, 36)

class Player:
    def __init__(self, x, y, width, height, speed):
        self.rect = pygame.Rect(x, y, width, height)
        self.speed = speed
        self.health = 100  # Initial health

    def move(self, keys):
        if keys[pygame.K_a]:
            self.rect.x -= self.speed
        if keys[pygame.K_d]:
            self.rect.x += self.speed
        if keys[pygame.K_w]:
            self.rect.y -= self.speed
        if keys[pygame.K_s]:
            self.rect.y += self.speed

        # Keep player on the screen
        self.rect.x = max(0, min(self.rect.x, WIDTH - self.rect.width))
        self.rect.y = max(0, min(self.rect.y, HEIGHT - self.rect.height))

class Obstacle:
    def __init__(self, x, y, width, height, speed):
        self.rect = pygame.Rect(x, y, width, height)
        self.speed = speed

    def update(self):
        self.rect.x -= self.speed

class Game:
    def __init__(self):
        self.state = MENU
        self.level = 1
        self.obstacles_spawned = 0
        self.player = Player(WIDTH / 2, HEIGHT / 2, 50, 50, 5)
        self.obstacles = []

    def handle_event(self, event):
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if self.state == MENU:
            if event.type == pygame.MOUSEBUTTONDOWN:
                self.start_game()

        elif self.state == GAME:
            if event.type == LEVEL_UP:
                self.level_up()

            elif event.type == SPAWN_OBSTACLE:
                self.spawn_obstacle()

        elif self.state == GAME_OVER:
            if event.type == pygame.MOUSEBUTTONDOWN:
                self.state = MENU

    def level_up(self):
        global SCROLL_SPEED
        SCROLL_SPEED += 1  # Increase scroll speed
        self.level += 1  # Increase level
        self.obstacles_spawned = 0
        pygame.time.set_timer(SPAWN_OBSTACLE, OBSTACLE_SPAWN_TIME)

    def spawn_obstacle(self):
        if self.obstacles_spawned < OBSTACLES_PER_LEVEL:
            self.obstacles.append(Obstacle(WIDTH, random.randint(0, HEIGHT - OBSTACLE_HEIGHT), OBSTACLE_WIDTH, OBSTACLE_HEIGHT, SCROLL_SPEED))
            self.obstacles_spawned += 1
        else:
            pygame.time.set_timer(SPAWN_OBSTACLE, 0)  # Stop spawning obstacles

    def start_game(self):
        self.state = GAME
        self.level = 1
        self.obstacles_spawned = 0
        self.obstacles.clear()
        pygame.time.set_timer(SPAWN_OBSTACLE, OBSTACLE_SPAWN_TIME)

    def update(self):
        if self.state == GAME:
            self.player.move(pygame.key.get_pressed())

            # Update obstacle positions and remove if off screen
            self.obstacles = [obs for obs in self.obstacles if obs.rect.x > -OBSTACLE_WIDTH]
            for obs in self.obstacles:
                obs.update()

            # Check for collisions
            if any(obs.rect.colliderect(self.player.rect) for obs in self.obstacles):
                self.state = GAME_OVER

    def draw_health_bar(self):
        # Draw the health on top of it (will decrease)
        pygame.draw.rect(screen, GREEN, (11, 11, self.player.health, 10))

    def draw(self):
        if self.state == MENU:
            screen.fill(BLACK)
            menu_text = font.render("New Game", True, WHITE)
            menu_rect = menu_text.get_rect(center=(WIDTH / 2, HEIGHT / 2))
            screen.blit(menu_text, menu_rect)
        elif self.state == GAME:
            screen.fill(WHITE)
            pygame.draw.rect(screen, BLACK, self.player.rect)
            for obs in self.obstacles:
                pygame.draw.rect(screen, RED, obs.rect)
            level_text = font.render(f"Level: {self.level}", True, BLACK)
            screen.blit(level_text, (WIDTH - level_text.get_width() - 10, 10))
            # Draw health bar
            self.draw_health_bar()
        elif self.state == GAME_OVER:
            screen.fill(BLACK)
            game_over_text = font.render(f"Game Over! Level: {self.level}", True, WHITE)
            game_over_rect = game_over_text.get_rect(center=(WIDTH / 2, HEIGHT / 2))
            screen.blit(game_over_text, game_over_rect)
            menu_text = font.render("New Game", True, WHITE)
            menu_rect = menu_text.get_rect(center=(WIDTH / 2, HEIGHT / 2 + 50))
            screen.blit(menu_text, menu_rect)
        pygame.display.flip()


game = Game()

while True:
    for event in pygame.event.get():
        game.handle_event(event)
    game.update()
    game.draw()
    pygame.time.Clock().tick(FPS)

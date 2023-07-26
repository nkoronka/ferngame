# Import the required libraries
import pygame
import math

# Initialize pygame
pygame.init()

# Set the screen dimensions
screen_width = 800
screen_height = 600

# Set the tank dimensions
tank_width = 50
tank_height = 30

# Set the turret dimensions
turret_length = 40
turret_width = 10

# Set the tank and turret colors
tank_color = (255, 0, 0)  # Red
turret_color = (0, 255, 0)  # Green

# Set the tank movement and turret rotation speeds
tank_speed = 5
turret_speed = 2

# Set the projectile dimensions and speed
projectile_width = 5
projectile_height = 5
projectile_speed = 10
projectile_color = (255, 255, 0)  # Yellow

# Create the screen
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Tank Game")

# Load the tank image
tank_image = pygame.Surface((tank_width, tank_height))
tank_image.fill(tank_color)

# Load the turret image
turret_image = pygame.Surface((turret_length, turret_width))
turret_image.fill(turret_color)

# Create the tanks
tank1_pos = [100, 100]
tank1_angle = 0
tank2_pos = [screen_width - 100, screen_height - 100]
tank2_angle = 180

# Create the projectiles
projectiles = []

# Create the clock to control the frame rate
clock = pygame.time.Clock()

# Game loop
running = True
tank1_control = True
while running:
    # Check for events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
            elif event.key == pygame.K_RETURN:
                # Fire a projectile from the active tank's turret
                if tank1_control:
                    angle = math.radians(tank1_angle)
                    pos = list(tank1_pos)
                else:
                    angle = math.radians(tank2_angle)
                    pos = list(tank2_pos)

                vel = [projectile_speed * math.cos(angle), -projectile_speed * math.sin(angle)]
                projectile = {"pos": pos, "vel": vel}
                projectiles.append(projectile)

    # Update tank positions and turret angles
    keys = pygame.key.get_pressed()
    if tank1_control:
        if keys[pygame.K_LEFT] and tank1_pos[0] > 0:
            tank1_pos[0] -= tank_speed
        if keys[pygame.K_RIGHT] and tank1_pos[0] < screen_width - tank_width:
            tank1_pos[0] += tank_speed
        if keys[pygame.K_UP] and tank1_pos[1] > 0:
            tank1_pos[1] -= tank_speed
        if keys[pygame.K_DOWN] and tank1_pos[1] < screen_height - tank_height:
            tank1_pos[1] += tank_speed
        if keys[pygame.K_a]:
            tank1_angle -= turret_speed
        if keys[pygame.K_d]:
            tank1_angle += turret_speed
    else:
        if keys[pygame.K_LEFT] and tank2_pos[0] > 0:
            tank2_pos[0] -= tank_speed
        if keys[pygame.K_RIGHT] and tank2_pos[0] < screen_width - tank_width:
            tank2_pos[0] += tank_speed
        if keys[pygame.K_UP] and tank2_pos[1] > 0:
            tank2_pos[1] -= tank_speed
        if keys[pygame.K_DOWN] and tank2_pos[1] < screen_height - tank_height:
            tank2_pos[1] += tank_speed
        if keys[pygame.K_a]:
            tank2_angle -= turret_speed
        if keys[pygame.K_d]:
            tank2_angle += turret_speed

    # Clear the screen
    screen.fill((0, 0, 0))

    # Rotate and draw the tanks
    tank1_rotated = pygame.transform.rotate(tank_image, tank1_angle)
    tank1_rect = tank1_rotated.get_rect(center=tank1_pos)
    screen.blit(tank1_rotated, tank1_rect)

    tank2_rotated = pygame.transform.rotate(tank_image, tank2_angle)
    tank2_rect = tank2_rotated.get_rect(center=tank2_pos)
    screen.blit(tank2_rotated, tank2_rect)

    # Rotate and draw the turrets
    turret1_rotated = pygame.transform.rotate(turret_image, tank1_angle)
    turret1_rect = turret1_rotated.get_rect(center=tank1_pos)
    screen.blit(turret1_rotated, turret1_rect)

    turret2_rotated = pygame.transform.rotate(turret_image, tank2_angle)
    turret2_rect = turret2_rotated.get_rect(center=tank2_pos)
    screen.blit(turret2_rotated, turret2_rect)

    # Update and draw the projectiles
    for projectile in projectiles:
        pos = projectile['pos']
        vel = projectile['vel']
        pos[0] += vel[0]
        pos[1] += vel[1]
        projectile_rect = pygame.Rect(pos[0], pos[1], projectile_width, projectile_height)
        pygame.draw.rect(screen, projectile_color, projectile_rect)

    # Remove projectiles that have gone off-screen
    projectiles = [projectile for projectile in projectiles if 0 <= projectile['pos'][0] <= screen_width and 0 <= projectile['pos'][1] <= screen_height]

    # Update the display
    pygame.display.flip()

    # Limit the frame rate
    clock.tick(60)

# Quit the game
pygame.quit()

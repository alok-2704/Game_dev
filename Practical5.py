import pygame
import math

pygame.init()

WIDTH = 800
HEIGHT = 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Diffuse Lighting Simulation")

clock = pygame.time.Clock()

light_x = 400
light_y = 150

object_x = 400
object_y = 350
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    screen.fill((20, 20, 20))

# Draw Light Source
    pygame.draw.circle(screen, (255, 255, 0), (light_x, light_y), 20)
# Distance Calculation
    distance = math.sqrt(
    (object_x - light_x)**2 +
    (object_y - light_y)**2
    )

    intensity = max(50, 255 - int(distance / 2))

    color = (intensity, intensity, intensity)


    # Draw Object
    pygame.draw.circle(screen, color,
    (object_x, object_y), 80)

    pygame.display.update()


    clock.tick(60)

pygame.quit()
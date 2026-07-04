import pygame
pygame.init()

WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Textured Triangle")

# Triangle points
points = [(400, 150), (250, 400), (550, 400)]

# Load texture
texture = pygame.image.load("texture1.jpg").convert()
texture = pygame.transform.scale(texture, (300, 250))

# Create mask surface
mask = pygame.Surface((300, 250), pygame.SRCALPHA)
triangle = [(150, 0), (0, 250), (300, 250)]

# RGBA(Aplha (Transparency))
pygame.draw.polygon(mask, (255, 255, 255, 255), triangle)

# Copy texture
textured_triangle = pygame.Surface((300, 250), pygame.SRCALPHA)
textured_triangle.blit(texture, (0, 0))

# Apply mask
textured_triangle.blit(mask, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)

running = True

while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill((0, 0, 0))

    # Draw textured triangle
    screen.blit(textured_triangle, (250, 150))

    # Draw outline
    pygame.draw.polygon(screen, (255, 255, 255), points, 3)

    pygame.display.flip()

pygame.quit()
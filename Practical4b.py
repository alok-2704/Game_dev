import pygame
pygame.init()

WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Textured Square")

# Square points
points = [(250, 150), (550, 150), (550, 450), (250, 450)]

# Load texture
texture = pygame.image.load("texture.jpg").convert()
texture = pygame.transform.scale(texture, (300, 300))

# Create mask surface
mask = pygame.Surface((300, 300), pygame.SRCALPHA)
square = [(0, 0), (300, 0), (300, 300), (0, 300)]

pygame.draw.polygon(mask, (255, 255, 255, 255), square)

# Copy texture
textured_square = pygame.Surface((300, 300), pygame.SRCALPHA)
textured_square.blit(texture, (0, 0))

# Apply mask
textured_square.blit(mask, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)

running = True

while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill((0, 0, 0))

    # Draw textured square
    screen.blit(textured_square, (250, 150))

    # Draw outline
    pygame.draw.polygon(screen, (255, 255, 255), points, 3)

    pygame.display.flip()

pygame.quit()
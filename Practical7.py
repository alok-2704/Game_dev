import pygame

pygame.init()

WIDTH = 800
HEIGHT = 600


screen = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("Model loading and rendering")

# Load Model(Sprite)
player = pygame.image.load("player.png")

# Resize Sprite
player = pygame.transform.scale(player,(100,100))

x = 350
y = 250

clock = pygame.time.Clock()


running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()

    if keys[pygame.K_LEFT]:
        x -=5

    if keys[pygame.K_RIGHT]:
        x +=5    

    if keys[pygame.K_UP]:
        y -=5        
    
    if keys[pygame.K_DOWN]:
        y +=5


    screen.fill((40,40,40))


    # Render Model
    screen.blit(player,(x,y))


    pygame.display.update()
    clock.tick(60)

pygame.quit()        
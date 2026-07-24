import pygame 
import random

pygame.init()

WIDTH = 800
HEIGHT = 600

screen = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("2D UFO Catching Game")

font = pygame.font.SysFont(None,40,)

player = pygame.Rect(375,500,50,50)

ufo = pygame.Rect(random.randint(50,750),random.randint(50,450),40,40)

score = 0

clock = pygame.time.Clock()

running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False


    keys = pygame.key.get_pressed()

    if keys[pygame.K_LEFT]:
        player.x -= 5

    if keys[pygame.K_RIGHT]:
        player.x += 5

    if keys[pygame.K_UP]:
        player.y -= 5

    if keys[pygame.K_DOWN]:
        player.y += 5

    if player.colliderect(ufo):
        score += 1

        ufo.x = random.randint(50,750)
        ufo.y = random.randint(50,450)

    screen.fill((0,0,20))

    # Player
    pygame.draw.rect(screen,(0,255,0),player)

    # UFO
    pygame.draw.ellipse(screen,(255,0,255),ufo)


    score_text = font.render(f"Score : {score}",True,(255,255,255))

    screen.blit(score_text,(10,10))

    pygame.display.update()
    clock.tick(60)

pygame.quit()    


import pygame 
import random

pygame.init()

WIDTH = 800
HEIGHT = 600

screen = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("Roll-Ball Game")

font = pygame.font.SysFont(None,40)

ball_x = 400
ball_y = 300
ball_radius = 20
speed = 5

score = 0

# Create collectibles 
collectibles = []

for i in range(10):
    collectibles.append(
        pygame.Rect(
            random.randint(50,750),
            random.randint(50,550),
            20,
            20
        )
    )

clock = pygame.time.Clock()

running = True

while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()

    
    if keys[pygame.K_LEFT]:
        ball_x -= speed

    if keys[pygame.K_RIGHT]:
        ball_x +=speed


    if keys[pygame.K_UP]:
        ball_y -= speed        
    
    if keys[pygame.K_DOWN]:
        ball_y += speed


    screen.fill((20,20,40))

    # Draw Ball
    pygame.draw.circle(
        screen,
        (0,255,0),
        (ball_x, ball_y),
        ball_radius
        )

    ball_rect = pygame.Rect( 
        ball_x - ball_radius,
        ball_y - ball_radius,
        ball_radius*2,
        ball_radius*2
        )

    #Draw collectibles
    for item in collectibles[:]:

        pygame.draw.rect(
            screen,
            (255,255,0),
            item
        )

        if ball_rect.colliderect(item):
            collectibles.remove(item)
            score += 1

    score_text = font.render(f"Score : {score}",True,(255,255,255))

    screen.blit(score_text,(10,10))

    if len(collectibles) == 0:
        win_text = font.render("YOU WIN!", True,(0,255,0))
        screen.blit(win_text,(320,280))


    pygame.display.update()
    clock.tick(60)

pygame.quit()                    
import pygame
import random

pygame.init()

WIDTH = 800
HEIGHT = 600

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space Shooter Game")

font = pygame.font.SysFont(None, 40)

# Player
player = pygame.Rect(375, 520, 50, 50)

# Bullets
bullets = []

# Enemies
enemies = []

for i in range(5):
    enemies.append(
        pygame.Rect(
            random.randint(50, 750),
            random.randint(20, 150),
            40,
            40
        )
    )

score = 0
game_over = False

clock = pygame.time.Clock()
running = True

while running:
    clock.tick(60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                bullets.append(
                    pygame.Rect(
                        player.x + 22,
                        player.y,
                        6,
                        15
                    )
                )

    keys = pygame.key.get_pressed()

    if keys[pygame.K_LEFT]:
        player.x -= 6

    if keys[pygame.K_RIGHT]:
        player.x += 6

    player.x = max(0, min(player.x, WIDTH - player.width))

    if not game_over:

        # Move bullets
        for bullet in bullets[:]:
            bullet.y -= 8
            if bullet.y < 0:
                bullets.remove(bullet)

        # Move enemies
        for enemy in enemies[:]:
            enemy.y += 2

            if enemy.y > HEIGHT:
                game_over = True

        # Collision detection
        for bullet in bullets[:]:
            for enemy in enemies[:]:
                if bullet.colliderect(enemy):

                    if bullet in bullets:
                        bullets.remove(bullet)

                    if enemy in enemies:
                        enemies.remove(enemy)

                    score += 1

                    enemies.append(
                        pygame.Rect(
                            random.randint(50, 750),
                            0,
                            40,
                            40
                        )
                    )
                    break

    # Drawing Section
    screen.fill((0, 0, 30))

    # Player spaceship
    pygame.draw.polygon(
        screen,
        (0, 255, 0),
        [
            (player.x + 25, player.y),
            (player.x, player.y + 50),
            (player.x + 50, player.y + 50)
        ]
    )

    # Bullets
    for bullet in bullets:
        pygame.draw.rect(screen, (255, 255, 0), bullet)

    # Enemies
    for enemy in enemies:
        pygame.draw.rect(screen, (255, 0, 0), enemy)

    score_text = font.render(
        f"Score : {score}",
        True,
        (255, 255, 255)
    )

    screen.blit(score_text, (10, 10))

    if game_over:
        over_text = font.render(
            "GAME OVER",
            True,
            (255, 0, 0)
        )
        screen.blit(over_text, (300, 280))

    pygame.display.update()

pygame.quit()
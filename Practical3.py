import pygame

pygame.init()

WIDTH = 800
HEIGHT = 600

screen = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("Triangle Drawing")

running = True

while running:

    for event in pygame.event.get():
        if event.type ==pygame.QUIT:
            running = False

    screen.fill((0,0,0))

    points = [(400,150), (250,400), (550,400)]

    pygame.draw.polygon(screen,(150,35,200),points)

    pygame.display.update()

pygame.quit()    



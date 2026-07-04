import pygame
import datetime

#Initialize pygame
pygame.init()

#Window settings
WIDTH = 800
HEIGHT = 600


screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Digital clock ")

# colors
WHITE =(255,2,155)
BLACK = (0,0,0)

# Font
font = pygame.font.SysFont("Arial",60)

# clock object
clock = pygame.time.Clock()

running = True

while running:
    # Event handling
    for event in pygame.event.get():
        if event.type ==pygame.QUIT:
            running = False
    # Background color
    screen.fill((30,30,30))

    # get current time
    current_time = datetime.datetime.now().strftime("%H:%M:%S")

    # Create Text surface
    time_text = font.render(current_time,True,WHITE)

    # Center the time on screen
    text_rect = time_text.get_rect(center=(WIDTH//2,HEIGHT//2))
    screen.blit(time_text,text_rect)

    # update display
    pygame.display.update()
    
    # limit to 60 fps
    clock.tick(60)

pygame.quit()            


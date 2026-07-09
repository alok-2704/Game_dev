import pygame

pygame.init()

WIDTH = 800
HEIGHT = 600


screen = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("Specular Lighting Simulator")

clock = pygame.time.Clock()

light_x = 200
light_y = 150 

object_x = 400
object_y = 300


running = True


while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Move Light Using Mouse
    light_x, light_y = pygame.mouse.get_pos()


    screen.fill((30,30,40))

    # Draw Light Source
    pygame.draw.circle(screen,(255,255,0),(light_x,light_y),12)

    # Main Object
    pygame.draw.circle(screen,(100,100,255),(object_x,object_y),100)


    # Specular Highlight
    highlight_x = object_x + (light_x - object_x) // 4
    highlight_y = object_y + (light_y - object_y) // 4



    pygame.draw.circle(screen,(255,255,255),(highlight_x,highlight_y) ,20)

    pygame.display.update()
    clock.tick(60)

pygame.quit()    
            
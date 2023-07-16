import pygame
import os

pygame.init()

win = pygame.display.set_mode((1000, 500))
bg_img = pygame.image.load(os.path.join("background.png"))
bg = pygame.transform.scale(bg_img, (1000, 500))

width = 1000

s_height = 768
s_width = 1024
screen = pygame.display.set_mode((s_width, s_height))
background = pygame.image.load(os.path.join("background.png"))
background = pygame.transform.scale(background, (1024, 768))

i = 0

run = True
while run:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False


    win.fill((0,0,0))

    #Create looping background
    win.blit(bg, (i, 0))
    win.blit(bg, (width+i, 0))
    if i == -width:
        win.blit(bg, (width+i, 0))

    screen.fill((0, 0, 0))
    #Create looping background
    screen.blit(background, (i, 0))
    screen.blit(background, (s_width + i, 0))
    if i == -s_width:
        screen.blit(background, (s_width + i, 0))

        i = 0
    i -= 1

    pygame.display.update()
#BitBallers
#Intro Video Game Design
#Main


import pygame as PG
import pygame.display as PD
import pygame.event as PE
import pygame.font as PF
import pygame.time as PT
import Enemy

#constants
WIDTH = 800
HEIGHT = 600
COLOR = (255, 255, 255)
INTERVAL = .1

PG.init()
screen = PD.set_mode((WIDTH, HEIGHT))
PD.set_caption("Gamma Ray Kitten")
screen.fill(COLOR)
clock = PT.Clock()
current_time = PT.get_ticks()

while True:
    new_time = PT.get_ticks()
    frame_time = (new_time - current_time) / 1000.0
    current_time = new_time
    clock.tick()

    screen.fill(COLOR)

    ship.draw(screen)
    PD.flip()
    while frame_time > INTERVAL:
        ship.update(INTERVAL)
        frame_time -= INTERVAL
    ship.update(frame_time)
    for event in PE.get():
        if event.type == PG.QUIT:
            exit()
        elif event.type == PG.KEYDOWN and event.key = PG.K_ESCAPE:
            exit();
        elif event.type == PG.KEYDOWN or event.type == PG.KEYUP:

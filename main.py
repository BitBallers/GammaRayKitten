#BitBallers
#Intro Video Game Design
#Main


import pygame as PG
import pygame.display as PD
import pygame.event as PE
import pygame.font as PF
import pygame.time as PT
import pygame.sprite as PS
import Enemy
import Player
import random

#constants
WIDTH = 800
HEIGHT = 600
COLOR = (255, 255, 255)
INTERVAL = .2

PG.init()
screen = PD.set_mode((WIDTH, HEIGHT))
PD.set_caption("Gamma Ray Kitten")
screen.fill(COLOR)
clock = PT.Clock()
current_time = PT.get_ticks()
all_sprites_list = PS.Group()
enemies = []
enemy_speed = 50

for i in range(13):
    new_x = random.randint(30,700)
    new_y = random.randint(30, 500)
    new_x_vel = random.randint(-2,1)*enemy_speed
    #new_x_vel = enemy_speed
    if new_x_vel == 0:
        new_y_vel = -enemy_speed
    else:
        new_y_vel = 0
    enemies.append( Enemy.Enemy(new_x, new_y, new_x_vel, new_y_vel) )
    all_sprites_list.add(enemies[i])

player = Player.Player(400, 300)
all_sprites_list.add(player)

while True:
    new_time = PT.get_ticks()
    frame_time = (new_time - current_time) / 1000.0
    current_time = new_time
    clock.tick()

    screen.fill(COLOR)

    all_sprites_list.draw(screen)

    PD.flip()
    #Update Loop
    while frame_time > INTERVAL:
        for e in enemies:
            e.update(INTERVAL)
        player.update(INTERVAL)
        frame_time -= INTERVAL
    #Update remaining frame_time
    for e in enemies:
        e.update(frame_time)
    player.update(frame_time)

    for event in PE.get():
        if event.type == PG.QUIT:
            exit()
        elif event.type == PG.KEYDOWN and event.key == PG.K_ESCAPE:
            exit()
        elif event.type == PG.KEYDOWN or event.type == PG.KEYUP:
            player.handle_events(event)

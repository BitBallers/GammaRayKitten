import pygame as PG
import pygame.color as PC
import pygame.event as PE
import pygame.time as PT
import pygame.sprite as PS
import pygame.mixer as PX
import Enemy
import Player
import random
import State
import Menu
import Globals as G

class Game(State.State):
    def __init__(self):
        State.State.__init__(self)
        self.all_sprites_list = PS.Group()
        self.enemy_speed = 1
        self.time = 0.0
        self.enemies = []
        #PX.music.load("Some_Song.mod") #if you want to add music Jay 
        #PX.music.play(-1)

        for i in range(13):
                new_x = random.randint(30, 700)
                new_y = random.randint(30, 500)
                new_x_vel = random.randint(-2, 1) * self.enemy_speed
                if new_x_vel == 0:
                    new_y_vel = -self.enemy_speed
                else:
                    new_y_vel = 0
                new_enemy = Enemy.Enemy(new_x, new_y, new_x_vel, new_y_vel)
                self.all_sprites_list.add(new_enemy)  
                self.enemies.append(new_enemy)
        self.player = Player.Player(400, 300)
        self.all_sprites_list.add(self.player)

    def render(self):
        G.Globals.SCREEN.fill(PC.Color("black"))    
        self.all_sprites_list.draw(G.Globals.SCREEN)

    def update(self, time):
        self.time += time
        while self.time > G.Globals.INTERVAL:
            for e in self.enemies:
                e.update()
            self.player.update(G.Globals.INTERVAL)
            self.time -= G.Globals.INTERVAL
    def event(self, event):
        if event.type == PG.KEYDOWN and event.key  == PG.K_ESCAPE:
            G.Globals.STATE = Menu.Menu()

        elif event.type == PG.KEYDOWN or event.type == PG.KEYUP:
            self.player.handle_events(event)

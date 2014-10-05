<<<<<<< HEAD
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
import Tile


class Game(State.State):

    TILE_WIDTH = 50
    TILE_HEIGHT = 50

    def __init__(self):
        State.State.__init__(self)
        self.all_sprites_list = PS.Group()
        self.wall_sprites_list = PS.Group()
        self.map_sprites_list = PS.Group()
        self.enemy_speed = 1
        self.time = 0.0
        self.enemies = []

        self.map = []

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

        self.load_map()



    def render(self):
        G.Globals.SCREEN.fill(PC.Color("white"))
        self.map_sprites_list.draw(G.Globals.SCREEN)
        self.all_sprites_list.draw(G.Globals.SCREEN)

    def update(self, time):
        self.time += time
        while self.time > G.Globals.INTERVAL:
            for e in self.enemies:
                e.update()
            self.player.update(G.Globals.INTERVAL)
            self.time -= G.Globals.INTERVAL

    def event(self, event):
        if event.type == PG.KEYDOWN and event.key == PG.K_ESCAPE:
            G.Globals.STATE = Menu.Menu()

        elif event.type == PG.KEYDOWN or event.type == PG.KEYUP:
            self.player.handle_events(event)

    def load_map(self):
        map_file = open("basic_map.txt")
        i = 0
        for line in map_file.readlines():
            k = 0
            for character in line:
                if k == 16:
                    continue
                self.map.append(Tile.Tile(k*Game.TILE_WIDTH, i*Game.TILE_HEIGHT, int(character)))
                self.map_sprites_list.add(self.map[-1])
                if int(character) != 1:
                    self.wall_sprites_list.add(self.map[-1])
                k += 1
            i += 1
=======
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
        G.Globals.SCREEN.fill(PC.Color("white"))
        self.all_sprites_list.draw(G.Globals.SCREEN)

    def update(self, time):
        self.time += time
        while self.time > G.Globals.INTERVAL:
            for e in self.enemies:
                e.update()
            self.player.update(G.Globals.INTERVAL)
            self.time -= G.Globals.INTERVAL

    def event(self, event):
        if event.type == PG.KEYDOWN and event.key == PG.K_ESCAPE:
            G.Globals.STATE = Menu.Menu()

        elif event.type == PG.KEYDOWN or event.type == PG.KEYUP:
            self.player.handle_events(event)
>>>>>>> FETCH_HEAD

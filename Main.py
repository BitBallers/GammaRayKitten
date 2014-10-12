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
import Camera
import Map
import math


class Game(State.State):

    TILE_WIDTH = 50
    TILE_HEIGHT = 50
    MAP_TILE_WIDTH = 16
    MAP_TILE_HEIGHT = 12

    def __init__(self):
        State.State.__init__(self)
        
        self.map = Map.Map("Map for Assignment 5.txt")
        self.camera = Camera.Camera(self.map.height*Map.TILE_HEIGHT-G.Globals.HEIGHT, 0)
        self.all_sprites_list = PS.Group()
        self.player_group = PS.Group()
        self.enemy_speed = 1
        self.time = 0.0
        self.enemies = []

    def render(self):
        G.Globals.SCREEN.fill(PC.Color("white"))
        self.map_sprites_list.draw(G.Globals.SCREEN)
        self.all_sprites_list.draw(G.Globals.SCREEN)
        self.player_group.draw(G.Globals.SCREEN)

    def update(self, time):
        self.time += time
        while self.time > G.Globals.INTERVAL:
            for e in self.enemies:
                e.update()
            self.player.update(G.Globals.INTERVAL)
            #Are there collisions
            result = PS.groupcollide(self.player_group, self.wall_sprites_list,
                                  False, False)
            for key in result: 
                self.player.wall_collision(result[key][0])
            self.time -= G.Globals.INTERVAL

    def event(self, event):
        if event.type == PG.KEYDOWN and event.key == PG.K_ESCAPE:
            G.Globals.STATE = Menu.Menu()

        elif event.type == PG.KEYDOWN or event.type == PG.KEYUP:
            self.player.handle_events(event)

    def set_screen_coords_map(self):
        self.wall_sprites_list = PS.Group()
        self.floor_sprites_list = PS.Group()
        self.special_sprites_list = PS.Group()

        first_x = math.floor(self.camera.x/Main.TILE_WIDTH)*Main.TILE_WIDTH
        first_y = math.floor(self.camera.y/Main.TILE_HEIGHT)*Main.TILE_HEIGHT
        offset_x = first_x - self.camera.x
        offset_y = first_y - self.camera.y
        for i in range(Main.MAP_TILE_WIDTH+1):
            for k in range(Main.MAP_TILE_HEIGHT+1):
                x = first_x+(i*Main.TILE_WIDTH)
                y = first_y*(k*Main.TILE_HEIGHT)
                tile = self.map.tiles[(x, y)]
                tile.rect.x = offset_x+(i*Main.TILE_WIDTH)
                tile.rect.y = offset_y+(k*Main.TILE_HEIGHT)

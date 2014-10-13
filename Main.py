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
        self.camera = Camera.Camera(0, Map.Map.HEIGHT-G.Globals.HEIGHT, self)
        self.all_sprites_list = PS.Group()
        self.player_group = PS.Group()
        self.player = Player.Player(100, Map.Map.HEIGHT-50, self.camera)
        self.player_group.add(self.player)
        self.enemy_speed = 1
        self.time = 0.0
        self.enemies = []
        self.set_screen_coords_map()
        self.set_screen_cords_player()
        
    def render(self):
        G.Globals.SCREEN.fill(PC.Color("white"))
        self.map_tiles.draw(G.Globals.SCREEN)
        self.player_group.draw(G.Globals.SCREEN)

    def update(self, time):
        self.time += time
        while self.time > G.Globals.INTERVAL:
            for e in self.enemies:
                e.update()
            self.player.update(G.Globals.INTERVAL)
            # Are there collisions
            self.set_screen_cords_player()
            result = PS.groupcollide(self.player_group, self.wall_sprites_list,
                                  False, False)
            for key in result:
                for wall in result[key]:
                    val = self.player.wall_collision(wall)
                    if val == 1:
                        self.wall_sprites_list.remove(wall)
                    if val == 2:
                        G.Globals.STATE = Menu.Menu()
                        
            self.time -= G.Globals.INTERVAL


    def event(self, event):
        if event.type == PG.KEYDOWN and event.key == PG.K_ESCAPE:
            G.Globals.STATE = Menu.Menu()

        elif event.type == PG.KEYDOWN or event.type == PG.KEYUP:
            self.player.handle_events(event)

    def set_screen_coords_map(self):
        self.map_tiles = PS.Group()
        self.wall_sprites_list = PS.Group()

        first_x = math.floor(self.camera.X/Game.TILE_WIDTH)*Game.TILE_WIDTH
        first_y = math.floor(self.camera.Y/Game.TILE_HEIGHT)*Game.TILE_HEIGHT
        offset_x = first_x - self.camera.X
        offset_y = first_y - self.camera.Y

        for i in range(Game.MAP_TILE_WIDTH+1):
            for k in range(Game.MAP_TILE_HEIGHT+1):
                x = first_x+(i*Game.TILE_WIDTH)
                y = first_y+(k*Game.TILE_HEIGHT)
                tile = self.map.tiles[(x, y)]
                tile.set_screen_coords(offset_x+(i*Game.TILE_WIDTH), offset_y+(k*Game.TILE_HEIGHT))
                self.map_tiles.add(tile)
                if tile.is_wall() or tile.is_key() or tile.is_door() or tile.is_stairs():
                    self.wall_sprites_list.add(tile)

    def set_screen_cords_player(self):
        screen_x = self.player.world_coord_x-self.camera.X
        screen_y = self.player.world_coord_y-self.camera.Y
        self.player.set_screen_coords(screen_x, screen_y)

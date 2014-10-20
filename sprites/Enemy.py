import pygame as PG
import pygame.image as PI
import pygame.sprite as PS
import Globals as G
import maps.Camera as Camera
import maps.Map as Map
import math
import random

class Enemy(PS.Sprite):

    IMAGES = None
    CYCLE = 1.0
    MAX_AI_DIST = 1000
    SPEED = 2
    AI_PERCENTAGE = .9

    def __init__(self, (x, y)):
        PS.Sprite.__init__(self)

        if not Enemy.IMAGES:
            self.load_images()

        self.image = Enemy.IMAGES[8]
        self.b_index = 8
        self.c_index = 8
        self.rect = self.image.get_rect()
        self.world_x = x
        self.world_y = y

        self.x_velocity = 0
        self.y_velocity = 0

        self.time = 0.0

    def update(self, time, player, map):
        self.ai(player, map)
        self.world_x += self.x_velocity
        self.world_y += self.y_velocity
        self.rect.x = self.world_x-Camera.Camera.X
        self.rect.y = self.world_y-Camera.Camera.Y

    def render(self):
        x = self.world_x-Camera.Camera.X
        y = self.world_y-Camera.Camera.Y
        if x >= self.rect.width*-1 and x <= G.Globals.WIDTH and y >= self.rect.height*-1 and y <= G.Globals.HEIGHT:
            G.Globals.SCREEN.blit(self.image, (x,y))

    def load_images(self):
        Enemy.IMAGES = []
        sheet = PI.load("sprites/images/slime_sprite_sheet.png").convert_alpha()
        key = sheet.get_at((0, 0))
        for y in range(4):
            for x in range(4):
                surface = PG.Surface((30, 20)).convert()
                surface.set_colorkey(key)
                surface.blit(sheet, (0, 0), (x*30, y*20, 30, 20))
                Enemy.IMAGES.append(surface)

    def update_image(self):
        if self.y_velocity > 0:
            self.b_index = 8
        elif self.y_velocity < 0:
            self.b_index = 12
        if self.x_velocity > 0:
            self.b_index = 0
        elif self.x_velocity < 0:
            self.b_index = 4
        self.image = Enemy.IMAGES[self.b_index + self.c_index]
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

    def ai(self, player, map):
        sight_vector = ((player.world_coord_x-self.world_x), (player.world_coord_y-self.world_y))
        dist = math.sqrt(sight_vector[0]**2+sight_vector[1]**2)
        if dist >= Enemy.MAX_AI_DIST:
            x_velocity = 0
            y_velocity = 0

        # full AI is only run certain percentage of the time
        if random.random() >= (1-Enemy.AI_PERCENTAGE):
            # check if our direction is still ok
            if self.is_good_direction(self.x_velocity, self.y_velocity, map):
                return
            else:
                # try flipping
                if self.is_good_direction(self.x_velocity*-1, self.y_velocity*-1, map):
                    self.x_velocity *= -1
                    self.y_velocity *= -1
                    return
                # else set it to 0
                self.x_velocity = 0
                self.y_velocity = 0
                return

        # full AI here
    
        # get which x or y direction will bring closest to player
        if sight_vector[0] == 0:
            return
        sight_slope = sight_vector[1]/sight_vector[0]
        if math.fabs(sight_slope) >= 1:
            suggested_x = 0
            suggested_y =  math.copysign(Enemy.SPEED, sight_vector[1])
        else:
            suggested_x = math.copysign(Enemy.SPEED, sight_vector[0])
            suggested_y =  0

        # check if next tile in that direction is a wall
        if self.is_good_direction(suggested_x, suggested_y, map):
            self.x_velocity = suggested_x
            self.y_velocity = suggested_y
            return

        # check next best direction, swap x y values and copy their signs from original sight vector
        suggested_x, suggested_y = math.copysign(suggested_y, sight_vector[0]), math.copysign(suggested_x, sight_vector[1])
        if self.is_good_direction(suggested_x, suggested_y, map):
            self.x_velocity = suggested_x
            self.y_velocity = suggested_y
            return

        # else don't move
        self.x_velocity = 0
        self.y_velocity = 0
        

    def is_good_direction(self, x, y, map):
        width = Map.Map.TILE_WIDTH
        height = Map.Map.TILE_HEIGHT
        if x > 0:
            map_x = math.floor((self.world_x+width)/width)*width
            if self.world_y % height >= height/2:
                map_y_down = math.floor((self.world_y+height)/height)*height
                return self.check_valid_tile(map, (map_x, map_y_down))
            else:
                map_y_up = math.ceil((self.world_y-height)/height)*height
                return self.check_valid_tile(map, (map_x, map_y_up))
            
                
        elif x < 0:
            map_x = math.ceil((self.world_x-width)/width)*width
            if self.world_y % height >= height/2:
                map_y_down = math.floor((self.world_y+height)/height)*height
                return self.check_valid_tile(map, (map_x, map_y_down))
            else:
                map_y_up = math.ceil((self.world_y-height)/height)*height
                return self.check_valid_tile(map, (map_x, map_y_up))

        elif y > 0:
            map_y = math.floor((self.world_y+height)/height)*height
            if self.world_x % width >= width/2:
                map_x_right = math.floor((self.world_x+width)/width)*width
                return self.check_valid_tile(map, (map_x_right, map_y))
            else:    
                map_x_left = math.ceil((self.world_x-width)/width)*width
                return self.check_valid_tile(map, (map_x_left, map_y))

        elif y < 0:
            map_y = math.ceil((self.world_y-height)/height)*height
            if self.world_x % width >= width/2:
                map_x_right = math.floor((self.world_x+width)/width)*width
                return self.check_valid_tile(map, (map_x_right, map_y))
            else:    
                map_x_left = math.ceil((self.world_x-width)/width)*width
                return self.check_valid_tile(map, (map_x_left, map_y))

        return False


    def check_valid_tile(self, map, tile_key):
        if tile_key in map.tiles:
            tile = map.tiles[tile_key]
            if tile.is_wall() or tile.is_forward_wall():
                    return False
            else:
                return True
        else:
            return False

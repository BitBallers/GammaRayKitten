import pygame.sprite as PS
import maps.Camera as Camera
import maps.Map as Map
import Globals as G
import math
import random


class Enemy(PS.Sprite):

    MIN_SEPERATION_DIST = 25

    def __init__(self):
        PS.Sprite.__init__(self)
        self.wander_time = 0
        self.max_wander_time = 50

    def update(self, time, player, map, enemies_list, index):
        self.ai(player, map, enemies_list, index)
        self.world_x += self.x_velocity
        self.world_y += self.y_velocity        
        self.animate(time)
        self.last_x = self.world_x
        self.last_y = self.world_y
        self.rect.x = self.world_x - Camera.Camera.X
        self.rect.y = self.world_y - Camera.Camera.Y
        self.wander_time += time
        return (self.dead, None)

    def render(self):
        x = self.world_x - Camera.Camera.X
        y = self.world_y - Camera.Camera.Y
        if (x >= -self.rect.width and x <= G.Globals.WIDTH and
                y >= -self.rect.height and y <= G.Globals.HEIGHT):
            G.Globals.SCREEN.blit(self.image, (x, y))

    def ai(self, player, map, enemies_list, index):
        pass

    def is_good_direction(self, x, y, map, enemies_list, index):
        if x == 0 and y == 0:
            return False
        self.world_x += x+math.copysign(5, x)
        self.world_y += y+math.copysign(5, y)
        for k in range(index):
            if k >= len(enemies_list):
                break
            e = enemies_list[k]
            if e is self:                
                continue
            if (self.world_x-e.world_x)**2+(self.world_y-e.world_y)**2 < 25**2:                
                self.world_x -= x+math.copysign(5, x)
                self.world_y -= y+math.copysign(5, y)
                return False
        if self.in_wall(map):
            self.world_x -= x+math.copysign(5, x)
            self.world_y -= y+math.copysign(5, y)
            return False
        else:
            self.world_x -= x+math.copysign(5, x)
            self.world_y -= y+math.copysign(5, y)
            return True

    def check_valid_tile(self, map, tile_key):
        if tile_key in map.tiles:
            tile = map.tiles[tile_key]
            if tile.is_wall() or tile.is_forward_wall():
                return False
            else:
                return True
        else:
            return False

    def in_wall(self, map):
        top_left = (self.world_x, self.world_y)
        top_right = (self.world_x + self.rect.width, self.world_y)
        bottom_left = (self.world_x, self.world_y + self.rect.height)
        bottom_right = (
            self.world_x + self.rect.width, self.world_y + self.rect.height)

        tlx = math.floor(top_left[0]/50)*50
        tly = math.floor(top_left[1]/50)*50

        blx = math.floor(bottom_left[0]/50)*50
        bly = math.floor(bottom_left[1]/50)*50

        trx = math.floor(top_right[0]/50)*50
        try_ = math.floor(top_right[1]/50)*50

        brx = math.floor(bottom_right[0]/50)*50
        bry = math.floor(bottom_right[1]/50)*50

        if self.check_valid_tile(map, (tlx, tly)) is False:
            return True
        if self.check_valid_tile(map, (blx, bly)) is False:
            return True
        if self.check_valid_tile(map, (trx, try_)) is False:
            return True
        if self.check_valid_tile(map, (brx, bry)) is False:
            return True
        return False

    def move_out_of_wall(self, map):
        top_left = (self.world_x, self.world_y)
        top_right = (self.world_x + self.rect.width, self.world_y)
        bottom_left = (self.world_x, self.world_y + self.rect.height)
        bottom_right = (
            self.world_x + self.rect.width, self.world_y + self.rect.height)

        tlx = math.floor(top_left[0]/50)*50
        tly = math.floor(top_left[1]/50)*50

        blx = math.floor(bottom_left[0]/50)*50
        bly = math.floor(bottom_left[1]/50)*50

        trx = math.floor(top_right[0]/50)*50
        try_ = math.floor(top_right[1]/50)*50

        brx = math.floor(bottom_right[0]/50)*50
        bry = math.floor(bottom_right[1]/50)*50

        if self.check_valid_tile(map, (tlx, tly)) is True:
            self.world_x = tlx
            self.world_y = tly
            return

        if self.check_valid_tile(map, (blx, bly)) is True:
            self.world_x = blx
            self.world_y = bly
            return

        if self.check_valid_tile(map, (trx, try_)) is True:
            self.world_x = trx
            self.world_y = try_
            return

        if self.check_valid_tile(map, (brx, bry)) is True:
            self.world_x = brx
            self.world_y = bry
            return

    def move_back(self):
        self.world_x = self.last_x
        self.world_y = self.last_y
        self.x_velocity = 0
        self.y_velocity = 0
        self.rect.x = self.world_x - Camera.Camera.X
        self.rect.y = self.world_y - Camera.Camera.Y

    def random_velocity(self, speed):
        if random.random() <= .5:
            x = (-1) ** random.randint(1, 2)                    
            return (x*speed, 0)
        else:
            y = (-1) ** random.randint(1, 2)            
            return (0, y*speed)

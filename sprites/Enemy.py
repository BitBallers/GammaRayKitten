import pygame.sprite as PS
import maps.Camera as Camera
import maps.Map as Map
import Globals as G
import math

class Enemy(PS.Sprite):

    MIN_SEPERATION_DIST = 25

    def __init__(self):
        PS.Sprite.__init__(self)

    def update(self, time, player, map, enemies_list):
        self.ai(player, map, enemies_list)
        self.world_x += self.x_velocity
        self.world_y += self.y_velocity
        if self.in_wall(map):
            self.move_back()
        else:
            self.animate(time)

        self.last_x = self.world_x
        self.last_y = self.world_y
        self.rect.x = self.world_x - Camera.Camera.X
        self.rect.y = self.world_y - Camera.Camera.Y        
        return (self.dead, None)

    def render(self):
        x = self.world_x - Camera.Camera.X
        y = self.world_y - Camera.Camera.Y
        if x >= -self.rect.width and x <= G.Globals.WIDTH and y >= -self.rect.height and y <= G.Globals.HEIGHT:
            G.Globals.SCREEN.blit(self.image, (x, y))

    def ai(self, player, map, enemies_list):
        pass

    def is_good_direction(self, x, y, map, enemies_list):
        padding = 5
        # check other Slime coords
        for e in enemies_list:
            if e == self:
                continue
            coord = (e.world_x, e.world_y)
            new_x = self.world_x + x
            new_y = self.world_y + y
            if math.sqrt((new_x - coord[0]) ** 2 + (new_y - coord[1]) ** 2) <= Enemy.MIN_SEPERATION_DIST:
                return False

        width = Map.Map.TILE_WIDTH
        height = Map.Map.TILE_HEIGHT
        top_left = (self.world_x, self.world_y)
        top_right = (self.world_x + self.rect.width, self.world_y)
        bottom_left = (self.world_x, self.world_y + self.rect.height)
        bottom_right = (
            self.world_x + self.rect.width, self.world_y + self.rect.height)

        map_x_right = math.floor((self.world_x + width) / width) * width
        map_x_left = math.ceil((self.world_x - width) / width) * width
        map_y_down = math.floor((self.world_y + height) / height) * height
        map_y_up = math.ceil((self.world_y - height) / height) * height

        if x > 0:
            tly = math.ceil((top_left[1] - height) / height) * height
            bly = math.ceil((bottom_left[1] - height) / height) * height
            x = math.floor((top_left[0] + width) / width) * width
            return x - top_right[0] >= padding or (self.check_valid_tile(map, (x, tly)) and self.check_valid_tile(map, (x, bly)))

        elif x < 0:
            tly = math.ceil((top_left[1] - height) / height) * height
            bly = math.ceil((bottom_left[1] - height) / height) * height
            x = math.floor((top_left[0] - width) / width) * width
            return top_left[0] - (x + width) >= padding or (self.check_valid_tile(map, (x, tly)) and self.check_valid_tile(map, (x, bly)))

        elif y > 0:
            blx = math.ceil((bottom_left[0] - width) / width) * width
            brx = math.ceil((bottom_right[0] - width) / width) * width
            y = math.floor((top_left[1] + height) / height) * height
            return y - bottom_left[1] >= padding or (self.check_valid_tile(map, (blx, y)) and self.check_valid_tile(map, (brx, y)))
        
        elif y < 0:
            tlx = math.ceil((top_left[0] - width) / width) * width
            trx = math.ceil((top_right[0] - width) / width) * width
            y = math.floor((top_left[1] - height) / height) * height
            return top_left[1] - (y + width) >= padding or (self.check_valid_tile(map, (tlx, y)) and self.check_valid_tile(map, (trx, y)))

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

    def move_back(self):
        self.world_x = self.last_x
        self.world_y = self.last_y
        self.rect.x = self.world_x - Camera.Camera.X
        self.rect.y = self.world_y - Camera.Camera.Y          
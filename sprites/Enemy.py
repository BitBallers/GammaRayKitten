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
    CYCLE = 0.5
    MAX_AI_DIST = 700
    SPEED = 1.5
    AI_PERCENTAGE = .9
    MIN_SEPERATION_DIST = 50

    def __init__(self, (x, y)):
        PS.Sprite.__init__(self)

        if not Enemy.IMAGES:
            self.load_images()

        self.image = Enemy.IMAGES[8]
        self.b_index = 0
        self.rect = self.image.get_rect()
        self.world_x = x
        self.world_y = y

        self.x_velocity = 0
        self.y_velocity = 0

        self.time = 0.0

    def update(self, time, player, map, enemies_list):
        self.ai(player, map, enemies_list)
        self.world_x += self.x_velocity
        self.world_y += self.y_velocity
        self.rect.x = self.world_x-Camera.Camera.X
        self.rect.y = self.world_y-Camera.Camera.Y
        self.animate(time)

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
            for x in range(5):
                surface = PG.Surface((30, 20)).convert()
                surface.set_colorkey(key)
                surface.blit(sheet, (0, 0), (x*30, y*20, 30, 20))
                Enemy.IMAGES.append(surface)

    def animate(self, time):
        
        k = Enemy.CYCLE/5.0
        index = math.floor(self.time/k)
        index = int(index)

        update_image = False
        if self.y_velocity > 0:
            self.b_index = 10
            update_image = True
        elif self.y_velocity < 0:
            self.b_index = 15
            update_image = True
        if self.x_velocity > 0:
            self.b_index = 0
            update_image = True
        elif self.x_velocity < 0:
            self.b_index = 5
            update_image = True
        
        if update_image:
            self.image = Enemy.IMAGES[self.b_index+index]
        self.time += time
        if self.time >= Enemy.CYCLE:
            self.time = 0
        

    def ai(self, player, map, enemies_list):
        sight_vector = ((player.world_coord_x-self.world_x), (player.world_coord_y-self.world_y))
        dist = math.sqrt(sight_vector[0]**2+sight_vector[1]**2)
        if dist >= Enemy.MAX_AI_DIST:
            x_velocity = 0
            y_velocity = 0

        # full AI is only run certain percentage of the time
        if random.random() >= (1-Enemy.AI_PERCENTAGE):
            # check if our direction is still ok
            if self.is_good_direction(self.x_velocity, self.y_velocity, map, enemies_list):
                return
            else:
                # else set it to 0
                self.x_velocity = 0
                self.y_velocity = 0
                return

        # full AI here
    
        # get which x or y direction will bring closest to player
        # avoid division by zero
        if sight_vector[0] == 0:
            suggested_x = 0
            suggested_y =  math.copysign(Enemy.SPEED, sight_vector[1])

        else:
            sight_slope = sight_vector[1]/sight_vector[0]
            if math.fabs(sight_slope) >= 1:
                suggested_x = 0
                suggested_y =  math.copysign(Enemy.SPEED, sight_vector[1])
            else:
                suggested_x = math.copysign(Enemy.SPEED, sight_vector[0])
                suggested_y =  0

        
        # check if next tile in that direction is a wall
        if self.is_good_direction(suggested_x, suggested_y, map, enemies_list):
            self.x_velocity = suggested_x
            self.y_velocity = suggested_y
            return

        # check next best direction, swap x y values and copy their signs from original sight vector
        suggested_x, suggested_y = math.copysign(suggested_y, sight_vector[0]), math.copysign(suggested_x, sight_vector[1])
        if self.is_good_direction(suggested_x, suggested_y, map, enemies_list):
            self.x_velocity = suggested_x
            self.y_velocity = suggested_y
            return

        # else don't move
        self.x_velocity = 0
        self.y_velocity = 0
        

    def is_good_direction(self, x, y, map, enemies_list):
        # check other enemy coords
        for e in enemies_list:
            if e == self:
                continue
            coord = (e.world_x, e.world_y)
            new_x = self.world_x + x
            new_y = self.world_y + y
            if math.sqrt((new_x-coord[0])**2+(new_y-coord[1])**2) <= Enemy.MIN_SEPERATION_DIST:
                return False

        width = Map.Map.TILE_WIDTH
        height = Map.Map.TILE_HEIGHT
        map_x_right = math.floor((self.world_x+width)/width)*width
        map_x_left = math.ceil((self.world_x-width)/width)*width
        map_y_down = math.floor((self.world_y+height)/height)*height
        map_y_up = math.ceil((self.world_y-height)/height)*height

        if x > 0:
            return self.check_valid_tile(map, (map_x_right, map_y_down)) or self.check_valid_tile(map, (map_x_right, map_y_up))
                        
        elif x < 0:
            return self.check_valid_tile(map, (map_x_left, map_y_down)) or self.check_valid_tile(map, (map_x_left, map_y_up))

        elif y > 0:
            return self.check_valid_tile(map, (map_x_left, map_y_down)) or self.check_valid_tile(map, (map_x_right, map_y_down))

        elif y < 0:
            return self.check_valid_tile(map, (map_x_left, map_y_up)) or self.check_valid_tile(map, (map_x_right, map_y_up))

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

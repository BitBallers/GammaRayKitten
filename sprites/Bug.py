import pygame as PG
import pygame.image as PI
import pygame.sprite as PS
import Globals as G
import maps.Camera as Camera
import maps.Map as Map
import math
import random
import pygame.mixer as PM
import Enemy


class Bug(Enemy.Enemy):

    IMAGES = None
    CYCLE = 0.5
    MAX_AI_DIST = 500
    SPEED = 4
    AI_PERCENTAGE = .3
    SOUND = None

    def __init__(self, (x, y)):
        Enemy.Enemy.__init__(self)

        if Bug.SOUND is None:
            Bug.SOUND = PM.Sound("sounds/slime_death.wav")
        if not Bug.IMAGES:
            self.load_images()

        self.image = Bug.IMAGES[8]
        self.b_index = 0
        self.rect = self.image.get_rect()
        self.width = self.rect.width
        self.height = self.rect.height
        self.world_x = x
        self.world_y = y

        self.x_velocity = 0
        self.y_velocity = 0

        self.time = 0.0
        self.dying = False
        self.dead = False        

        self.last_x = self.world_x
        self.last_y = self.world_y

    def load_images(self):
        Bug.IMAGES = []
        sheet = PI.load(
            "sprites/images/insect_sprite_sheet.png").convert_alpha()
        key = sheet.get_at((0, 0))
        for y in range(4):
            for x in range(4):
                surface = PG.Surface((48, 44)).convert()
                surface.set_colorkey(key)
                surface.blit(sheet, (0, 0), (x * 48, y * 44, 48, 44))
                Bug.IMAGES.append(surface)

    def animate(self, time):
        k = Bug.CYCLE / 4.0
        index = math.floor(self.time / k)
        index = int(index)

        update_image = False
        if self.y_velocity > 0:
            self.b_index = 0
            update_image = True
        elif self.y_velocity < 0:
            self.b_index = 4
            update_image = True
        if self.x_velocity > 0:
            self.b_index = 12
            update_image = True
        elif self.x_velocity < 0:
            self.b_index = 8
            update_image = True

        
        self.image = Bug.IMAGES[self.b_index + index]

        if self.dying:
            if index == 3:
                self.dead = True

        self.time += time
        if self.time >= Bug.CYCLE:
            self.time = 0

    def ai(self, player, map, enemies_list):                      
        sight_vector = ((player.world_coord_x - self.world_x),
                        (player.world_coord_y - self.world_y))
        dist = math.sqrt(sight_vector[0] ** 2 + sight_vector[1] ** 2)
        
        if dist >= Bug.MAX_AI_DIST:
            x_velocity = 0
            y_velocity = 0
            return

        # full AI is only run certain percentage of the time
        if random.random() >= (Bug.AI_PERCENTAGE):
            # check if our direction is still ok
            if self.is_good_direction(self.x_velocity, self.y_velocity,
                                      map, enemies_list):
                return
            else:                
                k = 0
                while True:
                    x, y = self.random_velocity(Bug.SPEED)
                    if(self.is_good_direction(x, y, map, enemies_list)):
                        self.x_velocity = x
                        self.y_velocity = y
                        # self.wander_time = 0
                        return
                    k += 1
                    if(k > 300):
                        self.x_velocity = 0
                        self.y_velocity = 0
                        return

        # full AI here
        
        # get which x or y direction will bring closest to player
        # avoid division by zero
        if sight_vector[0] == 0:
            suggested_x = 0
            suggested_y = math.copysign(Bug.SPEED, sight_vector[1])

        else:
            sight_slope = sight_vector[1] / sight_vector[0]
            if math.fabs(sight_slope) >= 1:
                suggested_x = 0
                suggested_y = math.copysign(Bug.SPEED, sight_vector[1])
            else:
                suggested_x = math.copysign(Bug.SPEED, sight_vector[0])
                suggested_y = 0

        # check if next tile in that direction is a wall
        if self.is_good_direction(suggested_x, suggested_y, map, enemies_list):
            self.x_velocity = suggested_x
            self.y_velocity = suggested_y
            return

        # check next best direction, swap x y values and copy their signs from
        # original sight vector
        suggested_x = math.copysign(suggested_y, sight_vector[0])
        suggested_y = math.copysign(suggested_x, sight_vector[1])

        if self.is_good_direction(suggested_x, suggested_y, map, enemies_list):
            self.x_velocity = suggested_x
            self.y_velocity = suggested_y
            return        
        
        if self.wander_time >= self.max_wander_time:           
            k = 0
            while True:
                x, y = self.random_velocity(Bug.SPEED)
                if self.is_good_direction(x, y, map, enemies_list):
                    self.x_velocity = x
                    self.y_velocity = y
                    self.wander_time = 0                    
                    break
                k += 1
                if(k > 50):
                    self.x_velocity = 0
                    self.y_velocity = 0
                    break

    def check_valid_tile(self, map, tile_key):
        if tile_key in map.tiles:
            tile = map.tiles[tile_key]
            if tile.is_table():
                return True
            if tile.is_wall() or tile.is_forward_wall():
                return False
            else:
                return True
        else:
            return False        

    def start_death(self):
        Bug.SOUND.play()
        self.dead = True
        if self.b_index == 15:
            self.death_index = 4
        else:
            self.death_index = 0
        self.dying = True
        self.time = 0

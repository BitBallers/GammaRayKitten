import pygame as PG
import pygame.image as PI
import pygame.sprite as PS
import Globals as G
import maps.Camera as Camera
import maps.Map as Map
import math
import random
import pygame.mixer as PM
import Bullet as B



class Scientist(PS.Sprite):

    IMAGES = None
    SHOT_IMAGES = None
    CYCLE = 0.5
    MAX_AI_DIST = 700
    SHOT_DIST = 300
    SPEED = 1
    AI_PERCENTAGE = .3
    MIN_SEPERATION_DIST = 25
    SOUND = None
    WILHEM_SCREAM = None
    SHOT_TIME = 1.0
    B_SPEED = 5

    def __init__(self, (x, y)):
        PS.Sprite.__init__(self)

        if Scientist.SOUND is None:
            Scientist.SOUND = PM.Sound("sounds/scientist_death.wav")
        if Scientist.WILHEM_SCREAM is None:
            Scientist.WILHEM_SCREAM = PM.Sound("sounds/wilhelmscream.wav")
        if not Scientist.IMAGES:
            self.load_images()

        self.image = Scientist.IMAGES[8]
        self.b_index = 0
        self.rect = self.image.get_rect()
        self.width = self.rect.width
        self.height = self.rect.height
        self.world_x = x
        self.world_y = y

        self.x_velocity = 0
        self.y_velocity = 0

        self.time = 0.0
        self.cur_shot_time = 0
        self.dying = False
        self.dead = False
        self.shooting = False
        self.last_x = self.world_x
        self.last_y = self.world_y

    def update(self, time, player, map, enemies_list):
        self.cur_shot_time += time
        if self.cur_shot_time > Scientist.SHOT_TIME:
            self.cur_shot_time = Scientist.SHOT_TIME
            self.shooting = False
        b = self.ai(player, map, enemies_list)
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
        return (self.dead, b)

    def render(self):
        x = self.world_x - Camera.Camera.X
        y = self.world_y - Camera.Camera.Y
        if x >= -self.rect.width and x <= G.Globals.WIDTH and y >= -self.rect.height and y <= G.Globals.HEIGHT:
            G.Globals.SCREEN.blit(self.image, (x, y))

    def load_images(self):
        Scientist.IMAGES = []
        Scientist.SHOT_IMAGES = []
        sheet = PI.load(
            "sprites/images/scientist_sprite_sheet.png").convert_alpha()
        key = sheet.get_at((0, 0))
        for y in range(4):
            for x in range(4):
                surface = PG.Surface((25, 50)).convert()
                surface.set_colorkey(key)
                surface.blit(sheet, (0, 0), (x * 25, y * 50, 25, 50))
                Scientist.IMAGES.append(surface)

        Scientist.DEATH_IMAGES = []
        for y in range(4):
            surface = PG.Surface((25, 50)).convert()
            surface.set_colorkey(key)
            surface.blit(sheet, (0, 0), (100, y * 50, 25, 50))
            Scientist.SHOT_IMAGES.append(surface)

    def animate(self, time):
        k = Scientist.CYCLE / 4.0
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

        if update_image and not self.shooting:
            self.image = Scientist.IMAGES[self.b_index + index]

        self.time += time
        if self.time >= Scientist.CYCLE:
            self.time = 0

    def ai(self, player, map, enemies_list):
        #Don't do anything if shooting 
        if self.shooting:
            return None
        sight_vector = ((player.world_coord_x - self.world_x), 
                        (player.world_coord_y - self.world_y))
        dist = math.sqrt(sight_vector[0] ** 2 + sight_vector[1] ** 2)
        if dist >= Scientist.MAX_AI_DIST:
            x_velocity = 0
            y_velocity = 0
            return None
        #Shot AI
        if dist < Scientist.SHOT_DIST:
            #Can we shoot in the Y-DIR?
            if player.world_coord_x + 50 >= self.world_x \
             and player.world_coord_x - 50 <= self.world_x:
                self.shooting = True
                self.cur_shot_time = 0
                shot_speed = Scientist.B_SPEED
                self.x_velocity = 0
                self.y_velocity = 0
                if player.world_coord_y <= self.world_y:
                    shot_speed = shot_speed * (-1)
                    self.image = Scientist.SHOT_IMAGES[1]
                else:
                    self.image = Scientist.SHOT_IMAGES[0]
                return B.Bullet(self.world_x + 12, self.world_y + 25, 0,
                                shot_speed, Scientist.SHOT_DIST) 
            #Can we shoot in the X-DIR?
            if player.world_coord_y + 50 >= self.world_y \
             and player.world_coord_y - 50 <= self.world_y:
                self.shooting = True
                self.cur_shot_time = 0
                shot_speed = Scientist.B_SPEED
                self.x_velocity = 0
                self.y_velocity = 0
                if player.world_coord_x <= self.world_x:
                    shot_speed = shot_speed * (-1)
                    self.image = Scientist.SHOT_IMAGES[2]
                else:
                    self.image = Scientist.SHOT_IMAGES[3]
                return B.Bullet(self.world_x + 12, self.world_y + 25, 
                                shot_speed, 0, Scientist.SHOT_DIST)
            #Which way should we move then?
            '''dist_x = abs(self.world_x - player.world_coord_x)
            dist_y = abs(self.world_y - player.world_coord_y)
            if dist_x < dist_y:
                suggested_y = 0
                if player.world_coord_x < self.world_x:
                    suggested_x = Scientist.SPEED * (-1)
                else:
                    suggested_x = Scientist.SPEED
                if self.is_good_direction(suggested_x, suggested_y,
                                          map, enemies_list):
                    self.x_velocity = suggested_x
                    self.y_velocity = suggested_y
            else:
                suggested_x = 0
                if player.world_coord_y < self.world_y:
                    suggested_y = Scientist.SPEED * (-1)
                else:
                    suggested_y = Scientist.SPEED
                if self.is_good_direction(suggested_x, suggested_y,
                                          map, enemies_list):
                    self.x_velocity = suggested_x
                    self.y_velocity = suggested_y
            return None '''
        
        # full AI is only run certain percentage of the time
        if random.random() >= (Scientist.AI_PERCENTAGE):
            # check if our direction is still ok
            if self.is_good_direction(self.x_velocity, self.y_velocity, 
                                      map, enemies_list):
                return None
            else:
                # else set it to 0
                self.x_velocity = 0
                self.y_velocity = 0
                return None

        # full AI here

        # get which x or y direction will bring closest to player
        # avoid division by zero
        if sight_vector[0] == 0:
            suggested_x = 0
            suggested_y = math.copysign(Scientist.SPEED, sight_vector[1])

        else:
            sight_slope = sight_vector[1] / sight_vector[0]
            if math.fabs(sight_slope) >= 1:
                suggested_x = 0
                suggested_y = math.copysign(Scientist.SPEED, sight_vector[1])
            else:
                suggested_x = math.copysign(Scientist.SPEED, sight_vector[0])
                suggested_y = 0

        # check if next tile in that direction is a wall
        if self.is_good_direction(suggested_x, suggested_y, map, enemies_list):
            self.x_velocity = suggested_x
            self.y_velocity = suggested_y
            return None

        # check next best direction, swap x y values and copy their signs from
        # original sight vector
        suggested_x, suggested_y = math.copysign(suggested_y, sight_vector[0]), math.copysign(suggested_x, sight_vector[1])
        if self.is_good_direction(suggested_x, suggested_y, map, enemies_list):
            self.x_velocity = suggested_x
            self.y_velocity = suggested_y
            return None

        # else don't move
        self.x_velocity = 0
        self.y_velocity = 0

    def is_good_direction(self, x, y, map, enemies_list):
        padding = 5
        # check other enemy coords
        for e in enemies_list:
            if e == self:
                continue
            coord = (e.world_x, e.world_y)
            new_x = self.world_x + x
            new_y = self.world_y + y
            if math.sqrt((new_x - coord[0]) ** 2 + (new_y - coord[1]) ** 2) <= Scientist.MIN_SEPERATION_DIST:
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
            return x - top_right[0] >= padding or (self.check_valid_tile(map, (x, tly)) and self.check_valid_tile(map, (x, bly)))

        elif y > 0:
            blx = math.ceil((bottom_left[0] - width) / width) * width
            brx = math.ceil((bottom_right[0] - width) / width) * width
            y = math.floor((top_left[1] + height) / height) * height
            return y - bottom_left[1] >= padding or (self.check_valid_tile(map, (blx, y)) and self.check_valid_tile(map, (brx, y)))
        
        elif y < 0:
            tlx = math.ceil((top_left[0] - width) / width) * width
            trx = math.ceil((top_right[0] - width) / width) * width
            y = math.floor((top_left[1] - height) / height) * height
            return y - bottom_left[1] >= padding or (self.check_valid_tile(map, (tlx, y)) and self.check_valid_tile(map, (trx, y)))

        return False


    def start_death(self):
        if random.random() <= .95:
            Scientist.SOUND.play()
        else:
            Scientist.WILHEM_SCREAM.play()
        self.dead = True

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

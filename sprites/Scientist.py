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
import Enemy


class Scientist(Enemy.Enemy):

    IMAGES = None
    SHOT_IMAGES = None
    CYCLE = 0.5
    MAX_AI_DIST = 500
    SHOT_DIST = 300
    SPEED = 1
    AI_PERCENTAGE = .3
    SOUND = None
    WILHEM_SCREAM = None
    SHOT_TIME = 1.0
    B_SPEED = 5

    def __init__(self, (x, y)):
        Enemy.Enemy.__init__(self)

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

    def update(self, time, player, map, enemies_list, i):
        self.cur_shot_time += time
        if self.cur_shot_time > Scientist.SHOT_TIME:
            self.cur_shot_time = Scientist.SHOT_TIME
            self.shooting = False
        b = self.ai(player, map, enemies_list, i)
        self.animate(time)
        self.world_x += self.x_velocity
        self.world_y += self.y_velocity        
        self.last_x = self.world_x
        self.last_y = self.world_y
        self.rect.x = self.world_x - Camera.Camera.X
        self.rect.y = self.world_y - Camera.Camera.Y
        if self.in_wall(map) and (self.rect.x <= -2*self.rect.width or
                                  self.rect.x >= G.Globals.WIDTH+2*self.rect.width or
                                  self.rect.y <= -2*self.rect.height or
                                  self.rect.y >= G.Globals.HEIGHT+2*self.rect.height):
            self.move_out_of_wall(map)
        self.wander_time += time
        return (self.dead, b)

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
        else:
            self.image = Scientist.IMAGES[self.b_index]

        self.time += time
        if self.time >= Scientist.CYCLE:
            self.time = 0

    def ai(self, player, map, enemies_list, index):
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
                                shot_speed, Scientist.SHOT_DIST, False)
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
                                shot_speed, 0, Scientist.SHOT_DIST, False)
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
                                      map, enemies_list, index):
                return
            else:                
                k = 0
                while True:
                    x, y = self.random_velocity(Scientist.SPEED)
                    if(self.is_good_direction(x, y, map, enemies_list, index)):
                        self.x_velocity = x
                        self.y_velocity = y
                        # self.wander_time = 0
                        return
                    k += 1
                    if(k > 15):
                        self.x_velocity = 0
                        self.y_velocity = 0                        
                        return

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
        if self.is_good_direction(suggested_x, suggested_y, map, enemies_list, index):
            self.x_velocity = suggested_x
            self.y_velocity = suggested_y
            return

        # check next best direction, swap x y values and copy their signs from
        # original sight vector
        suggested_x = math.copysign(suggested_y, sight_vector[0])
        suggested_y = math.copysign(suggested_x, sight_vector[1])

        if self.is_good_direction(suggested_x, suggested_y, map, enemies_list, index):
            self.x_velocity = suggested_x
            self.y_velocity = suggested_y
            return

        if self.wander_time >= self.max_wander_time:           
            k = 0
            while True:
                x, y = self.random_velocity(Scientist.SPEED)
                if(self.is_good_direction(x, y, map, enemies_list, index)):
                    self.x_velocity = x
                    self.y_velocity = y
                    self.wander_time = 0                    
                    break
                k += 1
                if(k > 15):
                    self.x_velocity = 0
                    self.y_velocity = 0                    
                    break

    def start_death(self):
        if random.random() <= .95:
            Scientist.SOUND.play()
        else:
            Scientist.WILHEM_SCREAM.play()
        self.dead = True
        self.dying = True

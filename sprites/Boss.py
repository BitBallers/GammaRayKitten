import pygame as PG
import random
import pygame.image as PI
import pygame.sprite as PS
import Globals as G
import Enemy
import pygame.mixer as PM
import Bullet as B
import maps.Map as Map
import maps.Camera as Camera
import math


class Boss(Enemy.Enemy):


    WALKING_BODY_IMAGES = None
    RUNNING_BODY_IMAGES = None
    REG_HEAD_IMAGES = None
    ATTACKING_HEAD_IMAGES = None
    SOUND = None
    WIDTH = 40
    HEIGHT = 50
    ACTUAL_WIDTH = 30
    ACTUAL_HEIGHT = 43
    BODY_HEIGHT = 27
    HEAD_HEIGHT = 27
    CYCLE = .5
    H_CYCLE = .4
    SPEED_TIME = .4
    DMG_TIME = 1
    MAX_HEALTH = 5
    SHOT_SOUND = None

    def __init__(self, (x_cord, y_cord)):
        Enemy.Enemy.__init__(self)
           
        if Boss.WALKING_BODY_IMAGES is None:
            self.load_images()

        if Boss.SOUND is None:
            Boss.SOUND = PM.Sound("sounds/meow.wav")

        if Boss.SHOT_SOUND is None:
            Boss.SHOT_SOUND = PM.Sound("sounds/cat_shoot.wav")

        self.health = Boss.MAX_HEALTH
        self.max_health = Boss.MAX_HEALTH
        self.image = None
        self.body_image = Boss.WALKING_BODY_IMAGES[10]
        self.head_image = Boss.REG_HEAD_IMAGES[1]

        self.rect = PG.Rect(0, 0, Boss.WIDTH-10, Boss.HEIGHT-7)

        self.world_coord_x = x_cord
        self.world_coord_y = y_cord
        self.x_velocity = 0
        self.y_velocity = 0
        self.speed = 4          
        self.time = 0
                
        #The time (s) when you can fire
        self.fire_rate = 0.8
        #1 is up, 2 is down, 3 is right, 4 is left, 0 is not shooting
        self.shot_dir = 0
        #time value for shooting
        self.s_time = 0.0
        #shooting vars
        self.b_speed = 8
        self.b_distance = 300
        self.old_head = self.head_image
        self.d_time = self.DMG_TIME
        self.shot_type = 0
        self.piercing = False
        self.drunk = False
                 
        self.dont_render = False   
        self.dead = False  

    def render(self):
        if self.dont_render:
            return
        # surf = PG.Surface((self.rect.width, self.rect.height)).convert()
        # G.Globals.SCREEN.blit(surf, (self.rect.x, self.rect.y))
        x = self.world_coord_x - Camera.Camera.X
        y = self.world_coord_y - Camera.Camera.Y
        G.Globals.SCREEN.blit(self.body_image, (x-5,
                              y+Boss.HEAD_HEIGHT-4-3.5))
        G.Globals.SCREEN.blit(self.head_image, (x-5,
                              y-3.5))  

    def update(self, time, player, map, enemies_list, index):
        # update world coords
        self.world_coord_x += self.x_velocity
        self.world_coord_y += self.y_velocity

        # animations
        k = Boss.CYCLE/8.0
        index = math.floor(self.time/k)
        index = int(index)
        if self.y_velocity < 0:            
            self.body_image = Boss.RUNNING_BODY_IMAGES[index+8]
        if self.y_velocity > 0:            
            self.body_image = Boss.RUNNING_BODY_IMAGES[index]         
        if self.x_velocity < 0:            
            self.body_image = Boss.RUNNING_BODY_IMAGES[index+16]                        
        if self.x_velocity > 0:            
            self.body_image = Boss.RUNNING_BODY_IMAGES[index+24]                            
        self.set_head_image()
        self.time += time
        self.s_time += time
        self.d_time += time
        if self.time >= Boss.CYCLE:
            self.time = 0
        #make sure shot time doesn't get too big
        if self.s_time > self.fire_rate \
                and self.s_time > Boss.H_CYCLE + time:
            self.s_time = (self.fire_rate if self.fire_rate >
                           Boss.H_CYCLE + time else Boss.H_CYCLE + time)
        self.d_time = (self.d_time if self.d_time < Boss.DMG_TIME
                       else Boss.DMG_TIME)

        if self.d_time < Boss.DMG_TIME \
                and math.floor(self.d_time/.1) % 2 == 0:
            self.dont_render = True
        else:
            self.dont_render = False

        self.rect.x = self.world_coord_x - Camera.Camera.X
        self.rect.y = self.world_coord_y - Camera.Camera.Y
        self.wander_time += time
        return self.dead, None

    def set_head_image(self):
        k = Boss.H_CYCLE/3.0
        index = math.floor(self.s_time/k)
        index = int(index)
        #Store old head
        if self.shot_dir == 0:
            self.old_head = self.head_image
        if index >= 3:
            self.shot_dir = 0
            self.head_image = self.old_head
        if self.shot_dir != 0:
            if self.shot_dir == 1:
                self.head_image = Boss.ATTACKING_HEAD_IMAGES[0 + index]
            elif self.shot_dir == 2:
                self.head_image = Boss.ATTACKING_HEAD_IMAGES[3 + index]
            elif self.shot_dir == 3:
                self.head_image = Boss.ATTACKING_HEAD_IMAGES[9 + index]
            elif self.shot_dir == 4:
                self.head_image = Boss.ATTACKING_HEAD_IMAGES[6 + index]
        elif self.y_velocity > 0:
            self.head_image = Boss.REG_HEAD_IMAGES[1]            
        elif self.y_velocity < 0:
            self.head_image = Boss.REG_HEAD_IMAGES[0]            
        elif self.x_velocity < 0:
            self.head_image = Boss.REG_HEAD_IMAGES[2]            
        elif self.x_velocity > 0:
            self.head_image = Boss.REG_HEAD_IMAGES[3]            

    def take_damage(self, h_lost):
        if self.d_time >= Boss.DMG_TIME:
            Boss.SOUND.play()
            self.health = self.health - h_lost
            self.d_time = 0
            if self.health <= 0:
                return True
        return False

    def load_images(self):        
        sheet = PI.load("sprites/images/boss_sprite_sheet_body.png").convert()
        key = sheet.get_at((0, 0))

        Boss.WALKING_BODY_IMAGES = []
        for k in range(4):
            for i in range(8):
                surface = PG.Surface((Boss.WIDTH,
                                     Boss.BODY_HEIGHT)).convert()
                surface.set_colorkey(key)
                surface.blit(sheet, (0, 0), (i * Boss.WIDTH,
                             k*Boss.BODY_HEIGHT, Boss.WIDTH,
                             Boss.BODY_HEIGHT))
                Boss.WALKING_BODY_IMAGES.append(surface)

        Boss.RUNNING_BODY_IMAGES = []
        for k in range(4):
            for i in range(8):
                surface = PG.Surface((Boss.WIDTH,
                                     Boss.BODY_HEIGHT)).convert()
                surface.set_colorkey(key)
                surface.blit(sheet, (0, 0), (i*Boss.WIDTH,
                             4 * Boss.BODY_HEIGHT + k * Boss.BODY_HEIGHT,
                             Boss.WIDTH, Boss.BODY_HEIGHT))
                Boss.RUNNING_BODY_IMAGES.append(surface)

        sheet = PI.load("sprites/images/boss_sprite_sheet_head.png").convert()
        key = sheet.get_at((0, 0))

        Boss.REG_HEAD_IMAGES = []
        for k in range(4):
            surface = PG.Surface((Boss.WIDTH, Boss.HEAD_HEIGHT)).convert()
            surface.set_colorkey(key)
            surface.blit(sheet, (0, 0), (0, k*Boss.HEAD_HEIGHT, Boss.WIDTH,
                         Boss.HEAD_HEIGHT))
            Boss.REG_HEAD_IMAGES.append(surface)

        Boss.ATTACKING_HEAD_IMAGES = []
        for k in range(4):
            for i in range(3):
                surface = PG.Surface((Boss.WIDTH,
                                     Boss.HEAD_HEIGHT)).convert()
                surface.set_colorkey(key)
                surface.blit(sheet, (0, 0), (Boss.WIDTH+i*Boss.WIDTH,
                             k*Boss.HEAD_HEIGHT, Boss.WIDTH,
                             Boss.HEAD_HEIGHT))
                Boss.ATTACKING_HEAD_IMAGES.append(surface)

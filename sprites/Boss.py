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
import pygame.transform as PT


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
        self.width = Boss.WIDTH
        self.height = Boss.HEIGHT
        self.world_x = x_cord
        self.world_y = y_cord
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
        self.dying = False
                 
        self.dont_render = False   
        self.dead = False
        self.move_targets = []
        self.closest_target = None 
        self.re_target = None
        self.jump = False
        self.jumpx = False
        self.jumpy = False
        self.jump_scale = 1
        self.target_index = 0 
        self.re_dir = False
        self.re_dir_target = None

    def render(self):
        if self.dont_render:
            return
        # surf = PG.Surface((self.rect.width, self.rect.height)).convert()
        # G.Globals.SCREEN.blit(surf, (self.rect.x, self.rect.y))
        x = self.world_x - Camera.Camera.X
        y = self.world_y - Camera.Camera.Y
        if self.jump is True:
            b_width = int(self.body_image.get_width()*self.jump_scale)
            b_height = int(self.body_image.get_height()*self.jump_scale)
            h_width = int(self.head_image.get_width()*self.jump_scale)
            h_height = int(self.head_image.get_height()*self.jump_scale)
            b = PT.scale(self.body_image, (b_width, b_height))
            h = PT.scale(self.head_image, (h_width, h_height))
            s = self.jump_scale
            """G.Globals.SCREEN.blit(b, int((s*(x-5)), int(s*(y+Boss.HEAD_HEIGHT-4-3.5))))
            G.Globals.SCREEN.blit(h, int((s*(x-5)), int(s*(y-3.5))))"""
            G.Globals.SCREEN.blit(b, (x-5, y+Boss.HEAD_HEIGHT-4-3.5))
            G.Globals.SCREEN.blit(h, (x-5, y-3.5-int((1-self.jump_scale)*5)))
            return
        G.Globals.SCREEN.blit(self.body_image, (x-5,
                              y+Boss.HEAD_HEIGHT-4-3.5))
        G.Globals.SCREEN.blit(self.head_image, (x-5,
                              y-3.5))  

    def update(self, time, player, map, enemies_list, index):
        bullet = self.ai(time, player, map)
        
        # update world coords
        self.world_x += self.x_velocity
        self.world_y += self.y_velocity

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
        self.d_time = (self.d_time if self.d_time < Boss.DMG_TIME
                       else Boss.DMG_TIME)

        if self.d_time < Boss.DMG_TIME \
                and math.floor(self.d_time/.1) % 2 == 0:
            self.dont_render = True
        else:
            self.dont_render = False

        self.rect.x = self.world_x - Camera.Camera.X
        self.rect.y = self.world_y - Camera.Camera.Y
        self.wander_time += time
        return self.dead, bullet

    def ai(self, time, player, map):
        bull = None
        x = self.world_x
        y = self.world_y
        # jumpx frames = 20
        # jumpy frames = 10
        if self.jump is True:
            f = self.jump_frame
            if self.jumpx is True:
                self.jump_scale = 1 + -f*(f-45)*.00125
                self.jump_frame += 1
                if self.jump_frame == 40:
                    self.jump = False
            else:
                self.jump_scale = 1 + -f*(f-35)*.00125
                self.jump_frame += 1
                if self.jump_frame == 30:
                    self.jump = False

        
        if len(self.move_targets) is 0:
            valid = False
            while valid is False:
                self.move_targets = []
                x_wall_dist = random.randint(50, 300)
                y_wall_dist = random.randint(50, 200)
                self.move_targets.append((100+x_wall_dist, 100+y_wall_dist))
                self.move_targets.append((map.WIDTH-50-x_wall_dist, 100+y_wall_dist))
                self.move_targets.append((map.WIDTH-50-x_wall_dist, map.HEIGHT-50-y_wall_dist))
                self.move_targets.append((100+x_wall_dist, map.HEIGHT-50-y_wall_dist))
                valid = True
                for t in self.move_targets:
                    if self.in_wall_xy(t, map):
                        valid = False
        if len(self.move_targets) > 0:
            if self.closest_target is None:
                min_dist = 99999999999
                for target in self.move_targets:
                    dist_sq = (x-target[0])**2+(y-target[1])**2
                    if dist_sq < min_dist:
                        min_dist = dist_sq
                        self.closest_target = target
            if abs(self.closest_target[0]-x) <= 5 or abs(self.closest_target[1]-y) <= 5:
                if abs(self.closest_target[0]-x) <= 5 and abs(self.closest_target[1]-y) <= 5:
                    if self.closest_target == self.re_dir_target:
                        self.re_dir_target = None
                        self.re_dir = False
                    self.move_targets.remove(self.closest_target)
                    self.closest_target = None
                elif abs(self.closest_target[0]-x) <= 5:
                    self.y_velocity = math.copysign(self.speed, self.closest_target[1]-y)
                    self.x_velocity = 0
                else:
                    self.x_velocity = math.copysign(self.speed, self.closest_target[0]-x)
                    self.y_velocity = 0
            elif abs(self.closest_target[0]-x) < abs(self.closest_target[1]-y):
                self.x_velocity = math.copysign(self.speed, self.closest_target[0]-self.world_x)
                self.y_velocity = 0
            else:
                self.y_velocity = math.copysign(self.speed, self.closest_target[1]-self.world_y)
                self.x_velocity = 0

        """if self.is_good_direction(self.x_velocity, self.y_velocity, map) is False and self.jump is False:
            self.jump = True
            self.jump_frame = 0
            if self.x_velocity != 0:
                self.jumpx = True
                self.jumpy = False
            else:
                self.jumpx = False
                self.jumpy = True"""
        if self.in_wall(map) and self.re_dir is False:
            if self.y_velocity == 0:
                if self.world_y <= map.HEIGHT/2:
                    new_targ = (self.world_x, random.randint(200, 300))
                else:
                    new_targ = (self.world_x, map.HEIGHT-random.randint(200, 300))
            else:
                if self.world_x <= map.WIDTH/2:
                    new_targ = (random.randint(100, 200), self.world_y)
                else:
                    new_targ = (map.WIDTH-random.randint(100, 200), self.world_y)
            self.move_targets.append(new_targ)
            self.re_dir = True
            self.re_dir_target = new_targ
            if self.closest_target is not None:
                self.move_targets.remove(self.closest_target)
            self.closest_target = new_targ
        if self.s_time >= self.fire_rate:
            bull = self.shoot(self.determine_shot(player))
        return bull

    def is_good_direction(self, x, y, map, enemies_list=[], index=0):
        self.world_x += x*3
        self.world_y += y*3
        if self.in_wall(map):
            self.world_x -= x*3
            self.world_y -= y*3
            return False
        else:
            self.world_x -= x*3
            self.world_y -= y*3
            return True

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

    def in_wall_xy(self, (x, y), map):
        top_left = (x, y)
        top_right = (x + self.rect.width, y)
        bottom_left = (x, y + self.rect.height)
        bottom_right = (
            x + self.rect.width, y + self.rect.height)

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


    def shoot(self, direction):
        adj_old = math.cos(math.pi/12)*self.b_speed
        adj_new = math.sin(math.pi/12)*self.b_speed
        bull = []
        self.s_time = 0.0
        bull.append(B.Bullet(self.world_x + Boss.WIDTH/2
                    - B.Bullet.WIDTH, self.world_y, direction[0]*self.b_speed,
                    direction[1]*self.b_speed, self.b_distance, True))
        if direction[0] == 0:
            bull.append(B.Bullet(self.world_x +
                    Boss.WIDTH/2 - B.Bullet.WIDTH,
                    self.world_y, adj_new, adj_old*direction[1],
                    self.b_distance, False))
            bull.append(B.Bullet(self.world_x +
                    Boss.WIDTH/2 - B.Bullet.WIDTH,
                    self.world_y, -adj_new, adj_old*direction[1],
                    self.b_distance, False))
            if direction[1] == -1:
                self.shot_dir = 1
            else:
                self.shot_dir = 2
        else:
            bull.append(B.Bullet(self.world_x +
                    Boss.WIDTH/2 - B.Bullet.WIDTH,
                    self.world_y, adj_old*direction[0], adj_new,
                    self.b_distance, False))
            bull.append(B.Bullet(self.world_x +
                    Boss.WIDTH/2 - B.Bullet.WIDTH,
                    self.world_y, adj_old*direction[0], -adj_new,
                    self.b_distance, False))
            if direction[0] == 1:
                self.shot_dir = 3
            else:
                self.shot_dir = 4
        return bull


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

    def start_death(self):
        if self.d_time >= Boss.DMG_TIME:
            G.Globals.FX_CHANNEL.play(Boss.SOUND)
            self.health = self.health - 1
            self.d_time = 0
            if self.health <= 0:
                self.dead = True
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

    def determine_shot(self, player):
        shots = [(self.world_x, self.world_y-self.b_distance),
                 (self.world_x, self.world_y+self.b_distance),
                 (self.world_x-self.b_distance, self.world_y),
                 (self.world_x+self.b_distance, self.world_y)]
        closest = min(shots, key = lambda x: (x[0]-player.world_coord_x)**2+(x[1]-player.world_coord_y)**2)
        return (int((closest[0]-self.world_x)/self.b_distance), int((closest[1]-self.world_y)/self.b_distance))


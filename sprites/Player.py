import pygame as PG
import sys as SYS
import random as R
import pygame.image as PI
import pygame.display as PDI
import pygame.event as PE
import pygame.sprite as PS
import pygame.mixer as PM
import math
import Globals as G
import Tile
import maps.Camera as Camera
import maps.Map as Map
import Bullet as B
import math as m


class Player(PS.Sprite):

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
    SCROLL_RIGHT_BOUND = 600
    SCROLL_LEFT_BOUND = 200
    SCROLL_UPPER_BOUND = 200
    SCROLL_LOWER_BOUND = 400
    SPRITE_IMAGE_KEY = None
    MAX_HEALTH = 5
    MOVE_KEYS = [PG.K_w, PG.K_a, PG.K_s, PG.K_d]
    SHOT_KEYS = [PG.K_UP, PG.K_DOWN, PG.K_RIGHT, PG.K_LEFT]
    SYRINGE_IMAGE = None
    SHAMPOO_IMAGE = None
    PILL_IMAGE = None
    GLOW = None
    SHOT_SOUND = None

    def __init__(self, x_cord, y_cord, cam):
        PS.Sprite.__init__(self)

        if Player.WALKING_BODY_IMAGES is None:
            self.load_images()

        if Player.SOUND is None:
            Player.SOUND = PM.Sound("sounds/meow.wav")

        if Player.SHOT_SOUND is None:
            Player.SHOT_SOUND = PM.Sound("sounds/cat_shoot.wav")

        self.health = Player.MAX_HEALTH
        self.max_health = Player.MAX_HEALTH
        self.image = None
        self.body_image = Player.WALKING_BODY_IMAGES[10]
        self.head_image = Player.REG_HEAD_IMAGES[1]

        self.rect = PG.Rect(0, 0, Player.WIDTH-10, Player.HEIGHT-7)

        self.world_coord_x = x_cord
        self.world_coord_y = y_cord
        self.x_velocity = 0
        self.y_velocity = 0
        self.speed = 5
        self.accel = (G.Globals.INTERVAL/Player.SPEED_TIME) * self.speed
        #This is the list of keys that
        #are currently pressed
        self.key = []
        self.time = 0
        self.camera = cam
        self.keys = 0
        #The time (s) when you can fire
        self.fire_rate = 1.0
        #1 is up, 2 is down, 3 is right, 4 is left, 0 is not shooting
        self.shot_dir = 0
        #time value for shooting
        self.s_time = 0.0
        #shooting vars
        self.b_speed = 10
        self.b_distance = 300
        self.old_head = self.head_image
        self.d_time = self.DMG_TIME
        self.shot_type = 0
        self.piercing = False

        self.items = []
        self.dont_render = False

    def handle_events(self, event):
        bull = []
        adj_old = m.cos(m.pi/12)*self.b_speed
        adj_new = m.sin(m.pi/12)*self.b_speed
        if event.type == PG.KEYDOWN:
            if event.key == PG.K_UP:
                if self.s_time >= self.fire_rate:
                    Player.SHOT_SOUND.play()
                    self.shot_dir = 1
                    self.s_time = 0.0
                    bull.append(B.Bullet(self.world_coord_x + Player.WIDTH/2
                                - B.Bullet.WIDTH, self.world_coord_y, 0,
                                - self.b_speed, self.b_distance))
                    if self.shot_type == 1:
                        bull.append(B.Bullet(self.world_coord_x +
                                    Player.WIDTH/2 - B.Bullet.WIDTH,
                                    self.world_coord_y, adj_new, -adj_old,
                                    self.b_distance))
                        bull.append(B.Bullet(self.world_coord_x +
                                    Player.WIDTH/2 - B.Bullet.WIDTH,
                                    self.world_coord_y, -adj_new, -adj_old,
                                    self.b_distance))

            elif event.key == PG.K_DOWN:
                if self.s_time >= self.fire_rate:
                    Player.SHOT_SOUND.play()
                    self.shot_dir = 2
                    self.s_time = 0.0
                    bull.append(B.Bullet(self.world_coord_x + Player.WIDTH/2
                                - B.Bullet.WIDTH, self.world_coord_y +
                                Player.HEAD_HEIGHT, 0, self.b_speed,
                                self.b_distance))
                    if self.shot_type == 1:
                        bull.append(B.Bullet(self.world_coord_x +
                                    Player.WIDTH/2 - B.Bullet.WIDTH,
                                    self.world_coord_y + Player.HEAD_HEIGHT,
                                    adj_new, adj_old, self.b_distance))
                        bull.append(B.Bullet(self.world_coord_x +
                                    Player.WIDTH/2 - B.Bullet.WIDTH,
                                    self.world_coord_y + Player.HEAD_HEIGHT,
                                    -adj_new, adj_old, self.b_distance))

            elif event.key == PG.K_RIGHT:
                if self.s_time >= self.fire_rate:
                    Player.SHOT_SOUND.play()
                    self.shot_dir = 3
                    self.s_time = 0.0
                    bull.append(B.Bullet(self.world_coord_x + Player.WIDTH,
                                self.world_coord_y + Player.HEAD_HEIGHT -
                                B.Bullet.HEIGHT, self.b_speed, 0,
                                self.b_distance))
                    if self.shot_type == 1:
                        bull.append(B.Bullet(self.world_coord_x + Player.WIDTH,
                                    self.world_coord_y + Player.HEAD_HEIGHT
                                    - B.Bullet.HEIGHT, adj_old, -adj_new,
                                    self.b_distance))
                        bull.append(B.Bullet(self.world_coord_x + Player.WIDTH,
                                    self.world_coord_y + Player.HEAD_HEIGHT -
                                    B.Bullet.HEIGHT, adj_old, adj_new,
                                    self.b_distance))

            elif event.key == PG.K_LEFT:
                if self.s_time >= self.fire_rate:
                    Player.SHOT_SOUND.play()
                    self.shot_dir = 4
                    self.s_time = 0.0
                    bull.append(B.Bullet(self.world_coord_x, self.world_coord_y
                                + Player.HEAD_HEIGHT - B.Bullet.HEIGHT,
                                -self.b_speed, 0, self.b_distance))
                    if self.shot_type == 1:
                        bull.append(B.Bullet(self.world_coord_x,
                                    self.world_coord_y + Player.HEAD_HEIGHT
                                    - B.Bullet.HEIGHT, -adj_old, adj_new,
                                    self.b_distance))
                        bull.append(B.Bullet(self.world_coord_x,
                                    self.world_coord_y + Player.HEAD_HEIGHT
                                    - B.Bullet.HEIGHT, -adj_old, -adj_new,
                                    self.b_distance))
            #Adding the new key press to the end of
            #the array
            elif event.key in Player.MOVE_KEYS:
                self.key.append(event.key)
                self.time = 0

        elif event.type == PG.KEYUP:
            #Remove the key from the array if
            #it is there
            if event.key in self.key:
                self.key.remove(event.key)
        return bull

    def set_screen_coords(self, x, y):
        self.rect.x = x
        self.rect.y = y

    def set_bottom_left(self):
        self.world_coord_x = 500
        self.world_coord_y = Map.Map.HEIGHT - 300

    def set_head_image(self):
        k = Player.H_CYCLE/3.0
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
                self.head_image = Player.ATTACKING_HEAD_IMAGES[0 + index]
            elif self.shot_dir == 2:
                self.head_image = Player.ATTACKING_HEAD_IMAGES[3 + index]
            elif self.shot_dir == 3:
                self.head_image = Player.ATTACKING_HEAD_IMAGES[9 + index]
            elif self.shot_dir == 4:
                self.head_image = Player.ATTACKING_HEAD_IMAGES[6 + index]
        elif self.y_velocity > 0:
            self.head_image = Player.REG_HEAD_IMAGES[1]
        elif self.y_velocity < 0:
            self.head_image = Player.REG_HEAD_IMAGES[0]
        elif self.x_velocity < 0:
            self.head_image = Player.REG_HEAD_IMAGES[2]
        elif self.x_velocity > 0:
            self.head_image = Player.REG_HEAD_IMAGES[3]

    def render(self):
        if self.dont_render:
            return
        # surf = PG.Surface((self.rect.width, self.rect.height)).convert()
        # G.Globals.SCREEN.blit(surf, (self.rect.x, self.rect.y))
        G.Globals.SCREEN.blit(self.body_image, (self.rect.x-5,
                              self.rect.y+Player.HEAD_HEIGHT-4-3.5))
        G.Globals.SCREEN.blit(self.head_image, (self.rect.x-5,
                              self.rect.y-3.5))

    # takes in the fixed time interval, dt
    def update(self, time):
        #update velocities if a key is currently held down
        if len(self.key) > 0:
            if self.key[-1] == PG.K_w:
                #turn on a dime!
                if self.x_velocity != 0:
                    self.y_velocity = -abs(self.x_velocity)
                self.y_velocity -= self.accel
                #Make sure they don't go too fast
                if self.y_velocity < -self.speed:
                    self.y_velocity = -self.speed
                #To avoid drift
                self.x_velocity = 0
            elif self.key[-1] == PG.K_s:
                #turn on a dime!
                if self.x_velocity != 0:
                    self.y_velocity = abs(self.x_velocity)
                self.y_velocity += self.accel
                if self.y_velocity > self.speed:
                    self.y_velocity = self.speed
                self.x_velocity = 0
            elif self.key[-1] == PG.K_d:
                #turn on a dime!
                if self.y_velocity != 0:
                    self.x_velocity = abs(self.y_velocity)
                self.x_velocity += self.accel
                if self.x_velocity > self.speed:
                    self.x_velocity = self.speed
                self.y_velocity = 0
            elif self.key[-1] == PG.K_a:
                #turn on a dime!
                if self.y_velocity != 0:
                    self.x_velocity = -abs(self.y_velocity)
                self.x_velocity -= self.accel
                if self.x_velocity < -self.speed:
                    self.x_velocity = -self.speed
                self.y_velocity = 0

        #No keys are held down---slow down
        else:
            if self.y_velocity > 0:
                self.y_velocity -= self.accel
                if self.y_velocity < 0:
                    self.y_velocity = 0
                    self.body_image = Player.WALKING_BODY_IMAGES[2]
            elif self.y_velocity < 0:
                self.y_velocity += self.accel
                if self.y_velocity > 0:
                    self.y_velocity = 0
                    self.body_image = Player.WALKING_BODY_IMAGES[2+8]
            if self.x_velocity > 0:
                self.x_velocity -= self.accel
                if self.x_velocity < 0:
                    self.x_velocity = 0
                    self.body_image = Player.WALKING_BODY_IMAGES[2+24]
            elif self.x_velocity < 0:
                self.x_velocity += self.accel
                if self.x_velocity > 0:
                    self.x_velocity = 0
                    self.body_image = Player.WALKING_BODY_IMAGES[2+16]

        # update world coords
        self.world_coord_x += self.x_velocity
        self.world_coord_y += self.y_velocity

        # check collisions with scrolling boundary
        if self.rect.x > Player.SCROLL_RIGHT_BOUND - self.rect.width and\
           self.x_velocity > 0 and\
           self.world_coord_x < Map.Map.WIDTH-Player.SCROLL_LEFT_BOUND:
            self.camera.shift_camera(self.x_velocity, 0)

        if self.rect.x < Player.SCROLL_LEFT_BOUND and\
           self.x_velocity < 0 and\
           self.world_coord_x > Player.SCROLL_LEFT_BOUND:
            self.camera.shift_camera(self.x_velocity, 0)

        if self.rect.y > (Player.SCROLL_LOWER_BOUND - self.rect.height) and\
           self.y_velocity > 0 and\
           self.world_coord_y < Map.Map.HEIGHT-Player.SCROLL_UPPER_BOUND:
            self.camera.shift_camera(0, self.y_velocity)

        if self.rect.y < Player.SCROLL_UPPER_BOUND and\
           self.y_velocity < 0 and\
           self.world_coord_y > Player.SCROLL_UPPER_BOUND:
            self.camera.shift_camera(0, self.y_velocity)

        # animations
        k = Player.CYCLE/8.0
        index = math.floor(self.time/k)
        index = int(index)
        if self.y_velocity < 0:
            if self.y_velocity == -self.speed:
                self.body_image = Player.RUNNING_BODY_IMAGES[index+8]
            else:
                self.body_image = Player.WALKING_BODY_IMAGES[index+8]
        if self.y_velocity > 0:
            if self.y_velocity == self.speed:
                self.body_image = Player.RUNNING_BODY_IMAGES[index]
            else:
                self.body_image = Player.WALKING_BODY_IMAGES[index]
        if self.x_velocity < 0:
            if self.x_velocity == -self.speed:
                self.body_image = Player.RUNNING_BODY_IMAGES[index+16]
            else:
                self.body_image = Player.WALKING_BODY_IMAGES[index+16]
        if self.x_velocity > 0:
            if self.x_velocity == self.speed:
                self.body_image = Player.RUNNING_BODY_IMAGES[index+24]
            else:
                self.body_image = Player.WALKING_BODY_IMAGES[index+24]
        self.set_head_image()
        self.time += time
        self.s_time += time
        self.d_time += time
        if self.time >= Player.CYCLE:
            self.time = 0
        #make sure shot time doesn't get too big
        if self.s_time > self.fire_rate \
                and self.s_time > Player.H_CYCLE + time:
            self.s_time = (self.fire_rate if self.fire_rate >
                           Player.H_CYCLE + time else Player.H_CYCLE + time)
        self.d_time = (self.d_time if self.d_time < Player.DMG_TIME
                       else Player.DMG_TIME)
        if self.d_time < Player.DMG_TIME \
                and math.floor(self.d_time/.1) % 2 == 0:
            self.dont_render = True
        else:
            self.dont_render = False

    def wall_collision(self, tile, map):
        val = 0
        #picking up a key
        if tile.is_key():
            self.keys = self.keys + 1
            tile.change_image(6)
            val = 1
        #picking up item
        elif tile.is_item():
            # syringe
            if tile.type == 12:
                self.shot_type = 1
                if 0 not in self.items:
                    self.items.append(0)
            # shampoo
            elif tile.type == 13:
                self.fire_rate = .5
                if 1 not in self.items:
                    self.items.append(1)
            # pill
            elif tile.type == 14:
                self.piercing = True
                if 2 not in self.items:
                    self.items.append(2)
            # sheild
            elif tile.type == 15:
                self.max_health = self.max_health + 1
                self.health = self.max_health
                if 3 not in self.items:
                    self.items.append(3)
            tile.change_image(6)
            val = 1
        #opening a door
        elif tile.is_door() and self.keys > 0:

            self.keys = self.keys - 1
            tile.change_image(6)
            val = 1
        #GAMEOVER
        elif tile.is_stairs():
            val = 2
        #In Case removing from wall list is slow
        elif not tile.is_wall() and not tile.is_door():
            val = 0
        #regular wall stuff
        elif self.x_velocity > 0:
            if tile.partial and self.world_coord_y >= tile.world_y:
                self.world_coord_y = tile.world_y+tile.rect.height
            elif tile.world_y - self.world_coord_y >= self.rect.height-15 \
                    and not map.tiles[(tile.world_x,
                                      tile.world_y-50)].is_wall():
                self.world_coord_y = tile.world_y-self.rect.height
            else:
                self.x_velocity = 0
                self.world_coord_x = tile.world_x - Player.ACTUAL_WIDTH
        elif self.x_velocity < 0:
            if tile.partial and self.world_coord_y >= tile.world_y:
                self.world_coord_y = tile.world_y+tile.rect.height
            elif tile.world_y - self.world_coord_y >= self.rect.height-15 \
                    and not map.tiles[(tile.world_x,
                                      tile.world_y-50)].is_wall():
                self.world_coord_y = tile.world_y-self.rect.height
            else:
                self.x_velocity = 0
                self.world_coord_x = tile.world_x + Tile.Tile.WIDTH
        elif self.y_velocity > 0:
            if tile.world_x + Tile.Tile.WIDTH - self.world_coord_x <= 15 \
                    and not map.tiles[(tile.world_x+50,
                                      tile.world_y)].is_wall():
                self.world_coord_x = tile.world_x + Tile.Tile.WIDTH
            elif tile.world_x - self.world_coord_x >= self.rect.width-15 \
                    and not map.tiles[(tile.world_x-50,
                                      tile.world_y)].is_wall():
                self.world_coord_x = tile.world_x - self.rect.width
            else:
                self.y_velocity = 0
                self.world_coord_y = tile.world_y - Player.ACTUAL_HEIGHT
        elif self.y_velocity < 0:
            if tile.world_x + tile.rect.width - self.world_coord_x <= 15 \
                    and not map.tiles[(tile.world_x+50,
                                      tile.world_y)].partial:
                self.world_coord_x = tile.world_x + Tile.Tile.WIDTH
            elif tile.world_x - self.world_coord_x >= self.rect.width-15 \
                    and not map.tiles[(tile.world_x-50,
                                      tile.world_y)].partial:
                self.world_coord_x = tile.world_x - self.rect.width
            else:
                self.y_velocity = 0
                self.world_coord_y = tile.world_y + tile.rect.height
        return val

    def take_damage(self, h_lost):
        if self.d_time >= Player.DMG_TIME:
            Player.SOUND.play()
            self.health = self.health - h_lost
            self.d_time = 0
            if self.health <= 0:
                return True
        return False

    def load_images(self):
        sheet = PI.load("sprites/images/cat_glow.png").convert()
        surface = PG.Surface((40, 50)).convert()
        surface.blit(sheet, (0, 0), (0, 0, 40, 50))
        Player.GLOW = surface
        sheet = PI.load("sprites/images/cat_sprite_sheet_body.png").convert()
        key = sheet.get_at((0, 0))

        Player.WALKING_BODY_IMAGES = []
        for k in range(4):
            for i in range(8):
                surface = PG.Surface((Player.WIDTH,
                                     Player.BODY_HEIGHT)).convert()
                surface.set_colorkey(key)
                surface.blit(sheet, (0, 0), (i * Player.WIDTH,
                             k*Player.BODY_HEIGHT, Player.WIDTH,
                             Player.BODY_HEIGHT))
                Player.WALKING_BODY_IMAGES.append(surface)

        Player.RUNNING_BODY_IMAGES = []
        for k in range(4):
            for i in range(8):
                surface = PG.Surface((Player.WIDTH,
                                     Player.BODY_HEIGHT)).convert()
                surface.set_colorkey(key)
                surface.blit(sheet, (0, 0), (i*Player.WIDTH,
                             4 * Player.BODY_HEIGHT + k * Player.BODY_HEIGHT,
                             Player.WIDTH, Player.BODY_HEIGHT))
                Player.RUNNING_BODY_IMAGES.append(surface)

        sheet = PI.load("sprites/images/cat_sprite_sheet_head.png").convert()
        key = sheet.get_at((0, 0))

        Player.REG_HEAD_IMAGES = []
        for k in range(4):
            surface = PG.Surface((Player.WIDTH, Player.HEAD_HEIGHT)).convert()
            surface.set_colorkey(key)
            surface.blit(sheet, (0, 0), (0, k*Player.HEAD_HEIGHT, Player.WIDTH,
                         Player.HEAD_HEIGHT))
            Player.REG_HEAD_IMAGES.append(surface)

        Player.ATTACKING_HEAD_IMAGES = []
        for k in range(4):
            for i in range(3):
                surface = PG.Surface((Player.WIDTH,
                                     Player.HEAD_HEIGHT)).convert()
                surface.set_colorkey(key)
                surface.blit(sheet, (0, 0), (Player.WIDTH+i*Player.WIDTH,
                             k*Player.HEAD_HEIGHT, Player.WIDTH,
                             Player.HEAD_HEIGHT))
                Player.ATTACKING_HEAD_IMAGES.append(surface)

    def render_items_on_hud(self, x, y):

        for i, image in enumerate(self.item_images):
            G.Globals.SCREEN.blit(image, (x, y))
            if i+1 < len(self.item_images):
                x -= self.item_images[i+1].get_width()
                x -= 10

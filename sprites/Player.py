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


class Player(PS.Sprite):

    WALKING_BODY_IMAGES = None
    RUNNING_BODY_IMAGES = None
    REG_HEAD_IMAGES = None
    ATTACKING_HEAD_IMAGES = None
    SOUND = None
    WIDTH = 40
    HEIGHT = 50
    BODY_HEIGHT = 27
    HEAD_HEIGHT = 27
    CYCLE = 1
    SPEED_TIME = .4
    SCROLL_RIGHT_BOUND = 600
    SCROLL_LEFT_BOUND = 200
    SCROLL_UPPER_BOUND = 200
    SCROLL_LOWER_BOUND = 400
    SPRITE_IMAGE_KEY = None

    def __init__(self, x_cord, y_cord, cam):
        PS.Sprite.__init__(self)

        if not Player.WALKING_BODY_IMAGES:
            self.load_images()

        if not Player.SOUND:
            Player.SOUND = PM.Sound("meow.wav")

        self.image = None
        self.body_image = Player.WALKING_BODY_IMAGES[10]
        self.head_image = Player.REG_HEAD_IMAGES[1]

        self.rect = PG.Rect(0,0,Player.WIDTH, Player.HEIGHT)

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

    def handle_events(self, event):
        if event.type == PG.KEYDOWN:
            #Adding the new key press to the end of
            #the array
            self.key.append(event.key)
            self.time = 0

        elif event.type == PG.KEYUP:
            #Remove the key from the array if
            #it is there
            if event.key in self.key:
                self.key.remove(event.key)

    def set_screen_coords(self, x, y):
        self.rect.x = x
        self.rect.y = y

    def set_head_image(self):
        if self.y_velocity > 0:
            self.head_image = Player.REG_HEAD_IMAGES[1]
        elif self.y_velocity < 0:
            self.head_image = Player.REG_HEAD_IMAGES[0]
        elif self.x_velocity < 0:
            self.head_image = Player.REG_HEAD_IMAGES[2]
        elif self.x_velocity > 0:
            self.head_image = Player.REG_HEAD_IMAGES[3]

    def render(self):
        G.Globals.SCREEN.blit(self.body_image, (self.rect.x, self.rect.y+Player.HEAD_HEIGHT-4))
        G.Globals.SCREEN.blit(self.head_image, (self.rect.x, self.rect.y))

    # takes in the fixed time interval, dt
    def update(self, time):
        #update velocities if a key is currently held down
        if len(self.key) > 0:
            if self.key[-1] == PG.K_w:
                self.y_velocity -= self.accel
                #Make sure they don't go too fast
                if self.y_velocity < -self.speed:
                    self.y_velocity = -self.speed
                #To avoid drift
                self.x_velocity = 0
            elif self.key[-1] == PG.K_s:
                self.y_velocity += self.accel
                if self.y_velocity > self.speed:
                    self.y_velocity = self.speed
                self.x_velocity = 0
            elif self.key[-1] == PG.K_d:
                self.x_velocity += self.accel
                if self.x_velocity > self.speed:
                    self.x_velocity = self.speed
                self.y_velocity = 0
            elif self.key[-1] == PG.K_a:
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
            self.set_head_image()
        if self.y_velocity > 0:
            if self.y_velocity == self.speed:
                self.body_image = Player.RUNNING_BODY_IMAGES[index]
            else:
                self.body_image = Player.WALKING_BODY_IMAGES[index]
            self.set_head_image()
        if self.x_velocity < 0:
            if self.x_velocity == -self.speed:
                self.body_image = Player.RUNNING_BODY_IMAGES[index+16]
            else:
                self.body_image = Player.WALKING_BODY_IMAGES[index+16]
            self.set_head_image()
        if self.x_velocity > 0:
            if self.x_velocity == self.speed:
                self.body_image = Player.RUNNING_BODY_IMAGES[index+24]
            else:
                self.body_image = Player.WALKING_BODY_IMAGES[index+24]
            self.set_head_image()
        self.time += time
        if self.time >= Player.CYCLE:
            self.time = 0


    def wall_collision(self, tile):
        val = 0
        #picking up a key
        if tile.is_key():
            self.keys = self.keys + 1
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
        elif not tile.is_wall and not tile.is_door():
            val = 0
        #regular wall stuff
        elif self.y_velocity > 0:    
            self.y_velocity = 0
            self.world_coord_y = tile.world_y - Player.HEIGHT
        elif self.y_velocity < 0:
            self.y_velocity = 0
            if tile.partial == True:
                self.world_coord_y = tile.world_y + tile.rect.height
            else:
                self.world_coord_y = tile.world_y + Tile.Tile.HEIGHT
        elif self.x_velocity > 0:
            self.x_velocity = 0
            self.world_coord_x = tile.world_x - Player.WIDTH
        elif self.x_velocity < 0:
            self.x_velocity = 0
            self.world_coord_x = tile.world_x + Tile.Tile.WIDTH
        return val

    def load_images(self):
        sheet = PI.load("sprites/images/cat_sprite_sheet_body.png").convert()
        key = sheet.get_at((0, 0))

        Player.WALKING_BODY_IMAGES = []
        for k in range(4):
            for i in range(8):
                surface = PG.Surface((Player.WIDTH, Player.BODY_HEIGHT)).convert()
                surface.set_colorkey(key)
                surface.blit(sheet, (0,0), (i*Player.WIDTH, k*Player.BODY_HEIGHT, Player.WIDTH, Player.BODY_HEIGHT))
                Player.WALKING_BODY_IMAGES.append(surface)
        print len(Player.WALKING_BODY_IMAGES)

        Player.RUNNING_BODY_IMAGES = []
        for k in range(4):
            for i in range(8):
                surface = PG.Surface((Player.WIDTH, Player.BODY_HEIGHT)).convert()
                surface.set_colorkey(key)
                surface.blit(sheet, (0,0), (i*Player.WIDTH, 4*Player.BODY_HEIGHT+k*Player.BODY_HEIGHT, Player.WIDTH, Player.BODY_HEIGHT))
                Player.RUNNING_BODY_IMAGES.append(surface)

        sheet = PI.load("sprites/images/cat_sprite_sheet_head.png").convert()
        key = sheet.get_at((0, 0))

        Player.REG_HEAD_IMAGES = []
        for k in range(4):
            surface = PG.Surface((Player.WIDTH, Player.HEAD_HEIGHT)).convert()
            surface.set_colorkey(key)
            surface.blit(sheet, (0,0), (0, k*Player.HEAD_HEIGHT, Player.WIDTH, Player.HEAD_HEIGHT))
            Player.REG_HEAD_IMAGES.append(surface)

        Player.ATTACKING_HEAD_IMAGES = []
        for k in range(4):
            for i in range(2):
                surface = PG.Surface((Player.WIDTH, Player.HEAD_HEIGHT)).convert()
                surface.set_colorkey(key)
                surface.blit(sheet, (0,0), (Player.WIDTH+i*Player.WIDTH, k*Player.HEAD_HEIGHT, Player.WIDTH, Player.HEAD_HEIGHT))
                Player.ATTACKING_HEAD_IMAGES.append(surface)


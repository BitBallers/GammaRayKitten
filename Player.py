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
import Camera
import Map


class Player(PS.Sprite):

    FORWARD_IMAGES = None
    FORWARD_R_IMAGES = None
    BACK_IMAGES = None
    BACK_R_IMAGES = None
    LEFT_IMAGES = None
    LEFT_R_IMAGES = None
    RIGHT_IMAGES = None
    RIGHT_R_IMAGES = None
    SOUND = None
    WIDTH = 40
    HEIGHT = 50
    CYCLE = 1
    SPEED_TIME = .4
    SCROLL_RIGHT_BOUND = 600
    SCROLL_LEFT_BOUND = 200
    SCROLL_UPPER_BOUND = 200
    SCROLL_LOWER_BOUND = 400

    def __init__(self, x_cord, y_cord, cam):
        PS.Sprite.__init__(self)

        if not Player.FORWARD_IMAGES:
            self.load_images()

        if not Player.SOUND:
            Player.SOUND = PM.Sound("meow.wav")
       
        self.image = Player.FORWARD_IMAGES[2]
        self.rect = self.image.get_rect()
        

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
        

    def handle_events(self, event):
        if event.type == PG.KEYDOWN:
            #Adding the new key press to the end of
            #the array 
            self.key.append(event.key)
            self.time = 0
            
        elif event.type == PG.KEYUP:
            #Remove the key from the array if
            #it is there
            self.key.remove(event.key)

    def set_screen_coords(self, x, y):
        self.rect.x = x
        self.rect.y = y

    # takes in the fixed time interval, dt
    def update(self, time):
        #update velocities if a key is currently held down
        if len(self.key) > 0:
            if self.key[-1] == PG.K_UP:
                self.y_velocity -= self.accel
                #Make sure they don't go too fast
                if self.y_velocity < -self.speed:
                    self.y_velocity = -self.speed
                #To avoid drift
                self.x_velocity = 0
            elif self.key[-1] == PG.K_DOWN:
                self.y_velocity += self.accel
                if self.y_velocity > self.speed:
                    self.y_velocity = self.speed
                self.x_velocity = 0
            elif self.key[-1] == PG.K_RIGHT:
                self.x_velocity += self.accel
                if self.x_velocity > self.speed:
                    self.x_velocity = self.speed
                self.y_velocity = 0
            elif self.key[-1] == PG.K_LEFT:
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
                    self.image = Player.FORWARD_IMAGES[2]
            elif self.y_velocity < 0:
                self.y_velocity += self.accel
                if self.y_velocity > 0:
                    self.y_velocity = 0
                    self.image = Player.BACK_IMAGES[2]
            if self.x_velocity > 0:
                self.x_velocity -= self.accel
                if self.x_velocity < 0:
                    self.x_velocity = 0
                    self.image = Player.RIGHT_IMAGES[2]
            elif self.x_velocity < 0:
                self.x_velocity += self.accel
                if self.x_velocity > 0:
                    self.x_velocity = 0
                    self.image = Player.LEFT_IMAGES[2]

        # update world coords
        self.world_coord_x += self.x_velocity
        self.world_coord_y += self.y_velocity

        # check collisions with scrolling boundary
        if self.rect.x > Player.SCROLL_RIGHT_BOUND - self.rect.width and self.x_velocity > 0 and self.world_coord_x < Map.Map.WIDTH-Player.SCROLL_LEFT_BOUND:
            self.camera.shift_camera(self.x_velocity, 0)
            

        if self.rect.x < Player.SCROLL_LEFT_BOUND and self.x_velocity < 0 and self.world_coord_x > Player.SCROLL_LEFT_BOUND:
            self.camera.shift_camera(self.x_velocity, 0)
            

        if self.rect.y > (Player.SCROLL_LOWER_BOUND - self.rect.height) and self.y_velocity > 0 and self.world_coord_y < Map.Map.HEIGHT-Player.SCROLL_UPPER_BOUND:
            self.camera.shift_camera(0, self.y_velocity)
            

        if self.rect.y < Player.SCROLL_UPPER_BOUND and self.y_velocity < 0 and self.world_coord_y > Player.SCROLL_UPPER_BOUND:
            self.camera.shift_camera(0, self.y_velocity)
            

        # animations
        k = Player.CYCLE/8.0
        index = math.floor(self.time/k)
        index = int(index)
        if self.y_velocity < 0:
            if self.y_velocity == -self.speed:
                self.image = Player.BACK_R_IMAGES[index]
            else:
                self.image = Player.BACK_IMAGES[index]
        if self.y_velocity > 0:
            if self.y_velocity == self.speed:
                self.image = Player.FORWARD_R_IMAGES[index]
            else:
                self.image = Player.FORWARD_IMAGES[index]
        if self.x_velocity < 0:
            if self.x_velocity == -self.speed:
                self.image = Player.LEFT_R_IMAGES[index]
            else:
                self.image = Player.LEFT_IMAGES[index]
        if self.x_velocity > 0:
            if self.x_velocity == self.speed:
                self.image = Player.RIGHT_R_IMAGES[index]
            else:
                self.image = Player.RIGHT_IMAGES[index]
        self.time += time
        if self.time >= Player.CYCLE:
            self.time = 0

    def wall_collision(self, tile):
        if self.y_velocity > 0:
            self.y_velocity = 0
            self.world_coord_y = tile.world_y - Player.HEIGHT
        elif self.y_velocity < 0:
            self.y_velocity = 0
            self.world_coord_y = tile.world_y + Tile.Tile.HEIGHT
        elif self.x_velocity > 0:
            self.x_velocity = 0
            self.world_coord_x = tile.world_x - Player.WIDTH
        elif self.x_velocity < 0:
            self.x_velocity = 0
            self.world_coord_x = tile.world_x + Tile.Tile.WIDTH


    def load_images(self):
        sheet = PI.load("cat_sprite_sheet.png").convert()
        key = sheet.get_at((0, 0))
        #Get Forward Images
        Player.FORWARD_IMAGES = []
        for i in range(8):

            surface = PG.Surface((Player.WIDTH, Player.HEIGHT)).convert()
            surface.set_colorkey(key)            
            surface.blit(sheet, (0, 0), (i*Player.WIDTH, 0,
                         Player.WIDTH, Player.HEIGHT))
            Player.FORWARD_IMAGES.append(surface)
        #Get Back Images
        Player.BACK_IMAGES = []
        for i in range(8):
            surface = PG.Surface((Player.WIDTH, Player.HEIGHT)).convert()
            surface.set_colorkey(key)
            
            surface.blit(sheet, (0, 0), (i*Player.WIDTH, Player.HEIGHT,
                         Player.WIDTH, Player.HEIGHT))
            
            Player.BACK_IMAGES.append(surface)
        #Get Left Images
        Player.LEFT_IMAGES = []
        for i in range(8):
            surface = PG.Surface((Player.WIDTH, Player.HEIGHT)).convert()
            surface.set_colorkey(key)
           
            surface.blit(sheet, (0, 0), (i*Player.WIDTH, Player.HEIGHT*2,
                         Player.WIDTH, Player.HEIGHT))
            Player.LEFT_IMAGES.append(surface)
        #Get Right Images
        Player.RIGHT_IMAGES = []
        for i in range(8):
            surface = PG.Surface((Player.WIDTH, Player.HEIGHT)).convert()
            surface.set_colorkey(key)
            
            surface.blit(sheet, (0, 0), (i*Player.WIDTH, Player.HEIGHT*3,
                         Player.WIDTH, Player.HEIGHT))
            Player.RIGHT_IMAGES.append(surface)
        #Get Forward Running images
        Player.FORWARD_R_IMAGES = []
        for i in range(8):
            surface = PG.Surface((Player.WIDTH, Player.HEIGHT)).convert()
            surface.set_colorkey(key)
            
            surface.blit(sheet, (0, 0), (i*Player.WIDTH, Player.HEIGHT*4,
                         Player.WIDTH, Player.HEIGHT))
            Player.FORWARD_R_IMAGES.append(surface)
        #Get Back Running Images
        Player.BACK_R_IMAGES = []
        for i in range(8):
            surface = PG.Surface((Player.WIDTH, Player.HEIGHT)).convert()
            surface.set_colorkey(key)
            
            surface.blit(sheet, (0, 0), (i*Player.WIDTH, Player.HEIGHT*5,
                         Player.WIDTH, Player.HEIGHT))
            Player.BACK_R_IMAGES.append(surface)
        #Get Left Running Images
        Player.LEFT_R_IMAGES = []
        for i in range(8):
            surface = PG.Surface((Player.WIDTH, Player.HEIGHT)).convert()
            surface.set_colorkey(key)
            
            surface.blit(sheet, (0, 0), (i*Player.WIDTH, Player.HEIGHT*6,
                         Player.WIDTH, Player.HEIGHT))
            Player.LEFT_R_IMAGES.append(surface)
        #Get Right Running Images
        Player.RIGHT_R_IMAGES = []
        for i in range(8):
            surface = PG.Surface((Player.WIDTH, Player.HEIGHT)).convert()
            surface.set_colorkey(key)
            
            surface.blit(sheet, (0, 0), (i*Player.WIDTH, Player.HEIGHT*7,
                         Player.WIDTH, Player.HEIGHT))
            Player.RIGHT_R_IMAGES.append(surface)

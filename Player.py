import pygame as PG
import sys as SYS
import random as R
import pygame.image as PI
import pygame.display as PDI
import pygame.event as PE
import pygame.sprite as PS
import pygame.mixer as PM
import math


class Player(PS.Sprite):

    FORWARD_IMAGES = None
    BACK_IMAGES = None
    LEFT_IMAGES = None
    RIGHT_IMAGES = None
    SOUND = None
    WIDTH = 40
    HEIGHT = 50
    CYCLE = 2

    def __init__(self, x_cord, y_cord):
        PS.Sprite.__init__(self)

        if not Player.FORWARD_IMAGES:
            self.load_images()

        if not Player.SOUND:
            Player.SOUND = PM.Sound("meow.wav")

        self.image = Player.FORWARD_IMAGES[2]
        self.rect = self.image.get_rect()
        self.rect.x = x_cord
        self.rect.y = y_cord
        self.x_velocity = 0
        self.y_velocity = 0
        self.speed = 2
        self.time = 0

    def handle_events(self, event):
        if event.type == PG.KEYDOWN:
            if event.key == PG.K_UP:
                self.y_velocity = - self.speed
                self.x_velocity = 0
                self.time = 0
            elif event.key == PG.K_DOWN:
                self.y_velocity = self.speed
                self.x_velocity = 0
                self.time = 0
            elif event.key == PG.K_LEFT:
                self.x_velocity = -self.speed
                self.y_velocity = 0
                self.time = 0
            elif event.key == PG.K_RIGHT:
                self.x_velocity = self.speed
                self.y_velocity = 0
                self.time = 0

        elif event.type == PG.KEYUP:
            if event.key == PG.K_UP:
                if self.y_velocity < 0:
                    self.y_velocity = 0
                    self.image = Player.BACK_IMAGES[2]
            elif event.key == PG.K_DOWN:
                if self.y_velocity > 0:
                    self.y_velocity = 0
                    self.image = Player.FORWARD_IMAGES[2]
            elif event.key == PG.K_LEFT:
                if self.x_velocity < 0:
                    self.x_velocity = 0
                    self.image = Player.LEFT_IMAGES[2]
            elif event.key == PG.K_RIGHT:
                if self.x_velocity > 0:
                    self.x_velocity = 0
                    self.image = Player.RIGHT_IMAGES[2]

    # takes in the fixed time interval, dt
    def update(self, time):
        # update rect.x and rect.y
        self.rect.x += self.x_velocity
        self.rect.y += self.y_velocity
        # check wall collisions, change directions
        if self.rect.x > 800 - self.rect.width:
            self.x_velocity = 0
            self.rect.x = 800 - self.rect.width
            Player.SOUND.play()

        if self.rect.x < 0:
            self.x_velocity = 0
            self.rect.x = 0
            Player.SOUND.play()

        if self.rect.y > 600 - self.rect.height:
            self.y_velocity = 0
            self.rect.y = 600 - self.rect.height
            Player.SOUND.play()

        if self.rect.y < 0:
            self.y_velocity = 0
            self.rect.y = 0
            Player.SOUND.play()

        # animations
        k = Player.CYCLE/8.0
        index = math.floor(self.time/k)
        index = int(index)
        if self.y_velocity < 0:
            self.image = Player.BACK_IMAGES[index]
        if self.y_velocity > 0:
            self.image = Player.FORWARD_IMAGES[index]
        if self.x_velocity < 0:
            self.image = Player.LEFT_IMAGES[index]
        if self.x_velocity > 0:
            self.image = Player.RIGHT_IMAGES[index]
        self.time += time
        if self.time >= Player.CYCLE:
            self.time = 0

    def load_images(self):
        sheet = PI.load("cat_sprite_sheet.png").convert_alpha()
        #key = sheet.get_at((0, 0))

        Player.FORWARD_IMAGES = []
        for i in range(8):
            surface = PG.Surface((Player.WIDTH, Player.HEIGHT)).convert()
            #surface.set_colorkey(key)
            surface.blit(sheet, (0, 0), (i*Player.WIDTH, 0,
                         Player.WIDTH, Player.HEIGHT))
            Player.FORWARD_IMAGES.append(surface)

        Player.BACK_IMAGES = []
        for i in range(8):
            surface = PG.Surface((Player.WIDTH, Player.HEIGHT)).convert()
            #surface.set_colorkey(key)
            surface.blit(sheet, (0, 0), (i*Player.WIDTH, Player.HEIGHT,
                         Player.WIDTH, Player.HEIGHT))
            Player.BACK_IMAGES.append(surface)

        Player.LEFT_IMAGES = []
        for i in range(8):
            surface = PG.Surface((Player.WIDTH, Player.HEIGHT)).convert()
            #surface.set_colorkey(key)
            surface.blit(sheet, (0, 0), (i*Player.WIDTH, Player.HEIGHT*2,
                         Player.WIDTH, Player.HEIGHT))
            Player.LEFT_IMAGES.append(surface)

        Player.RIGHT_IMAGES = []
        for i in range(8):
            surface = PG.Surface((Player.WIDTH, Player.HEIGHT)).convert()
            #surface.set_colorkey(key)
            surface.blit(sheet, (0, 0), (i*Player.WIDTH, Player.HEIGHT*3,
                         Player.WIDTH, Player.HEIGHT))
            Player.RIGHT_IMAGES.append(surface)

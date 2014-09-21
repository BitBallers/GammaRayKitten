import pygame as PG
import sys as SYS
import random as R
import pygame.image as PI
import pygame.display as PDI
import pygame.event as PE
import pygame.sprite as PS
import pygame.mixer as PM

class Player(PS.Sprite):
    IMAGE = None
    SOUND = None
    
    def __init__(self, x_cord, y_cord):
        PS.Sprite.__init__(self)

        if not Player.IMAGE:
            Player.IMAGE = PI.load("cat_sprite.png").convert()

        if not Player.SOUND:
            Player.SOUND = PM.Sound("meow.wav")

        self.image = Player.IMAGE
        self.rect = self.image.get_rect()
        self.rect.height -= 20  
        self.rect.centerx = x_cord
        self.rect.centery = y_cord+10
        self.x_velocity = 0
        self.y_velocity = 0
        self.speed = 10.2


    def handle_events(self, event):
        if event.type == PG.KEYDOWN:
            if event.key == PG.K_UP:
                self.y_velocity = - self.speed
            elif event.key == PG.K_DOWN:
                self.y_velocity = self.speed
            elif event.key == PG.K_LEFT:
                self.x_velocity = -self.speed
            elif event.key == PG.K_RIGHT:
                self.x_velocity = self.speed

        elif event.type == PG.KEYUP:
            if event.key == PG.K_UP:
                if self.y_velocity < 0:
                    self.y_velocity = 0
            elif event.key == PG.K_DOWN:
                if self.y_velocity > 0:
                    self.y_velocity = 0
            elif event.key == PG.K_LEFT:
                if self.x_velocity < 0:
                    self.x_velocity = 0
            elif event.key == PG.K_RIGHT:
                if self.x_velocity > 0:
                    self.x_velocity = 0

    #takes in the fixed time interval, dt
    def update(self, dt):
        pls = 0
        if self.x_velocity > 0:
            print "VEL"
            print self.x_velocity
            print "COORDINATE"
            print self.rect.centerx
            pls = 1
        self.rect.centerx += self.x_velocity * dt
        self.rect.centery += self.y_velocity * dt
        if pls == 1:
            print "VEL"
            print self.x_velocity
            print "COORDINATE"
            print self.rect.centerx
        
        if self.rect.x > 800 - self.rect.width:
            self.x_velocity = 0
            self.rect.x = 800 - self.rect.width
            SOUND.play()

        if self.rect.x < 0:
            self.x_velocity = 0
            self.rect.x = 0
            SOUND.play()
            
        if self.rect.y > 600 - self.rect.height:
            self.y_velocity = 0
            self.rect.y = 600 - self.rect.height
            SOUND.play()

        if self.rect.y < 0:
            self.y_velocity = 0
            self.rect.y = 0
            SOUND.play()
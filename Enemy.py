import pygame as PG
import pygame.image as PI
import pygame.sprite as PS

class Enemy(PS.Sprite):
    
    IMAGE = None

    def __init__(self, x_cord, y_cord, x_vel, y_vel):
        PS.Sprite.__init__(self)
        
        if not Enemy.IMAGE:
            Enemy.IMAGE = PI.load("slime_sprite.png").convert_alpha()
       
        self.image = Enemy.IMAGE
        self.rect = self.image.get_rect()
        self.rect.x = x_cord
        self.rect.y = y_cord

        self.x_velocity = x_vel
        self.y_velocity = y_vel
        self.x = self.rect.x
        self.y = self.rect.y


    def update(self, dt):
        self.x += self.x_velocity * dt
        self.y += self.y_velocity * dt
        #update rect.x and rect.y
        self.rect.x = self.x
        self.rect.y = self.y
        #check wall collisions, change directions
        if self.rect.x > 800 - self.rect.width:
            self.x_velocity *= -1
            self.rect.x = 800 - self.rect.width

        if self.rect.x < 0:
            self.x_velocity *= -1
            self.rect.x = 0
            
        if self.rect.y > 600 - self.rect.height:
            self.y_velocity *= -1
            self.rect.y = 600 - self.rect.height
            
        if self.rect.y < 0:
            self.y_velocity *= -1
            self.rect.y = 0

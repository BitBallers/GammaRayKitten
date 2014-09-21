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


    def update(self):
        
        #check wall collisions, change directions
        if self.rect.x >= 800 - self.rect.width \
            or self.rect.x <= 0:
            self.x_velocity *= -1
        if self.rect.y >= 600 - self.rect.height \
            or self.rect.y <= 0:
            self.y_velocity *= -1

        self.rect.x += self.x_velocity
        self.rect.y += self.y_velocity
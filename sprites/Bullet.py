import pygame as PG
import pygame.image as PI
import pygame.display as PDI
import pygame.event as PE
import pygame.sprite as PS
import maps.Camera as Camera
import maps.Map as Map
import Globals as G


class Bullet(PS.Sprite):

    IMAGE = None
    WIDTH = 10
    HEIGHT = 10

    def __init__(self, w_x, w_y, x_vel, y_vel, dist):
        PS.Sprite.__init__(self) 
        if not Bullet.IMAGE:
            surf = PI.load("sprites/images/cat_spit_sprite.png").convert()
            key = surf.get_at((0,0))
            surf.set_colorkey(key)
            Bullet.IMAGE = surf
        self.image = Bullet.IMAGE
        self.rect = self.image.get_rect()
        self.world_x = w_x
        self.world_y = w_y
        self.begin_x = w_x
        self.begin_y = w_y
        self.dist = dist
        self.x_vel = x_vel
        self.y_vel = y_vel
        self.rect.x = self.world_x - Camera.Camera.X
        self.rect.y = self.world_y - Camera.Camera.Y

    def render(self):
        x = self.world_x - Camera.Camera.X
        y = self.world_y - Camera.Camera.Y
        if x>= self.rect.width*-1 and x <= G.Globals.WIDTH and y>= self.rect.height*-1 and y<= G.Globals.HEIGHT:
            G.Globals.SCREEN.blit(self.image, (x,y))

    def update(self, time):
        self.world_x += self.x_vel
        self.world_y += self.y_vel
        self.rect.x = self.world_x - Camera.Camera.X
        self.rect.y = self.world_y - Camera.Camera.Y
        cur_dist = ((self.world_x - self.begin_x)**2 + (self.world_y - self.begin_y)**2) ** (0.5)
        return cur_dist > self.dist

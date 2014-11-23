import pygame as PG
import pygame.image as PI
import pygame.display as PDI
import pygame.event as PE
import pygame.sprite as PS
import maps.Camera as Camera
import maps.Map as Map
import Globals as G
import math


class Bullet(PS.Sprite):

    IMAGE = None
    WIDTH = 10
    HEIGHT = 10

    def __init__(self, w_x, w_y, x_vel, y_vel, dist, drunk):
        PS.Sprite.__init__(self)
        if not Bullet.IMAGE:
            surf = PI.load("sprites/images/cat_spit_sprite.png").convert()
            key = surf.get_at((0, 0))
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
        self.dr_dir = -1
        self.val = 0.0
        if drunk:
            if x_vel is 0:
                self.dr_dir = 0
                self.base = w_x
            else:
                self.dr_dir = 1 
                self.base = w_y

    def render(self):
        x = int(self.world_x - Camera.Camera.X)
        y = int(self.world_y - Camera.Camera.Y)
        if x >= self.rect.width * -1 and x <= G.Globals.WIDTH and \
                y >= self.rect.height * -1 and y <= G.Globals.HEIGHT:
            G.Globals.SCREEN.blit(self.image, (x, y))

    def update(self, time):
        self.val = self.val + 30*time
        if self.dr_dir is 0:
            self.world_x = self.base + 15 * math.sin(self.val)
        elif self.dr_dir is 1:
            self.world_y = self.base + 15 * math.sin(self.val)
        self.world_x += self.x_vel
        self.world_y += self.y_vel
        self.rect.x = int(self.world_x - Camera.Camera.X)
        self.rect.y = int(self.world_y - Camera.Camera.Y)
        if self.dr_dir is -1:
            cur_dist = ((self.world_x - self.begin_x) **
                        2 + (self.world_y - self.begin_y) ** 2) ** (0.5)
        elif self.dr_dir is 0:
            cur_dist = abs(self.world_y - self.begin_y)
        elif self.dr_dir is 1:
            cur_dist = abs(self.world_x - self.begin_x)
        return cur_dist > self.dist

import pygame as PG
import pygame.image as PI
import pygame.sprite as PS
import maps.Camera as Camera
import Globals as G


class Heart(PS.Sprite):

    IMAGE = None

    def __init__(self, x, y):
        PS.Sprite.__init__(self)

        if not Heart.IMAGE:
            img = PI.load("sprites/images/heart.png").convert()
            Heart.IMAGE = PG.Surface(img.get_size()).convert()
            Heart.IMAGE.set_colorkey(img.get_at((0, 0)))
            Heart.IMAGE.blit(img, (0, 0))

        self.world_x = x
        self.world_y = y
        self.init_y = y
        self.image = Heart.IMAGE
        self.rect = self.image.get_rect()
        self.flying = True
        self.y_velocity = -2
        self.gravity = .1

    def render(self):
        x = self.world_x - Camera.Camera.X
        y = self.world_y - Camera.Camera.Y
        if x >= -self.rect.width and x <= G.Globals.WIDTH and \
                y >= -self.rect.height and y <= G.Globals.HEIGHT:
            G.Globals.SCREEN.blit(self.image, (x, y))

    def update(self):

        if self.flying:
            self.world_y += self.y_velocity
            self.y_velocity += self.gravity
            if self.world_y >= self.init_y:
                if self.y_velocity > .1:
                    self.y_velocity *= -.7
                else:
                    self.flying = False

        self.rect.x = self.world_x - Camera.Camera.X
        self.rect.y = self.world_y - Camera.Camera.Y

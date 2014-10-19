import pygame as PG
import pygame.image as PI
import pygame.sprite as PS
import Globals as G
import maps.Camera as Camera


class Enemy(PS.Sprite):

    IMAGES = None
    CYCLE = 1.0

    def __init__(self, (x, y)):
        PS.Sprite.__init__(self)

        if not Enemy.IMAGES:
            self.load_images()

        self.image = Enemy.IMAGES[8]
        self.b_index = 8
        self.c_index = 8
        self.rect = self.image.get_rect()
        self.world_x = x
        self.world_y = y

        self.time = 0.0

    def update(self):
        pass

    def render(self):
        x = self.world_x-Camera.Camera.X
        y = self.world_y-Camera.Camera.Y
        if x >= self.rect.width*-1 and x <= G.Globals.WIDTH and y >= self.rect.height*-1 and y <= G.Globals.HEIGHT:
            G.Globals.SCREEN.blit(self.image, (x,y))

    def load_images(self):
        Enemy.IMAGES = []
        sheet = PI.load("sprites/images/slime_sprite_sheet.png").convert_alpha()
        key = sheet.get_at((0, 0))
        for y in range(4):
            for x in range(4):
                surface = PG.Surface((30, 20)).convert()
                surface.set_colorkey(key)
                surface.blit(sheet, (0, 0), (x*30, y*20, 30, 20))
                Enemy.IMAGES.append(surface)

    def update_image(self):
        if self.y_velocity > 0:
            self.b_index = 8
        elif self.y_velocity < 0:
            self.b_index = 12
        if self.x_velocity > 0:
            self.b_index = 0
        elif self.x_velocity < 0:
            self.b_index = 4
        self.image = Enemy.IMAGES[self.b_index + self.c_index]
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

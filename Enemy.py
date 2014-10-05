import pygame as PG
import pygame.image as PI
import pygame.sprite as PS
import Globals


class Enemy(PS.Sprite):

    IMAGES = None
    CYCLE = 1.0

    def __init__(self, x_cord, y_cord, x_vel, y_vel):
        PS.Sprite.__init__(self)

        if not Enemy.IMAGES:
            self.load_images()

        self.image = Enemy.IMAGES[8]
        self.b_index = 8
        self.c_index = 8
        self.rect = self.image.get_rect()
        self.rect.x = x_cord
        self.rect.y = y_cord
        self.x = self.rect.x
        self.y = self.rect.y

        self.x_velocity = x_vel
        self.y_velocity = y_vel
        self.time = 0.0

    def update(self):
        self.rect.x += self.x_velocity
        self.rect.y += self.y_velocity
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
        self.x = self.rect.x
        self.y = self.rect.y

        self.time += Globals.Globals.INTERVAL
        if self.time > Enemy.CYCLE:
            self.time = 0.0
        index = int(self.time / (Enemy.CYCLE / 4))
        if index != self.c_index:
            self.c_index = index
            self.update_image()

    def load_images(self):
        Enemy.IMAGES = []
        sheet = PI.load("slime_sprite_sheet.png").convert_alpha()
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

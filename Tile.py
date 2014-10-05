import pygame as PG
import pygame.sprite as PS
import pygame.image as PI


class Tile(PS.Sprite):

    IMAGES = None
    WIDTH = 50
    HEIGHT = 50

    def __init__(self, x, y, type):
        PS.Sprite.__init__(self)
        if not Tile.IMAGES:
            self.load_images()
        self.image = Tile.IMAGES[type]
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def change_image(self, type):
        self.image = Tile.IMAGES[type]

    def load_images(self):
        sheet = PI.load("texture_sprite_sheet.png").convert()
        Tile.IMAGES = []

        for i in range(4):
            surface = PG.Surface((Tile.WIDTH, Tile.HEIGHT))
            
            surface.blit(sheet, (0, 0), (i*Tile.WIDTH, 0,
                         Tile.WIDTH, Tile.HEIGHT))
            Tile.IMAGES.append(surface)
import pygame as PG
import pygame.sprite as PS
import pygame.image as PI


class Item(PS.Sprite):

    IMAGES = None
    KEY = 0
    
    def __init__(self, x, y, item_type):
        PS.Sprite.__init__(self)
        if not Item.IMAGES:
            self.load_images()
        self.image = Item.IMAGES[item_type]
        self.rect = self.image.get_rect()
        self.world_x = x
        self.world_y = y
        self.item_type = item_type

    def is_key(self):
        return self.type == KEY

    def load_images(self):
        img = PI.load("name").covert()
        key = sheet.get_at((0,0))
        img.set_colorkey(key)
        IMAGES = img

    def set_screen_coords(self, x, y):
        self.rect.x = x
        self.rect.y = y


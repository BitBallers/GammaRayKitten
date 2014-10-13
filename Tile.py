import pygame as PG
import pygame.sprite as PS
import pygame.image as PI


class Tile(PS.Sprite):

    IMAGES = None
    WIDTH = 50
    HEIGHT = 50
    SPRITE_SHEET_LENGTH = 8
    WALL_TILES = [0, 2, 3, 4, 7]
    DOOR_TILES = [1]
    STAIR_TILES = [5]

    def __init__(self, x, y, type):
        PS.Sprite.__init__(self)
        if not Tile.IMAGES:
            self.load_images()
        self.image = Tile.IMAGES[type]
        self.rect = self.image.get_rect()
        self.world_x = x
        self.world_y = y
        self.type = type
        
    def change_image(self, type):
        self.image = Tile.IMAGES[type]
        self.type = type

    def set_screen_coords(self, x, y):
        self.rect.x = x
        self.rect.y = y

    def load_images(self):
        sheet = PI.load("texture_sprite_sheet.png").convert()
        Tile.IMAGES = []

        for i in range(Tile.SPRITE_SHEET_LENGTH):
            surface = PG.Surface((Tile.WIDTH, Tile.HEIGHT))
            
            surface.blit(sheet, (0, 0), (i*Tile.WIDTH, 0,
                         Tile.WIDTH, Tile.HEIGHT))
            Tile.IMAGES.append(surface)

        # create key tile
        key = PI.load("20x12_key.png").convert()
        color_key = key.get_at((19, 0))
        key.set_colorkey(color_key)
        surface = Tile.IMAGES[6].copy().convert()
        surface.set_colorkey(color_key)
        surface.blit(key, (15, 19))
        Tile.IMAGES.append(surface)
        
        

    def is_wall(self):
        if self.type in Tile.WALL_TILES:
            return True
        else:
            return False

    def is_door(self):
        if self.type in Tile.DOOR_TILES:
            return True
        else:
            return False

    def is_stairs(self):
        if self.type in Tile.STAIR_TILES:
            return True
        else:
            return False

    def is_key(self):
        if self.type == 8:
            return True
        else:
            return False



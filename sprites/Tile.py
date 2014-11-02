import pygame as PG
import pygame.sprite as PS
import pygame.image as PI


class Tile(PS.Sprite):

    IMAGES = None
    WIDTH = 50
    HEIGHT = 50
    SPRITE_SHEET_LENGTH = 8
    WALL_TILES = [7]
    DOOR_TILES = [1]
    STAIR_TILES = [5]
    FORWARD_WALL_TILE = [0, 2, 3, 4, 8]
    ITEM_TILES = [12]
    KEY_TILES = [10]

    def __init__(self, x, y, type, level):
        PS.Sprite.__init__(self)
        if not Tile.IMAGES:
            self.load_images()
        self.image = Tile.IMAGES[level-1][type]
        self.rect = self.image.get_rect()
        self.world_x = x
        self.world_y = y
        self.type = type
        self.level = level
        self.partial = False

    def change_image(self, type):
        self.image = Tile.IMAGES[type]
        self.type = type

    def set_screen_coords(self, x, y):
        self.rect.x = x
        self.rect.y = y

    def load_images(self):
        
        Tile.IMAGES = []

        sheet = PI.load("sprites/images/lvl1_texture_sprite_sheet.png").convert()
        level_1_images = []

        for i in range(8):
            surface = PG.Surface((Tile.WIDTH, Tile.HEIGHT))

            surface.blit(sheet, (0, 0), (i * Tile.WIDTH, 0,
                                         Tile.WIDTH, Tile.HEIGHT))
            level_1_images.append(surface)

        level_1_images.append(None)
        level_1_images.append(None)

        sheet = PI.load("sprites/images/lvl2_texture_sprite_sheet.png").convert()
        level_2_images = []

        for i in range(8):
            surface = PG.Surface((Tile.WIDTH, Tile.HEIGHT))

            surface.blit(sheet, (0, 0), (i * Tile.WIDTH, 0,
                                         Tile.WIDTH, Tile.HEIGHT))
            level_2_images.append(surface)

        # create key tile
        key = PI.load("sprites/images/20x12_key.png").convert()
        color_key = key.get_at((19, 0))
        key.set_colorkey(color_key)
        
        surface11 = level_1_images[6].copy().convert()
        surface11.set_colorkey(color_key)
        surface11.blit(key, (15, 19))
        level_1_images.append(surface11)
        
        surface12 = level_2_images[6].copy().convert()
        surface12.set_colorkey(color_key)
        surface12.blit(key, (15, 19))
        
        level_2_images.append(surface12)

        # create syringe tile
        syringe = PI.load("sprites/images/syringe_sprite.png").convert()
        color_key = syringe.get_at((0, 0))
        syringe.set_colorkey(color_key)
        
        surface21 = level_1_images[6].copy().convert()
        surface21.set_colorkey(color_key)
        surface21.blit(syringe, (0, 0))
        level_1_images.append(surface21)

        surface22 = level_2_images[6].copy().convert()
        surface22.set_colorkey(color_key)
        surface22.blit(syringe, (0, 0))
        level_2_images.append(surface22)

        Tile.IMAGES.append(level_1_images)
        Tile.IMAGES.append(level_2_images)

    def is_wall(self):
        if self.type in Tile.WALL_TILES:
            return True
        else:
            return False

    def is_item(self):
        if self.type in Tile.ITEM_TILES:
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
        if self.type == 10:
            return True
        else:
            return False

    def is_forward_wall(self):
        if self.type in Tile.FORWARD_WALL_TILE:
            return True
        else:
            return False

    def get_wall_partial(self):
        new_tile = Tile(self.world_x, self.world_y, 7, self.level)
        new_tile.rect.height = Tile.HEIGHT / 3
        new_tile.partial = True
        return new_tile

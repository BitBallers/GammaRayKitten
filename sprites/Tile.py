import pygame as PG
import pygame.sprite as PS
import pygame.image as PI


class Tile(PS.Sprite):

    IMAGES = None
    LIGHT_IMG = None
    WIDTH = 50
    HEIGHT = 50
    SPRITE_SHEET_LENGTH = 11
    WALL_TILES = [7]
    DOOR_TILES = [1]
    STAIR_TILES = [5]
    FORWARD_WALL_TILE = [0, 2, 3, 4, 8, 9, 10]
    TABLE_TILES = [9, 10]
    ITEM_TILES = [12, 13, 14, 15, 16, 17, 18]
    KEY_TILES = [11]

    def __init__(self, x, y, type, level):
        PS.Sprite.__init__(self)
        if not Tile.IMAGES:
            self.load_images()
        if not Tile.LIGHT_IMG:
            self.load_light()
        
        self.image = Tile.IMAGES[level-1][type]
        self.rect = self.image.get_rect()
        self.world_x = x
        self.world_y = y
        self.type = type
        self.level = level
        self.partial = False
        self.light_img = None
        if type is 4:
            self.light_img = Tile.LIGHT_IMG

    def get_light(self):
        return self.light_img

    def change_image(self, type):
        self.image = Tile.IMAGES[self.level-1][type]
        self.type = type

    def set_screen_coords(self, x, y):
        self.rect.x = x
        self.rect.y = y

    def load_light(self):
        sheet = PI.load("sprites/images/wall_light.png").convert()
        key = sheet.get_at((0, 0))
        surf = PG.Surface((50, 75))
        surf.set_colorkey(key)
        surf.blit(sheet, (0, 0), (0, 0, 50, 75))
        Tile.LIGHT_IMG = surf

    def load_images(self):
        Tile.IMAGES = []
        s_string = "sprites/images/lvl1_texture_sprite_sheet.png"
        sheet = PI.load(s_string).convert()
        level_1_images = []
        for i in range(Tile.SPRITE_SHEET_LENGTH):
            surface = PG.Surface((Tile.WIDTH, Tile.HEIGHT))
            surface.blit(sheet, (0, 0), (i * Tile.WIDTH, 0,
                                         Tile.WIDTH, Tile.HEIGHT))
            level_1_images.append(surface)
        
        s_string = "sprites/images/lvl2_texture_sprite_sheet.png"
        sheet = PI.load(s_string).convert()
        level_2_images = []

        for i in range(Tile.SPRITE_SHEET_LENGTH):
            surface = PG.Surface((Tile.WIDTH, Tile.HEIGHT))

            surface.blit(sheet, (0, 0), (i * Tile.WIDTH, 0,
                                         Tile.WIDTH, Tile.HEIGHT))
            level_2_images.append(surface)

        s_string = "sprites/images/lvl3_texture_sprite_sheet.png"
        sheet = PI.load(s_string).convert()
        level_3_images = []

        for i in range(Tile.SPRITE_SHEET_LENGTH):
            surface = PG.Surface((Tile.WIDTH, Tile.HEIGHT))

            surface.blit(sheet, (0, 0), (i * Tile.WIDTH, 0,
                                         Tile.WIDTH, Tile.HEIGHT))
            level_3_images.append(surface)

        s_string = "sprites/images/lvl4_texture_sprite_sheet.png"
        sheet = PI.load(s_string).convert()
        level_4_images = []

        for i in range(Tile.SPRITE_SHEET_LENGTH):
            surface = PG.Surface((Tile.WIDTH, Tile.HEIGHT))

            surface.blit(sheet, (0, 0), (i * Tile.WIDTH, 0,
                                         Tile.WIDTH, Tile.HEIGHT))
            level_4_images.append(surface)

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

        surface13 = level_3_images[6].copy().convert()
        surface13.set_colorkey(color_key)
        surface13.blit(key, (15, 19))
        level_3_images.append(surface13)

        surface14 = level_4_images[6].copy().convert()
        surface14.set_colorkey(color_key)
        surface14.blit(key, (15, 19))
        level_4_images.append(surface14)

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

        surface23 = level_3_images[6].copy().convert()
        surface23.set_colorkey(color_key)
        surface23.blit(syringe, (0, 0))
        level_3_images.append(surface23)

        surface24 = level_4_images[6].copy().convert()
        surface24.set_colorkey(color_key)
        surface24.blit(syringe, (0, 0))
        level_4_images.append(surface24)

        # create shampoo tile
        shampoo = PI.load("sprites/images/shampoo_sprite.png").convert()
        color_key = shampoo.get_at((0, 0))
        shampoo.set_colorkey(color_key)

        surface31 = level_1_images[6].copy().convert()
        surface31.set_colorkey(color_key)
        surface31.blit(shampoo, (0, 0))
        level_1_images.append(surface31)

        surface32 = level_2_images[6].copy().convert()
        surface32.set_colorkey(color_key)
        surface32.blit(shampoo, (0, 0))
        level_2_images.append(surface32)

        surface33 = level_3_images[6].copy().convert()
        surface33.set_colorkey(color_key)
        surface33.blit(shampoo, (0, 0))
        level_3_images.append(surface33)

        surface34 = level_4_images[6].copy().convert()
        surface34.set_colorkey(color_key)
        surface34.blit(shampoo, (0, 0))
        level_4_images.append(surface34)

        # create pill tile
        pill = PI.load("sprites/images/pill_sprite.png").convert()
        color_key = pill.get_at((0, 0))
        pill.set_colorkey(color_key)

        surface41 = level_1_images[6].copy().convert()
        surface41.set_colorkey(color_key)
        surface41.blit(pill, (0, 0))
        level_1_images.append(surface41)

        surface42 = level_2_images[6].copy().convert()
        surface42.set_colorkey(color_key)
        surface42.blit(pill, (0, 0))
        level_2_images.append(surface42)

        surface43 = level_3_images[6].copy().convert()
        surface43.set_colorkey(color_key)
        surface43.blit(pill, (0, 0))
        level_3_images.append(surface43)

        surface44 = level_4_images[6].copy().convert()
        surface44.set_colorkey(color_key)
        surface44.blit(pill, (0, 0))
        level_4_images.append(surface44)

        # create heart up tile
        heart = PI.load("sprites/images/heart_sprite.png").convert()
        color_key = heart.get_at((0, 0))
        heart.set_colorkey(color_key)

        surface51 = level_1_images[6].copy().convert()
        surface51.set_colorkey(color_key)
        surface51.blit(heart, (0, 0))
        level_1_images.append(surface51)

        surface52 = level_2_images[6].copy().convert()
        surface52.set_colorkey(color_key)
        surface52.blit(heart, (0, 0))
        level_2_images.append(surface52)

        surface53 = level_3_images[6].copy().convert()
        surface53.set_colorkey(color_key)
        surface53.blit(heart, (0, 0))
        level_3_images.append(surface53)

        surface54 = level_4_images[6].copy().convert()
        surface54.set_colorkey(color_key)
        surface54.blit(heart, (0, 0))
        level_4_images.append(surface54)

        # create shield tile
        shield = PI.load("sprites/images/shield_sprite.png").convert()
        color_key = shield.get_at((0, 0))
        shield.set_colorkey(color_key)

        surface61 = level_1_images[6].copy().convert()
        surface61.set_colorkey(color_key)
        surface61.blit(shield, (0, 0))
        level_1_images.append(surface61)

        surface62 = level_2_images[6].copy().convert()
        surface62.set_colorkey(color_key)
        surface62.blit(shield, (0, 0))
        level_2_images.append(surface62)

        surface63 = level_3_images[6].copy().convert()
        surface63.set_colorkey(color_key)
        surface63.blit(shield, (0, 0))
        level_3_images.append(surface63)

        surface64 = level_4_images[6].copy().convert()
        surface64.set_colorkey(color_key)
        surface64.blit(shield, (0, 0))
        level_4_images.append(surface64)

        # create laser tile
        laser = PI.load("sprites/images/laser_sprite.png").convert()
        color_key = laser.get_at((0, 0))
        laser.set_colorkey(color_key)

        surface71 = level_1_images[6].copy().convert()
        surface71.set_colorkey(color_key)
        surface71.blit(laser, (0, 0))
        level_1_images.append(surface71)

        surface72 = level_2_images[6].copy().convert()
        surface72.set_colorkey(color_key)
        surface72.blit(laser, (0, 0))
        level_2_images.append(surface72)

        surface73 = level_3_images[6].copy().convert()
        surface73.set_colorkey(color_key)
        surface73.blit(laser, (0, 0))
        level_3_images.append(surface73)

        surface74 = level_4_images[6].copy().convert()
        surface74.set_colorkey(color_key)
        surface74.blit(laser, (0, 0))
        level_4_images.append(surface74)

        # create the beer tile
        beer = PI.load("sprites/images/beer_sprite.png").convert()
        color_key = beer.get_at((0, 0))
        beer.set_colorkey(color_key)

        surface81 = level_1_images[6].copy().convert()
        surface81.set_colorkey(color_key)
        surface81.blit(beer, (0, 0))
        level_1_images.append(surface81)

        surface82 = level_2_images[6].copy().convert()
        surface82.set_colorkey(color_key)
        surface82.blit(beer, (0, 0))
        level_2_images.append(surface82)

        surface83 = level_3_images[6].copy().convert()
        surface83.set_colorkey(color_key)
        surface83.blit(beer, (0, 0))
        level_3_images.append(surface83)

        surface84 = level_4_images[6].copy().convert()
        surface84.set_colorkey(color_key)
        surface84.blit(beer, (0, 0))
        level_4_images.append(surface84)


        Tile.IMAGES.append(level_1_images)
        Tile.IMAGES.append(level_2_images)
        Tile.IMAGES.append(level_3_images)
        Tile.IMAGES.append(level_4_images)

    def is_wall(self):
        if self.type in Tile.WALL_TILES:
            return True
        else:
            return False

    def is_table(self):
        if self.type in Tile.TABLE_TILES:
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
        if self.type in Tile.KEY_TILES:
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

import Globals as G
import sprites.Tile as Tile
from random import randint
from random import random
from random import choice


class Map(object):

    TILE_WIDTH = 50
    TILE_HEIGHT = 50
    KEY_DICT = None
    KEY_FILENAME = "maps/texts/level_key.txt"
    WIDTH = 0
    HEIGHT = 0
    SUB_WIDTH = 800
    SUB_HEIGHT = 600
    ENEMIES = ['e']
    LEVEL_1_SLIME_RATE = .8
    LEVEL_1_SCI_RATE = .2
    LEVEL_1_BUG_RATE = 0
    LEVEL_1_SS_RATE = 0
    LEVEL_2_SLIME_RATE = .2
    LEVEL_2_SCI_RATE = .7
    LEVEL_2_BUG_RATE = .1
    LEVEL_2_SS_RATE = 0.0
    LEVEL_3_SLIME_RATE = .2
    LEVEL_3_SCI_RATE = .2
    LEVEL_3_BUG_RATE = .6
    LEVEL_3_SS_RATE = 0
    LEVEL_4_SLIME_RATE = 0
    LEVEL_4_SCI_RATE = .2
    LEVEL_4_BUG_RATE = .2
    LEVEL_4_SS_RATE = .6

    # Blank Room is Maps[0],  Stairs, Item, key
    MAPS = None
    MAP_FILE = "maps/texts/map_collection.txt"
    BOSS_MAP_FILE = "maps/texts/boss_map.txt"
    BOSS_MAP = None

    def __init__(self, size, level, player):
        if player is None:
            self.player_items = []
            self.player_activated_item = -1
        else:
            self.player_items = player.items
            self.player_activated_item = player.activated_item
        self.level = level
        self.size = size
        if not Map.KEY_DICT:
            self.load_key_dict()

        if Map.MAPS is None:
            self.read_maps()

        self.tiles = {}
        self.enemy_coords = []
        self.sci_coords = []
        self.bug_coords = []
        self.ss_coords = []
        self.boss_coord = None

        map_matrix = self.create_map(size)

        for row_number, row in enumerate(map_matrix):
            for col_number, sub_map in enumerate(row):
                self.load_sub_map(sub_map, row_number, col_number)

        if self.size == 1:
            print len(self.tiles)
            boss_width = 22
            boss_height = 16
            Map.WIDTH = boss_width*50+50
            Map.HEIGHT = boss_height*50+50
            x = 0
            while x < Map.WIDTH:
                self.tiles.update(
                    {(x, 0): Tile.Tile(x, 0, Map.KEY_DICT['0'], self.level)})
                x += Map.TILE_WIDTH
            y = 0
            while y < Map.HEIGHT:
                self.tiles.update(
                    {(0, y): Tile.Tile(0, y, Map.KEY_DICT['0'], self.level)})
                y += Map.TILE_HEIGHT
            return

        Map.HEIGHT = len(map_matrix) * Map.SUB_HEIGHT + 50
        Map.WIDTH = len(map_matrix[0]) * Map.SUB_WIDTH + 50

        # fill in map
        for k in range(size):
            x = 7 * 50 + k * Map.SUB_WIDTH + 50
            y = 50
            self.tiles.update(
                {(x, y): Tile.Tile(x, y, Map.KEY_DICT['X'], level)})
            x += 50
            self.tiles.update(
                {(x, y): Tile.Tile(x, y, Map.KEY_DICT['X'], level)})
            y = Map.HEIGHT - 50
            self.tiles.update(
                {(x, y): Tile.Tile(x, y, Map.KEY_DICT['0'], level)})
            x -= 50
            self.tiles.update(
                {(x, y): Tile.Tile(x, y, Map.KEY_DICT['0'], level)})

            x = 50
            y = 4 * 50 + k * Map.SUB_HEIGHT + 50
            self.tiles.update(
                {(x, y): Tile.Tile(x, y, Map.KEY_DICT['0'], level)})
            y += 50
            self.tiles.update(
                {(x, y): Tile.Tile(x, y, Map.KEY_DICT['0'], level)})
            y += 50
            self.tiles.update(
                {(x, y): Tile.Tile(x, y, Map.KEY_DICT['0'], level)})
            x = Map.WIDTH - 50
            self.tiles.update(
                {(x, y): Tile.Tile(x, y, Map.KEY_DICT['0'], level)})
            y -= 50
            self.tiles.update(
                {(x, y): Tile.Tile(x, y, Map.KEY_DICT['0'], level)})
            y -= 50
            self.tiles.update(
                {(x, y): Tile.Tile(x, y, Map.KEY_DICT['0'], level)})
        x = 0
        while x < Map.WIDTH:
            self.tiles.update(
                {(x, 0): Tile.Tile(x, 0, Map.KEY_DICT['0'], level)})
            x += Map.TILE_WIDTH
        y = 0
        while y < Map.HEIGHT:
            self.tiles.update(
                {(0, y): Tile.Tile(0, y, Map.KEY_DICT['0'], level)})
            y += Map.TILE_HEIGHT

    def load_key_dict(self):
        Map.KEY_DICT = {}
        level_key_file = open(Map.KEY_FILENAME)
        for line in level_key_file.readlines():
            int_key = int(line[1])
            if line[2].isdigit():
                int_key *= 10
                int_key += int(line[2])
            Map.KEY_DICT.update({line[0]: int_key})
        level_key_file.close()

    def load_sub_map(self, sub_matrix, row_number, col_number):
        for y_index, row in enumerate(sub_matrix):
            for x_index, char in enumerate(row):
                x = x_index * Map.TILE_WIDTH + col_number * \
                    Map.SUB_WIDTH + Map.TILE_WIDTH
                y = y_index * Map.TILE_HEIGHT + row_number * \
                    Map.SUB_HEIGHT + Map.TILE_WIDTH

                if char not in Map.KEY_DICT:
                    new_tile = Tile.Tile(x, y, Map.KEY_DICT['~'], self.level)
                    self.tiles.update({(x, y): new_tile})
                    continue

                if char == 'I':
                    k = choice(Tile.Tile.ITEM_TILES)
                    while (k - 12) in self.player_items or (k - 12) == self.player_activated_item:
                        k = choice(Tile.Tile.ITEM_TILES)
                    new_tile = Tile.Tile(x, y, k, self.level)
                    self.tiles.update({(x, y): new_tile})
                    continue

                if char in Map.ENEMIES:
                    if self.size is 1:
                        self.boss_coord = (x, y)
                    elif self.level is 1:
                        self.choose_enemies(Map.LEVEL_1_SLIME_RATE,
                                       Map.LEVEL_1_SCI_RATE,
                                       Map.LEVEL_1_BUG_RATE,
                                       Map.LEVEL_1_SS_RATE, x, y)
                    elif self.level is 2:
                        self.choose_enemies(Map.LEVEL_2_SLIME_RATE,
                                       Map.LEVEL_2_SCI_RATE,
                                       Map.LEVEL_2_BUG_RATE, 
                                       Map.LEVEL_2_SS_RATE, x, y)
                    elif self.level is 3:
                        self.choose_enemies(Map.LEVEL_3_SLIME_RATE,
                                       Map.LEVEL_3_SCI_RATE,
                                       Map.LEVEL_3_BUG_RATE,
                                       Map.LEVEL_3_SS_RATE, x, y)
                    elif self.level is 4:
                        self.choose_enemies(Map.LEVEL_4_SLIME_RATE,
                                       Map.LEVEL_4_SCI_RATE,
                                       Map.LEVEL_4_BUG_RATE,
                                       Map.LEVEL_4_SS_RATE, x, y)

                if char == 'W':
                    if random() <= .5:
                        char = 'X'

                new_tile = Tile.Tile(x, y, Map.KEY_DICT[char], self.level)
                self.tiles.update({(x, y): new_tile})

    def choose_enemies(self, sRate, sciRate, bugRate, ssRate, x, y):
        r = random()
        if r <= sRate:
            self.enemy_coords.append((x, y))
        elif r <= sciRate+sRate:
            self.sci_coords.append((x, y))
        elif r <= sciRate+sRate+bugRate:
            self.bug_coords.append((x, y))
        elif r <= sciRate+sRate+bugRate+ssRate:
            self.ss_coords.append((x, y))

    def create_map(self, size):
        m = [["v" for x in range(size)] for x in range(size)]
        if size == 1:
            self.level = 1
            m[0][0] = Map.BOSS_MAP            
            return m
        # Add blank room
        m[size - 1][0] = Map.MAPS[0]
        # Add Stair room
        x = randint(0, size - 1)
        y = randint(0, size - 1)
        while m[x][y] is not "v":
            x = randint(0, size - 1)
            y = randint(0, size - 1)
        m[x][y] = Map.MAPS[1]
        # Add Item Room
        while m[x][y] is not "v":
            x = randint(0, size - 1)
            y = randint(0, size - 1)
        if random() < .3:
            # locked item room
            m[x][y] = Map.MAPS[2]
        else:
            # unlocked item room
            m[x][y] = Map.MAPS[3]
        # Add key room
        while m[x][y] is not "v":
            x = randint(0, size - 1)
            y = randint(0, size - 1)
        m[x][y] = Map.MAPS[4]

        for i in range(size):
            for j in range(size):
                if m[i][j] is "v":
                    k = randint(5, len(Map.MAPS) - 1)
                    m[i][j] = Map.MAPS[k]
        return m

    def read_maps(self):
        Map.MAPS = []
        sub_map = []
        mfile = open(Map.MAP_FILE)
        for line in mfile.readlines():
            if line in ['\n']:
                Map.MAPS.append(list(sub_map))
                sub_map = []
            else:
                sub_map.append(line)

        mfile = open(Map.BOSS_MAP_FILE)
        Map.BOSS_MAP = []
        for line in mfile.readlines():
            if line in ['\n']:
                pass                
            else:
                Map.BOSS_MAP.append(line)
        # Map.BOSS_MAP.append(sub_map)

import Globals as G
import sprites.Tile as Tile
from random import randint


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

    # Blank Room is Maps[0],  Stairs, Item, key
    MAPS = None
    MAP_FILE = "maps/texts/map_collection.txt"

    def __init__(self, size):
        self.size = size
        if not Map.KEY_DICT:
            self.load_key_dict()

        if Map.MAPS is None:
            self.read_maps()

        self.tiles = {}
        self.enemy_coords = []

        map_matrix = self.create_map(size)

        for row_number, row in enumerate(map_matrix):
            for col_number, sub_map in enumerate(row):
                self.load_sub_map(sub_map, row_number, col_number)

        Map.HEIGHT = len(map_matrix) * Map.SUB_HEIGHT + 50
        Map.WIDTH = len(map_matrix[0]) * Map.SUB_WIDTH + 50

        # fill in map
        for k in range(size):
            x = 7 * 50 + k * Map.SUB_WIDTH + 50
            y = 50
            self.tiles.update({(x, y): Tile.Tile(x, y, Map.KEY_DICT['X'])})
            x += 50
            self.tiles.update({(x, y): Tile.Tile(x, y, Map.KEY_DICT['X'])})
            y = Map.HEIGHT - 50
            self.tiles.update({(x, y): Tile.Tile(x, y, Map.KEY_DICT['0'])})
            x -= 50
            self.tiles.update({(x, y): Tile.Tile(x, y, Map.KEY_DICT['0'])})

            x = 50
            y = 4 * 50 + k * Map.SUB_HEIGHT + 50
            self.tiles.update({(x, y): Tile.Tile(x, y, Map.KEY_DICT['0'])})
            y += 50
            self.tiles.update({(x, y): Tile.Tile(x, y, Map.KEY_DICT['0'])})
            y += 50
            self.tiles.update({(x, y): Tile.Tile(x, y, Map.KEY_DICT['0'])})
            x = Map.WIDTH - 50
            self.tiles.update({(x, y): Tile.Tile(x, y, Map.KEY_DICT['0'])})
            y -= 50
            self.tiles.update({(x, y): Tile.Tile(x, y, Map.KEY_DICT['0'])})
            y -= 50
            self.tiles.update({(x, y): Tile.Tile(x, y, Map.KEY_DICT['0'])})
        x = 0
        while x < Map.WIDTH:
            self.tiles.update({(x, 0): Tile.Tile(x, 0, Map.KEY_DICT['0'])})
            x += Map.TILE_WIDTH
        y = 0
        while y < Map.HEIGHT:
            self.tiles.update({(0, y): Tile.Tile(0, y, Map.KEY_DICT['0'])})
            y += Map.TILE_HEIGHT

    def load_key_dict(self):
        Map.KEY_DICT = {}
        level_key_file = open(Map.KEY_FILENAME)
        for line in level_key_file.readlines():
            Map.KEY_DICT.update({line[0]: int(line[1])})
        level_key_file.close()

    def load_sub_map(self, sub_matrix, row_number, col_number):
        for y_index, row in enumerate(sub_matrix):
            for x_index, char in enumerate(row):
                x = x_index * Map.TILE_WIDTH + col_number * \
                    Map.SUB_WIDTH + Map.TILE_WIDTH
                y = y_index * Map.TILE_HEIGHT + row_number * \
                    Map.SUB_HEIGHT + Map.TILE_WIDTH

                if char not in Map.KEY_DICT:
                    new_tile = Tile.Tile(x, y, Map.KEY_DICT['~'])
                    self.tiles.update({(x, y): new_tile})
                    continue

                if char in Map.ENEMIES:
                    self.enemy_coords.append((x, y))

                new_tile = Tile.Tile(x, y, Map.KEY_DICT[char])
                self.tiles.update({(x, y): new_tile})

    def create_map(self, size):

        m = [["v" for x in range(size)] for x in range(size)]
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
        m[x][y] = Map.MAPS[2]
        # Add key room
        while m[x][y] is not "v":
            x = randint(0, size - 1)
            y = randint(0, size - 1)
        m[x][y] = Map.MAPS[3]

        for i in range(size):
            for j in range(size):
                if m[i][j] is "v":
                    m[i][j] = Map.MAPS[11]
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

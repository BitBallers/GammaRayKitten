import Globals as G
import Tile

class Map(object):

    TILE_WIDTH = 50
    TILE_HEIGHT = 50
    KEY_DICT = None
    KEY_FILENAME = "Level Key.txt"

    def __init__(self, map_text_file):
        if not KEY_DICT:
            self.load_key_dict()

        self.tiles = {}
        map_file = open(map_text_file)
        self.width = 0
        self.height = 0

        max_width = 0
        max_height = 0
        i = 0
        for line in map_file.readlines():
            k = 0
            for char in line:
                if not char in Map.KEY_DICT:
                    print "Invalid symbol in map file"
                new_x = k*TILE_WIDTH
                new_y = i*TILE_HEIGHT
                new_tile = Tile.Tile(new_x, new_y, Map.KEY_DICT[char])
                self.tiles.update({(new_x, new_y):new_tile})
                if k > max_width:
                    self.width = k
                    max_width = self.width
                k += 1
            if i > max_height:
                self.height = i
                max_height = self.height
            i += 1
        map_file.close()

    def load_key_dict(self):
        Map.KEY_DICT = {}
        level_key_file = open(KEY_FILENAME)
        for line in level_key_file.readlines():
            KEY_DICT.update({line[0]:int(line[1])})
        level_key_file.close()


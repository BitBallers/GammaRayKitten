import Globals as G
import Tile

class Map(object):

    TILE_WIDTH = 50
    TILE_HEIGHT = 50
    KEY_DICT = None
    KEY_FILENAME = "Level Key.txt"
    WIDTH = 0
    HEIGHT = 0

    def __init__(self, map_text_file):
        if not Map.KEY_DICT:
            self.load_key_dict()

        self.tiles = {}
        map_file = open(map_text_file)

        max_width = 0
        max_height = 0
        i = 0
        for line in map_file.readlines():
            k = 0
            for char in line:
                if not char in Map.KEY_DICT:
                    continue
                new_x = k*Map.TILE_WIDTH
                new_y = i*Map.TILE_HEIGHT
                new_tile = Tile.Tile(new_x, new_y, Map.KEY_DICT[char])
                self.tiles.update({(new_x, new_y):new_tile})
                if k > max_width:
                    Map.WIDTH = k
                    max_width = Map.WIDTH
                k += 1
            if i > max_height:
                Map.HEIGHT = i
                max_height = Map.HEIGHT
            i += 1
        map_file.close()
        Map.HEIGHT = Map.HEIGHT*Map.TILE_HEIGHT
        Map.WIDTH = Map.WIDTH*Map.TILE_WIDTH

    def load_key_dict(self):
        Map.KEY_DICT = {}
        level_key_file = open(Map.KEY_FILENAME)
        for line in level_key_file.readlines():
            Map.KEY_DICT.update({line[0]:int(line[1])})
        
        level_key_file.close()


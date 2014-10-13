import Globals as G
import Main

class Camera(object):
    X = None
    Y = None
    
    def __init__(self, x, y, game_state):
        Camera.X = x
        Camera.Y = y
        self.game_state = game_state

    def shift_camera(self, x, y):
        Camera.X += x
        Camera.Y += y
        self.game_state.set_screen_coords_map()


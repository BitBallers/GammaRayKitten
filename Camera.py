import Globals as G

class Camera(object):

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def shift_camera(self, x, y):
        self.x += x
        self.y += y


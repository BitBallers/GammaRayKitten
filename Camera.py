import Globals as G

class Camera(object):
    X = None
    Y = None
    NEW_CAMERA = True
    def __init__(self, x, y):
        Camera.X = x
        Camera.Y = y

    def shift_camera(self, x, y):
        Camera.X += x
        Camera.Y += y
        NEW_CAMERA = True


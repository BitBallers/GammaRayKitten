import game_states.Main as Main

class Globals(object):
    RUNNING = True
    SCREEN = None
    WIDTH = None
    HEIGHT = None
    STATE = None
    INTERVAL = .02
    HUD_HEIGHT = 50

def new_level(player):
	Globals.STATE = Main.Game(2, 4, player)
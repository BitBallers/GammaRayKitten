import game_states.Main as Main
import game_states.CutScene as CutScene
import game_states.GameOver as GameOver


class Globals(object):
    RUNNING = True
    SCREEN = None
    WIDTH = None
    HEIGHT = None
    STATE = None
    INTERVAL = .02
    HUD_HEIGHT = 50


def new_level(player):
    if Main.Game.LEVEL+1 <= Main.Game.MAX_LEVEL:
        if Main.Game.LEVEL+1 < Main.Game.MAX_LEVEL:
            Globals.STATE = CutScene.CutScene(Main.Game.LEVEL+1, 4, player)
        else:
            Globals.STATE = CutScene.CutScene(Main.Game.LEVEL+1, 1, player)
    else:
        Globals.STATE = GameOver.GameOver(True, Main.Game.SCORE)

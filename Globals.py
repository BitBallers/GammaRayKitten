import pygame as PG
import pygame.image as PI
import game_states.Main as Main
import game_states.CutScene as CutScene
import game_states.GameOver as GameOver
import game_states.StoryBoard as StoryBoard


class Globals(object):
    RUNNING = True
    SCREEN = None
    WIDTH = None
    HEIGHT = None
    STATE = None
    INTERVAL = .02
    HUD_HEIGHT = 50
    BRIGHT_INTERVAL = 75
    BUTTONUP = set([PG.KEYUP])
    BUTTONDOWN = set([PG.KEYDOWN])
    JOY_IN_USE = False
    UP = PG.K_w
    DOWN = PG.K_s
    LEFT = PG.K_a
    RIGHT = PG.K_d
    SHOOT_UP = PG.K_UP
    SHOOT_DOWN = PG.K_DOWN
    SHOOT_LEFT = PG.K_LEFT
    SHOOT_RIGHT = PG.K_RIGHT
    ACT_KEY = PG.K_SPACE
    FX_CHANNEL = None
    MUSIC_CHANNEL = None


def new_level(player):
    if Main.Game.LEVEL+1 <= Main.Game.MAX_LEVEL:
        if Main.Game.LEVEL+1 < Main.Game.MAX_LEVEL:
            Globals.STATE = CutScene.CutScene(Main.Game.LEVEL+1, 4, player)
        else:
            images = []
            img_1 = PI.load("sprites/images/enter.jpg").convert()
            img_2 = PI.load("sprites/images/catfight.jpg").convert()
            images.append(img_1)
            images.append(img_2)
            Globals.STATE = StoryBoard.StoryBoard("story_texts/boss_text.txt", 
                                                  images, Main.Game.LEVEL, player)   
    else:
        Globals.STATE = GameOver.GameOver(True, Main.Game.SCORE)

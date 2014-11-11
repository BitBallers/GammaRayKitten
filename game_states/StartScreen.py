import pygame as PG
import pygame.display as PD
import pygame.font as PF
import Globals as G
import pygame.image as PI
import pygame.time as PT
import pygame.mixer as PX
import random as r
import Menu
import State


class StartScreen(State.State):

    FONT = None
    SECFONT = None
    INTERVAL = 10

    def __init__(self):
        State.State.__init__(self)
        # load fonts
        StartScreen.FONT = PF.Font("fonts/red_october.ttf", 40)
        StartScreen.SECFONT = PF.Font("fonts/red_october.ttf", 65)

        self.index = 0

        self.strings1 = []
        self.strings2 = []

        self.strings1.append("HIT SPACE TO CONTINUE")
        self.strings2.append(" GAMMA RAY KITTEN")
        # render surfaces for the strings
        self.surf1 = StartScreen.FONT.render(self.strings1[self.index], True,
                                             (255, 0, 0))
        self.surf2 = StartScreen.SECFONT.render(self.strings2[self.index],
                                                True, (255, 0, 0))

        self.xy1 = ((G.Globals.WIDTH / 2 - self.surf1.get_width() / 2,
                     (G.Globals.HEIGHT / 2 + G.Globals.HEIGHT / 4)
                     + self.surf1.get_height()))
        self.xy2 = ((G.Globals.WIDTH / 2 - self.surf2.get_width() / 2,
                     (G.Globals.HEIGHT / 10)
                     - self.surf1.get_height()))

        self.screen = G.Globals.SCREEN
        self.time = 0
        self.fade_in_value = 0
        self.fade_out_value = 255
        self.fade_value = 75  # adjust this value to get desired fade effect

    def render(self):
        G.Globals.SCREEN.fill((0, 0, 0))
        # G.Globals.SCREEN.blit(self.images[self.index], (0, 0))
        G.Globals.SCREEN.blit(self.surf1, self.xy1)
        if r.random() <= .80:
            G.Globals.SCREEN.blit(self.surf2, self.xy2)

    def event(self, event):
        if event.type == PG.KEYDOWN:
            if event.key == PG.K_SPACE:
                G.Globals.STATE = Menu.Menu()

    def update(self, time):
        pass

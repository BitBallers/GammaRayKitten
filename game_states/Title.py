import pygame as PG
import pygame.font as PF
import Globals as G
import StartScreen
import Menu
import State


class Title(State.State):

    FONT = None
    SECFONT = None
    INTERVAL = .5

    def __init__(self):
        State.State.__init__(self)
        Title.FONT = PF.Font("fonts/Blox.ttf", 100)
        Title.SECFONT = PF.Font("fonts/Red October-Regular.ttf", 60)

        temp_surf = Title.FONT.render("Bit Ballers", True, (255, 255, 255))
        self.init_x = G.Globals.WIDTH / 2 - temp_surf.get_width() / 2
        self.init_y = G.Globals.HEIGHT / 2 - temp_surf.get_height() / 2
        self.strings = [" ", "B", "Bi", "Bit ", "Bit B", "Bit Ba",
                        "Bit Bal", "Bit Ball", "Bit Balle", "Bit Baller",
                        "Bit Ballers", "Bit Ballers"]
        self.surf = Title.FONT.render(self.strings[0], True, (255, 255, 255))

        self.time = 0
        self.index = 1
        self.value = 255

    def render(self):
        G.Globals.SCREEN.fill((0, 0, 0))
        G.Globals.SCREEN.blit(self.surf, (self.init_x, self.init_y))

    def event(self, event):
        if event.type == PG.KEYDOWN:
            G.Globals.STATE = StartScreen.StartScreen()

    def update(self, time):
        self.time += time
        if self.time >= self.index * Title.INTERVAL:
            self.surf = Title.FONT.render(self.strings[self.index],
                                          True, (255, 255, 255))
            self.index += 1
            if self.index >= len(self.strings):
                G.Globals.STATE = StartScreen.StartScreen()

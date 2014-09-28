import pygame.font as PF
import Globals as G
import Menu
import State

class Title(State.State):
    FONT = None
    INTERVAL = .5
    def __init__(self):
        State.State.__init__(self)
        Title.FONT = PF.Font("Blox.ttf", 100)
        
        temp_surf = Title.FONT.render("Bit Ballers", True, (255,255,255))
        self.init_x = G.Globals.WIDTH/2 - temp_surf.get_width()/2
        self.init_y = G.Globals.HEIGHT/2 - temp_surf.get_height()/2
        
        self.strings = [" ", "B", "Bi", "Bit ", "Bit B", "Bit Ba", \
            "Bit Bal", "Bit Ball", "Bit Balle", "Bit Baller", \
            "Bit Ballers", "Bit Ballers"]
        
        self.surf = Title.FONT.render(self.strings[0], True, (255, 255, 255))
        
        self.time = 0
        self.index = 1

    def render(self):
        G.Globals.SCREEN.fill((0, 0, 0))
        G.Globals.SCREEN.blit(self.surf, (self.init_x, self.init_y))

    def update(self, time):
        self.time += time
        if self.time >= self.index * Title.INTERVAL:
            self.surf = Title.FONT.render(self.strings[self.index], True, (255, 255, 255))
            self.index += 1

        if self.index == len(self.strings):
            G.Globals.STATE = Menu.Menu()

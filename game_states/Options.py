import pygame as PG
import pygame.font as PF
import pygame.mouse as PM
import pygame.draw as PD
import pygame.image as PI
import State
import Globals as G
import Menu
import JoySettings
import AdjBright

class Options(State.State):

    FONT = None
    IMAGE = None
    INIT_X = 10
    INIT_Y = 100
    Y_SPACING = 100


    def __init__(self):
        State.State.__init__(self)
        if not Options.FONT:
                Options.FONT = PF.Font("fonts/red_october.ttf", 40)
        self.font = Options.FONT
        self.back_surf = self.font.render("Back", True, (255, 0, 0))
        self.back_x, self.back_y = self.back_surf.get_size()
        self.option_strings = ["Adjust Brightness", "Adjust Sound", 
          "Controller Settings"]
        self.surfs = []
        for i in range(len(self.option_strings)):
                self.surfs.append(self.font.render(self.option_strings[i],
          True, (255, 255, 255)))  
        #self.screen = G.Globals.SCREEN

        self.selected = []
        for i in range(3):
            self.selected.append(False) 

    def render(self):
        G.Globals.SCREEN.fill((0, 0, 0))
        G.Globals.SCREEN.blit(self.back_surf, (0, 0))   

        x_cord = Options.INIT_X
        y_cord = Options.INIT_Y
        y_spacing = Options.Y_SPACING

        for surf in self.surfs:
                G.Globals.SCREEN.blit(surf, (x_cord, y_cord)) 
                y_cord += (surf.get_height() + y_spacing)      

    def update(self, time):
        x_cord = Options.INIT_X
        y_cord = Options.INIT_Y
        y_spacing = Options.Y_SPACING
        for i in range(len(self.option_strings)):
            self.surfs[i] = self.font.render(self.option_strings[i],
                                   True, (255, 255, 255))
            surf = self.surfs[i]
            self.selected[i] = False
            if Menu.Menu.check_mouse(Menu.Menu(), x_cord,
             y_cord, surf.get_width(), surf.get_height()):
                self.surfs[i] = self.font.render(self.option_strings[i],
                                    True, (255, 0, 0))
                self.selected[i] = True
            y_cord += (surf.get_height() + y_spacing)                                                                                          

    def event(self, event):
        if event.type == PG.KEYDOWN and event.key == PG.K_ESCAPE:
                G.Globals.STATE = Menu.Menu()
        if event.type == PG.MOUSEBUTTONDOWN:
                pos = PM.get_pos()
                if pos[0] >= 0 and pos[0] <= self.back_x:
                    if pos[1] >= 0 and pos[1] <= self.back_y:
                            G.Globals.STATE = Menu.Menu()
                if self.selected[0]:
                    G.Globals.STATE = AdjBright.AdjBright()
                if self.selected[1]:
                    G.Globals.STATE = AdjSound.AdjSound()
                if self.selected[2]:
                    G.Globals.STATE = JoySettings.JoySettings()                     
                  





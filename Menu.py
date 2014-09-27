import pygame as PG
import pygame.font as PF
import pygame.color as PC
import grk

class Menu(State):
    FONT = NONE
    def __init__(self):
        State.__init__(self)
        if not Menu.FONT:
            Menu.FONT = PF.Font("Red October-Regular.ttf", 30)
        self.menu_colors

    def render(self):
        grk.Globals.SCREEN.fill(PC.Color("black"))
        surfs = []
        surfs.append(FONT.render("New Game", True, PC.Color("white")))
        surfs.append(FONT.render("Adjust Brightness", True, PC.Color("white")))
        surfs.append(FONT.render("Adjust Sound", True, PC.Color("white")))
        surfs.append(FONT.render("Display Highscores", True, PC.Color("white")))
        surfs.append(FONT.render("Quit", True, PC.Color("white")))


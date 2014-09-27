import pygame as PG
import pygame.font as PF
import pygame.mouse as PM
import Globals as G
import State

class Menu(State.State):
    FONT = None
    def __init__(self):
        State.State.__init__(self)
        if not Menu.FONT:
            Menu.FONT = PF.Font("Red October-Regular.ttf", 30)

        self.menu_strings = ["New Game", "Adjust Brightness", "Adjust Sound", \
            "Display Highscores", "Quit"]

    def render(self):
        G.Globals.SCREEN.fill((0,0,0))
        
        x_cord = 10
        y_cord = 300
        y_spacing = 20

        for i in range(5):
            surf = Menu.FONT.render(self.menu_strings[i], True, (255, 255, 255))
            if self.check_mouse(x_cord, y_cord, surf.get_width(), surf.get_height()):
                surf = Menu.FONT.render(self.menu_strings[i], True, (255, 0, 0))
            G.Globals.SCREEN.blit(surf, (x_cord, y_cord))
            y_cord += (surf.get_height() + y_spacing)

    def update(self, time):
        pass

    def event(self, event):
        pass

    def check_mouse(self, x, y, width, height):
        pos = PM.get_pos()
        if pos[0] >= x and pos[0] <= (x+width):
            pass
        else:
            return False
        if pos[1] >= y and pos[1] <= (y+height):
            return True
        else:
            return False

import pygame as PG
import pygame.font as PF
import pygame.mouse as PM
import Globals as G
import State

class Menu(State.State):
    FONT = None
    INIT_X = 10
    INIT_Y = 300
    Y_SPACING = 30
    def __init__(self):
        State.State.__init__(self)
        if not Menu.FONT:
            Menu.FONT = PF.Font("Red October-Regular.ttf", 30)

        self.menu_strings = ["New Game", "Adjust Brightness", "Adjust Sound", \
            "Display Highscores", "Quit"]
        self.surfs = []
        for i in range(5):
            self.surfs.append(Menu.FONT.render(self.menu_strings[i], True, (255, 255, 255)))
        self.selected = []
        for i in range(5):
            self.selected.append(False)

    def render(self):
        G.Globals.SCREEN.fill((0,0,0))
        
        x_cord = Menu.INIT_X
        y_cord = Menu.INIT_Y
        y_spacing = Menu.Y_SPACING        

        for surf in self.surfs:
            G.Globals.SCREEN.blit(surf, (x_cord, y_cord))
            y_cord += (surf.get_height() + y_spacing)

    def update(self, time):
        x_cord = Menu.INIT_X
        y_cord = Menu.INIT_Y
        y_spacing = Menu.Y_SPACING
        for i in range(5):
            self.surfs[i] = Menu.FONT.render(self.menu_strings[i], True, (255, 255, 255))
            surf = self.surfs[i]
            self.selected[i] = False
            if self.check_mouse(x_cord, y_cord, surf.get_width(), surf.get_height()):
                self.surfs[i] = Menu.FONT.render(self.menu_strings[i], True, (255, 0, 0))
                self.selected[i] = True
            y_cord += (surf.get_height() + y_spacing)

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

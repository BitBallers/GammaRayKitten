import pygame as PG
import pygame.font as PF
import pygame.mouse as PM
import pygame.image as PI
import Globals as G
import State
import Score
import Main
import StoryBoard
import Instructions


class Menu(State.State):

    FONT = None
    TITLEFONT = None
    TITLEIMAGE = None
    IMG_1 = None
    IMG_2 = None
    IMG_3 = None
    IMG_4 = None
    INIT_X = 10
    INIT_Y = 300
    Y_SPACING = 30

    def __init__(self):
        State.State.__init__(self)
        if not Menu.FONT:
            Menu.FONT = PF.Font("fonts/red_october.ttf", 30)
        if not Menu.TITLEFONT:
            Menu.TITLEFONT = PF.Font("fonts/red_october.ttf", 65)
        if not Menu.TITLEIMAGE:
            Menu.TITLEIMAGE = PI.load("sprites/images/menuimage.jpg").convert()
        if not Menu.IMG_1:
            Menu.IMG_1 = PI.load("sprites/images/intro1.jpg").convert()
        if not Menu.IMG_2:
            Menu.IMG_2 = PI.load("sprites/images/intro2.jpg").convert()
        if not Menu.IMG_3:
            Menu.IMG_3 = PI.load("sprites/images/intro3.jpg").convert()
        if not Menu.IMG_4:
            Menu.IMG_4 = PI.load("sprites/images/intro4.jpg").convert()


        self.menu_strings = ["New Game", "Instructions", "Options", 
                            "Display Highscores", "Quit"]
        self.surfs = []
        self.title_surf = Menu.TITLEFONT.render("Gamma Ray Kitten",
                                                True, (0, 255, 0))
        self.image = Menu.TITLEIMAGE
        for i in range(5):
            self.surfs.append(Menu.FONT.render(self.menu_strings[i],
                                               True, (255, 255, 255)))
        self.selected = []
        for i in range(5):
            self.selected.append(False)

        self.images = []
        self.images.append(Menu.IMG_1)
        self.images.append(Menu.IMG_2)
        self.images.append(Menu.IMG_3)
        self.images.append(Menu.IMG_4)    

    def render(self):
        G.Globals.SCREEN.fill((0, 0, 0))
        G.Globals.SCREEN.blit(self.image, (0, 0))
        G.Globals.SCREEN.blit(self.title_surf, (10, 0))
        x_cord = Menu.INIT_X
        y_cord = Menu.INIT_Y
        y_spacing = Menu.Y_SPACING

        for surf in self.surfs:
            # for each surface in self.surf, blit the surface to the
            # screen with an x and y coordinate
            G.Globals.SCREEN.blit(surf, (x_cord, y_cord))
            # increment the y coordinate by the height of the current surface
            # and the y-spacing
            y_cord += (surf.get_height() + y_spacing)

    def update(self, time):
        x_cord = Menu.INIT_X
        y_cord = Menu.INIT_Y
        y_spacing = Menu.Y_SPACING
        for i in range(5):
            self.surfs[i] = Menu.FONT.render(self.menu_strings[i],
                                             True, (255, 255, 255))
            surf = self.surfs[i]
            self.selected[i] = False
            if self.check_mouse(x_cord, y_cord, surf.get_width(),
                                surf.get_height()):
                self.surfs[i] = Menu.FONT.render(self.menu_strings[i],
                                                 True, (255, 0, 0))
                self.selected[i] = True
            y_cord += (surf.get_height() + y_spacing)

    def event(self, event):
        if event.type == PG.MOUSEBUTTONDOWN:
            if self.selected[0]:
                G.Globals.STATE = StoryBoard.StoryBoard("story_texts/intro.txt", self.images)
            if self.selected[1]:
                G.Globals.STATE = Instructions.Instructions()   
            if self.selected[3]:
                G.Globals.STATE = Score.Score()    
            if self.selected[4]:
                G.Globals.RUNNING = False

    def check_mouse(self, x, y, width, height):
        pos = PM.get_pos()
        if pos[0] >= x and pos[0] <= (x + width):
            pass
        else:
            return False
        if pos[1] >= y and pos[1] <= (y + height):
            return True
        else:
            return False

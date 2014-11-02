import pygame as PG
import pygame.font as PF
import pygame.mouse as PM
import pygame.image as PI
import Globals as G
import State
import Score
import Main
import Intro


class Menu(State.State):

    FONT = None
    TITLEFONT = None
    IMAGE = None
    INIT_X = 10
    INIT_Y = 300
    Y_SPACING = 30

    def __init__(self):
        State.State.__init__(self)
        if not Menu.FONT: # if no font is loaded, load a font
            Menu.FONT = PF.Font("fonts/red_october.ttf", 30)
        if not Menu.TITLEFONT: # if no font for title is loaded, load a title font
            Menu.TITLEFONT = PF.Font("fonts/red_october.ttf", 65)
        """if not Menu.IMAGE:
            Menu.IMAGE = PI.load("sprites/images/cat1.jpg").convert()"""

        self.menu_strings = ["New Game", "Adjust Brightness", "Adjust Sound",
                             "Display Highscores", "Quit"] # put the strings to be rendered to the string in menu_strings arrayh
        self.surfs = [] # create an array to store the surfaces
        self.title_surf = Menu.TITLEFONT.render("Gamma Ray Kitten",
                                                True, (0, 255, 0)) # set title surface to the rendered text
        """self.image = Menu.IMAGE # sets the menu's image to the loaded image"""
        for i in range(5):
            self.surfs.append(Menu.FONT.render(self.menu_strings[i], # for each text string in menu_strings, append it to surf array
                                               True, (255, 255, 255)))
        self.selected = [] # create array to keep track of whether text is selected or not
        for i in range(5):
            self.selected.append(False) # set wordIsSelected initially to False

    def render(self):
        G.Globals.SCREEN.fill((0, 0, 0)) # makes the screen black
        # G.Globals.SCREEN.blit(self.image, (0, 0)) # blit image under all other surfaces
        G.Globals.SCREEN.blit(self.title_surf, (10, 0)) # blit the title surface to the screen
        x_cord = Menu.INIT_X # sets x-coordinate to the Menu's initial x-coordinate
        y_cord = Menu.INIT_Y # sets y-coordinate to the Menu's initial y-coordinate
        y_spacing = Menu.Y_SPACING # sets spacing variable that determines how far away words
        
        # will be in menu
        for surf in self.surfs: 
            # for each surface in self.surf, blit the surface to the 
            # screen with an x and y coordinate
            G.Globals.SCREEN.blit(surf, (x_cord, y_cord))
            # increment the y coordinate by the height of the current surface
            # and the y-spacing 
            y_cord += (surf.get_height() + y_spacing)


    def update(self, time):
        x_cord = Menu.INIT_X # reset the x coordinate 
        y_cord = Menu.INIT_Y # reset the y coordinate
        y_spacing = Menu.Y_SPACING # reset the spacing variable for y coordinate
        for i in range(5):
            # set each cell in surface array to the rendered string in menu_strings array
            self.surfs[i] = Menu.FONT.render(self.menu_strings[i],
                                             True, (255, 255, 255))
            surf = self.surfs[i] # set current surface in surf array to surface variable
            self.selected[i] = False # set boolean for wordIsSelected to False
            if self.check_mouse(x_cord, y_cord, surf.get_width(),
                                surf.get_height()): # checks to see if the mouse is on the text surface
                self.surfs[i] = Menu.FONT.render(self.menu_strings[i], # rerender the text surface as green
                                                 True, (255, 0, 0))
                self.selected[i] = True # boolean for wordIsSelected gets True
            y_cord += (surf.get_height() + y_spacing) # increase y coordinate to examine next text surface

    def event(self, event):
        if event.type == PG.MOUSEBUTTONDOWN:
            if self.selected[0]: # if the first menu option is selected, start the intro the game
                G.Globals.STATE = Intro.Intro()
            if self.selected[4]: # if the last option (quit) is selected, stop the program
                G.Globals.RUNNING = False
            if self.selected[3]: # if the fourth option (display highscores) is selected, start the score state
                G.Globals.STATE = Score.Score()

    def check_mouse(self, x, y, width, height):
        pos = PM.get_pos() # gets position of the mouse on the screen
        if pos[0] >= x and pos[0] <= (x + width): # checks to see if mouse is in x range of text surface
            pass # do nothing/ the mouse has "passed the first test"
        else:
            return False # if not in this range, return false
        if pos[1] >= y and pos[1] <= (y + height): # checks to see if mouse is in y range of text surface
            return True # if method has gotten this far, the mouse is both in the x and y ranges, i.e. is on the text surface
        else:
            return False # if not in this range, return false

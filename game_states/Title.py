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
        Title.FONT = PF.Font("fonts/Blox.ttf", 100) # set the font for the title
        Title.SECFONT = PF.Font("fonts/Red October-Regular.ttf", 60) # set the font for the subtitle

        temp_surf = Title.FONT.render("Bit Ballers", True, (255, 255, 255))
        self.init_x = G.Globals.WIDTH / 2 - temp_surf.get_width() / 2 # set the initial x coordinate for the text
        self.init_y = G.Globals.HEIGHT / 2 - temp_surf.get_height() / 2 # set the initial y coordinate for the text
        self.strings = [" ", "B", "Bi", "Bit ", "Bit B", "Bit Ba",
                        "Bit Bal", "Bit Ball", "Bit Balle", "Bit Baller",
                        "Bit Ballers", "Bit Ballers"] # the array of strings to be rendered sequentially
        self.surf = Title.FONT.render(self.strings[0], True, (255, 255, 255)) # set the initial surface to the empty string

        self.time = 0 
        self.index = 1
        self.value = 255

    def render(self):
        G.Globals.SCREEN.fill((0, 0, 0)) 
        G.Globals.SCREEN.blit(self.surf, (self.init_x, self.init_y))

    def event(self, event):
        if event.type == PG.KEYDOWN: # if a button is pressed, switch to menu state
            G.Globals.STATE = StartScreen.StartScreen()

    def update(self, time):
        self.time += time 
    #    if self.index < 0: # if all letters of title have been rendered
    #        self.value -= self.time # letters start at 255(green) but decrement to get fadeout effect
    #        if self.value <= 0: # if the letters have faded all the way to black (0)
    #            G.Globals.STATE = StartScreen.StartScreen() # go to start screen state
    #        else:
    #            # otherwise, continue to render image with new value
    #            self.surf = Title.SECFONT.render("Gamma Ray Kit         ten",
    #                                             True, (0, self.value, 0)) 
    #    elif self.index == len(self.strings): # checks to see if all letters have been rendered
    #        lsurf = Title.SECFONT.render("Gamma Ray Kitten", True, (0, 255, 0)) # create new temp surface of rendered text
    #        l_x = G.Globals.WIDTH / 2 - lsurf.get_width() / 2 # set temp x coordinate for the text
    #        l_y = G.Globals.HEIGHT / 2 - lsurf.get_height() / 2 # set temp y coordinate for text
    #        self.surf = lsurf # set the main surface to the text surface
    #        self.init_x = l_x # set the initial x coordinate to temp x coordinate
    #        self.init_y = l_y # set the initial y coordinate to temp y coordinate
    #        self.index = -1 # set the index to -1
    #        self.time = 0 # set the time of the state to 0
        if self.time >= self.index * Title.INTERVAL: # checks to see if time is >= index * interval of state
            self.surf = Title.FONT.render(self.strings[self.index],
                                          True, (255, 255, 255)) # render the string in the string array with the given index
            self.index += 1 # increment
            if self.index >= len(self.strings):
                G.Globals.STATE = StartScreen.StartScreen()

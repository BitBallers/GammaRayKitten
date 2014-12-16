import pygame as PG
import sys as SYS
import pygame.font as PF
import pygame.image as PI
import pygame.mixer as PX
import Globals as G
import State
import Main


class StoryBoard(State.State):

    FONT = None
    LENGTH = 7

    def __init__(self, level, filename, images = []):
        State.State.__init__(self)
        StoryBoard.FONT = PF.Font("fonts/red_october.ttf", 18)

        self.images = images
        self.index = -1
        self.time = 0
        self.level = level

        self.fadein = 0
        self.fadeout = 255
        self.fade_value = 100

        try:
            text_file = open(filename, 'r')
        except:
            print "ERROR: Text file failed to load."
            SYS.exit()

        self.strings1, self.strings2 = \
            StoryBoard.parse_strings(self, text_file)

    def render(self):
        G.Globals.SCREEN.fill((0, 0, 0))
        if self.index == -1:
            return
        G.Globals.SCREEN.blit(self.images[self.index], (0, 0))
        G.Globals.SCREEN.blit(self.surf1, self.xy1)
        G.Globals.SCREEN.blit(self.surf2, self.xy2)

    def update(self, time):
        if self.index == -1:
            self.index = 0
        self.time += time
        self.fadein += time * self.fade_value  # controls fade in time
        if self.fadein <= 255:  # values over 255 do not matter
            self.images[self.index].set_alpha(self.fadein)
            self.surf1 = StoryBoard.FONT.render(self.strings1[self.index], True,
                                               (self.fadein, 0, 0))
            self.surf2 = StoryBoard.FONT.render(self.strings2[self.index], True,
                                               (self.fadein, 0, 0))

        # begin to fade out if time has reached point
        # that is >= the fade in time
        if StoryBoard.LENGTH - (self.time % StoryBoard.LENGTH) \
                <= 255 / self.fade_value + 1:
            # controls the fade out time
            self.fadeout -= time * self.fade_value
            if self.fadeout >= 0:
                # if not the last image, fade out
                if self.index != len(self.images):
                    self.images[self.index].set_alpha(self.fadeout)
                    self.surf1 = StoryBoard.FONT.render(self.strings1[self.index],
                                                   True, (self.fadeout, 0, 0))
                    self.surf2 = StoryBoard.FONT.render(self.strings2[self.index],
                                                   True, (self.fadeout, 0, 0))

        # decides whether or not it is time to change the image
        if self.time >= (self.index + 1) * StoryBoard.LENGTH:
            if self.index + 1 < len(self.images):
                self.index += 1
                # we changed images so we reset values
                self.fadein = 0
                self.fadeout = 255
                self.images[self.index].set_alpha(self.fadein)
            else:
                if self.level == 4:
                    G.Globals.STATE = Main.Game(self.level+1, 1)
                else:
                    G.Globals.STATE = Main.Game(self.level)    

        self.xy1 = ((400 - self.surf1.get_width() / 2,
                     500 - self.surf1.get_height()))
        self.xy2 = ((400 - self.surf2.get_width() / 2,
                     500 + self.surf2.get_height()))
        G.Globals.SCREEN.blit(self.images[self.index], (0, 0))
        G.Globals.SCREEN.blit(self.surf1, self.xy1)
        G.Globals.SCREEN.blit(self.surf2, self.xy2)

    def event(self, event):
        if event.type == PG.KEYDOWN:
            #G.Globals.STATE = Main.Game(self.level)
            if self.level == 4:
                G.Globals.STATE = Main.Game(self.level+1, 1)
            else:
                G.Globals.STATE = Main.Game(self.level) 

    def parse_strings(self, text_file):

        s = text_file.readline()
        if s[0] == '/':
            list_length = int(s[1])
        else:
            print "ERROR: Incorrect text file format"
            PG.quit()   

        string_list = [None] * list_length  
        # go through each line to create strings lists
        for line in text_file:
            # first line
            if line[0] == '/':
                continue
            # tells which string list to add to 
            index = int(line[0])-1
            # if no list, create new one
            if string_list[index] is None:
                line = line[1:len(line)-1]
                strings = []
                strings.append(line)
                string_list[index] = strings
            else:
                line = line[1:len(line)-1]
                string_list[index].append(line)

        return string_list  
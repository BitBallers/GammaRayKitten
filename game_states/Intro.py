import pygame as PG
import pygame.font as PF
import pygame.image as PI
import pygame.mixer as PX
import Globals as G
import State
import Main


class Intro(State.State):

    FONT = None
    LENGTH = 3

    def __init__(self):
        State.State.__init__(self)
        PX.stop()
        """self.sound = PX.Sound("music/march.wav")
        self.sound.play()"""
        Intro.FONT = PF.Font("fonts/red_october.ttf", 18)
        """img_1 = PI.load("sprites/images/cat1.jpg").convert() # change when at arrives
        img_2 = PI.load("sprites/images/cat2.jpg").convert() # change when art arrives
        img_3 = PI.load("sprites/images/cat3.jpg").convert() # change when art arrives
        img_4 = img_1 # change when art arrives
        img_5 = img_2 # change when art arrives"""
        self.strings1 = []
        self.strings2 = []
        self.images = []
        self.index = 0
        self.time = 0

        self.strings1.append("Scientists performing radioactive " +
                             "experimentation")
        self.strings2.append("on animals, have made a grave mistake.")

        self.strings1.append("Through a flawed experiment, a powerful, " +
                             "radioactive")
        self.strings2.append("kitten was created. Known as Gamma Ray Kitten.")

        self.strings1.append("It is now your task to guide Gamma Ray Kitten " +
                             "out of the building")
        self.strings2.append("and into the free world. For he is now " +
                             "a sentient being.")

        self.strings1.append("Make your way down the building by " +
                             "locating the keys on each floor.")
        self.strings2.append("Then, unlock the doors to the " +
                             "next level of the building!")

        self.strings1.append("Move Gamma Ray Kitten with WASD.")
        self.strings2.append("Attack directionally with the arrow keys.")

        """self.images.append(img_1)
        self.images.append(img_2)
        self.images.append(img_3)
        self.images.append(img_4)
        self.images.append(img_5)"""

        self.surf1 = Intro.FONT.render(self.strings1[self.index], True,
                                       (255, 0, 0))
        self.surf2 = Intro.FONT.render(self.strings2[self.index], True,
                                       (255, 0, 0))
        self.xy1 = ((400 - self.surf1.get_width() / 2,
                     300 - self.surf1.get_height()))
        self.xy2 = ((400 - self.surf2.get_width() / 2,
                     300 + self.surf2.get_height()))
        self.fadein = 0
        self.fadeout = 255

    def render(self):
        G.Globals.SCREEN.fill((0, 0, 0))
        # G.Globals.SCREEN.blit(self.images[self.index], (0, 0))
        G.Globals.SCREEN.blit(self.surf1, self.xy1)
        G.Globals.SCREEN.blit(self.surf2, self.xy2)

    def update(self, time):
        self.time += time
        if self.time >= Intro.LENGTH:
            if self.index < len(self.strings1)-1:
                self.index += 1
            elif self.index == len(self.strings1)-1:
                G.Globals.STATE = Main.Game()
            self.time = 0

        self.surf1 = Intro.FONT.render(self.strings1[self.index], True,
                                       (255, 0, 0))
        self.surf2 = Intro.FONT.render(self.strings2[self.index], True,
                                       (255, 0, 0))
        self.xy1 = ((400 - self.surf1.get_width() / 2,
                     300 - self.surf1.get_height()))
        self.xy2 = ((400 - self.surf2.get_width() / 2,
                     300 + self.surf2.get_height()))

    def event(self, event):
        if event.type == PG.KEYDOWN:
            G.Globals.STATE = Main.Game()

import pygame as PG
import pygame.font as PF
import pygame.image as PI
import pygame.mixer as PX
import Globals as G
import State
import Main


class Intro(State.State):

    FONT = None
    LENGTH = 7

    def __init__(self):
        State.State.__init__(self)
        PX.stop()
        """self.sound = PX.Sound("music/march.wav")
        self.sound.play()"""
        Intro.FONT = PF.Font("fonts/red_october.ttf", 18)
        img_1 = PI.load("sprites/images/intro1.jpg").convert() # change when at arrives
        img_2 = PI.load("sprites/images/intro2.jpg").convert() # change when art arrives
        img_3 = PI.load("sprites/images/intro3.jpg").convert() # change when art arrives
        img_4 = PI.load("sprites/images/intro4.jpg").convert()
       # img_5 = img_2 # change when art arrives"""
        self.strings1 = []
        self.strings2 = []
        self.images = []
        self.index = 0
        self.time = 0

        self.strings1.append("In a secret government lab, deep" +
                            "within a deserted Russian town,")
        self.strings2.append("Scientists concocted experiments on" +
                            " a large group of specimens.")

        self.strings1.append("Through a series of radioactive experiments" +
                            " and countless injections")
        self.strings2.append("a powerful new age weapon was created.")

        self.strings1.append("A fierce creature, the product of science" +
                             " and one's worst fears")
        self.strings2.append("was brought into this world as a dangerous " +
                             "and sentient being.")

        self.strings1.append("It is now time for you to make your escape" +
                            "from the lab,")
        self.strings2.append("for you are now, the Gamma Ray Kitten.")

        self.images.append(img_1)
        self.images.append(img_2)
        self.images.append(img_3)
        self.images.append(img_4)
        #self.images.append(img_5)

        self.surf1 = Intro.FONT.render(self.strings1[self.index], True,
                                       (255, 0, 0))
        self.surf2 = Intro.FONT.render(self.strings2[self.index], True,
                                       (255, 0, 0))
        self.xy1 = ((400 - self.surf1.get_width() / 2,
                     500 - self.surf1.get_height()))
        self.xy2 = ((400 - self.surf2.get_width() / 2,
                     500 + self.surf2.get_height()))

        self.fadein = 0
        self.fadeout = 255
        self.fade_value = 100

    def render(self):
        G.Globals.SCREEN.fill((0, 0, 0))
        G.Globals.SCREEN.blit(self.images[self.index], (0, 0))
        G.Globals.SCREEN.blit(self.surf1, self.xy1)
        G.Globals.SCREEN.blit(self.surf2, self.xy2)

    def update(self, time):
        self.time += time
        self.fadein += time * self.fade_value # controls fade in time
        if self.fadein <= 255: # values over 255 do not matter
            self.images[self.index].set_alpha(self.fadein)
            self.surf1 = Intro.FONT.render(self.strings1[self.index], True,
                                             (self.fadein, 0, 0))
            self.surf2 = Intro.FONT.render(self.strings2[self.index], True,
                                             (self.fadein, 0, 0))

        # begin to fade out if time has reached point 
        # that is >= the fade in time
        if Intro.LENGTH - (self.time % Intro.LENGTH) \
            <= 255/self.fade_value + 1:
            # controls the fade out time
            self.fadeout -= time * self.fade_value 
            if self.fadeout >= 0:
                # if not the last image, fade out
                if self.index != len(self.images): 
                    self.images[self.index].set_alpha(self.fadeout)
                    self.surf1 = Intro.FONT.render(self.strings1[self.index], True,
                                             (self.fadeout, 0, 0))
                    self.surf2 = Intro.FONT.render(self.strings2[self.index], True,
                                             (self.fadeout, 0, 0))


        # decides whether or not it is time to change the image
        if self.time >= (self.index+1) * Intro.LENGTH:
            if self.index + 1 < len(self.images):
                self.index += 1
                # we changed images so we reset values
                self.fadein = 0
                self.fadeout = 255
                self.images[self.index].set_alpha(self.fadein)
            else:
                G.Globals.STATE = Main.Game(1)   

        self.xy1 = ((400 - self.surf1.get_width() / 2,
                     500 - self.surf1.get_height()))
        self.xy2 = ((400 - self.surf2.get_width() / 2,
                     500 + self.surf2.get_height()))    
        G.Globals.SCREEN.blit(self.images[self.index], (0, 0))
        G.Globals.SCREEN.blit(self.surf1, self.xy1)
        G.Globals.SCREEN.blit(self.surf2, self.xy2)                  

    def event(self, event):
        if event.type == PG.KEYDOWN:
            G.Globals.STATE = Main.Game(1)

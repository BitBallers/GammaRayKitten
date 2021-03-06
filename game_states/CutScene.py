import pygame as PG
import Globals as G
import pygame.image as PI
import State
import Main
import StoryBoard
import Globals as G


class CutScene(State.State):

    IMAGE = None
    SCROLL_SPEED = 15
    INTERVAL = 1

    def __init__(self, level, size, player):
        State.State.__init__(self)
        G.play_amb()
        # loads image if not already
        if not CutScene.IMAGE:
            CutScene.IMAGE = PI.load("sprites/images/down.jpg").convert()
        self.image = CutScene.IMAGE
        # lets us know when to fade in
        self.fade_in = True
        # the x variable of the black shade surface
        self.dx = G.Globals.WIDTH
        # the x, y top left positions
        self.x = 0
        self.y = 0
        self.time = 0
        # surface that shades over image to create sliding effect
        self.slide_surface = PG.Surface((self.dx, G.Globals.HEIGHT +
                                         G.Globals.HUD_HEIGHT))
        self.level = level
        self.size = size
        self.player = player   
        if level == 5:
            images = []
            img_1 = PI.load("sprites/images/enter.jpg").convert()
            img_2 = PI.load("sprites/images/catfight.jpg").convert()
            images.append(img_1)
            images.append(img_2)
            G.Globals.STATE = StoryBoard.StoryBoard("story_texts/boss_text.txt",
                                                  images)     

    def render(self):
        G.Globals.SCREEN.fill((0, 0, 0))
        self.slide_surface.fill((0, 0, 0))
        G.Globals.SCREEN.blit(self.image, (0, 0))
        G.Globals.SCREEN.blit(self.slide_surface, (self.x, self.y))

    def event(self, event):
        if event.type == PG.KEYDOWN:
            if event.key == PG.K_SPACE:                
                G.Globals.STATE = Main.Game(self.level, self.size, self.player)

    def update(self, time):

        self.time += time
        # fade in the image by decreasing rect of black surface
        if self.fade_in:
            self.dx -= CutScene.SCROLL_SPEED
            self.x += CutScene.SCROLL_SPEED
        # if x value or dx is out of range, reset values to fade out
        if self.x >= G.Globals.WIDTH or self.dx <= 0:
            self.fade_in = False
            self.x = 0
            self.dx = 0
        # sets how long the image stays on the screen
        # change this by changing right side of boolean
        if self.time > CutScene.INTERVAL + CutScene.SCROLL_SPEED:
            self.dx += CutScene.SCROLL_SPEED
            if self.dx > G.Globals.WIDTH:
                G.Globals.STATE = Main.Game(self.level, self.size, self.player)

        self.slide_surface = PG.Surface((self.dx, G.Globals.HEIGHT +
                                         G.Globals.HUD_HEIGHT))
        G.Globals.SCREEN.blit(self.slide_surface, (self.x, self.y))

import pygame as PG
import pygame.font as PF
import pygame.mouse as PM
import pygame.image as PI
import State
import Globals as G
import Menu

class Instructions(State.State):

    IMAGE = None

    def __init__(self):
        State.State.__init__(self)
        if not Instructions.IMAGE:    
              Instructions.IMAGE = PI.load("sprites/images/instructions.jpg") \
                                         .convert()
        self.image = Instructions.IMAGE    

        self.font = PF.Font("fonts/red_october.ttf", 42)    
        self.back_surf = self.font.render("Back", True, (255, 0, 0))
        self.back_x, self.back_y = self.back_surf.get_size()

    def render(self):
        G.Globals.SCREEN.fill((0, 0, 0))
        G.Globals.SCREEN.blit(self.image, (0, 0))
        G.Globals.SCREEN.blit(self.back_surf, (0, 0))

    def update(self, time):
        pass

    def event(self, event):
        if event.type == PG.KEYDOWN and event.key == PG.K_ESCAPE:
            G.Globals.STATE = Menu.Menu()
        if event.type == PG.MOUSEBUTTONDOWN:
            pos = PM.get_pos()
            if pos[0] >= 0 and pos[0] <= self.back_x:
                if pos[1] >= 0 and pos[1] <= self.back_y:
                    G.Globals.STATE = Menu.Menu()        
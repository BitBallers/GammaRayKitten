import sys as SYS
import pygame as PG
import pygame.display as PD
import pygame.event as PE
import pygame.font as PF
import pygame.sprite as PS
import pygame.image as PI
import pygame.time as PT
import pygame.color as PC
import pygame.mixer as PX
import pygame.mouse as PM
import State
import Globals as G
import Menu


class Score(State.State):

    def __init__(self):
        State.State.__init__(self)
        title_font = PF.Font("fonts/GUEVARA.ttf", 42)
        main_font = PF.Font(None, 22)
        scores = []
        with open('scores.txt') as open_file:
            for line in open_file:
                scores.append(line)
        color = PC.Color("white")
        self.title_surf = title_font.render("High Scores", True, color)
        self.back_surf = title_font.render("Back", True, (255, 0, 0))
        self.back_x, self.back_y = self.back_surf.get_size()
        self.score_surf = []
        for score in scores:
            self.score_surf.append(main_font.render(score.rstrip(),
                                                    True, color))

    def render(self):
        G.Globals.SCREEN.fill(PC.Color("black"))
        width, height = self.title_surf.get_size()
        G.Globals.SCREEN.blit(self.title_surf,
                              (G.Globals.WIDTH / 2 - width / 2, height))
        G.Globals.SCREEN.blit(self.back_surf, (0, 0))
        c_height = 3 * height
        for score in self.score_surf:
            width, height = score.get_size()
            G.Globals.SCREEN.blit(score,
                                  (G.Globals.WIDTH / 2 - width / 2, c_height))
            c_height += height * 1.5
            if c_height > G.Globals.HEIGHT:
                break

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

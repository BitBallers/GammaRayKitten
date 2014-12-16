import pygame as PG
import pygame.font as PF
import pygame.draw as PD
import Globals as G
import Options
import Menu
import State

class AdjBright(State.State):

    FONT = None
    SECFONT = None
    BRIGHT_INTERVAL = 75
    FADEOUT = .5

    def __init__(self):
        State.State.__init__(self)
        if not AdjBright.FONT:
            AdjBright.FONT = PF.Font("fonts/red_october.ttf", 20)
        self.font = AdjBright.FONT
        if not AdjBright.SECFONT:
            AdjBright.SECFONT = PF.Font("fonts/red_october.ttf", 40)
        self.font2 = AdjBright.SECFONT
        self.save_surf = self.font2.render("Save", True, (255, 255, 255))
        self.save_x, self.save_y = self.save_surf.get_size()
        self.instructions = self.font.render("Click a square to" + 
               " adjust brightness.", True, (255, 255, 255))
        self.color1 = (255, 255, 255)
        self.color2 = (255, 255, 255)
        self.color3 = (255, 255, 255)
        self.interval = AdjBright.BRIGHT_INTERVAL
        self.interval_surf = self.font.render(str(self.interval),
        True, (255, 255, 255))
        self.time = 0
        self.fadeout = AdjBright.FADEOUT

    def render(self):
        G.Globals.SCREEN.fill((0, 0, 0))
        G.Globals.SCREEN.blit(self.instructions, 
           (G.Globals.WIDTH/2-self.instructions.get_width()/2, 10))
        PD.rect(G.Globals.SCREEN, (self.color1), 
                (340, 40, 20, 20))
        PD.rect(G.Globals.SCREEN, (self.color2),
                (430, 40, 20, 20))
        self.interval_surf = self.font.render(str(self.interval),
        True, (255, 255, 255))
        G.Globals.SCREEN.blit(self.interval_surf, (380, 40))
        G.Globals.SCREEN.blit(self.save_surf, 
            (G.Globals.WIDTH-(self.save_x+20), G.Globals.HEIGHT))

    def event(self, event):
        if event.type == PG.MOUSEBUTTONDOWN:
            if Menu.Menu.check_mouse(Menu.Menu(),
                340, 40, 20, 20):
                self.color1 = (0, 255, 0)
                if (self.interval + 1) <= 100: 
                    self.interval -= 1
            elif Menu.Menu.check_mouse(Menu.Menu(),
                 430, 40, 20, 20):
                 self.color2 = (255, 0, 0)
                 if (self.interval - 1) >= 0:
                     self.interval += 1
            elif Menu.Menu.check_mouse(Menu.Menu(), 
                     G.Globals.WIDTH-(self.save_x+20), G.Globals.HEIGHT,
                     self.save_surf.get_width(), self.save_surf.get_height()):
                         G.Globals.STATE = Options.Options()     
    def update(self, time):
        if self.interval > AdjBright.BRIGHT_INTERVAL:  
            self.time += time *1000
            if self.time <= 255:
                self.color1 = (self.time, 255, self.time)  
            elif self.time > 255:
                self.time = 0         
                AdjBright.BRIGHT_INTERVAL = self.interval
                G.Globals.BRIGHT_INTERVAL = AdjBright.BRIGHT_INTERVAL
        elif self.interval < AdjBright.BRIGHT_INTERVAL:
            self.time += time *1000
            if self.time <= 255:
                self.color2 = (255, self.time, self.time)  
            elif self.time > 255:
                self.time = 0
                AdjBright.BRIGHT_INTERVAL = self.interval
                G.Globals.BRIGHT_INTERVAL = AdjBright.BRIGHT_INTERVAL         
        elif Menu.Menu.check_mouse(Menu.Menu(),
            G.Globals.WIDTH-(self.save_x+20), G.Globals.HEIGHT,
            self.save_surf.get_width(), self.save_surf.get_height()):
            self.color3 = ((0, 255, 0))
        else:
            self.color3 = ((255, 255, 255))    
        self.save_surf = self.font2.render("Save", True,
                                         (self.color3))              
        
            





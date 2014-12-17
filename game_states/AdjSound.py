import pygame as PG
import pygame.font as PF
import pygame.draw as PD
import Globals as G
import Options
import Menu
import State

class AdjSound(State.State):

    FONT = None
    SECFONT = None
    FADEOUT = .5

    def __init__(self):
        State.State.__init__(self)
        if not AdjSound.FONT:
            AdjSound.FONT = PF.Font("fonts/red_october.ttf", 20)
        self.font = AdjSound.FONT
        if not AdjSound.SECFONT:
            AdjSound.SECFONT = PF.Font("fonts/red_october.ttf", 40)
        self.font2 = AdjSound.SECFONT
        self.save_surf = self.font2.render("Save", True, (255, 255, 255))
        self.save_x, self.save_y = self.save_surf.get_size()
        self.instructions = self.font.render("Adjust sound FX volume", True, (255, 255, 255))
        self.instructions2 = self.font.render("Adjust Music Volume", True, (255, 255, 255))
        self.color1 = (255, 255, 255)
        self.color2 = (255, 255, 255)
        self.color3 = (255, 255, 255)
        self.interval_surf = self.font.render(str(G.Globals.FX_VOL),
            True, (255, 255, 255))
        self.time = 0        

    def render(self):
        G.Globals.SCREEN.fill((0, 0, 0))
        G.Globals.SCREEN.blit(self.instructions, 
           (G.Globals.WIDTH/2-self.instructions.get_width()/2, 10))
        G.Globals.SCREEN.blit(self.instructions2, 
           (G.Globals.WIDTH/2-self.instructions2.get_width()/2, 70))
        PD.rect(G.Globals.SCREEN, (self.color1), 
                (340, 40, 20, 20))
        PD.rect(G.Globals.SCREEN, (self.color2),
                (430, 40, 20, 20))
        PD.rect(G.Globals.SCREEN, (self.color1), 
                (340, 100, 20, 20))
        PD.rect(G.Globals.SCREEN, (self.color2),
                (430, 100, 20, 20))
        self.interval_surf = self.font.render(str(G.Globals.FX_VOL),
            True, (255, 255, 255))
        G.Globals.SCREEN.blit(self.interval_surf, (380, 40))
        self.interval_surf2 = self.font.render(str(G.Globals.MUSIC_VOL),
            True, (255, 255, 255))
        G.Globals.SCREEN.blit(self.interval_surf2, (380, 100))
        G.Globals.SCREEN.blit(self.save_surf, 
            (G.Globals.WIDTH-(self.save_x+20), G.Globals.HEIGHT))

    def event(self, event):
        if event.type == PG.MOUSEBUTTONDOWN:
            if Menu.Menu.check_mouse(Menu.Menu(),
                340, 40, 20, 20):
                
                if (G.Globals.FX_VOL - 1) >= 0:
                    G.Globals.FX_VOL -= 1
            elif Menu.Menu.check_mouse(Menu.Menu(),
                 430, 40, 20, 20):
                 
                 if (G.Globals.FX_VOL + 1) <= 10:
                     G.Globals.FX_VOL += 1
            elif Menu.Menu.check_mouse(Menu.Menu(),
                340, 100, 20, 20):
                
                if (G.Globals.MUSIC_VOL - 1) >= 0:
                    G.Globals.MUSIC_VOL -= 1
            elif Menu.Menu.check_mouse(Menu.Menu(),
                 430, 100, 20, 20):
                 
                 if (G.Globals.MUSIC_VOL + 1) <= 10:
                     G.Globals.MUSIC_VOL += 1
            elif Menu.Menu.check_mouse(Menu.Menu(), 
                     G.Globals.WIDTH-(self.save_x+20), G.Globals.HEIGHT,
                     self.save_surf.get_width(), self.save_surf.get_height()):
                        G.set_vol()
                        G.Globals.STATE = Options.Options()     
    
    def update(self, time):
        pass    
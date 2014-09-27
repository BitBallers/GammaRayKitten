#The main architecture of the game

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

class Globals(object):
    RUNNING = True
    SCREEN = None
    WIDTH = None
    HEIGHT = None
    STATE = None
    INTERVAL = .02

def main():
    initialize()
    loop()
    finalize()

def initialize():
    passed, failed = PG.init()
    #make sure nothing weird is going on
    if failed > 0:
        print "ERROR: %d Pygame modules failed to initialize" % failed
        PG.quit()
    Globals.SCREEN = PD.set_mode((800, 600))
    PD.set_caption("Gamma Ray Kitten")
    GLOBALS.WIDTH = Globals.SCREEN.get_width()
    GLOBALS.HEIGHT = Globals.SCREEN.get_height()
    Globals.STATE = #ADD WHEN WE HAVE STATES

def loop():
    while Globals.RUNNING:
        last = PT.get_ticks()
        Globals.STATE.render()
        PD.flip()
        elapsed = (PT.get_ticks() - last) / 1000.0
        Globals.STATE.update(elapsed)
        for event in PE.get():
            if event.type == PG.QUIT:
                Globals.RUNNING = False
            else:
                Globals.STATE.event(event)

def finalize():
    PG.quit()
    
        

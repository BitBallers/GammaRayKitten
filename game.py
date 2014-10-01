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
import Menu
import Globals as G
import Title
import Main


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
    G.Globals.SCREEN = PD.set_mode((800, 600))
    PD.set_caption("Gamma Ray Kitten")
    G.Globals.WIDTH = G.Globals.SCREEN.get_width()
    G.Globals.HEIGHT = G.Globals.SCREEN.get_height()
    G.Globals.STATE = Title.Title()


def loop():
    while G.Globals.RUNNING:
        last = PT.get_ticks()
        G.Globals.STATE.render()
        PD.flip()
        elapsed = (PT.get_ticks() - last) / 1000.0
        G.Globals.STATE.update(elapsed)
        for event in PE.get():
            if event.type == PG.QUIT:
                G.Globals.RUNNING = False
            else:
                G.Globals.STATE.event(event)


def finalize():
    PG.quit()

main()

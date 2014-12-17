# The main architecture of the game
import os
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
import pygame.surface as PSF
import game_states.Menu as Menu
import Globals as G
import game_states.Title as Title
import game_states.Main as Main
import game_states.Intro as Intro


def main():

    initialize()
    loop()
    finalize()


def initialize():
    passed, failed = PG.init()
    # make sure nothing weird is going on
    if failed > 0:
        print "ERROR: %d Pygame modules failed to initialize" % failed
        PG.quit()
    G.Globals.SCREEN = PD.set_mode((800, 650))
    PD.set_caption("Gamma Ray Kitten")
    G.Globals.WIDTH = G.Globals.SCREEN.get_width()
    G.Globals.HEIGHT = G.Globals.SCREEN.get_height() - G.Globals.HUD_HEIGHT
    G.Globals.STATE = Title.Title()
    G.Globals.AMB_MUSIC = PX.Sound("sounds/menu.ogg")
    if PX.get_num_channels() >= 2:
        G.Globals.FX_CHANNEL = PX.Channel(0)
        G.Globals.MUSIC_CHANNEL = PX.Channel(1)
    else:
        G.Globals.FX_CHANNEL = PX.Channel(0)
        G.Globals.MUSIC_CHANNEL = PX.Channel(0)


def loop():
    brightness = PSF.Surface((G.Globals.WIDTH, G.Globals.HEIGHT))
    while G.Globals.RUNNING:
        last = PT.get_ticks()
        G.Globals.STATE.render()
        if G.Globals.BRIGHT_INTERVAL <= 102 and G.Globals.BRIGHT_INTERVAL >= 80:
            brightness.set_alpha(((100-G.Globals.BRIGHT_INTERVAL)/100.0)*255)
            G.Globals.SCREEN.blit(brightness, (0, 0))
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

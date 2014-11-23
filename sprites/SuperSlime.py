import pygame as PG
import pygame.image as PI
import pygame.sprite as PS
import Globals as G
import maps.Camera as Camera
import maps.Map as Map
import math
import random
import pygame.mixer as PM
import Enemy
import Slime


class SuperSlime(Slime.Slime):

    IMAGES = None
    DEATH_IMAGES = None
    CYCLE = 0.5
    MAX_AI_DIST = 500
    SPEED = 2
    AI_PERCENTAGE = .3
    SOUND = None
    HEALTH = 2

    def __init__(self, (x, y)):
        Slime.Slime.__init__(self, (x, y))

        if SuperSlime.SOUND is None:
            SuperSlime.SOUND = PM.Sound("sounds/slime_death.wav")
        if not SuperSlime.IMAGES:
            self.sup_load_images()

        self.image = SuperSlime.IMAGES[8]
        self.b_index = 0
        self.rect = self.image.get_rect()
        self.width = self.rect.width
        self.height = self.rect.height
        self.world_x = x
        self.world_y = y

        self.x_velocity = 0
        self.y_velocity = 0

        self.time = 0.0
        self.dying = False
        self.dead = False

        self.last_x = self.world_x
        self.last_y = self.world_y
        self.health = SuperSlime.HEALTH

    def sup_load_images(self):
        SuperSlime.IMAGES = []
        sheet = PI.load(
            "sprites/images/slime_sprite_sheet.png").convert_alpha()
        c_surface = PG.Surface((sheet.get_width(), sheet.get_height())).convert()
        c_surface.fill((150, 0, 150))
        sheet.blit(c_surface, (0, 0), None, PG.BLEND_ADD)
        key = sheet.get_at((0, 0))
        for y in range(4):
            for x in range(5):
                surface = PG.Surface((30, 20)).convert()
                surface.set_colorkey(key)
                surface.blit(sheet, (0, 0), (x * 30, y * 20, 30, 20))
                SuperSlime.IMAGES.append(surface)

        SuperSlime.DEATH_IMAGES = []
        sheet = PI.load(
            "sprites/images/slime_sprite_sheet_death.png").convert_alpha()
        c_surface = PG.Surface((sheet.get_width(), sheet.get_height())).convert()
        c_surface.fill((150, 0, 150))
        sheet.blit(c_surface, (0, 0), None, PG.BLEND_ADD)

        key = sheet.get_at((0, 0))
        for y in range(2):
            for x in range(4):
                surface = PG.Surface((30, 20)).convert()
                surface.set_colorkey(key)
                surface.blit(sheet, (0, 0), (x * 30, y * 20, 30, 20))
                SuperSlime.DEATH_IMAGES.append(surface)

    def animate(self, time):
        k = SuperSlime.CYCLE / 5.0
        index = math.floor(self.time / k)
        index = int(index)

        update_image = False
        if self.y_velocity > 0:
            self.b_index = 10
            update_image = True
        elif self.y_velocity < 0:
            self.b_index = 15
            update_image = True
        if self.x_velocity > 0:
            self.b_index = 0
            update_image = True
        elif self.x_velocity < 0:
            self.b_index = 5
            update_image = True

        if update_image:
            self.image = SuperSlime.IMAGES[self.b_index + index]

        if self.dying:
            self.image = SuperSlime.DEATH_IMAGES[self.death_index + index]
            if index == 3:
                self.dead = True

        self.time += time
        if self.time >= SuperSlime.CYCLE:
            self.time = 0

    def start_death(self):
        #Make sure the death doesn't reset if it is already dead
        if self.dying:
            return
        SuperSlime.SOUND.play()
        self.health = self.health - 1
        #Doesn't do anything else if it isn't dead yet
        if self.health > 0:
            return
        if self.b_index == 15:
            self.death_index = 4
        else:
            self.death_index = 0
        self.dying = True
        self.time = 0

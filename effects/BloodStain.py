import random
import math
import pygame as PG
import maps.Camera as Camera
import Globals as G


class BloodStain(object):

    def __init__(self, x, y, width, height):

        self.max_speed = 6
        self.init_x = x
        self.init_y = y

        self.positions = []
        self.velocities = []
        self.targets = []
        self.surfs = []
        self.sizes = []
        self.anim_done = False

        self.num_particles = random.randint(25, 50)

        for i in range(self.num_particles):
            self.positions.append((x, y))
            self.velocities.append((random.uniform(1, -1) * self.max_speed,
                                    random.uniform(1, -1) * self.max_speed))

            self.targets.append((random.randint(0, int(.8 * width)),
                                 random.randint(0, int(.8 * height))))

            self.sizes.append(random.randint(3, 5))

            self.surfs.append(PG.Surface((self.sizes[-1],
                                          self.sizes[-1])))

            # fill different shades of red
            self.surfs[-1].fill((random.randint(150, 180), 0, 0))

    def update(self):
        if self.anim_done:
            return

        for i in range(self.num_particles):
            p = self.positions[i]
            v = self.velocities[i]
            if abs(v[0]) < .01 and abs(v[1]) < .01:
                self.anim_done = True
                return
            target = self.targets[i]
            if abs(self.init_x - p[0]) < target[0] and \
                    abs(self.init_y - p[1]) < target[1]:
                self.positions[i] = (p[0] + v[0], p[1] + v[1])
            self.velocities[i] = (v[0] * .9, v[1] * .9)

    def render(self):
        for i in range(self.num_particles):
            x = self.positions[i][0] - Camera.Camera.X
            y = self.positions[i][1] - Camera.Camera.Y
            size = self.sizes[i]

            if x >= -size and x <= G.Globals.WIDTH \
                    and y >= -size and y <= G.Globals.HEIGHT:
                G.Globals.SCREEN.blit(self.surfs[i], (x, y))

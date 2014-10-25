import random
import pygame as PG
import maps.Camera as Camera
import Globals as G

class Blood(object):

    GRAVITY = .01

    def __init__(self, x, y, max_decay):
        
        self.max_speed = 3

        self.positions = []
        self.velocities = []
        self.sizes = []
        self.size_decay = []
        self.surfs = []

        self.num_particles = random.randint(75, 150)
        self.particles_gone = 0
        self.gone = False

        for i in range(self.num_particles):
            self.positions.append((x, y))
            self.velocities.append((random.uniform(1, -1)*self.max_speed, 
                                    random.uniform(1, -1)*self.max_speed))
            self.sizes.append(random.randint(2, 5))
            self.size_decay.append((0, random.uniform(max_decay, .5)))
            self.surfs.append(PG.Surface((self.sizes[-1], 
                              self.sizes[-1])).convert())

            # fill different shades of red
            self.surfs[-1].fill((random.randint(180, 230), 0, 0))

    def update(self, time):
        for i in range(self.num_particles):
            p = self.positions[i]
            v = self.velocities[i]
            size_decay = self.size_decay[i]

            self.positions[i] = (p[0]+v[0], p[1]+v[1])
            self.velocities[i] = (v[0]*.96, (v[1]+Blood.GRAVITY)*.96)

            self.size_decay[i] = (size_decay[0]+time, size_decay[1])
            if self.size_decay[i][0] >= size_decay[1]:
                self.surfs[i] = PG.transform.scale(self.surfs[i], 
                                                  (self.sizes[i]-1, 
                                                   self.sizes[i]-1))
                if self.sizes[i] > 1:
                    self.sizes[i] = self.sizes[i]-1
                
            
        if all(s == 1 for s in self.sizes):
            self.gone = True

    def render(self):
        for i in range(self.num_particles):
            x = self.positions[i][0]-Camera.Camera.X
            y = self.positions[i][1]-Camera.Camera.Y
            size = self.sizes[i]

            if x >= -size and x <= G.Globals.WIDTH \
                    and y >= -size and y <= G.Globals.HEIGHT:
                G.Globals.SCREEN.blit(self.surfs[i], (x,y))

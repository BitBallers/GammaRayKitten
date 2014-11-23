import pygame.sprite as PS
import pygame.image as PI
import maps.Camera as Camera
import pygame.transform as PT
import Globals as G


class Laser(PS.Sprite):
	LASER_IMAGE = None

	def __init__(self, (x, y), angle):
		PS.Sprite.__init__(self)
		if Laser.LASER_IMAGE is None:
			Laser.LASER_IMAGE = PI.load("sprites/images/wall_light.png").convert()
		self.image = PT.rotate(Laser.LASER_IMAGE, angle)
		self.rect = self.image.get_rect()
		self.rect.x = x - Camera.Camera.X
		self.rect.y = y - Camera.Camera.Y

	def render(self):
		G.Globals.SCREEN.blit(self.image, (self.rect.x, self.rect.y),
							  None, PG.BLEND_ADD)
		

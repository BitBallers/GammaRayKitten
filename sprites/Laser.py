import pygame as PG
import pygame.sprite as PS
import pygame.image as PI
import maps.Camera as Camera
import pygame.transform as PT
import Globals as G



class Laser(PS.Sprite):
	
	LASER_IMAGE = None
	FADE_SPEED = 10

	def __init__(self, (x, y), angle):
		PS.Sprite.__init__(self)
		if Laser.LASER_IMAGE is None:
			Laser.LASER_IMAGE = PI.load("sprites/images/laser_beam.png").convert()
		
		self.image = PT.rotate(Laser.LASER_IMAGE, angle)
		self.rect = self.image.get_rect()		
		self.rect.x = x - Camera.Camera.X
		self.rect.y = y - Camera.Camera.Y
		if angle == 180:
			self.rect.x -= self.image.get_width()
		if angle == 90:
			self.rect.y -= self.image.get_height()
		self.fade_image = PG.Surface(self.image.get_size()).convert_alpha()
		self.alpha = 0

	def render(self):
		self.fade_image.fill((0, 0, 0, self.alpha))
		self.image.blit(self.fade_image, (0,0))		
		G.Globals.SCREEN.blit(self.image, (self.rect.x, self.rect.y),
							  None, PG.BLEND_ADD)

	def update(self, time):
		self.alpha += Laser.FADE_SPEED
		if(self.alpha >= 255):
			self.alpha = 255
			return True
		return False
		

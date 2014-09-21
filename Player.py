import pygame as PG
import sys as SYS
import random as R
import pygame.image as PI
import pygame.display as PDI
import pygame.event as PE
import pygame.sprite as PS
import math

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
WIDTH = screen.get_width() 
HEIGHT = screen.get_height()

PG.init()
screen = PDI.set_mode((800, 800))

class Player(PS.Sprite):
	IMAGE = None

	def _init__(self):
		PS.Sprite.__init__(self, x_cord, y_cord)
		if not Player.IMAGE:
			Player.IMAGE = PI.load("Cat_Sprite.png").convert()
		self.image = Player.IMAGE
		self.rect = self.image.get_rect()	
		self.rect.x = x_cord
		self.rect.y = y_cord
		self.vx = 0
		self.vy = 0


	def handle_events(self, event):
		PE.pump()

		for event in PE.get():
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_UP:
					self.vx = 0
					self.vy += -math.sin(90)
				elif event.key == pygame.K_DOWN:
					self.vx = 0
					self.vy += math.sin(90)
				elif event.key == pygame.K_LEFT:
					self.vx += -math.cos(0)
					self.vy = 0
				elif event.key == pygame.K_RIGHT:
					self.vx = math.cos(0)
					self.vy = 0
			elif event.type == pygame.KEYUP:
				if event.key == pygame.K_UP:
					stop_player()
				elif event.key == pygame.K_DOWN:
					stop_player()
				elif event.key == pygame.K_LEFT:
					stop_player()
				elif event.key == pygame.K_RIGHT:
					stop_player()

	def stop_player():
		self.vx, self.vy = 0, 0

	#takes in the fixed time interval, dt
	def update(self, dt):
		self.vx += self.vx * dt
		self.vy += self.vy * dt
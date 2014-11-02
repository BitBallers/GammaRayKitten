import pygame as PG
import pygame.display as PD
import pygame.font as PF
import Globals as G
import pygame.image as PI
import pygame.time as PT
import pygame.mixer as PX
import random as r
import Menu 
import State

class StartScreen(State.State):

	FONT = None
	SECFONT = None
	INTERVAL = 10

	def __init__(self):
		State.State.__init__(self)
		# load fonts
		StartScreen.FONT = PF.Font("fonts/GUEVARA.ttf", 40)
		StartScreen.SECFONT = PF.Font("fonts/mrsmonster.ttf", 75)
		# load images
		img_1 = PI.load("sprites/images/cat1.jpg").convert()
		img_2 = PI.load("sprites/images/cat2.jpg").convert()
		img_3 = PI.load("sprites/images/cat3.jpg").convert()

		self.index = 0

		# create image list and append images
		self.images = []
		self.images.append(img_1)
		self.images.append(img_2)
		self.images.append(img_3)

		# create string lists and append strings
		self.strings1 = []
		self.strings2 = []
		self.strings1.append("AN ULTRAVIOLET STUDIOS GAME")
		self.strings1.append("  A BITBALLERS PRODUCTION")
		self.strings1.append("   HIT SPACE TO CONTINUE") # will have to change when joystick implemented
		self.strings2.append("")
		self.strings2.append("")
		self.strings2.append("GAMMA RAY KITTEN")
		# render surfaces for the strings
		self.surf1 = StartScreen.FONT.render(self.strings1[self.index], True,
											 (255, 0, 0))
		self.surf2 = StartScreen.SECFONT.render(self.strings2[self.index], True,
											 (255, 0, 0)) 

		self.xy1 = ((G.Globals.WIDTH / 2 - self.surf1.get_width() / 2,
					  (G.Globals.HEIGHT / 2 + G.Globals.HEIGHT / 4) 
					  + self.surf1.get_height()))
		self.xy2 = ((G.Globals.WIDTH / 10 - self.surf2.get_width() / 2,
					  (G.Globals.HEIGHT / 10) 
					  - self.surf1.get_height()))

		self.screen = G.Globals.SCREEN
		self.time = 0
		self.fade_in_value = 0
		self.fade_out_value = 255
		self.fade_value = 75 # adjust this value to get desired fade effect

		# play music
		self.music = PX.Sound("music.wav")
		self.music.play(-1)

	def render(self):
		G.Globals.SCREEN.fill((0, 0, 0))		
		G.Globals.SCREEN.blit(self.images[self.index], (0, 0))
		G.Globals.SCREEN.blit(self.surf1, self.xy1)
		if r.random() <= .80:
			G.Globals.SCREEN.blit(self.surf2, self.xy2)
				

	def event(self, event):
		if event.type == PG.KEYDOWN:
			if event.key == PG.K_SPACE:
				G.Globals.STATE = Menu.Menu()

	def update(self, time):
		self.time += time
		self.fade_in_value += time * self.fade_value # controls fade in time
		if self.fade_in_value <= 255: # values over 255 do not matter
			self.images[self.index].set_alpha(self.fade_in_value)

		# begin to fade out if time has reached point that is >= the fade in time
		if StartScreen.INTERVAL - (self.time % StartScreen.INTERVAL) \
			<= 255/self.fade_value + 1:
			self.fade_out_value -= time * self.fade_value # controls the fade out time
			if self.fade_out_value >= 0:
				if self.index != 2: # if not the last image, fade out
					self.images[self.index].set_alpha(self.fade_out_value)

		# decides whether or not it is time to change the image
		if self.time >= (self.index+1) * StartScreen.INTERVAL:
			if self.index + 1 < 3:
				self.index += 1
				# we changed images so we reset values
				self.fade_in_value = 0
				self.fade_out_value = 255
				self.images[self.index].set_alpha(self.fade_in_value)
				G.Globals.SCREEN.blit(self.images[self.index], (0, 0)) # for good measure, but render also handles this
				self.surf1 = StartScreen.FONT.render(self.strings1[self.index], True,
											 (255, 0, 0))
				self.surf2 = StartScreen.SECFONT.render(self.strings2[self.index], True,
											 (255, 0, 0))	
		






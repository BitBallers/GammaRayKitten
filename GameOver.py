import pygame as PG
import pygame.font as PF
import pygame.key as PK
import Globals as G
import random as r
import State
import Score
import Main
import Menu

class GameOver(State.State):

	FONT = None
	INTERVAL = .5
	FADETIME = 2

	def __init__(self, hasWon, score):
		State.State.__init__(self)
		GameOver.FONT = PF.Font("fonts/Red October-Regular.ttf", 60)
		# determines whether player has won or lost
		self.hasWon = hasWon 
		self.score = score
		if (self.hasWon):
		    self.surf = GameOver.FONT.render("You Won! Score: " + str(self.score), True, (255, 255, 255))
		else:
		    self.surf = GameOver.FONT.render("You Lost! Score: " + str(self.score), True, (255, 255, 255))    
		# rect of the text to be displayed   
		self.text_rect = self.surf.get_rect()
		# centers the text to the center of the screen
		self.text_rect.center = G.Globals.SCREEN.get_rect().center    
		# value used to keep track of number of entries in high score initials list
		self.value = 0
		# stores the initials of the player
		self.initials = []
		self.time = 0
		# just adds some color to the text
		self.rgb1 = int(r.random() * 255) + 1
		self.rgb2 = int(r.random() * 255) + 1
		self.rgb3 = int(r.random() * 255) + 1

	def render(self):
	    G.Globals.SCREEN.fill((0, 0, 0))
	    G.Globals.SCREEN.blit(self.surf, (self.text_rect))

	def event(self, event):
		if event.type == PG.KEYDOWN and event.key == PG.K_ESCAPE:
			G.Globals.STATE = Menu.Menu()
		elif event.type == PG.KEYDOWN:
			# render the key pressed by the player to the screen
			self.surf = GameOver.FONT.render(PK.name(event.key), True, (self.rgb1, self.rgb2, self.rgb3))
			# adds that key to the initials array
			self.initials.append(PK.name(event.key))
			#move the rect over so that a new char value can be placed on screen
			self.text_rect = self.text_rect.move(75, 0) 
			# relates value to length of array of player's initials to ensure only
			# three are inputted  
			self.value = len(self.initials)
			if self.value >= 4:
				# after 3 initials are inputted, data is written to score file
				self.send_data() 	
	
	def update(self, time):
		self.time += time
		while self.time > G.Globals.INTERVAL:
			self.rgb1 = int(r.random() * 255) + 1
			self.rgb2 = int(r.random() * 255) + 1
			self.rgb3 = int(r.random() * 255) + 1
			self.time -= G.Globals.INTERVAL	

	def send_data(self):
		# sends player's initials and score to score text file
		score_file = open("scores.txt", "a")
		for i in range(3):
			score_file.write(self.initials[i])
		score_file.write(" - Score: " + str(self.score) + "\n")
		score_file.close()	
		G.Globals.STATE = Menu.Menu()


		
	



				






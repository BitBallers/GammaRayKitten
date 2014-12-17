import sys as SYS
import pygame as PG
import pygame.event as PE
import pygame.joystick as PJ
import pygame.font as PF
import Globals as G
import Options
import Menu
import State


class JoySettings(State.State):

    FONT = None
    SECFONT = None
    INIT_X = 400
    INIT_Y = 40
    Y_SPACING = 40
    INTERVAL = 3
    POSS_BUTTONS = []

    def __init__(self):
        State.State.__init__(self)
        if not JoySettings.FONT:
            JoySettings.FONT = PF.Font("fonts/red_october.ttf", 15)
        if not JoySettings.SECFONT:
            JoySettings.SECFONT = PF.Font("fonts/red_october.ttf", 20)   
                 
        self.font = JoySettings.FONT
        self.font2 = JoySettings.SECFONT
        self.num_joys = PJ.get_count()
        self.no_joy = False
        if self.num_joys ==  0:
            self.no_joy = True
            return
        joys = []
        for i in range(self.num_joys):
            joy = PJ.Joystick(i)
            joy.init()
            joys.append(joy)
           

        self.buttons = ["Move Up" , "Move Down", "Move Left","Move Right",
         "Shoot Up", "Shoot Down", "Shoot Left", "Shoot Right", "Activation Key"]
        self.instructions = self.font.render("Configure your joystick below." ""
         " Press X to set to default settings.",
                                             True, (255, 255, 255))

        self.surfs = []
        for i in range(len(self.buttons)):
            self.surfs.append(self.font2.render(self.buttons[i],
                          True, (255, 255, 255)))    
        self.index = 0
        self.selected_buttons = []
        if joys[0].get_numbuttons() < 9:
            self.no_joy = True
            return
        for i in range(joys[0].get_numbuttons()):
            JoySettings.POSS_BUTTONS.append(i)

        self.continue_string = self.font2.render("", True, (255, 255, 255))
        self.button_pos = set([(1,0), (-1,0), (0,1), (0,-1)])

    def render(self):
        if self.no_joy:
            G.Globals.STATE = Options.Options()
            return
        G.Globals.SCREEN.fill((0, 0, 0))
        G.Globals.SCREEN.blit(self.instructions,
            (G.Globals.WIDTH/2-self.instructions.get_width()/2,
                10))
        x_cord = JoySettings.INIT_X
        y_cord = JoySettings.INIT_Y
        y_spacing = JoySettings.Y_SPACING

        for surf in self.surfs:
            G.Globals.SCREEN.blit(surf, (x_cord-surf.get_width()/2,
                	                     y_cord))
            y_cord += (surf.get_height() + y_spacing)
        G.Globals.SCREEN.blit(self.continue_string,
         (x_cord-self.continue_string.get_width()/2, 
          620))

    def event(self, event):
        button = None
        if event.type == PG.JOYBUTTONDOWN:
           button = event.button
        elif event.type == PG.JOYAXISMOTION:
           button = event.axis
        elif event.type == PG.JOYBALLMOTION:
           button = event.rel
        elif event.type == PG.JOYHATMOTION:
           button = event.value    		

        if button is None:
            if event.type == PG.KEYDOWN:
                if len(self.selected_buttons) == 9: 
                    if event.key == PG.K_SPACE:
                        self.index = 0
                        G.Globals.BUTTONUP = set([PG.JOYBUTTONUP])
                        G.Globals.BUTTONDOWN = set([PG.JOYBUTTONDOWN, PG.JOYHATMOTION,
                                                PG.JOYBALLMOTION])
                        G.Globals.JOY_IN_USE = True
                        JoySettings.POSS_BUTTONS = self.selected_buttons
                        G.Globals.STATE = Options.Options()
                elif event.key == PG.K_x:
                    self.default()    

        elif button not in self.selected_buttons:
            if button in self.button_pos or event.type == PG.JOYBUTTONDOWN:      
                if self.index < len(self.buttons):
                    if self.index == 0:
                         G.Globals.UP = button
                    elif self.index == 1:
                        G.Globals.DOWN = button
                    elif self.index == 2:
                        G.Globals.LEFT = button
                    elif self.index == 3:
                        G.Globals.RIGHT = button
                    elif self.index == 4:
                        G.Globals.SHOOT_UP = button
                    elif self.index == 5:
                        G.Globals.SHOOT_DOWN = button
                    elif self.index == 6:
                        G.Globals.SHOOT_LEFT = button
                    elif self.index == 7:
                        G.Globals.SHOOT_RIGHT = button  
                    elif self.index == 8:
                        G.Globals.ACT_KEY = button      
                    if self.index < 8:                                     
                        self.selected_buttons.append(button)
                    self.index += 1  
                     
    def update(self, time):
        if self.no_joy:
            G.Globals.STATE = Options.Options()
            return

        for i in range(self.index):
        	self.surfs[i] = self.font2.render(self.buttons[i],
        		            True, (0, 255, 0))
        if self.index >= len(self.buttons):
        	self.continue_string = self.font2.render("Hit Space to conitnue",
        			                               True, (255, 255, 255))
    def default(self):

        G.Globals.BUTTONUP = set([PG.KEYUP])
        G.Globals.BUTTONDOWN = set([PG.KEYDOWN])    
        G.Globals.JOY_IN_USE = False
        G.Globals.UP = PG.K_w
        G.Globals.DOWN = PG.K_s
        G.Globals.LEFT = PG.K_a
        G.Globals.RIGHT = PG.K_d
        G.Globals.SHOOT_UP = PG.K_UP
        G.Globals.SHOOT_DOWN = PG.K_DOWN
        G.Globals.SHOOT_LEFT = PG.K_LEFT
        G.Globals.SHOOT_RIGHT = PG.K_RIGHT
        G.Globals.ACT_KEY = PG.K_SPACE
        G.Globals.STATE = Options.Options()    	

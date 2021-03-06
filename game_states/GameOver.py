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
        GameOver.FONT = PF.Font("fonts/red_october.ttf", 60)
        # determines whether player has won or lost
        self.hasWon = hasWon
        self.score = score
        if (self.hasWon):
            self.surf = GameOver.FONT.render("You Won! Score: " +
                                             str(self.score),
                                             True,
                                             (255, 255, 255))
        else:
            self.surf = GameOver.FONT.render("You Lost! Score: " +
                                             str(self.score),
                                             True,
                                             (255, 255, 255))
        # rect of the text to be displayed
        self.text_rect = self.surf.get_rect()
        # centers the text to the center of the screen
        self.text_rect.center = G.Globals.SCREEN.get_rect().center
        # stores the initials of the player
        self.initials = []
        self.time = 0
        self.color = (255, 0, 0)
        self.first_key_pressed = True
        self.instruct = GameOver.FONT.render("Enter Initials", True,
                                             (255, 255, 255))

    def render(self):
        G.Globals.SCREEN.fill((0, 0, 0))
        if self.first_key_pressed is False:
            center = self.get_center(self.instruct)
            x, y = center[0], center[1] - 100
            G.Globals.SCREEN.blit(self.instruct, (x, y))
        G.Globals.SCREEN.blit(self.surf, self.get_center(self.surf))

    def event(self, event):
        if event.type == PG.KEYDOWN and event.key == PG.K_ESCAPE:
            G.Globals.STATE = Menu.Menu()
        elif event.type == PG.KEYDOWN and ((event.key >= PG.K_a
                                            and event.key <= PG.K_z) or
                                           len(self.initials) is 3):
            if len(self.initials) is 3:
                self.send_data()
            elif self.first_key_pressed:
                self.first_key_pressed = False
                self.surf = GameOver.FONT.render("".join(self.initials),
                                                 True, self.color)
            else:
                self.initials.append(PK.name(event.key))
                self.surf = GameOver.FONT.render("".join(self.initials),
                                                 True, self.color)

            if len(self.initials) == 4:
                self.send_data()

    def update(self, time):
        pass

    def send_data(self):
        scores = []
        has_writ = False
        # Set up string
        t_string = ""
        for char in self.initials:
            t_string += char
        t_string += "-" + str(self.score) + "\n"

        with open("scores.txt") as open_file:
            for line in open_file:
                lhs, rhs = line.split("-", 1)
                val = int(rhs)
                if self.score > val:
                    scores.append(t_string)
                    has_writ = True
                scores.append(line)
        if not has_writ:
            scores.append(t_string)
        # write data
        with open("scores.txt", "w") as open_file:
            for line in scores:
                open_file.write(line)
        '''score_file = open("scores.txt", "a")
        for i in range(3):
            score_file.write(self.initials[i])
        score_file.write(" - Score: " + str(self.score) + "\n")
        score_file.close() '''
        G.Globals.STATE = Menu.Menu()

    def get_center(self, surf):
        x = G.Globals.WIDTH / 2 - surf.get_width() / 2
        y = G.Globals.HEIGHT / 2 - surf.get_height() / 2
        return (x, y)
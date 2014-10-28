import pygame as PG
import pygame.color as PC
import pygame.event as PE
import pygame.time as PT
import pygame.sprite as PS
import pygame.mixer as PX
import sprites.Enemy as Enemy
import sprites.Player as Player
import sprites.Bullet as Bullet
import sprites.Heart as Heart
import pygame.image as PI
import random
import State
import Menu
import Globals as G
import sprites.Tile as Tile
import maps.Camera as Camera
import maps.Map as Map
import math
import pygame.font as PF
import GameOver
import effects.Blood as Blood
import effects.BloodStain as BloodStain


class Game(State.State):

    TILE_WIDTH = 50
    TILE_HEIGHT = 50
    MAP_TILE_WIDTH = 16
    MAP_TILE_HEIGHT = 12
    SCORE = 0
    SCORE_FONT = None
    HEART_IMAGE = None
    HEALTH_DROP_RATE = .2
    KEY_IMAGE = None
    SYRINGE_IMAGE = None

    def __init__(self):
        Game.SCORE = 0
        State.State.__init__(self)
        Game.SCORE_FONT = PF.Font("fonts/Red October-Regular.ttf", 16)
        self.map = Map.Map(3)

        heart_surf = PI.load("sprites/images/heart.png").convert()
        Game.HEART_IMAGE = PG.Surface((25, 25))
        Game.HEART_IMAGE.set_colorkey(heart_surf.get_at((0, 0)))
        Game.HEART_IMAGE.blit(heart_surf, (0, 0))

        key_surf = PI.load("sprites/images/20x12_key.png")
        Game.KEY_IMAGE = PG.Surface((20, 12))
        Game.KEY_IMAGE.set_colorkey(key_surf.get_at((0, 0)))
        Game.KEY_IMAGE.blit(key_surf, (0, 0))

        s_surf = PI.load("sprites/images/syringe_sprite.png")
        Game.SYRINGE_IMAGE = PG.Surface(s_surf.get_size())
        Game.SYRINGE_IMAGE.set_colorkey(s_surf.get_at((0, 0)))
        Game.SYRINGE_IMAGE.blit(s_surf, (0, 0))

        self.camera = Camera.Camera(0, Map.Map.HEIGHT - G.Globals.HEIGHT, self)
        self.all_sprites_list = PS.Group()
        self.player_group = PS.Group()
        self.bullets = PS.Group()
        self.player = Player.Player(400, Map.Map.HEIGHT - 300, self.camera)
        self.player_group.add(self.player)
        self.enemy_speed = 1
        self.time = 0.0
        self.set_screen_coords_map()
        self.set_screen_cords_player()
        self.spawn_enemies()
        self.blood = []
        self.blood_stains = []

        self.non_black_tiles = None
        self.wall_sprites_list = None
        self.black_tiles = None
        self.set_screen_coords_map()

        self.hearts_group = PS.Group()

    def render(self):
        G.Globals.SCREEN.fill((0, 0, 0))
        self.non_black_tiles.draw(G.Globals.SCREEN)
        for stain in self.blood_stains:
            stain.render()
        for heart in self.hearts_group.sprites():
            heart.render()
        self.player.render()
        for e in self.enemies.sprites():
            e.render()
        for b in self.bullets.sprites():
            b.render()
        for blood in self.blood:
            blood.render()
        self.black_tiles.draw(G.Globals.SCREEN)
        self.render_HUD()

    def spawn_enemies(self):
        self.enemies = PS.Group()
        for coords in self.map.enemy_coords:
            new_enemy = Enemy.Enemy(coords)
            self.enemies.add(new_enemy)

    def update(self, time):
        self.time += time
        while self.time > G.Globals.INTERVAL:
            for e in self.enemies.sprites():
                if e.update(G.Globals.INTERVAL, self.player, self.map,
                            self.enemies.sprites()):
                    self.enemies.remove(e)
            for b in self.bullets.sprites():
                if b.update(G.Globals.INTERVAL):
                    self.bullets.remove(b)
            for blood in self.blood:
                blood.update(G.Globals.INTERVAL)
                if blood.gone:
                    self.blood.remove(blood)
            for stain in self.blood_stains:
                stain.update()
            for heart in self.hearts_group.sprites():
                heart.update()

            self.player.update(G.Globals.INTERVAL)
            self.set_screen_cords_player()
            # Are there collisions
            # Player Collision with walls
            result = PS.groupcollide(self.player_group, self.wall_sprites_list,
                                     False, False)
            for key in result:
                for wall in result[key]:
                    if self.player.rect.colliderect(wall.rect):
                        val = self.player.wall_collision(wall, self.map)
                        self.set_screen_cords_player()
                        if val == 1:
                            self.wall_sprites_list.remove(wall)
                        if val == 2:
                            Game.SCORE += 100
                            G.Globals.STATE = GameOver.GameOver(
                                True, Game.SCORE)
            result = PS.groupcollide(self.player_group, self.enemies,
                                     False, False)
            for key in result:
                for enemy in result[key]:
                    if self.player.take_damage(1):
                        G.Globals.STATE = GameOver.GameOver(False, Game.SCORE)
            # Enemy Collision with Bullets
            result = PS.groupcollide(self.enemies, self.bullets, False, False)
            for enemy in result:
                enemy.start_death()
                blood_x = enemy.world_x + enemy.width / 2
                blood_y = enemy.world_y + enemy.height / 2
                self.blood.append(Blood.Blood(blood_x,
                                              blood_y, .8))
                self.blood_stains.append(BloodStain.BloodStain(blood_x,
                                                               blood_y,
                                                               enemy.width,
                                                               enemy.height))

                Game.SCORE = Game.SCORE + 10
                for bullet in result[enemy]:
                    self.bullets.remove(bullet)
                if random.random() < Game.HEALTH_DROP_RATE:
                    self.hearts_group.add(Heart.Heart(enemy.world_x,
                                                      enemy.world_y))

            # Bullets Collide with Wall
            result = PS.groupcollide(
                self.bullets, self.wall_sprites_list, False, False)
            for bullet in result:
                self.bullets.remove(bullet)
            self.time -= G.Globals.INTERVAL

            # Player picking up hearts
            if self.player.health < Player.Player.MAX_HEALTH:
                heart = PS.spritecollideany(self.player, self.hearts_group)
                if heart is not None:
                    self.hearts_group.remove(heart)
                    self.player.health += 1

    def event(self, event):
        if event.type == PG.KEYDOWN and event.key == PG.K_ESCAPE:
            G.Globals.STATE = Menu.Menu()

        elif event.type == PG.KEYDOWN or event.type == PG.KEYUP:
            bull = self.player.handle_events(event)
            for b in bull:
                self.bullets.add(b)

    def set_screen_coords_map(self):
        self.non_black_tiles = PS.Group()
        self.wall_sprites_list = PS.Group()
        self.black_tiles = PS.Group()

        first_x = math.floor(self.camera.X / Game.TILE_WIDTH) * Game.TILE_WIDTH
        first_y = math.floor(
            self.camera.Y / Game.TILE_HEIGHT) * Game.TILE_HEIGHT
        offset_x = first_x - self.camera.X
        offset_y = first_y - self.camera.Y

        for i in range(Game.MAP_TILE_WIDTH + 1):
            for k in range(Game.MAP_TILE_HEIGHT + 1):
                x = first_x + (i * Game.TILE_WIDTH)
                y = first_y + (k * Game.TILE_HEIGHT)
                if x >= Map.Map.WIDTH or y >= Map.Map.HEIGHT:
                    continue

                tile = self.map.tiles[(x, y)]
                tile.set_screen_coords(offset_x + (i * Game.TILE_WIDTH),
                                       offset_y + (k * Game.TILE_HEIGHT))
                if tile.is_wall():
                    self.black_tiles.add(tile)
                else:
                    self.non_black_tiles.add(tile)

                if tile.is_wall() or tile.is_key() or \
                        tile.is_door() or tile.is_stairs() or tile.is_item():
                    self.wall_sprites_list.add(tile)
                if tile.is_forward_wall():
                    partial_tile = tile.get_wall_partial()
                    partial_tile.set_screen_coords(offset_x +
                                                   (i * Game.TILE_WIDTH),
                                                   offset_y +
                                                   (k * Game.TILE_HEIGHT))
                    self.wall_sprites_list.add(partial_tile)

    def set_screen_cords_player(self):
        screen_x = self.player.world_coord_x - self.camera.X
        screen_y = self.player.world_coord_y - self.camera.Y
        self.player.set_screen_coords(screen_x, screen_y)

    def render_HUD(self):
        surface = PG.Surface((G.Globals.WIDTH, G.Globals.HUD_HEIGHT))
        surface.fill((80, 0, 0))
        G.Globals.SCREEN.blit(surface, (0, G.Globals.HEIGHT))
        score_string = "Score: " + str(Game.SCORE)
        score_surf = Game.SCORE_FONT.render(
            score_string, True, (255, 255, 255))
        G.Globals.SCREEN.blit(score_surf, (5, G.Globals.HEIGHT + 10))
        heart_x = G.Globals.WIDTH - Player.Player.MAX_HEALTH * 25 - 5
        heart_y = 25 / 2 + G.Globals.HEIGHT
        key_x = heart_x - 40
        for i in range(self.player.health):
            G.Globals.SCREEN.blit(Game.HEART_IMAGE, (heart_x, heart_y))
            heart_x += 25
        if self.player.keys > 0:
            G.Globals.SCREEN.blit(Game.KEY_IMAGE, (key_x, heart_y + 7))
        if self.player.shot_type == 1:
            G.Globals.SCREEN.blit(
                Game.SYRINGE_IMAGE, (key_x - 25, heart_y + 5))

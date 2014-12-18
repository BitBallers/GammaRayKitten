import pygame as PG
import pygame.color as PC
import pygame.event as PE
import pygame.time as PT
import pygame.sprite as PS
import pygame.mixer as PX
import sprites.Scientist as Scientist
import sprites.SuperSlime as SuperSlime
import sprites.Bug as Bug
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
import sprites.Slime as Slime
import sprites.Boss as Boss


class Game(State.State):

    TILE_WIDTH = 50
    TILE_HEIGHT = 50
    MAP_TILE_WIDTH = 16
    MAP_TILE_HEIGHT = 12
    SCORE = 0
    SCORE_FONT = None
    HEART_IMAGE = None
    HEALTH_DROP_RATE = .1
    KEY_IMAGE = None    
    ITEM_IMAGES = None
    ACTIVATED_ITEM_IMAGES = None
    LEVEL = 1
    MAX_LEVEL = 5
    DOUBLE_KILL_SOUND = None
    DOUBLE_KILL_TIME = .20
    IMG_1 = None
    IMG_2 = None
    LEVEL_TRACKS = None

    def __init__(self, level, size=3, player=None):
        State.State.__init__(self)
        if not Game.LEVEL_TRACKS:
            self.load_tracks() 
        G.Globals.MUSIC_CHANNEL.play(Game.LEVEL_TRACKS[level-1], loops=-1)
        if not Game.SCORE_FONT:
            Game.SCORE_FONT = PF.Font("fonts/red_october.ttf", 16)
        self.map = Map.Map(size, level, player)
        self.camera = Camera.Camera(0, Map.Map.HEIGHT - G.Globals.HEIGHT, self)

        self.blood = []
        self.blood_stains = []

        if level is 1:
            Game.SCORE = 0

        if Game.DOUBLE_KILL_SOUND is None:
            Game.DOUBLE_KILL_SOUND = PX.Sound("sounds/double_kill.wav")

        if Game.HEART_IMAGE is None:
            heart_surf = PI.load("sprites/images/heart.png").convert()
            Game.HEART_IMAGE = PG.Surface((25, 25))
            Game.HEART_IMAGE.set_colorkey(heart_surf.get_at((0, 0)))
            Game.HEART_IMAGE.blit(heart_surf, (0, 0))

        if Game.ITEM_IMAGES is None:
            self.load_item_images()

        if Game.KEY_IMAGE is None:
            key_surf = PI.load("sprites/images/20x12_key.png")
            Game.KEY_IMAGE = PG.Surface((20, 12))
            Game.KEY_IMAGE.set_colorkey(key_surf.get_at((0, 0)))
            Game.KEY_IMAGE.blit(key_surf, (0, 0))

        if player is None:
            self.player = Player.Player(500, Map.Map.HEIGHT - 300, self.camera)
        else:
            self.player = player
            self.player.camera = self.camera
            self.player.world_coord_x = 500
            self.player.world_coord_y = Map.Map.HEIGHT - 300

        self.set_screen_cords_player()

        self.spawn_enemies()
        self.all_sprites_list = PS.Group()
        self.player_group = PS.Group()
        self.bullets = PS.Group()
        self.lasers = PS.Group()
        self.e_bullets = PS.Group()
        self.player_group.add(self.player)
        self.enemy_speed = 1
        self.time = 0.0
        Game.LEVEL = level

        self.non_black_tiles = None
        self.wall_sprites_list = None
        self.black_tiles = None
        self.set_screen_coords_map()

        self.hearts_group = PS.Group()
        self.l_interval = 0.0
        self.player.reset_movement()
        self.double_kill_timer = 0
        self.double_kill = False
        self.last_killed = None
        self.boss = None


    def render(self):
        G.Globals.SCREEN.fill((0, 0, 0))
        self.non_black_tiles.draw(G.Globals.SCREEN)
        for stain in self.blood_stains:
            stain.render()
        for heart in self.hearts_group.sprites():
            heart.render()
        for e in self.enemies.sprites():
            e.render()
        for b in self.bullets.sprites():
            b.render()
        for b in self.e_bullets.sprites():
            b.render()
        for blood in self.blood:
            blood.render()
        
        # Cat Glow
        '''if not self.player.dont_render:
            G.Globals.SCREEN.blit(Player.Player.GLOW, (self.player.rect.x,
                                                       self.player.rect.y),
                                None, PG.BLEND_ADD)'''
        self.player.render()
        # Render Tile lighting
        for tile in self.non_black_tiles.sprites():
            light = tile.get_light()
            if light is not None:
                coords = (tile.rect.x, tile.rect.y)
                G.Globals.SCREEN.blit(light, coords, None, PG.BLEND_ADD)
        # Siren
        if Game.LEVEL is 2:
            surface = PG.Surface((G.Globals.WIDTH, G.Globals.HEIGHT)).convert()
            c = int(100 + 50 * math.sin(self.l_interval))
            surface.fill((255, c, c))
            G.Globals.SCREEN.blit(surface, (0, 0), None, PG.BLEND_MULT) 
        self.black_tiles.draw(G.Globals.SCREEN)
        self.render_HUD()

    def spawn_enemies(self):
        self.enemies = PS.Group()
        self.scientists = PS.Group()
        for coords in self.map.sci_coords:
            new_enemy = Scientist.Scientist(coords)
            self.enemies.add(new_enemy)
        for coords in self.map.enemy_coords:
            new_enemy = Slime.Slime(coords)
            self.enemies.add(new_enemy)
        for coords in self.map.bug_coords:
            new_enemy = Bug.Bug(coords)
            self.enemies.add(new_enemy)
        for coords in self.map.ss_coords:
            new_enemy = SuperSlime.SuperSlime(coords)
            self.enemies.add(new_enemy)
        if self.map.boss_coord is not None:            
            self.boss = Boss.Boss(self.map.boss_coord)
            self.enemies.add(self.boss)

    def update(self, time):
        self.l_interval = self.l_interval + .01
        if self.l_interval >= 4 * math.pi:
            self.l_interval = 0.0
        self.time += time
        while self.time > G.Globals.INTERVAL:
            self.time -= G.Globals.INTERVAL
            curr_enemies = PS.Group()
            for i, e in enumerate(self.enemies.sprites()):                
                dead, bull = e.update(G.Globals.INTERVAL, self.player,
                                      self.map, self.enemies.sprites(), i)
                if dead:
                    self.enemies.remove(e)
                    if self.map.boss_coord is not None:            
                        Game.SCORE += 500
                        G.new_level(self.player)
                        return
                elif not (e.rect.x < - e.rect.width or e.rect.x > G.Globals.WIDTH + e.rect.width \
                        or e.rect.y < -e.rect.height or e.rect.y > G.Globals.HEIGHT + e.rect.height):
                    curr_enemies.add(e)
                if bull is not None:
                    self.e_bullets.add(bull)
            for b in self.bullets.sprites():
                if b.update(G.Globals.INTERVAL):
                    self.bullets.remove(b)
            for b in self.e_bullets.sprites():
                if b.update(G.Globals.INTERVAL):
                    self.e_bullets.remove(b)
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

            #self.collision(curr_enemies, self.bullets, self.e_bullets, self.player_group, self.wall_sprites_list) 
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
                            G.new_level(self.player)
            # Player collision with enemies
            result = PS.groupcollide(self.player_group, curr_enemies,
                                     False, False)
            for key in result:
                for enemy in result[key]:
                    if enemy.dying is False and self.player.take_damage(1):
                        G.Globals.STATE = GameOver.GameOver(False, Game.SCORE)
            # Player collision with enemy bullets
            result = PS.groupcollide(self.player_group, self.e_bullets, False,
                                     False)
            for player in result:
                if self.player.take_damage(1):
                    G.Globals.STATE = GameOver.GameOver(False, Game.SCORE)
                blood_x = player.world_coord_x + Player.Player.WIDTH / 2
                blood_y = player.world_coord_y + Player.Player.HEIGHT / 2
                self.blood.append(Blood.Blood(blood_x,
                                              blood_y, .8))
                p_width = Player.Player.WIDTH
                p_height = Player.Player.HEIGHT
                self.blood_stains.append(BloodStain.BloodStain(blood_x,
                                                               blood_y,
                                                               p_width,
                                                               p_height))

                for bullet in result[player]:
                    self.e_bullets.remove(bullet)

            # Enemy Collision with Bullets
            result = PS.groupcollide(curr_enemies, self.bullets, False, False)            
            for enemy in result:
                if enemy.dying is True:
                    continue
                if self.double_kill is False:                   
                    self.double_kill = True
                    self.double_kill_timer = 0
                    self.last_killed = enemy
                if self.double_kill_timer < Game.DOUBLE_KILL_TIME and self.double_kill \
                and self.last_killed is not enemy:
                    #Game.DOUBLE_KILL_SOUND.play()
                    self.double_kill = False                

                enemy.start_death()
                blood_x = int(enemy.world_x + enemy.width / 2)
                blood_y = int(enemy.world_y + enemy.height / 2)
                self.blood.append(Blood.Blood(blood_x,
                                              blood_y, .8))
                self.blood_stains.append(BloodStain.BloodStain(blood_x,
                                                               blood_y,
                                                               enemy.width,
                                                               enemy.height))

                Game.SCORE = Game.SCORE + 10
                for bullet in result[enemy]:
                    if self.player.piercing is False and bullet.__class__.__name__ is not "Laser":
                        self.bullets.remove(bullet)
                if random.random() < Game.HEALTH_DROP_RATE:
                    self.hearts_group.add(Heart.Heart(enemy.world_x,
                                                      enemy.world_y))                        

            # Bullets Collide with Wall
            result = PS.groupcollide(
                self.bullets, self.wall_sprites_list, False, False)
            for bullet in result:
                if bullet.__class__.__name__ is not "Laser": 
                    self.bullets.remove(bullet)
            # Enemy Bullets Collide with Wall
            result = PS.groupcollide(
                self.e_bullets, self.wall_sprites_list, False, False)
            for bullet in result:
                self.e_bullets.remove(bullet)

            # Player picking up hearts
            if self.player.health < self.player.max_health:
                heart = PS.spritecollideany(self.player, self.hearts_group)
                if heart is not None:
                    self.hearts_group.remove(heart)
                    self.player.health += 1
                    if self.player.health > self.player.max_health:
                        self.player.health = self.player.max_health
            if self.double_kill:                
                self.double_kill_timer += time
                if self.double_kill_timer > Game.DOUBLE_KILL_TIME:
                    self.double_kill = False                  

    def event(self, event):
        if event.type == PG.KEYDOWN and event.key == PG.K_ESCAPE:
            G.Globals.STATE = Menu.Menu()

        if event.type == PG.KEYDOWN and event.key == PG.K_0:
            G.new_level(self.player)
            # G.Globals.STATE = Game2.Game2()
        if event.type == PG.KEYDOWN and event.key == PG.K_9:
            self.player.activated_item = 1
        if event.type == PG.KEYDOWN and event.key == PG.K_8:
            self.player.activated_item = 0

        elif event.type in G.Globals.BUTTONDOWN \
             or event.type in G.Globals.BUTTONUP:
            bull, laser = self.player.handle_events(event)
            for b in bull:
                self.bullets.add(b)
                self.double_kill_timer = 0

            if laser is not None:
                self.bullets.add(laser)

    def set_screen_coords_map(self):
        self.non_black_tiles = PS.Group()
        self.wall_sprites_list = PS.Group()
        self.black_tiles = PS.Group()

        first_x = math.floor(self.camera.X / Game.TILE_WIDTH) * Game.TILE_WIDTH - Game.TILE_WIDTH
        first_y = math.floor(
            self.camera.Y / Game.TILE_HEIGHT) * Game.TILE_HEIGHT - Game.TILE_HEIGHT
        offset_x = first_x - self.camera.X
        offset_y = first_y - self.camera.Y

        for i in range(Game.MAP_TILE_WIDTH + 2):
            for k in range(Game.MAP_TILE_HEIGHT + 2):
                x = first_x + (i * Game.TILE_WIDTH)
                y = first_y + (k * Game.TILE_HEIGHT)
                if x >= Map.Map.WIDTH or y >= Map.Map.HEIGHT:
                    continue
                if x < 0 or y < 0:
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
        item_box_dimension = 30
        surface = PG.Surface((G.Globals.WIDTH, G.Globals.HUD_HEIGHT))
        surface.fill((80, 0, 0))
        G.Globals.SCREEN.blit(surface, (0, G.Globals.HEIGHT))
        score_string = "Score: " + str(Game.SCORE)
        score_surf = Game.SCORE_FONT.render(
            score_string, True, (255, 255, 255))
        G.Globals.SCREEN.blit(score_surf, (5, G.Globals.HEIGHT + 10))
        activated_string = "Activated Item:"
        activated_surf = Game.SCORE_FONT.render(activated_string, 
            True, (255, 255, 255))
        G.Globals.SCREEN.blit(activated_surf, (200, G.Globals.HEIGHT+10))
        if self.player.activated_item != -1:
            x = activated_surf.get_width()+205
            activated_item = Game.ACTIVATED_ITEM_IMAGES[self.player.activated_item]
            if self.player.activate_ready is False:
                activated_item = Game.ACTIVATED_ITEM_IMAGES[self.player.activated_item].copy()
                fade = PG.Surface(activated_item.get_size()).convert_alpha()
                fade.fill((0, 0, 0, 200))
                activated_item.blit(fade, (0, 0))
                activated_item.set_colorkey(activated_item.get_at((0, 0)))            
            G.Globals.SCREEN.blit(activated_item, (x, G.Globals.HEIGHT+10))
            

        heart_x = G.Globals.WIDTH - self.player.max_health * 25 - 5
        hud_y = 25 / 2 + G.Globals.HEIGHT
        heart_y = hud_y + item_box_dimension / \
            2 - Game.HEART_IMAGE.get_height() / 2
        key_x = heart_x - item_box_dimension / 2
        key_x -= Game.KEY_IMAGE.get_width() / 2
        key_y = hud_y + item_box_dimension / \
            2 - Game.KEY_IMAGE.get_height() / 2
        for i in range(self.player.health):
            G.Globals.SCREEN.blit(Game.HEART_IMAGE, (heart_x, heart_y))
            heart_x += 25
        if self.player.keys > 0:
            G.Globals.SCREEN.blit(Game.KEY_IMAGE, (key_x, key_y))
        init_x = key_x - 30
        for index, image in enumerate(self.player.items):
            x = init_x - index * item_box_dimension
            item_image = Game.ITEM_IMAGES[image]
            x += item_box_dimension / 2
            x -= item_image.get_width() / 2
            y = hud_y + item_box_dimension / 2 - item_image.get_height() / 2
            G.Globals.SCREEN.blit(item_image, (x, y))

    def load_tracks(self):
        Game.LEVEL_TRACKS = []
        Game.LEVEL_TRACKS.append(PX.Sound("sounds/level1.ogg"))
        Game.LEVEL_TRACKS.append(PX.Sound("sounds/level2.ogg"))
        Game.LEVEL_TRACKS.append(PX.Sound("sounds/level3.ogg"))
        Game.LEVEL_TRACKS.append(PX.Sound("sounds/level4.ogg"))
        Game.LEVEL_TRACKS.append(PX.Sound("sounds/level5.ogg"))

    def load_item_images(self):
        s_surf = PI.load("sprites/images/syringe_sprite.png")
        Game.SYRINGE_IMAGE = PG.Surface(s_surf.get_size())
        Game.SYRINGE_IMAGE.set_colorkey(s_surf.get_at((0, 0)))
        Game.SYRINGE_IMAGE.blit(s_surf, (0, 0))

        shampoo = PI.load("sprites/images/shampoo_sprite.png").convert()
        color_key = shampoo.get_at((0, 0))        
        Game.SHAMPOO_IMAGE = PG.Surface(shampoo.get_size())
        Game.SHAMPOO_IMAGE.set_colorkey(color_key)
        Game.SHAMPOO_IMAGE.blit(shampoo, (0, 0))

        pill = PI.load("sprites/images/pill_sprite.png").convert()
        color_key = pill.get_at((0, 0))        
        Game.PILL_IMAGE = PG.Surface(pill.get_size())
        Game.PILL_IMAGE.set_colorkey(color_key)
        Game.PILL_IMAGE.blit(pill, (0, 0))

        heart = PI.load("sprites/images/heart_sprite.png").convert()
        color_key = heart.get_at((0, 0))        
        Game.HEART_UP_IMAGE = PG.Surface(heart.get_size())
        Game.HEART_UP_IMAGE.set_colorkey(color_key)
        Game.HEART_UP_IMAGE.blit(heart, (0, 0))

        sheild = PI.load("sprites/images/shield_sprite.png").convert()
        color_key = sheild.get_at((0, 0))        
        Game.SHEILD_IMAGE = PG.Surface(sheild.get_size())
        Game.SHEILD_IMAGE.set_colorkey(color_key)
        Game.SHEILD_IMAGE.blit(sheild, (0, 0))

        laser = PI.load("sprites/images/laser_sprite.png").convert()
        color_key = laser.get_at((0, 0))        
        Game.LASER_IMAGE = PG.Surface(laser.get_size())
        Game.LASER_IMAGE.set_colorkey(color_key)
        Game.LASER_IMAGE.blit(laser, (0, 0))

        beer = PI.load("sprites/images/beer_sprite.png").convert()
        color_key = laser.get_at((0, 0))
        Game.BEER_IMAGE = PG.Surface(beer.get_size())
        Game.BEER_IMAGE.set_colorkey(color_key)
        Game.BEER_IMAGE.blit(beer, (0, 0))

        boot = PI.load("sprites/images/boot.png").convert()
        color_key = boot.get_at((0, 0))
        Game.BOOT_IMAGE = PG.Surface(boot.get_size())
        Game.BOOT_IMAGE.set_colorkey(color_key)
        Game.BOOT_IMAGE.blit(boot, (0, 0))


        Game.ITEM_IMAGES = []

        Game.ITEM_IMAGES.append(Game.SYRINGE_IMAGE)
        Game.ITEM_IMAGES.append(Game.SHAMPOO_IMAGE)
        Game.ITEM_IMAGES.append(Game.PILL_IMAGE)
        Game.ITEM_IMAGES.append(Game.HEART_UP_IMAGE)
        Game.ITEM_IMAGES.append(Game.BEER_IMAGE)
        Game.ITEM_IMAGES.append(Game.BOOT_IMAGE)
        
        Game.ACTIVATED_ITEM_IMAGES = []

        Game.ACTIVATED_ITEM_IMAGES.append(Game.SHEILD_IMAGE)
        Game.ACTIVATED_ITEM_IMAGES.append(Game.LASER_IMAGE)

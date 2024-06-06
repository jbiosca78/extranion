import pygame
from extranion.states.state import State
#from extranion.entities.hero import Hero
#from extranion.entities.rendergroup import RenderGroup
#from extranion.assets.assetmanager import AssetManager
#from extranion.assets.asset import AssetType
#from extranion.config import cfg_item
#from extranion.entities.projectiles.projectile_factory import ProjectileFactory, ProjectileType
#from extranion.assets.soundmanager import SoundManager
#from extranion.entities.enemy.spawner import Spawner
#from extranion.entities.pool import Pool
#from extranion.entities.enemy.enemy import Enemy
#from extranion.entities.explosion import Explosion

class Play(State):

    def __init__(self):
        super().__init__()
        self.next_state = "Intro"

        #self.__enemy_pool = Pool(Enemy, 2)
        #self.__players = RenderGroup()
        #self.__allied_projectiles = RenderGroup()
        #self.__enemy_projectiles= RenderGroup()
        #self.__enemies = RenderGroup()
        #self.__explosions = RenderGroup()

    def enter(self):
        self.__load_assets()

        #self.__players.add(Hero(self.__spawn_projectile))
        #SoundManager.instance().play_music(cfg_item("music", "mission", "name"))
        #self.__spawner = Spawner(self.__spawn_enemy)

    def release(self):
        #for enemy in self.__enemies:
        #    self.__enemy_pool.release(enemy)

        #self.__players.empty()
        #self.__allied_projectiles.empty()
        #self.__enemy_projectiles.empty()
        #self.__enemies.empty()
        #self.__explosions.empty()
        #self.__spawner = None
        ##SoundManager.instance().stop_music()
        #self.__unload_assets()
        pass

    def event(self, event):
        #if event.type == pygame.KEYDOWN:
        #    self.__players.handle_input(event.key, True)
        #if event.type == pygame.KEYUP:
        #    self.__players.handle_input(event.key, False)
        #if event.type == pygame.MOUSEBUTTONDOWN:
        #    self.done = True
        pass

    def update(self, delta_time):
        pass
        #self.__players.update(delta_time)
        #self.__allied_projectiles.update(delta_time)
        #self.__enemy_projectiles.update(delta_time)
        #self.__enemies.update(delta_time)
        #self.__spawner.update(delta_time)
        #self.__explosions.update(delta_time)

        #for player in pygame.sprite.groupcollide(self.__players, self.__enemy_projectiles, True, True).keys():
        #    self.__spawn_explosion(player.get_position())
        #    self.__game_over()

        #for enemy in pygame.sprite.groupcollide(self.__enemies, self.__allied_projectiles, False, True).keys():
        #    self.__spawn_explosion(enemy.body.position)
        #    self.__kill_enemy(enemy)

        #for enemy in pygame.sprite.groupcollide(self.__enemies, self.__players, False, True).keys():
        #    self.__spawn_explosion(enemy.body.position)
        #    self.__kill_enemy(enemy)
        #    self.__game_over()

    def render(self, surface):
        #self.__players.draw(surface)
        #self.__enemies.draw(surface)
        #self.__allied_projectiles.draw(surface)
        #self.__enemy_projectiles.draw(surface)
        #self.__explosions.draw(surface)
        pass

    def __load_assets(self):
        #AssetManager.instance().load(AssetType.SpriteSheet, 'gameplay', cfg_item("entities", "name"), cfg_item("entities", "image_file"), data_filename = cfg_item("entities", "data_file"))
        #AssetManager.instance().load(AssetType.Music, 'gameplay', cfg_item("music", "mission", "name"), cfg_item("music", "mission", "file"))
        #AssetManager.instance().load(AssetType.Sound, 'gameplay', cfg_item("sfx", "allied_gunfire", "name"), cfg_item("sfx", "allied_gunfire", "file"))
        #AssetManager.instance().load(AssetType.Sound, 'gameplay', cfg_item("sfx", "enemy_gunfire", "name"), cfg_item("sfx", "enemy_gunfire", "file"))
        #AssetManager.instance().load(AssetType.Sound, 'gameplay', cfg_item("sfx", "explosion1", "name"), cfg_item("sfx", "explosion1", "file"))
        #AssetManager.instance().load(AssetType.Sound, 'gameplay', cfg_item("sfx", "explosion2", "name"), cfg_item("sfx", "explosion2", "file"))
        #AssetManager.instance().load(AssetType.FlipBook, 'gameplay', cfg_item("entities", "explosion", "name"), cfg_item("entities", "explosion" , "image_file"), rows = cfg_item("entities", "explosion", "size")[0], cols = cfg_item("entities", "explosion", "size")[1])
        pass

    def __unload_assets(self):
        #AssetManager.instance().clear("gameplay")
        pass

    def __spawn_projectile(self, proj_type, position):
        #if proj_type == ProjectileType.Allied:
        #    self.__allied_projectiles.add(ProjectileFactory.create_projectile(proj_type, position))
        #    SoundManager.instance().play_sound(cfg_item("sfx", "allied_gunfire", "name"))
        #elif proj_type == ProjectileType.Enemy:
        #    self.__enemy_projectiles.add(ProjectileFactory.create_projectile(proj_type, position))
        #    SoundManager.instance().play_sound(cfg_item("sfx", "enemy_gunfire", "name"))
        pass

    def __spawn_enemy(self, enemy_type, spawn_point):
        enemy = self.__enemy_pool.acquire()
        enemy.init(enemy_type, spawn_point, self.__spawn_projectile, self.__kill_enemy)
        self.__enemies.add(enemy)

    def __kill_enemy(self, enemy):
        self.__enemies.remove(enemy)
        self.__enemy_pool.release(enemy)

    def __spawn_explosion(self, position):
        #self.__explosions.add(Explosion(position))
        pass

    def __game_over(self):
        print("GAME OVER")

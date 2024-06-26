import pygame
from pygame.math import Vector2 as vector
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
from extranion import log
from extranion.asset import asset
from extranion.config import cfg
from extranion.effects.stars import Stars
from extranion.effects.stars3d import Stars3D
from extranion.effects.planetsurface import PlanetSurface
from extranion.entities.hero import Hero
from extranion.entities.entitygroup import EntityGroup
from extranion.entities.enemies.scenecontroller import SceneController

class Gameplay(State):

	def __init__(self):
		super().__init__()
		self.name="Gameplay"

		# debug

		# grupos de entidades
		self.__herobullets=EntityGroup()
		self.__enemybullets=EntityGroup()
		self.__enemies=EntityGroup()

		self._board_rect=cfg("layout.game.board_rect")


	def enter(self):

		log.info("Entering state Gameplay")

		self._pause=False

		# control de escenas
		self.__scenecontroller=SceneController()

		# inicializamos valores de partida
		self._score=0
		self._maxscore=1234

		# cargamos assets
		self._load_assets()

		# cargamos efectos
		#self.__stars=Stars3D(cfg("layout.game.space_rect")[2:4], direction="up", speed=0.5)
		self.__stars=Stars3D(cfg("layout.game.space_rect")[2:4])
		self.__planetsurface=PlanetSurface(cfg("layout.game.space_rect"))

		# iniciamos héroe
		self.__hero=Hero("hero", self.__herobullets)

	def _load_assets(self):

		asset.load('gameplay', 'sprites.hero', 'hero')
		asset.load('gameplay', 'sprites.enemies', 'enemies')
		asset.load('gameplay', 'sprites.bullets', 'bullets')
		asset.load('gameplay', 'sprites.exerion', 'exerion')
		asset.load('gameplay', 'sprites.mountains', 'mountains')

		#months = [ "J", "F", "M",

		#self.starship=entity
		#asset.load('intro','intro.logo')

		#AssetManager.instance().load(AssetType.SpriteSheet, 'gameplay', cfg_item("entities", "name"), cfg_item("entities", "image_file"), data_filename = cfg_item("entities", "data_file"))
		#AssetManager.instance().load(AssetType.Music, 'gameplay', cfg_item("music", "mission", "name"), cfg_item("music", "mission", "file"))
		#AssetManager.instance().load(AssetType.Sound, 'gameplay', cfg_item("sfx", "allied_gunfire", "name"), cfg_item("sfx", "allied_gunfire", "file"))
		#AssetManager.instance().load(AssetType.Sound, 'gameplay', cfg_item("sfx", "enemy_gunfire", "name"), cfg_item("sfx", "enemy_gunfire", "file"))
		#AssetManager.instance().load(AssetType.Sound, 'gameplay', cfg_item("sfx", "explosion1", "name"), cfg_item("sfx", "explosion1", "file"))
		#AssetManager.instance().load(AssetType.Sound, 'gameplay', cfg_item("sfx", "explosion2", "name"), cfg_item("sfx", "explosion2", "file"))
		#AssetManager.instance().load(AssetType.FlipBook, 'gameplay', cfg_item("entities", "explosion", "name"), cfg_item("entities", "explosion" , "image_file"), rows = cfg_item("entities", "explosion", "size")[0], cols = cfg_item("entities", "explosion", "size")[1])

	def event(self, event):

		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_RETURN:
				self._pause=not self._pause
				log.info(f"PAUSE: {self._pause}")
			if event.key == pygame.K_ESCAPE:
				self.change_state="Intro"
			if event.key == pygame.K_TAB:
				self.__debug_info()
		if self._pause: return

		if event.type == pygame.KEYDOWN: self.__hero.input(event.key, True)
		if event.type == pygame.KEYUP:   self.__hero.input(event.key, False)

	def update(self, delta_time):

		if self._pause: return

		self.__scenecontroller.update(delta_time, self.__hero, self.__enemies, self.__enemybullets)
		if self.__hero: self.__hero.update(delta_time)
		self.__enemies.update(delta_time)
		self.__herobullets.update(delta_time)
		self.__enemybullets.update(delta_time)

		if self.__hero and pygame.sprite.spritecollide(self.__hero, self.__enemies, False):
			if self.__hero.lives==0:
				self.change_state="Intro"
			self.__hero.die()
			#self.__hero.lives-=1
			#self.__hero=None
			#self.__hero_respawn=cfg("entities.hero.respawn_time")

		for enemy in pygame.sprite.groupcollide(self.__enemies, self.__herobullets, True, True):
			# TODO: mover a hero.enemy_hit
			self.__hero.charge+=1
			self._score+=10

		self.__stars.update(delta_time)
		self.__planetsurface.update(delta_time, self.__hero)

	def render(self, canvas):

		self.__stars.render(canvas)
		self.__planetsurface.render(canvas)

		#self.__players.draw(surface)
		#self.___enemies.draw(surface)
		#self.__allied_projectiles.draw(surface)
		#self.__enemy_projectiles.draw(surface)
		#self.__explosions.draw(surface)

		self.__enemybullets.render(canvas)
		self.__herobullets.render(canvas)
		self.__enemies.render(canvas)
		if self.__hero: self.__hero.render(canvas)

		# draw blue box in board rect
		# asdfa
		canvas.fill((33,36,255), self._board_rect)

		font=asset.get("font.default")
		text = font.render(f"TOP SCORE", True, cfg("game.foreground_color"), None)
		canvas.blit(text, cfg("layout.game.topscore_text_pos"))
		text = font.render(f"SCORE", True, cfg("game.foreground_color"), None)
		canvas.blit(text, cfg("layout.game.score_text_pos"))
		text = font.render(f"CHARGE", True, cfg("game.foreground_color"), None)
		canvas.blit(text, cfg("layout.game.charge_text_pos"))
		text = font.render(f"SCENE", True, cfg("game.foreground_color"), None)
		canvas.blit(text, cfg("layout.game.scene_text_pos"))

		topscore=1234

		text = font.render(f"{topscore:12}", True, cfg("game.foreground_color"), None)
		canvas.blit(text, cfg("layout.game.topscore_pos"))
		text = font.render(f"{self._score:12}", True, cfg("game.foreground_color"), None)
		canvas.blit(text, cfg("layout.game.score_pos"))
		text = font.render(str(self.__hero.charge), True, cfg("game.foreground_color"), None)
		canvas.blit(text, cfg("layout.game.charge_pos")-vector(text.get_width()/2, 0))
		text = font.render(f"{self.__scenecontroller.scene}", True, cfg("game.foreground_color"), None)
		canvas.blit(text, cfg("layout.game.scene_pos")-vector(text.get_width()/2, 0))

		# draw lives
		exerion=asset.get("exerion")
		for l in range(self.__hero.lives):
			canvas.blit(exerion[0][0], cfg("layout.game.lives_pos")+vector((32+2)*l,0))

		# pause text
		if self._pause:
			text=font.render("PAUSE", True, cfg("game.foreground_color"), None)
			pause_box=pygame.rect.Rect(cfg("layout.game.pause_text_pos")-vector(5,5), text.get_size()+vector(10,10))
			canvas.fill(cfg("game.menu_color"), pause_box)
			canvas.blit(text, cfg("layout.game.pause_text_pos"))

	def _spawn_projectile(self, proj_type, position):
		#if proj_type == ProjectileType.Allied:
		#    self.__allied_projectiles.add(ProjectileFactory.create_projectile(proj_type, position))
		#    SoundManager.instance().play_sound(cfg_item("sfx", "allied_gunfire", "name"))
		#elif proj_type == ProjectileType.Enemy:
		#    self.__enemy_projectiles.add(ProjectileFactory.create_projectile(proj_type, position))
		#    SoundManager.instance().play_sound(cfg_item("sfx", "enemy_gunfire", "name"))
		pass

	#def __spawn_enemy(self, enemy_type, spawn_point):
	#	enemy = self.__enemy_pool.acquire()
	#	enemy.init(enemy_type, spawn_point, self.__spawn_projectile, self.__kill_enemy)
	#	self.__enemies.add(enemy)

	#def __kill_enemy(self, enemy):
	#	self.__enemies.remove(enemy)
	#	self.__enemy_pool.release(enemy)

	#def __spawn_explosion(self, position):
	#	#self.__explosions.add(Explosion(position))
	#	pass

	#def __game_over(self):
	#	print("GAME OVER")

	def exit(self):
		# vaciamos los EntityGroups
		self.__enemybullets.empty()
		self.__herobullets.empty()
		self.__enemies.empty()

		asset.unload('gameplay')
		self.__planetsurface.release()
		self.__stars.release()
		#for enemy in self.___enemies:
		#    self.__enemy_pool.release(enemy)

		#self.__players.empty()
		#self.__allied_projectiles.empty()
		#self.__enemy_projectiles.empty()
		#self.___enemies.empty()
		#self.__explosions.empty()
		#self.__spawner = None
		##SoundManager.instance().stop_music()

	def __debug_info(self):
		log.info(f"Num enemies: {len(self.__enemies)}")
		log.info(f"Num enemy bullets: {len(self.__enemybullets)}")
		log.info(f"Num hero bullets: {len(self.__herobullets)}")

		#pass


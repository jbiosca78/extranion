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
from extranion import log
from extranion.asset import asset
from extranion.config import cfg
from extranion.effects.stars import Stars
from extranion.entities.hero import Hero
from extranion.entities.enemy import Enemy
from extranion.entities.entitygroup import EntityGroup

class Gameplay(State):

	def __init__(self):
		super().__init__()

		#self.__enemy_pool = Pool(Enemy, 2)
		#self.__players = RenderGroup()
		#self.__allied_projectiles = RenderGroup()
		#self.__enemy_projectiles= RenderGroup()
		#self.__enemies = RenderGroup()
		#self.__explosions = RenderGroup()
		self._board_rect=cfg("layout.game.board_rect")
		self._bullet_pos = [0,0]

		self._lives=cfg("mechanics.start_lives")
		self._charge=cfg("mechanics.start_charge")
		self._score=0
		self._maxscore=1234

		self._scene=0
		self._wave=0
		self._wavewait=0


	def enter(self):

		log.info("Entering state Gameplay")
		self._stars=Stars(cfg("layout.game.space_rect")[2:4])
		self._load_assets()
		self._hero=Hero("hero",cfg("entities.hero.start_pos"))

		self._herobullets=EntityGroup()

		self._enemies=EntityGroup()
		#self._enemies.add(Enemy("elefante", [150,100]))
		#self._enemies.add(Enemy("mariposa", [200,100], self._hero.get_position))
		#self._enemies.add(Enemy("pajaro", [250,100]))
		#self._enemies.add(Enemy("pluma", [300,100]))
		#self._enemies.add(Enemy("rueda", [350,100], self._hero.get_position))
		#self._enemies.add(Enemy("ovni", [400,100]))
		#self._enemies.add(Enemy(position=[250,100], spritesheet="exerion", spriterow=2))
		#self._enemies.add(Enemy(position=[200,100], spritesheet="exerion", spriterow=3))
		#self._enemies.add(Enemy(position=[300,100], spritesheet="exerion", spriterow=4))
		#self._stars=Stars(cfg("game.canvas_size"))

		#self.__players.add(Hero(self.__spawn_projectile))
		#SoundManager.instance().play_music(cfg_item("music", "mission", "name"))
		#self.__spawner = Spawner(self.__spawn_enemy)

	def _load_assets(self):

		asset.load('gameplay', 'sprites.hero', 'hero')
		asset.load('gameplay', 'sprites.bullets', 'bullets')
		asset.load('gameplay', 'sprites.exerion', 'exerion')
		asset.load('gameplay', 'sprites.enemies', 'enemies')
		#self.starship=entity
		#asset.load('intro','intro.logo')

		#AssetManager.instance().load(AssetType.SpriteSheet, 'gameplay', cfg_item("entities", "name"), cfg_item("entities", "image_file"), data_filename = cfg_item("entities", "data_file"))
		#AssetManager.instance().load(AssetType.Music, 'gameplay', cfg_item("music", "mission", "name"), cfg_item("music", "mission", "file"))
		#AssetManager.instance().load(AssetType.Sound, 'gameplay', cfg_item("sfx", "allied_gunfire", "name"), cfg_item("sfx", "allied_gunfire", "file"))
		#AssetManager.instance().load(AssetType.Sound, 'gameplay', cfg_item("sfx", "enemy_gunfire", "name"), cfg_item("sfx", "enemy_gunfire", "file"))
		#AssetManager.instance().load(AssetType.Sound, 'gameplay', cfg_item("sfx", "explosion1", "name"), cfg_item("sfx", "explosion1", "file"))
		#AssetManager.instance().load(AssetType.Sound, 'gameplay', cfg_item("sfx", "explosion2", "name"), cfg_item("sfx", "explosion2", "file"))
		#AssetManager.instance().load(AssetType.FlipBook, 'gameplay', cfg_item("entities", "explosion", "name"), cfg_item("entities", "explosion" , "image_file"), rows = cfg_item("entities", "explosion", "size")[0], cols = cfg_item("entities", "explosion", "size")[1])

	def exit(self):

		# vaciamos los EntityGroups
		self._herobullets.empty()
		self._enemies.empty()

		asset.unload('gameplay')
		self._stars.release()
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

	def event(self, event):

		if event.type == pygame.KEYDOWN: self._hero.input(event.key, True)
		if event.type == pygame.KEYUP:   self._hero.input(event.key, False)

		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_SPACE:
				self._bullet_pos=self._hero.get_position()
				self._bullet_pos[0]+=self._hero.width//2-3

	def update(self, delta_time):

		if len(self._enemies)==0:
			self._wavewait+=delta_time
			if self._wavewait>cfg("mechanics.wave_wait"):
				self._wavewait=0
				self._scene+=1
				self._enemies.add(Enemy("mariposa", [200,100], self._hero.get_position))

		self._hero.update(delta_time)
		self._enemies.update(delta_time)
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

		#bullets=pygame.sprite.Group()
		#bullets.add(self.__allied_projectiles)

		#self._bullet_pos[1]-=1
		#print(type(self._bullet_pos))
		self._bullet_pos[1]-=4.5

		self._stars.update(delta_time)

		for enemy in pygame.sprite.spritecollide(self._hero, self._enemies, True):
			print("COLLISION")
			self._charge+=1
			self._score+=10
		#	self._hero.kill()
		#	self._lives-=1

	def render(self, canvas):

		self._stars.render(canvas)
		#self.__players.draw(surface)
		#self.__enemies.draw(surface)
		#self.__allied_projectiles.draw(surface)
		#self.__enemy_projectiles.draw(surface)
		#self.__explosions.draw(surface)

		bullets=asset.get("bullets")
		# draw bullets[0][0]
		bpos=self._bullet_pos
		canvas.blit(bullets[0][0], bpos)
		#canvas.blit(bullets[0][1], (300,200))
		#canvas.blit(bullets[0][2], (320,200))

		self._enemies.render(canvas)
		self._hero.render(canvas)

		# draw blue box in board rect
		canvas.fill((33,36,255), self._board_rect, 1)

		font=asset.get("font.default")
		text = font.render(f"TOP SCORE", True, cfg("game.foreground_color"), None)
		canvas.blit(text, cfg("layout.game.topscore_text_pos"))
		text = font.render(f"SCORE", True, cfg("game.foreground_color"), None)
		canvas.blit(text, cfg("layout.game.score_text_pos"))
		text = font.render(f"CHARGE", True, cfg("game.foreground_color"), None)
		canvas.blit(text, cfg("layout.game.charge_text_pos"))
		text = font.render(f"SCENE", True, cfg("game.foreground_color"), None)
		canvas.blit(text, cfg("layout.game.scene_text_pos"))

		score=1234
		#self._charge+=1
		#self._score+=10

		text = font.render(f"{score:12}", True, cfg("game.foreground_color"), None)
		canvas.blit(text, cfg("layout.game.topscore_pos"))
		text = font.render(f"{self._score:12}", True, cfg("game.foreground_color"), None)
		canvas.blit(text, cfg("layout.game.score_pos"))
		text = font.render(str(self._charge), True, cfg("game.foreground_color"), None)
		canvas.blit(text, cfg("layout.game.charge_pos")-pygame.math.Vector2(text.get_width()/2, 0))
		text = font.render(f"{self._scene}", True, cfg("game.foreground_color"), None)
		canvas.blit(text, cfg("layout.game.scene_pos")-pygame.math.Vector2(text.get_width()/2, 0))

		# draw lives
		exerion=asset.get("exerion")
		for l in range(self._lives):
			canvas.blit(exerion[0][0], cfg("layout.game.lives_pos")+pygame.math.Vector2((32+2)*l,0))

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

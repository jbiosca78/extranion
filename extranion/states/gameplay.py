import pygame
from pygame.math import Vector2 as vector
from extranion.states.state import State
from extranion.tools import log, gvar
from extranion.config import cfg
from extranion.asset import asset
from extranion.sound.soundmanager import SoundManager
from extranion.effects.stars import Stars
from extranion.effects.stars3d import Stars3D
from extranion.effects.planetsurface import PlanetSurface
from extranion.entities.hero import Hero
from extranion.entities.entitygroup import EntityGroup
from extranion.entities.explossion import Explossion
from extranion.entities.enemies.scenecontroller import SceneController

class Gameplay(State):

	def __init__(self):
		super().__init__()
		self.name="gameplay"

		# grupos de entidades
		self.__herobullets=EntityGroup()
		self.__enemybullets=EntityGroup()
		self.__enemies=EntityGroup()
		self.__explossions=EntityGroup()

	def enter(self):

		# cargamos assets
		self.__load_assets()

		# control de escenas
		self.__scenecontroller=SceneController()

		# inicializamos valores de partida
		gvar.scene=0
		gvar.score=0
		self.__pause=False
		self.__gameover=False
		self.__gameover_time=0

		# cargamos efectos
		self.__stars=Stars3D(cfg("layout.gameplay.space_rect")[2:4])
		self.__planetsurface=PlanetSurface(cfg("layout.gameplay.space_rect"))

		# iniciamos héroe
		gvar.lives=cfg("gameplay.initial_lives")
		gvar.charge=cfg("gameplay.initial_charge")
		self.__hero=Hero("hero", self.__herobullets)

		# iniciamos música
		SoundManager.play_music("gameplay")

	def __load_assets(self):

		asset.load('gameplay', 'sprites.hero', 'hero')
		asset.load('gameplay', 'sprites.enemies', 'enemies')
		asset.load('gameplay', 'sprites.bullets', 'bullets')
		asset.load('gameplay', 'sprites.explossions', 'explossions')
		asset.load('gameplay', 'sprites.icons', 'icons')
		asset.load('gameplay', 'sprites.mountains', 'mountains')

		asset.load('gameplay', 'sound.gameplay.shoot')
		asset.load('gameplay', 'sound.gameplay.hero_killed')
		asset.load('gameplay', 'sound.gameplay.enemy_killed')
		asset.load('gameplay', 'sound.gameplay.extralife')
		asset.load('gameplay', 'sound.gameplay.hero_died')

		asset.load('gameplay', 'music.gameplay')
		asset.load('gameplay', 'music.gameover')

	def event(self, event):

		# eventos globales
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_ESCAPE:
				self.change_state="intro"
			if event.key == pygame.K_TAB:
				self.__debug_info()

		# eventos según estado
		if self.__gameover: self.__event_gameover(event)
		elif self.__pause: self.__event_pause(event)
		else: self.__event_playing(event)

	def __event_playing(self, event):
		if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN: self.__toggle_pause()
		if event.type == pygame.KEYDOWN: self.__hero.input(event.key, True)
		if event.type == pygame.KEYUP: self.__hero.input(event.key, False)

	def __event_pause(self, event):
		if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
			self.__toggle_pause()

	def __event_gameover(self, event):
		if self.__gameover_time>0: return
		if event.type == pygame.KEYDOWN:
			if event.key in [pygame.K_SPACE, pygame.K_RETURN]:
				self.change_state="intro"

	def __toggle_pause(self):
		self.__pause=not self.__pause

		if self.__pause:
			SoundManager.pause_music()
		else:
			SoundManager.resume_music()

		log.info(f"PAUSE: {self.__pause}")

	def __collisions(self):

		if self.__hero.alive:

			herodie=False
			# colisiones del héroe con los enemigos
			if pygame.sprite.spritecollide(self.__hero, self.__enemies, False): herodie=True
			# colisiones del héroe con las balas enemigas
			if pygame.sprite.spritecollide(self.__hero, self.__enemybullets, False): herodie=True

			# heroe muere!
			if herodie:
				self.__explossions.add(Explossion("hero", self.__hero.position))
				self.__hero.die()
				if gvar.lives<0:
					SoundManager.stop_music()
					SoundManager.play_sound("hero_died")
					self.__gameover=True
					self.__gameover_time=cfg("gameplay.gameover_time")

		# colisiones de los enemigos con las balas del héroe
		for enemy in pygame.sprite.groupcollide(self.__enemies, self.__herobullets, True, True):
			self.__explossions.add(Explossion(enemy.name, enemy.position))
			self.__hero.enemy_hit()

	def update(self, delta_time):

		if self.__gameover_time>0:
			self.__gameover_time-=delta_time
			if self.__gameover_time<=0:
				SoundManager.play_music("gameover")

		if self.__pause: return
		if self.__gameover: return

		self.__collisions()

		self.__scenecontroller.update(delta_time, self.__hero, self.__enemies, self.__enemybullets)
		if self.__hero: self.__hero.update(delta_time)

		self.__enemies.update(delta_time)
		self.__herobullets.update(delta_time)
		self.__enemybullets.update(delta_time)
		self.__explossions.update(delta_time)

		self.__stars.update(delta_time)
		self.__planetsurface.update(delta_time, self.__hero)

	def render(self, canvas):

		self.__stars.render(canvas)
		self.__planetsurface.render(canvas)

		self.__enemies.render(canvas)
		self.__explossions.render(canvas)
		self.__herobullets.render(canvas)
		self.__enemybullets.render(canvas)
		if self.__hero: self.__hero.render(canvas)

		self.render_board(canvas)

		# pause text
		if self.__pause:
			font=asset.get("font_default")
			text=font.render(cfg("layout.gameplay.pause.text"), True, cfg("layout.gameplay.pause.text_color"), None)
			box=pygame.rect.Rect(cfg("layout.gameplay.pause.text_pos")-vector(5,5), text.get_size()+vector(10,10))
			canvas.fill(cfg("layout.gameplay.pause.background_color"), box)
			canvas.blit(text, cfg("layout.gameplay.pause.text_pos"))

		# game over
		if self.__gameover and self.__gameover_time<=0:
				font=asset.get("font_default")
				text=font.render(cfg("layout.gameplay.gameover.text"), True, cfg("layout.gameplay.gameover.text_color"), None)
				box=pygame.rect.Rect(cfg("layout.gameplay.gameover.text_pos")-vector(5,5), text.get_size()+vector(10,10))
				canvas.fill(cfg("layout.gameplay.gameover.background_color"), box)
				canvas.blit(text, cfg("layout.gameplay.gameover.text_pos"))

	def render_board(self, canvas):

		canvas.fill(cfg("layout.gameplay.board.background_color"), cfg("layout.gameplay.board.board_rect"))

		font=asset.get("font_default")
		text = font.render(f"TOP SCORE", True, cfg("game.foreground_color"), None)
		canvas.blit(text, cfg("layout.gameplay.board.topscore_text_pos"))
		text = font.render(f"SCORE", True, cfg("game.foreground_color"), None)
		canvas.blit(text, cfg("layout.gameplay.board.score_text_pos"))
		text = font.render(f"CHARGE", True, cfg("game.foreground_color"), None)
		canvas.blit(text, cfg("layout.gameplay.board.charge_text_pos"))
		text = font.render(f"SCENE", True, cfg("game.foreground_color"), None)
		canvas.blit(text, cfg("layout.gameplay.board.scene_text_pos"))

		text = font.render(f"{gvar.topscore:12}", True, cfg("game.foreground_color"), None)
		canvas.blit(text, cfg("layout.gameplay.board.topscore_pos"))
		text = font.render(f"{gvar.score:12}", True, cfg("game.foreground_color"), None)
		canvas.blit(text, cfg("layout.gameplay.board.score_pos"))
		text = font.render(str(gvar.charge), True, cfg("game.foreground_color"), None)
		canvas.blit(text, cfg("layout.gameplay.board.charge_pos")-vector(text.get_width()/2, 0))
		text = font.render(f"{gvar.scene+1}", True, cfg("game.foreground_color"), None)
		canvas.blit(text, cfg("layout.gameplay.board.scene_pos")-vector(text.get_width()/2, 0))

		# dibujamos un icono de nave por cada vida
		ship=asset.get("icons")[0][0]
		for l in range(gvar.lives):
			canvas.blit(ship, cfg("layout.gameplay.board.lives_pos")+vector((ship.get_width()+2)*l,0))

	def exit(self):
		SoundManager.stop_music()

		# vaciamos los EntityGroups
		self.__enemybullets.empty()
		self.__herobullets.empty()
		self.__enemies.empty()
		self.__explossions.empty()

		# descargamos assets
		asset.unload('gameplay')

		# descargamos efectos
		self.__planetsurface.release()
		self.__stars.release()

	def __debug_info(self):
		log.info(f"Num enemies: {len(self.__enemies)}")
		log.info(f"Num enemy bullets: {len(self.__enemybullets)}")
		log.info(f"Num hero bullets: {len(self.__herobullets)}")
		log.info(f"Num explossions: {len(self.__explossions)}")

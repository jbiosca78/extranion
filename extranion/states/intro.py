import pygame
from pygame.math import Vector2 as vector
from extranion.states.state import State
from extranion.tools import log,gvar
from extranion.config import cfg
from extranion.asset import asset
from extranion.effects.stars3d import Stars3D
from extranion.soundmanager import SoundManager

class Intro(State):

	def __init__(self):
		super().__init__()
		self.name="intro"

		# variables para hacer parpadear el texto.
		self.__menu_options=cfg("layout.intro.menu.options")
		self.__selected=0
		self.__selected_blink=cfg("layout.intro.menu.blink")
		self.__selected_show=True
		self.__selected_time=0

	def enter(self):

		# cargamos assets
		self.__load_assets()

		# efecto de estrellas a mínima velocidad
		self.__stars=Stars3D(cfg("game.canvas_size"), speed=0.1)

		# pre-renderizamos las opciones del menu
		self.__render_text()

		# iniciamos música
		SoundManager.play_music("intro")

	def __load_assets(self):
		asset.load('intro','layout.intro.logo', 'logo')
		asset.load('intro', 'sound.intro.select_option', 'select_option')
		asset.load('intro', 'music.intro')
		asset.load('intro', 'sprites.icons', 'icons')

	def exit(self):
		SoundManager.stop_music()
		asset.unload('intro')
		self.__stars.release()

	def event(self, event):
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_ESCAPE:
				gvar.running=False
			if event.key in [ pygame.K_SPACE, pygame.K_RETURN ]:
				self.__select_option()
			# movemos la nave que elige la opción del menu
			if event.key == pygame.K_UP:
				self.__change_option(-1)
			if event.key == pygame.K_DOWN:
				self.__change_option(1)

	def update(self, delta_time):

		# parpadeo del selector de opciones
		if self.__selected_blink>0:
			self.__selected_time+=delta_time
			if self.__selected_time>self.__selected_blink:
				self.__selected_time=0
				self.__selected_show=not self.__selected_show

		# bajo un cielo estrellado
		self.__stars.update(delta_time)

	def render(self, canvas):

		# primero ponemos las estrellas de fondo
		self.__stars.render(canvas)

		# mostramos el logo
		canvas.blit(asset.get("logo"), cfg("layout.intro.logo_pos"))

		# mostramos las opciones del menu
		for i in range(0, len(self.__menu_options)):
			canvas.blit(self.__menu_rendered[i], self.__menu_options[i]["pos"])

		# mostramos la opción seleccionada
		ship=asset.get("icons")[0][1]
		if self.__selected_show:
			canvas.blit(ship, vector(self.__menu_options[self.__selected]["pos"])-vector(ship.get_width(),0))

	def __render_text(self):

		font=asset.get("font_default")

		self.__menu_rendered=[]
		for i in range(0, len(self.__menu_options)):
			img=font.render(self.__menu_options[i]["text"], True, cfg("game.foreground_color"), None)
			self.__menu_rendered.append(img)

	def __select_option(self):

		SoundManager.play_sound("select_option")
		action=self.__menu_options[self.__selected]["action"]
		if action=="exit":
			gvar.running=False
		else:
			self.change_state=action

	def __change_option(self, direction):

		self.__selected+=direction
		if self.__selected<0: self.__selected=0
		if self.__selected>len(self.__menu_options)-1: self.__selected=len(self.__menu_options)-1

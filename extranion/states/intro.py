import pygame
from extranion.states.state import State
from extranion.config import cfg
from extranion.asset import asset
from extranion.effects.stars import Stars
import extranion.log as log

class Intro(State):

	def __init__(self):
		super().__init__()
		# variables para hacer parpadear el texto. TODO: efecto de parpadeo en effects?
		self._text_show=True
		self._text_time=0

	def enter(self):
		log.info("Entering state Intro")
		asset.load('intro','intro.logo', 'logo')
		# iniciamos el efecto de estrellas
		self._stars=Stars(cfg("game.canvas_size"))
		self.__render_text()

	def release(self):
		asset.unload('intro')
		self._stars.release()
		pass

	def event(self, event):
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_SPACE:
				self.change_state = "Gameplay"

	def update(self, delta_time):
		# parpadeo del texto
		self._text_time+=delta_time
		if self._text_time>cfg("intro.text_blink_time"):
			self._text_time=0
			self._text_show=not self._text_show
		# bajo un cielo estrellado
		self._stars.update(delta_time)
		pass

	def render(self, canvas):
		# primero pintamos las estrellas de fondo
		self._stars.render(canvas)
		# mostramos el super logo
		logo=asset.get("logo")
		canvas.blit(logo, cfg("intro.logo_pos"))
		# y finalmente el texto
		if self._text_show:
			canvas.blit(self._text, cfg("intro.text_pos"))

	def __render_text(self):
		font=asset.get("fonts.hack")
		#self.__image.blit(logo, (400,0))
		self._text = font.render("PRESS SPACE TO CONTINUE", True, cfg("game.foreground_color"), None)
import pygame
from extranion.states.state import State
from extranion.tools import log
from extranion.config import cfg
from extranion.asset import asset
from extranion.effects.stars3d import Stars3D
from extranion.soundmanager import SoundManager

class Intro(State):

	def __init__(self):
		super().__init__()
		self.name="Intro"
		# variables para hacer parpadear el texto. TODO: efecto de parpadeo en effects?
		self._text_show=True
		self._text_time=0
		self._text_blink_time=cfg("layout.intro.text_blink_time")

	def enter(self):
		log.info("Entering state Intro")
		asset.load('intro','layout.intro.logo', 'logo')
		asset.load('intro', 'sound.intro.select_option', 'select_option')
		asset.load('intro', 'music.intro')

		SoundManager.play_music("intro")

		# efecto de estrellas a mínima velocidad
		self._stars=Stars3D(cfg("game.canvas_size"), speed=0.1)
		self.__render_text()

	def exit(self):
		SoundManager.stop_music()
		asset.unload('intro')
		self._stars.release()

	def event(self, event):
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_SPACE:
				#self.change_state = "Gameplay"
				self.change_state = "Travel"
				SoundManager.play_sound("select_option")

	def update(self, delta_time):
		# parpadeo del texto
		if self._text_blink_time>0:
			self._text_time+=delta_time
			if self._text_time>self._text_blink_time:
				self._text_time=0
				self._text_show=not self._text_show
		# bajo un cielo estrellado
		self._stars.update(delta_time)

	def render(self, canvas):
		# primero pintamos las estrellas de fondo
		self._stars.render(canvas)
		# mostramos el super logo
		logo=asset.get("logo")
		canvas.blit(logo, cfg("layout.intro.logo_pos"))
		# y finalmente el texto
		if self._text_show:
			canvas.blit(self._text, cfg("layout.intro.text_pos"))

	def __render_text(self):
		font=asset.get("font_default")
		#self.__image.blit(logo, (400,0))
		self._text = font.render("PRESS SPACE TO CONTINUE", True, cfg("game.foreground_color"), None)

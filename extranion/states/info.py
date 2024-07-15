import pygame
import random
from pygame.math import Vector2 as vector
from extranion.tools import log
from extranion.config import cfg
from extranion.states.state import State
from extranion.effects.stars3d import Stars3D
from extranion.sound.soundmanager import SoundManager
from extranion.asset import asset

class Info(State):

	def __init__(self):
		super().__init__()
		self.name="info"

	def enter(self):
		log.info("Entering state Info")
		asset.load('info','game.font_small')
		asset.load('info','layout.info.background')
		asset.load('info','layout.info.text_info')
		asset.load('info','layout.info.text_keys')
		asset.load('info', 'music.info')

		SoundManager.play_music("info")

	def exit(self):
		SoundManager.stop_music()
		asset.unload("info")

	def event(self, event):
		if event.type == pygame.KEYDOWN:
			if event.key in [pygame.K_SPACE, pygame.K_RETURN, pygame.K_ESCAPE]:
				self.change_state = "intro"

	def update(self, delta_time):
		pass

	def render(self, canvas):

		background = asset.get("background")
		background.set_alpha(cfg("layout.info.background.alpha"))
		canvas.blit(background, (0,0))
		font=asset.get("font_small")

		x,y=cfg("layout.info.text_info.pos")
		for line in asset.get("text_info"):
			line=line.strip()
			text = font.render(line, True, cfg("game.foreground_color"), None)
			canvas.blit(text, (x,y))
			y+=cfg("layout.info.text_info.spacing")

		x,y=cfg("layout.info.text_keys.pos")
		for line in asset.get("text_keys"):
			line=line.strip()
			text = font.render(line, True, cfg("game.foreground_color"), None)
			canvas.blit(text, (x,y))
			y+=cfg("layout.info.text_keys.spacing")

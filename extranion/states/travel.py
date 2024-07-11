import pygame
import random
from pygame.math import Vector2 as vector
from extranion.tools import log
from extranion.config import cfg
from extranion.states.state import State
from extranion.effects.stars3d import Stars3D
from extranion.soundmanager import SoundManager
from extranion.asset import asset

class Travel(State):

	def __init__(self):
		super().__init__()
		self.name="travel"

	def enter(self):
		asset.load('travel','layout.travel.ship-straight', 'ship')
		asset.load('travel','layout.travel.ship-turn', 'ship-turn')
		asset.load('travel', 'sound.travel.traveling')

		self.__ship_pos=cfg("layout.travel.ship_pos")
		self.__travelling_time=cfg("layout.travel.travelling_time")
		self.__arriving_time=cfg("layout.travel.arriving_time")
		self.__turbulencias_time=cfg("layout.travel.turbulencias_time")
		self.__turbulencias=vector(0,0)

		# iniciamos el efecto de estrellas a máxima velocidad
		self.__stars=Stars3D(cfg("game.canvas_size"), speed=8)

		SoundManager.play_sound("traveling")

	def exit(self):
		SoundManager.stop_sound("traveling")
		asset.unload("travel")
		self.__stars.release()

	def event(self, event):
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_SPACE:
				self.change_state = "gameplay"
			if event.key == pygame.K_ESCAPE:
				self.change_state = "intro"

	def update(self, delta_time):

		# actualizamos estrellas
		self.__stars.update(delta_time)

		# actualizamos turbulencias de la nave
		self.__turbulencias_time-=delta_time
		if self.__turbulencias_time<=0:
			shift=cfg("layout.travel.turbulencias_shift")
			self.__turbulencias=vector(random.randint(0,shift)-shift/2, random.randint(0,shift)-shift/2)
			self.__turbulencias_time=cfg("layout.travel.turbulencias_time")

		# tiempo de vuelo
		if self.__travelling_time>0:
			self.__travelling_time-=delta_time
		else:
			self.__arriving_time-=delta_time
			self.__ship_pos+=vector(6,-2)

		if self.__arriving_time<=0:
			self.change_state = "gameplay"

	def render(self, canvas):
		# primero pintamos las estrellas de fondo
		self.__stars.render(canvas)

		if self.__travelling_time>0:
			# mostramos la nave viajando
			logo=asset.get("ship")
			canvas.blit(logo, self.__ship_pos+self.__turbulencias)
		else:
			# mostramos la nave girando
			logo=asset.get("ship-turn")
			canvas.blit(logo, self.__ship_pos+self.__turbulencias)

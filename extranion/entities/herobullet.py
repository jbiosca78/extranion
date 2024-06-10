from extranion.entities.entity import Entity
import pygame
from pygame.math import Vector2 as vector
from extranion.config import cfg
from extranion import log

class HeroBullet(Entity):

	def __init__(self, name, position=(0,0)):
		super().__init__(name, position)

		self._speed=cfg("entities.herobullet.speed")



	def update(self, delta_time):
		super().update(delta_time)

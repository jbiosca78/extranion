import pygame
from pygame.math import Vector2 as vector
from extranion.tools import log
from extranion.config import cfg
from extranion.entities.entity import Entity

class Explossion(Entity):

	def __init__(self, name, position):
		super().__init__("explossion."+name, position)
		self.__time=cfg(f"entities.explossion.{name}.time")
		log.debug(f"Explossion {name} created at {position}")

	def update(self, delta_time):
		super().update(delta_time)

		self.__time-=delta_time
		if int(self.__time)<=0:
			self.kill()
			log.debug(f"Explossion {self.name} at {self.position} timed out")


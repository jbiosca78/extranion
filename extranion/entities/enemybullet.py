from extranion.entities.entity import Entity
import pygame
from pygame.math import Vector2 as vector
from extranion.config import cfg
from extranion import log

class HeroBullet(Entity):

	def __init__(self, position=(0,0)):
		super().__init__("herobullet", position)

		self.velocity=vector(0, cfg("entities.enemybullet.speed"))


	def update(self, delta_time):
		super().update(delta_time)

		if self.position.y < 0: self.kill()

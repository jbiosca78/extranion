from abc import ABC, abstractmethod
import pygame
from extranion.asset import asset

# Esta clase representa una entidad del juego, y gestiona:
# El asset (spritesheet), y su animación
# La posición y dirección de movimiento (velocidad)
# La actualización de la posición y el renderizado

class Entity(ABC):

	def __init__(self, position, spritesheet, spriterow, spritecol=0, spriteframes=3, spritespeed=120):

		self.position = pygame.math.Vector2(position[0], position[1])
		self.velocity = pygame.math.Vector2(0.0, 0.0)

		self.spritesheet=asset.get(spritesheet)
		self.spriterow=spriterow
		self.spritecol=spritecol
		self.spriteframes=spriteframes
		self.spritespeed=spritespeed

		self.spriteidx=0

	@abstractmethod
	def update(self, delta_time):

		# animación sprite
		self.spriteidx+=delta_time/self.spritespeed
		if self.spriteidx>=self.spriteframes: self.spriteidx=0

		# desplazamiento
		self.position+=self.velocity*delta_time

	@abstractmethod
	def render(self, canvas):

		sprite=self.spritesheet[self.spriterow][self.spritecol+int(self.spriteidx)]
		canvas.blit(sprite, self.position)

	def get_position(self):
		return list(self.position)

	def get_width(self):
		return self.spritesheet[self.spriterow][self.spritecol].get_width()

	def get_height(self):
		return self.spritesheet[self.spriterow][self.spritecol].get_height()

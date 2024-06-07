from abc import ABC, abstractmethod
import pygame
from extranion.asset import asset

class Entity(ABC):

	def __init__(self, position, spritesheet, spriterow, spritecol=0, spriteframes=3, spritespeed=64):

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
		#self.position.x+=self.velocity.x
		#self.position.y+=self.velocity.y

	@abstractmethod
	def render(self, canvas):

		sprite=self.spritesheet[self.spriterow][self.spritecol+int(self.spriteidx)]
		canvas.blit(sprite, self.position)

	def get_position(self):
		return list(self.position)

	def get_width(self):
		return self.spritesheet[self.spriterow][0].get_width()

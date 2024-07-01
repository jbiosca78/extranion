import pygame
import random
from extranion.entities.entity import Entity
from extranion.config import cfg
from extranion import log

class Pajaro(Entity):

	@staticmethod
	def create_wave(enemies):
		log.info("Creating wave of pajaros")
		space_rect=cfg("layout.game.space_rect")
		for i in range(cfg("gameplay.wave_size")):
			xpos=random.randint(space_rect[0], space_rect[2])
			enemies.add(Pajaro([xpos,-30*i]))

	def __init__(self, position=(0,0)):
		super().__init__("pajaro", position)

		# direcciones de movimiento inicial
		self.__space_rect=cfg("layout.game.space_rect")
		middle=self.__space_rect[2]//2
		if self.position.x<middle: self.__direction_x=1
		else: self.__direction_x=-1
		self.__direction_y=1

	def update(self, delta_time):

		super().update(delta_time)

		if self.position.y<-100:
			self.kill()
			return

		if self.position.x<self.__space_rect[0]: self.__direction_x=1
		if self.position.x>self.__space_rect[2]: self.__direction_x=-1

		if self.position.y>self.__space_rect[3]*0.8: self.__direction_y=-1

		self.velocity.y=cfg("entities.pajaro.speed_y")*self.__direction_y
		self.velocity.x=cfg("entities.pajaro.speed_x")*self.__direction_x

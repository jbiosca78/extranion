import pygame
import random
from extranion import log
from extranion.config import cfg
from extranion.entities.enemies.enemy import Enemy

class Pajaro(Enemy):

	# método para crear olas de enemigos de tipo pajaro
	@staticmethod
	def create_wave(enemies, wave_size, speed_mul):
		log.info("Creating wave of pajaros")
		space_rect=cfg("layout.game.space_rect")
		for i in range(0,wave_size):
			xpos=random.randint(space_rect[0], space_rect[2])
			enemies.add(Pajaro([xpos,-30*i], speed_mul=speed_mul))

	def __init__(self, position=(0,0), speed_mul=1):
		super().__init__("pajaro", position)

		self.__speed_mul=speed_mul

		# direcciones de movimiento inicial, hacia abajo en diagonal
		self.__direction_y=1
		self.__space_rect=cfg("layout.game.space_rect")
		middle=self.__space_rect[2]//2
		if self.position.x<middle: self.__direction_x=1
		else: self.__direction_x=-1

	def _update_attack(self, delta_time):

		# el pájaro cambia de dirección aleatoriamente
		if random.randint(0,cfg("entities.enemy.pajaro.turn_rand"))==0:
			self.__direction_x*=-1

		# se mueve en diagonal, rebotando en los lados
		if self.position.x<self.__space_rect[0]: self.__direction_x=1
		if self.position.x>self.__space_rect[2]: self.__direction_x=-1

		# si llega abajo del todo, vuelve hacia arriba
		if self.position.y>self.__space_rect[3]: self.__direction_y=-1

		self.velocity.x=cfg("entities.enemy.pajaro.speed_x")*self.__direction_x*self.__speed_mul
		self.velocity.y=cfg("entities.enemy.pajaro.speed_y")*self.__direction_y*self.__speed_mul

	def flee(self):
		# se van hacia arriba
		self.velocity.y=-cfg("entities.enemy.pajaro.speed_y")*self.__speed_mul
		super().flee()

	def _update_flee(self, delta_time):

		# el pájaro cambia de dirección aleatoriamente
		if random.randint(0,cfg("entities.enemy.pajaro.turn_rand"))==0:
			self.__direction_x*=-1

		# rebotando en los lados
		if self.position.x<self.__space_rect[0]: self.__direction_x=1
		if self.position.x>self.__space_rect[2]: self.__direction_x=-1

		self.velocity.x=cfg("entities.enemy.pajaro.speed_x")*self.__direction_x*self.__speed_mul

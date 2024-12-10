import random
import pygame
from pygame.math import Vector2 as vector
from extranion.tools import log
from extranion.config import cfg
from extranion.entities.enemies.enemy import Enemy

class Rueda(Enemy):

	# método para crear las olas de enemigos de tipo rueda
	@staticmethod
	def create_wave(enemies, wave_size, speed_mul):
		log.info("Creating wave of ruedas")
		space_rect=cfg("layout.gameplay.space_rect")
		xpos=random.randint(space_rect[0], space_rect[2])
		for i in range(0,wave_size):
			enemies.add(Rueda([xpos,-32-i*32], speed_mul=speed_mul))

	def __init__(self, position=(0,0), speed_mul=1):
		super().__init__("rueda", position)

		self.destination=None
		self.new_destination=None
		self.__speed_mul=speed_mul

	def _update_attack(self, delta_time):

		# Las ruedas se mueven en fila hacia el jugador a una velocidad constante,
		# calculamos el vector unitario hacia el objetivo para un movimiento directo.

		# Para evitar el apelotonamiento, en lugar de que cada enemigo siga al jugador
		# desde gameplay le damos a cada enemigo la posición del anterior, que se actualiza
		# a la nueva posición cuando llega. El primer enemigo persigue al jugador.

		# En el exerion original la rueda era la tercera ola, pero al ir rectos es
		# mucho mas fácil que la primera ola, por eso las hemos intercambiado.

		if self.destination is None: self.destination=self.new_destination
		if self.destination is None: return

		# calculamos el vector hacia nuestro destino
		direction = vector(self.destination) - self.position
		# calculamos la distancia
		distance = direction.length()
		# si estamos muy cerca, vamos al nuevo destino
		if distance<2: self.destination=self.new_destination
		# lo convertimos a vector unitario
		if distance>0: direction.normalize_ip()
		# y lo ajustamos a la velocidad
		velocity=direction*cfg("entities.enemy.rueda.speed")
		# si estamos muy cerca, frenamos un poco
		if distance<30: velocity=velocity*0.8
		#	self.destination=self.new_destination
		self.velocity=velocity*self.__speed_mul

	# si se acaba el tiempo de ataque o el jugador muere, los enemigos huyen
	def flee(self):
		# cuando huyen, establecemos direcciones aleatorias
		speed_max=cfg("entities.enemy.rueda.speed")
		self.velocity.x=speed_max*(random.randint(0,1)*2-1)*self.__speed_mul
		self.velocity.y=speed_max*(random.randint(0,1)*2-1)*self.__speed_mul
		super().flee()

	def _update_flee(self, delta_time):
		# nos movemos en la dirección establecida sin cambiar de dirección
		pass


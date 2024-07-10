import random
import pygame
from pygame.math import Vector2 as vector
from extranion.tools import log
from extranion.config import cfg
from extranion.entities.enemies.enemy import Enemy

class Ovni(Enemy):

	# método para crear olas de enemigos de tipo mariposa
	@staticmethod
	def create_wave(enemies, wave_size, speed_mul):
		log.info("Creating wave of ovnis")
		space_rect=cfg("layout.gameplay.space_rect")
		xpos=random.randint(space_rect[0], space_rect[2])
		for i in range(0,wave_size):
			enemies.add(Ovni([xpos,-30-i*30], speed_mul=speed_mul))

	def __init__(self, position=(0,0), speed_mul=1):
		super().__init__("ovni", position)
		self.__speed_mul=speed_mul
		self.__set_destination()

	def __set_destination(self):
		x=random.randint(self.space_rect[0], self.space_rect[2])
		y=random.randint(self.space_rect[1], self.space_rect[3])
		self.__destination=vector(x,y)

	def _update_attack(self, delta_time):

		# los ovnis se mueven hacia una posicion aleatoria de la pantalla
		# cuando llega al destino, se dirige a otra posición aleatoria

		# si estamos muy cerca del destino, establecemos otro
		distance = (self.__destination-self.position).length()
		if distance<16: self.__set_destination()

		# calculamos el vector hacia nuestro destino
		direction = vector(self.__destination) - self.position
		# calculamos la distancia
		distance = direction.length()
		# si estamos muy cerca, vamos al nuevo destino
		if distance<2: self.destination=self.new_destination
		# lo convertimos a vector unitario
		if distance>0: direction.normalize_ip()
		# y lo ajustamos a la velocidad
		velocity=direction*cfg("entities.enemy.ovni.speed")
		# si estamos muy cerca, frenamos un poco
		if distance<30: velocity=velocity*0.8
		#	self.destination=self.new_destination
		self.velocity=velocity*self.__speed_mul

	# si se acaba el tiempo de ataque o el jugador muere, los enemigos huyen
	def flee(self):
		# cuando huyen, establecemos direcciones aleatorias
		speed=cfg("entities.enemy.ovni.speed")
		self.velocity.x=speed*(random.randint(0,1)*2-1)*self.__speed_mul
		self.velocity.y=speed*(random.randint(0,1)*2-1)*self.__speed_mul
		super().flee()

	def _update_flee(self, delta_time):
		# nos movemos en la dirección establecida sin cambiar de dirección
		pass

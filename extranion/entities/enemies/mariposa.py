import pygame
import random
from extranion.tools import log
from extranion.config import cfg
from extranion.entities.enemies.enemy import Enemy

class Mariposa(Enemy):

	# método para crear olas de enemigos de tipo mariposa
	@staticmethod
	def create_wave(enemies, wave_size, speed_mul):
		log.info("Creating wave of mariposas")
		space_rect=cfg("layout.gameplay.space_rect")
		xpos=random.randint(space_rect[0], space_rect[2])
		for i in range(0,wave_size):
			enemies.add(Mariposa([xpos,-30-i*30], speed_mul=speed_mul))

	def __init__(self, position=(0,0), speed_mul=1):
		super().__init__("mariposa", position)

		# la mariposa persigue al jugador o a la posición de otra mariposa
		# cuando llega al destino, se dirige a la siguiente posición
		self.destination=None
		self.new_destination=None
		self.__speed_mul=speed_mul

	def _update_attack(self, delta_time):

		# La mariposa sigue al jugador. Pero a diferencia de Exerion que siempre
		# iba a la misma velocidad en direcciones ortogonales o diagonales, aquí
		# agregamos el concepto de aceleración, obteniendo un movimiento mucho más
		# orgánico. además se consigue un efecto de 'ondulación' que hace que se
		# parezca más aun al movimiento de una mariposa. Éxito absoluto aquí.

		if self.destination is None: self.destination=self.new_destination

		# si estamos muy cerca del objetivo anterior, vamos al nuevo objetivo
		distance = (pygame.math.Vector2(self.destination)-self.position).length()
		if distance<16: self.destination=self.new_destination
		if self.destination is None: return

		# Aceleramos cada componente hacia el objetivo
		acceleration=cfg("entities.enemy.mariposa.acceleration")

		if self.destination.x > self.position.x: self.velocity.x += acceleration
		if self.destination.x < self.position.x: self.velocity.x -= acceleration
		if self.destination.y > self.position.y: self.velocity.y += acceleration
		if self.destination.y < self.position.y: self.velocity.y -= acceleration

		# limitamos la velocidad
		speed_max=cfg("entities.enemy.mariposa.speed_max")
		if self.velocity.x>speed_max*self.__speed_mul: self.velocity.x=speed_max
		if self.velocity.x<-speed_max*self.__speed_mul: self.velocity.x=-speed_max
		if self.velocity.y>speed_max*self.__speed_mul: self.velocity.y=speed_max
		if self.velocity.y<-speed_max*self.__speed_mul: self.velocity.y=-speed_max

	# si se acaba el tiempo de ataque o el jugador muere, los enemigos huyen
	def flee(self):
		# cuando huyen, establecemos direcciones aleatorias
		speed_max=cfg("entities.enemy.mariposa.speed_max")
		self.velocity.x=speed_max*(random.randint(0,1)*2-1)*self.__speed_mul
		self.velocity.y=speed_max*(random.randint(0,1)*2-1)*self.__speed_mul
		super().flee()

	def _update_flee(self, delta_time):
		# nos movemos en la dirección establecida sin cambiar de dirección
		pass

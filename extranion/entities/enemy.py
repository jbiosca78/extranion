from extranion.entities.entity import Entity
import pygame
from pygame.math import Vector2 as vector
from extranion.config import cfg
from extranion import log

class Enemy(Entity):

	def __init__(self, name, position=(0,0), destination=None):
		super().__init__(name, position)

		self.name=name
		self._space_rect=cfg("layout.game.space_rect")

		if name=="rueda" or name=="mariposa":
			self.destination=destination
			self.new_destination=None

		if name=="pajaro":
			middle=self._space_rect[2]//2
			if self.position.x<middle:
				self._direction=1
			else:
				self._direction=-1

	def update(self, delta_time):
		super().update(delta_time)

		if self.name == "rueda": self.__update_rueda()
		if self.name == "pajaro": self.__update_pajaro()
		if self.name == "mariposa": self.__update_mariposa()

	def __update_rueda(self):
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
		direction = pygame.math.Vector2(self.destination) - self.position
		# calculamos la distancia
		distance = direction.length()
		# si estamos muy cerca, vamos al nuevo destino
		if distance<2: self.destination=self.new_destination
		# lo convertimos a vector unitario
		if distance>0: direction.normalize_ip()
		# y lo ajustamos a la velocidad
		velocity=direction*cfg("entities.rueda.speed")
		# si estamos muy cerca, frenamos un poco
		if distance<30: velocity=velocity*0.8
		#	self.destination=self.new_destination
		self.velocity=velocity

	def __update_pajaro(self):

		if self.position.x<self._space_rect[0]: self._direction=1
		if self.position.x>self._space_rect[2]: self._direction=-1

		self.velocity.y=cfg("entities.pajaro.speed_y")
		self.velocity.x=cfg("entities.pajaro.speed_x")*self._direction

	def __update_mariposa(self):

		# La mariposa sigue al jugador. Pero a diferencia de Exerion que siempre
		# iba a la misma velocidad en direcciones ortogonales o diagonales, aquí
		# agregamos el concepto de aceleración, obteniendo un movimiento mucho más
		# orgánico. además se consigue un efecto de 'ondulación' que hace que se
		# parezca más aun al movimiento de una mariposa. Éxito absoluto aquí.

		if self.destination is None: self.destination=self.new_destination

		# si estamos muy cerca del objetivo anterior, vamos al nuevo objetivo
		distance = (pygame.math.Vector2(self.destination)-self.position).length()
		if distance<8: self.destination=self.new_destination

		# si no tenemos destino aun, salimos
		if self.destination is None: return

		# Aceleramos cada componente hacia el objetivo
		acceleration=cfg("entities.mariposa.acceleration")
		if self.destination.x > self.position.x: self.velocity.x += acceleration
		if self.destination.x < self.position.x: self.velocity.x -= acceleration
		if self.destination.y > self.position.y: self.velocity.y += acceleration
		if self.destination.y < self.position.y: self.velocity.y -= acceleration

		# limitamos la velocidad
		speed_max=cfg("entities.mariposa.speed_max")
		if self.velocity.x>speed_max: self.velocity.x=speed_max
		if self.velocity.x<-speed_max: self.velocity.x=-speed_max
		if self.velocity.y>speed_max: self.velocity.y=speed_max
		if self.velocity.y<-speed_max: self.velocity.y=-speed_max




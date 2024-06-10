from extranion.entities.entity import Entity
import pygame
from pygame.math import Vector2 as vector
from extranion.config import cfg
from extranion import log

class Enemy(Entity):

	def __init__(self, name, position=(0,0), destination=None):
		super().__init__(name, position)

		self._name=name
		self._space_rect=cfg("layout.game.space_rect")
		self.destination=destination
		self.new_destination=None

	def update(self, delta_time):
		super().update(delta_time)

		if self._name == "mariposa": self._move_mariposa()
		if self._name == "rueda": self._move_rueda()

	def _move_mariposa(self):
		# La mariposa sigue al jugador. Pero a diferencia de Exerion que siempre
		# iba a la misma velocidad en direcciones ortogonales o diagonales, aquí
		# agregamos el concepto de aceleración, obteniendo un movimiento mucho más
		# orgánico. además se consigue un efecto de 'ondulación' que hace que se
		# parezca más aun al movimiento de una mariposa. éxito absoluto aquí.

		# Para evitar el apelotonamiento, en lugar de que cada enemigo siga al jugador
		# con un callback de posición, desde gameplay le damos a cada enemigo la posición
		# del anterior, que se actualiza a la nueva cuando llega. El primer enemigo
		# persigue al jugador.

		if self.destination is None: self.destination=self.new_destination
		if self.destination is None: return

		# si estamos muy cerca del objetivo anterior, vamos al nuevo objetivo
		distance = (pygame.math.Vector2(self.destination)-self.position).length()
		if distance<10: self.destination=self.new_destination

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

	def _move_rueda(self):
		# La rueda es parecida a la mariposa pero sin aceleración y calculando el vector
		# unitario hacia el objetivo para un movimiento directo. Debido a eso es mas
		# fácil que se acaben apelotonando, por lo que agregamos un 'freno' cuando el
		# siguiente objetivo está cerca.

		if self.destination is None: self.destination=self.new_destination
		if self.destination is None: return

		# calculamos el vector hacia nuestro destino
		direction = pygame.math.Vector2(self.destination) - self.position
		# calculamos la distancia
		distance = direction.length()
		# si estamos muy cerca, vamos al nuevo destino
		if distance<4: self.destination=self.new_destination
		# lo convertimos a vector unitario
		if distance>0: direction.normalize_ip()
		# y lo ajustamos a la velocidad
		velocity=direction*cfg("entities.rueda.speed")
		# si estamos muy cerca, frenamos un poco
		if distance<30: velocity=velocity*0.8
		#	self.destination=self.new_destination
		self.velocity=velocity

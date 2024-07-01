import pygame
import random
from extranion.entities.entity import Entity
from extranion.config import cfg
from extranion import log

class Mariposa(Entity):

	@staticmethod
	def create_wave(enemies):
		log.info("Creating wave of mariposas")
		space_rect=cfg("layout.game.space_rect")
		xpos=random.randint(space_rect[0], space_rect[2])
		for i in range(cfg("gameplay.wave_size")):
			enemies.add(Mariposa([xpos,-30-i*30]))

	def __init__(self, position=(0,0)):
		super().__init__("mariposa", position)

		self._space_rect=cfg("layout.game.space_rect")
		self.destination=None
		self.new_destination=None

	def update(self, delta_time):
		super().update(delta_time)

		# La mariposa sigue al jugador. Pero a diferencia de Exerion que siempre
		# iba a la misma velocidad en direcciones ortogonales o diagonales, aquí
		# agregamos el concepto de aceleración, obteniendo un movimiento mucho más
		# orgánico. además se consigue un efecto de 'ondulación' que hace que se
		# parezca más aun al movimiento de una mariposa. Éxito absoluto aquí.

		if self.destination is None: self.destination=self.new_destination

		# si estamos muy cerca del objetivo anterior, vamos al nuevo objetivo
		distance = (pygame.math.Vector2(self.destination)-self.position).length()
		if distance<8: self.destination=self.new_destination
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


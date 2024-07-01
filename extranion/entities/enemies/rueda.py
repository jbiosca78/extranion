from extranion.entities.entity import Entity
import pygame
from extranion.config import cfg
from extranion import log
import random

class Rueda(Entity):

	@staticmethod
	def create_wave(enemies):
		log.info("Creating wave of ruedas")
		space_rect=cfg("layout.game.space_rect")
		xpos=random.randint(space_rect[0], space_rect[2])
		for i in range(cfg("gameplay.wave_size")):
			enemies.add(Rueda([xpos,-30-i*30]))

	def __init__(self, position=(0,0)):
		super().__init__("rueda", position)

		self._space_rect=cfg("layout.game.space_rect")

		self.destination=None
		self.new_destination=None

	def update(self, delta_time):
		super().update(delta_time)

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

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

		# iniciamos los enemigos ne modo ataque
		self.attack=True
		self.__attack_time=cfg("entities.mariposa.attack_time")
		self.__flee_time=cfg("entities.mariposa.flee_time")

	def update(self, delta_time):

		if self.attack:
			self.__update_attack(delta_time)
			# tiempo de ataque
			self.__attack_time-=delta_time
			if self.__attack_time<0: self.flee()
		else:
			self.__update_flee(delta_time)
			# tiempo de huida
			self.__flee_time-=delta_time
			if self.__flee_time<0:
				self.kill()

	# si se acaba el tiempo de ataque o el jugador muere, los enemigos huyen
	def flee(self):
		self.attack=False

		speed_max=cfg("entities.mariposa.speed_max")
		if random.randint(0,1)==0: self.velocity.y=speed_max
		else: self.velocity.y=-speed_max
		if random.randint(0,1)==0: self.velocity.x=speed_max
		else: self.velocity.x=-speed_max

	def __update_attack(self, delta_time):

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

		super().update(delta_time)

	def __update_flee(self, delta_time):

		# nos movemos en la dirección que tuvieramos sin descanso
		super().update(delta_time)

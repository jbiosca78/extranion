from abc import ABC, abstractmethod
from extranion.entities.entity import Entity
from extranion.config import cfg

class Enemy(Entity, ABC):

	def __init__(self, name, position=(0,0)):
		super().__init__("enemy."+name, position, random_frame=True)

		# iniciamos los enemigos en modo ataque
		self.attacking=True
		self.__attack_time=cfg(f"entities.enemy.{name}.attack_time")
		self.__flee_time=cfg(f"entities.enemy.{name}.flee_time")

	def update(self, delta_time):

		if self.attacking:
			self._update_attack(delta_time)
			# tiempo de duración en estado de ataque
			self.__attack_time-=delta_time
			if self.__attack_time<0: self.flee()
		else:
			self._update_flee(delta_time)
			# tiempo de duración en estado de huida
			self.__flee_time-=delta_time
			if self.__flee_time<0: self.kill()

		super().update(delta_time)

	# si se acaba el tiempo de ataque o el jugador muere, los enemigos huyen
	def flee(self):
		self.attacking=False

	# movimiento del enemigo cuando está atacando
	@abstractmethod
	def _update_attack(self, delta_time):
		pass

	# movimiento del enemigo cuando está huyendo
	@abstractmethod
	def _update_flee(self, delta_time):
		pass

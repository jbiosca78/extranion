from pygame.math import Vector2 as vector
from extranion.tools import log
from extranion.config import cfg
from extranion.entities.entity import Entity

class EnemyBullet(Entity):

	def __init__(self, position=(0,0)):
		super().__init__("bullet.enemy", position)

		self.velocity=vector(0, cfg("entities.bullet.enemy.speed"))

	def update(self, delta_time):
		super().update(delta_time)

		if self.position.y > self.space_rect[3]: self.kill()


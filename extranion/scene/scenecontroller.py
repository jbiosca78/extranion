from extranion.entities.enemy import Enemy
from extranion.config import cfg

class SceneController:

	def __init__(self):
		self.scene=0
		self.wave=0
		self.wavewait=0

	def update(self, delta_time, hero, enemies):

		if len(enemies)==0:

			if self.wavewait==0:
				self.scene+=1
				self.wave=1
			self.wavewait+=delta_time
			if self.wavewait>cfg("mechanics.wave_wait"):
				for i in range(cfg("mechanics.wave_size")):
					enemies.add(Enemy("mariposa", [400+i*30,0-i*30]))
					#self._enemies.add(Enemy("rueda", [400+i*30,0-i*30]))
				self.wavewait=0

		pos=None
		for enemy in enemies:
			if pos is None: enemy.destination=hero.get_position()
			else: enemy.new_destination=pos
			pos=enemy.get_position()

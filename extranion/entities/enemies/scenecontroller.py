import random
#from extranion.entities.enemy import Enemy
from extranion.entities.enemybullet import EnemyBullet
from extranion.config import cfg
from extranion import log
from extranion.entities.enemies.rueda import Rueda
from extranion.entities.enemies.pajaro import Pajaro
from extranion.entities.enemies.mariposa import Mariposa

# Esta clase se encarga de gestionar las distintas escenas (olas de enemigos).
# Cada escena tiene un tipo de enemigos que vienen en varias olas de ataque.
# Cuando todos los enemigos de una ola mueren o huyen, se pasa a la siguiente
# ola tras un breve periodo de tiempo.

class SceneController:

	def __init__(self):
		self.scene=1
		self.wave=0
		self.__wavewait=cfg("gameplay.wave_wait")
		self.__waves_per_scene=cfg("gameplay.waves_per_scene")
		self.__enemy_list=cfg("gameplay.enemy_list")
		self.__current_enemy=self.__enemy_list[0]

	def update(self, delta_time, hero, enemies, enemybullets):

		if self.__wavewait>0:
			# tiempo de espera entre olas de enemigos
			self.__wavewait-=delta_time
			if self.__wavewait<=0:
				# nueva ola
				log.info(f"New wave. wave={self.wave}, scene={self.scene}")
				self.__current_enemy=self.__enemy_list[(self.scene-1)%len(self.__enemy_list)]
				if self.__current_enemy=="rueda": Rueda.create_wave(enemies)
				if self.__current_enemy=="pajaro": Pajaro.create_wave(enemies)
				if self.__current_enemy=="mariposa": Mariposa.create_wave(enemies)
		else:
			# si no quedan enemigos, pasamos a la siguiente ola
			if len(enemies)==0:
				self.wave+=1
				if self.wave==self.__waves_per_scene:
					self.wave=0
					self.scene+=1
				# iniciamos espera entre olas
				self.__wavewait=cfg("gameplay.wave_wait")

		pos=None
		for enemy in enemies:

			# Para los enemigos que persiguen al jugador, el primero de ellos
			# siempre tiene de objetivo al jugador, el resto tienen de objetivo
			# la posición del enemigo anterior, y solo la actualizan al llegar (new_destination)
			# De esta forma conseguimos un movimiento 'en fila' en lugar de apelotonarse todos.
			if enemy.name in ["rueda", "mariposa"]:
				if pos is None: enemy.destination=hero.get_position()
				else: enemy.new_destination=pos
				# get position for next enemy
				pos=enemy.get_position()

				# random fire
				if random.randint(0,100)==0:
					enemybullets.add(EnemyBullet(pos))

			# Si el jugador muere, los enemigos se van
			if not hero.alive:
				enemy.attack=False

import random
from extranion.tools import log,gvar
from extranion.config import cfg
from extranion.entities.enemies.rueda import Rueda
from extranion.entities.enemies.pajaro import Pajaro
from extranion.entities.enemies.mariposa import Mariposa
from extranion.entities.enemies.ovni import Ovni
from extranion.entities.enemybullet import EnemyBullet

# Esta clase se encarga de gestionar las distintas escenas (olas de enemigos).
# Cada escena tiene un tipo de enemigos que vienen en varias olas de ataque.
# Cuando todos los enemigos de una ola mueren o huyen, se pasa a la siguiente
# ola tras un breve periodo de tiempo.

class SceneController:

	def __init__(self):
		self.scene=0
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
				# ajustamos velocidad según la escena, para aumentar complejidad
				speed_mul=1+self.scene/100
				hero.speed_mul=speed_mul
				# creamos ola de enemigos
				log.info(f"New wave. wave={self.wave+1}, scene={self.scene+1}")
				wave_size=int(cfg("gameplay.wave_size"))
				self.__current_enemy=self.__enemy_list[self.scene%len(self.__enemy_list)]
				if self.__current_enemy=="rueda": Rueda.create_wave(enemies, wave_size, speed_mul)
				if self.__current_enemy=="pajaro": Pajaro.create_wave(enemies, wave_size, speed_mul)
				if self.__current_enemy=="mariposa": Mariposa.create_wave(enemies, wave_size, speed_mul)
				if self.__current_enemy=="ovni": Ovni.create_wave(enemies, wave_size, speed_mul)

		else:
			# si no quedan enemigos, pasamos a la siguiente ola
			if len(enemies)==0:
				self.wave+=1
				if self.wave==self.__waves_per_scene:
					self.wave=0
					self.scene+=1
					gvar.scene=self.scene
				# iniciamos espera entre olas
				self.__wavewait=cfg("gameplay.wave_wait")

		# Para los enemigos que persiguen al jugador, el primero de ellos
		# siempre tiene de objetivo al jugador, el resto tienen de objetivo
		# la posición del enemigo anterior, y solo la actualizan al llegar (new_destination)
		# De esta forma conseguimos un movimiento 'en fila' en lugar de apelotonarse todos.
		if self.__current_enemy in ["rueda", "mariposa"]:
			destination=None
			for enemy in enemies:
				if destination is None: enemy.destination=hero.get_position()
				else: enemy.new_destination=destination
				destination=enemy.get_position()

		# Si el jugador muere, los enemigos se van
		if not hero.alive:
			for enemy in enemies:
				if enemy.attacking: enemy.flee()

		# Si el jugador está vivo, los enemigos disparan. en cada escena hay un proyectil
		# más que la anterior, para incrementar la complejidad del juego
		enemy_shots_max=cfg("gameplay.enemy_shots")+self.scene*cfg("gameplay.enemy_shots_add_scene")
		if hero.alive:
			for enemy in enemies:
				if enemy.position.y>0 and \
				len(enemybullets)<enemy_shots_max and \
				random.randint(0,cfg("gameplay.enemy_shot_rand"))==0:
					enemybullets.add(EnemyBullet(enemy.get_position()))

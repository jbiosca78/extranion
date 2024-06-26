from extranion.entities.enemy import Enemy
from extranion.config import cfg

# Esta clase se encarga de gestionar las olas de enemigos y las escenas.
# Cada escena tiene un tipo de enemigos que vienen en varias olas de ataque.
# Cuando todos los enemigos de una ola mueren o huyen, se pasa a la siguiente
# ola tras un breve periodo de tiempo.

class SceneController:

	def __init__(self):
		self.scene=1
		self.wave=0
		self.__wavewait=0
		self.__enemy_list=cfg("gameplay.enemy_list")
		self.__waves_per_scene=cfg("gameplay.waves_per_scene")

	def update(self, delta_time, hero, enemies, enemybullets):

		# Si hay enemigos activos, estamos en una ola
		# Cuando no queda ninguno pasamos a la siguiente
		if len(enemies)==0:

			# Si wavewait es cero, comienza nueva ola de enemigos
			if self.__wavewait==0:
				self.wave+=1
				if self.wave>self.__waves_per_scene:
					self.wave=0
					self.scene+=1

			# Si no, lo incrementamos para 'descansar' un poco entre olas
			self.__wavewait+=delta_time

			# Cuando termina la espera vienen los enemigos
			if self.__wavewait>cfg("gameplay.wave_wait"):
				for i in range(cfg("gameplay.wave_size")):
					if (self.scene-1)%2==0: enemies.add(Enemy("mariposa", [400+i*30,0-i*30]))
					if (self.scene-1)%2==1: enemies.add(Enemy("rueda", [400+i*30,0-i*30]))

					#self._enemies.add(Enemy("rueda", [400+i*30,0-i*30]))
				self.__wavewait=0

		# Para los enemigos que persiguen al jugador, el primero de ellos
		# siempre tiene de objetivo al jugador, el resto tienen de objetivo
		# la posición del enemigo anterior, y sólo la actualizan al llegar (new_destination)
		# De esta forma conseguimos un movimiento 'en fila' en lugar de apelotonarse todos.
		pos=None
		for enemy in enemies:
			if pos is None: enemy.destination=hero.get_position()
			else: enemy.new_destination=pos
			pos=enemy.get_position()

	def __fire(self):

		self.__bullets.add(EnemyBullet(self.position))

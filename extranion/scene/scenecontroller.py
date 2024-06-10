from extranion.entities.enemy import Enemy
from extranion.config import cfg

class SceneController:

	def __init__(self):
		self.scene=0
		self.wave=0
		self.wavewait=0

	def update(self, delta_time, hero, enemies):

		# Si hay enemigos activos, estamos en una ola
		# Cuando no queda ninguno pasamos a la siguiente
		if len(enemies)==0:

			# Si wavewait es cero, comienza nueva ola de enemigos
			if self.wavewait==0:
				self.scene+=1
				self.wave=1

			# Si no, lo incrementamos para 'descansar' un poco entre olas
			self.wavewait+=delta_time

			# Cuando termina la espera vienen los enemigos
			if self.wavewait>cfg("mechanics.wave_wait"):
				for i in range(cfg("mechanics.wave_size")):
					if self.scene%2==0: enemies.add(Enemy("mariposa", [400+i*30,0-i*30]))
					if self.scene%2==1: enemies.add(Enemy("rueda", [400+i*30,0-i*30]))

					#self._enemies.add(Enemy("rueda", [400+i*30,0-i*30]))
				self.wavewait=0

		# Para los enemigos que persiguen al jugador, el primero de ellos
		# siempre tiene de objetivo al jugador, el resto tienen de objetivo
		# la posición del enemigo anterior, y sólo la actualizan al llegar (new_destination)
		# De esta forma consguimos un movimiento 'en fila' en lugar de apelotonarse todos.
		pos=None
		for enemy in enemies:
			if pos is None: enemy.destination=hero.get_position()
			else: enemy.new_destination=pos
			pos=enemy.get_position()

from extranion.entities.entity import Entity
import pygame
from extranion.config import cfg
from extranion import log

class Enemy(Entity):

	def __init__(self, name, position=(0,0), hero_position_callback=None):
		super().__init__(name, position)

		self._name=name
		self._space_rect=cfg("layout.game.space_rect")
		self._hero_position_callback = hero_position_callback

	def update(self, delta_time):
		super().update(delta_time)

		if self._name == "mariposa": self._move_mariposa()
		if self._name == "rueda": self._move_rueda()

	def render(self, canvas):
		super().render(canvas)

	def input(self, key, pressed):
		if key in self._keymap["up"]:
			self._input_pressed["up"] = pressed
			log.debug(f"up = {pressed}")
		elif key in self._keymap["down"]:
			self._input_pressed["down"]  = pressed
			log.debug(f"down = {pressed}")
		elif key in self._keymap["left"]:
			self._input_pressed["left"] = pressed
			log.debug(f"left = {pressed}")
		elif key in self._keymap["right"]:
			self._input_pressed["right"] = pressed
			log.debug(f"right = {pressed}")

		#if event.type == pygame.KEYDOWN:
		#	if event.key in self._keymap["left"]:
		#	#if event.key == pygame.K_LEFT:
		#		_dir=-1
		#	elif event.key == pygame.K_RIGHT:
		#		_dir=1
		#if event.type == pygame.KEYUP:
		#	_dir=0

	def _move_mariposa(self):
		# La mariposa sigue al jugador. Pero a diferencia de Exerion que siempre
		# iba a la misma velocidad en direcciones ortogonales o diagonales, aquí
		# agregamos el concepto de aceleración, obteniendo un movimiento mucho más
		# orgánico. además se consigue un efecto de 'ondulación' que hace que se
		# parezca más aun al movimiento de una mariposa. éxito absoluto aquí.

		hero_position = self._hero_position_callback()

		acceleration=cfg("entities.mariposa.acceleration")
		if hero_position.x > self.position.x: self.velocity.x += acceleration
		if hero_position.x < self.position.x: self.velocity.x -= acceleration
		if hero_position.y > self.position.y: self.velocity.y += acceleration
		if hero_position.y < self.position.y: self.velocity.y -= acceleration

		speed_max=cfg("entities.mariposa.speed_max")
		if self.velocity.x>speed_max: self.velocity.x=speed_max
		if self.velocity.x<-speed_max: self.velocity.x=-speed_max
		if self.velocity.y>speed_max: self.velocity.y=speed_max
		if self.velocity.y<-speed_max: self.velocity.y=-speed_max

	def _move_rueda(self):
		# La rueda se mueve exactamente igual que en Exerión, siempre hacia el jugador
		# a una velocidad fija. Es una especie de "bonus track" porque es muy fácil
		# de matar (aunque en niveles altos donde dispara mucho y hay que dar vueltas)
		# su puntación es mas baja por este motivo

		hero_position = self._hero_position_callback()
		# calculamos el vector hacia el jugador
		direction = pygame.math.Vector2(hero_position) - self.position
		# lo convertimos a vector unitario
		direction.normalize_ip()
		# y lo ajustamos a la velocidad
		self.velocity=direction*cfg("entities.rueda.speed")

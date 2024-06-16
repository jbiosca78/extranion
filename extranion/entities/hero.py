from extranion.entities.entity import Entity
import pygame
from pygame.math import Vector2 as vector
from extranion.config import cfg, gvar
from extranion import log
from extranion.entities.herobullet import HeroBullet

class Hero(Entity):

	def __init__(self, name, position, bullets):
		super().__init__(name, position)

		self._map_input()
		self._input_pressed = { "left": False, "right": False, "up": False, "down": False }

		self._acceleration=cfg("entities.hero.acceleration")
		self._speed_max=cfg("entities.hero.speed_max")
		self._speed_decay=cfg("entities.hero.speed_decay")

		# dimensiones del espacio donde puede entrar la nave
		space=cfg("layout.game.space_rect")
		self._space_rect=(space[0]+self.width/2, space[1]+self.height/2, space[2]-self.width/2, space[3]-self.height/2)

		# referencia a los proyectiles
		self.__bullets=bullets
		self.__cooldown_fast_fire=0
		self.__fast_firing=False
		self.charge=cfg("mechanics.initial_charge")

	def _map_input(self):
		self._keymap = {}
		kmap = cfg("keymap.hero")
		for g, v in kmap.items():
			self._keymap[g] = []
			for k in v:
				if k == "LALT": code=pygame.K_LALT
				else: code=pygame.key.key_code(k)
				self._keymap[g].append(code)

	def input(self, key, pressed):
		if key in self._keymap["up"]:
			self._input_pressed["up"] = pressed
			log.debug(f"up = {pressed}")
		elif key in self._keymap["down"]:
			self._input_pressed["down"] = pressed
			log.debug(f"down = {pressed}")
		elif key in self._keymap["left"]:
			self._input_pressed["left"] = pressed
			log.debug(f"left = {pressed}")
		elif key in self._keymap["right"]:
			self._input_pressed["right"] = pressed
			log.debug(f"right = {pressed}")
		elif key in self._keymap["fire_fast"]:
			self.__fast_firing = pressed
			log.debug(f"fire_fast = {pressed}")

		if pressed:
			if key in self._keymap["fire_normal"]: self.__fire("normal")
			#if key in self._keymap["fire_fast"]: self.__fire("fast")

	def update(self, delta_time):

		super().update(delta_time)
		gvar.HERO_POS=self.get_position()

		# obtenemos las direcciones de movimiento horizontal y vertical
		moving_x=moving_y=0
		if self._input_pressed["left"]: moving_x-=1
		if self._input_pressed["right"]: moving_x+=1
		if self._input_pressed["up"]: moving_y-=1
		if self._input_pressed["down"]: moving_y+=1

		# aceleramos en la dirección de movimiento correspondiente hasta el máximo
		self.velocity.x += moving_x*self._acceleration
		if self.velocity.x>self._speed_max: self.velocity.x=self._speed_max
		if self.velocity.x<-self._speed_max: self.velocity.x=-self._speed_max
		if moving_x==0: self.velocity.x*=(1-self._speed_decay)
		self.velocity.y += moving_y*self._acceleration
		if self.velocity.y>self._speed_max: self.velocity.y=self._speed_max
		if self.velocity.y<-self._speed_max: self.velocity.y=-self._speed_max
		if moving_y==0: self.velocity.y*=(1-self._speed_decay)

		# si estamos en un borde, no nos movemos y quitamos la aceleración hacia ese borde
		# para evitar el efecto "pegajoso". además si llegamos a un borde, permitimos
		# movimiento en otra dirección si es posible
		# simplifica esto en python
		if self.position.x<self._space_rect[0]:
			self.position.x=self._space_rect[0]
			if self.velocity.x<0: self.velocity.x=0
			log.debug("hero in left boundary")
		if self.position.y<self._space_rect[1]:
			self.position.y=self._space_rect[1]
			if self.velocity.y<0: self.velocity.y=0
			log.debug("hero in top boundary")
		if self.position.x>self._space_rect[2]:
			self.position.x=self._space_rect[2]
			if self.velocity.x>0: self.velocity.x=0
			log.debug("hero in right boundary")
		if self.position.y>self._space_rect[3]:
			self.position.y=self._space_rect[3]
			if self.velocity.y>0: self.velocity.y=0
			log.debug("hero in bottom boundary")

		# establecemos la animación según el movimiento horizontal
		self.set_animation(["left","default","right"][moving_x+1])

		if self.__cooldown_fast_fire>0: self.__cooldown_fast_fire-=delta_time
		if self.__fast_firing: self.__fire("fast")


	def __fire(self, fire_type):

		if fire_type=="normal":
			if len(self.__bullets)>1: return
			self.__bullets.add(HeroBullet(self.position-vector(8,0)))
			self.__bullets.add(HeroBullet(self.position+vector(8,0)))

		if fire_type=="fast":
			if self.__cooldown_fast_fire>0: return
			if self.charge==0: return
			self.charge-=1
			self.__cooldown_fast_fire=cfg("entities.hero.cooldown_fast_fire")
			self.__bullets.add(HeroBullet(self.position))

		#if event.type == pygame.KEYDOWN:
		#	if event.key in self._keymap["left"]:
		#	#if event.key == pygame.K_LEFT:
		#		_dir=-1
		#	elif event.key == pygame.K_RIGHT:
		#		_dir=1
		#if event.type == pygame.KEYUP:
		#	_dir=0

from extranion.entities.entity import Entity
import pygame
from extranion.config import cfg
from extranion import log

class Hero(Entity):

	def __init__(self, name, position):
		#super().__init__(spritesheet=spritesheet, position=position, spriterow=1, spritespeed=64)
		super().__init__(name, position)

		self._map_input()
		self._input_pressed = { "left": False, "right": False, "up": False, "down": False }

		self._acceleration=cfg("entities.hero.acceleration")
		self._speed_max=cfg("entities.hero.speed_max")
		self._speed_decay=cfg("entities.hero.speed_decay")

		self._space_rect=cfg("layout.game.space_rect")

	def _map_input(self):
		self._keymap = {}
		kmap = cfg("keymap.hero")
		for g, v in kmap.items():
			self._keymap[g] = []
			for k in v:
				code=pygame.key.key_code(k)
				self._keymap[g].append(code)

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

	def update(self, delta_time):
		super().update(delta_time)

		# get move directions
		moving_x=moving_y=0
		if self._input_pressed["left"]: moving_x-=1
		if self._input_pressed["right"]: moving_x+=1
		if self._input_pressed["up"]: moving_y-=1
		if self._input_pressed["down"]: moving_y+=1

		# increase velocity in moving direction
		self.velocity.x += moving_x*self._acceleration
		if self.velocity.x>self._speed_max: self.velocity.x=self._speed_max
		if self.velocity.x<-self._speed_max: self.velocity.x=-self._speed_max
		if moving_x==0: self.velocity.x*=(1-self._speed_decay)
		self.velocity.y += moving_y*self._acceleration
		if self.velocity.y>self._speed_max: self.velocity.y=self._speed_max
		if self.velocity.y<-self._speed_max: self.velocity.y=-self._speed_max
		if moving_y==0: self.velocity.y*=(1-self._speed_decay)
		self._spriterow=moving_x+1 # seleccionamos animación (izquierda, centro, derecha)

		# check boundaries
		# si estamos en un borde, no nos movemos y quitamos la aceleración hacia ese borde
		# para evitar el efecto "pegajoso"
		if self.position.x<self._space_rect[0]+self.width/2:
			self.position.x=self._space_rect[0]+self.width/2
			if self.velocity.x<0: self.velocity.x=0
			log.debug("hero in left boundary")
		if self.position.x>self._space_rect[2]-self.width/2:
			self.position.x=self._space_rect[2]-self.width/2
			if self.velocity.x>0: self.velocity.x=0
			log.debug("hero in right boundary")
		if self.position.y<self._space_rect[1]+self.height/2:
			self.position.y=self._space_rect[1]+self.height/2
			if self.velocity.y<0: self.velocity.y=0
			log.debug("hero in top boundary")
		if self.position.y>self._space_rect[3]-self.height/2:
			self.position.y=self._space_rect[3]-self.height/2
			if self.velocity.y>0: self.velocity.y=0
			log.debug("hero in bottom boundary")

	def render(self, canvas):
		super().render(canvas)

		#if event.type == pygame.KEYDOWN:
		#	if event.key in self._keymap["left"]:
		#	#if event.key == pygame.K_LEFT:
		#		_dir=-1
		#	elif event.key == pygame.K_RIGHT:
		#		_dir=1
		#if event.type == pygame.KEYUP:
		#	_dir=0

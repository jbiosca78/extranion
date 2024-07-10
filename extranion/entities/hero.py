from extranion.entities.entity import Entity
import pygame
from pygame.math import Vector2 as vector
from extranion.tools import log,gvar
from extranion.config import cfg
from extranion.entities.herobullet import HeroBullet
from extranion.soundmanager import SoundManager

class Hero(Entity):

	def __init__(self, name, bullets):

		super().__init__(name)

		self.__map_input()

		self.speed_mul=1
		self._speed_max=cfg("entities.hero.speed_max")
		self._speed_decay=cfg("entities.hero.speed_decay")
		self._acceleration=cfg("entities.hero.acceleration")

		# dimensiones del espacio donde puede entrar la nave
		space=self.space_rect
		self._space_rect=(space[0]+self.width/2, space[1]+self.height/2, space[2]-self.width/2, space[3]-self.height/2)

		# control de proyectiles
		self.__bullets=bullets
		self.__cooldown_fast_fire=0
		self.charge=self.charge=cfg("gameplay.initial_charge")

		# control de vidas
		self.lives=cfg("gameplay.initial_lives")
		self.alive=True

		self._input_pressed = { "left": False, "right": False, "up": False, "down": False, "fastfire": False}
		self.__respawn_time=0
		self.__spawn()

	def __spawn(self):
		self.velocity=vector(0,0)
		self.position=vector(cfg("entities.hero.start_pos"))
		self.alive=True

	def __map_input(self):
		self._keymap = {}
		kmap = cfg("keymap.hero")
		for g, v in kmap.items():
			self._keymap[g] = []
			for k in v:
				if k == "LALT": code=pygame.K_LALT
				elif k == "RALT": code=pygame.K_RALT
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
		elif key in self._keymap["fastfire"]:
			self._input_pressed["fastfire"] = pressed
			log.debug(f"fastfire = {pressed}")
		elif key in self._keymap["fire"] and pressed:
			self.__fire("normal")

	def update(self, delta_time):

		# controlamos respawn para 'revivir' al héroe
		if self.__respawn_time>0:
			self.__respawn_time-=delta_time
			if self.__respawn_time<=0: self.__spawn()

		# no actualizamos heroe si estamos muertos
		if not self.alive: return

		# obtenemos las direcciones de movimiento horizontal y vertical
		moving_x=moving_y=0
		if self._input_pressed["left"]: moving_x-=1
		if self._input_pressed["right"]: moving_x+=1
		if self._input_pressed["up"]: moving_y-=1
		if self._input_pressed["down"]: moving_y+=1

		# aceleramos en la dirección de movimiento correspondiente hasta el máximo
		self.velocity.x += moving_x*self._acceleration
		if self.velocity.x>self._speed_max*self.speed_mul: self.velocity.x=self._speed_max
		if self.velocity.x<-self._speed_max*self.speed_mul: self.velocity.x=-self._speed_max
		if moving_x==0: self.velocity.x*=(1-self._speed_decay)
		self.velocity.y += moving_y*self._acceleration
		if self.velocity.y>self._speed_max*self.speed_mul: self.velocity.y=self._speed_max
		if self.velocity.y<-self._speed_max*self.speed_mul: self.velocity.y=-self._speed_max
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

		# fast fire
		if self.__cooldown_fast_fire>0:
			self.__cooldown_fast_fire-=delta_time
		else:
			if self._input_pressed["fastfire"]: self.__fire("fast")

		super().update(delta_time)

	def render(self, delta_time):
		if not self.alive: return
		super().render(delta_time)

	def __fire(self, fire_type):

		if not self.alive: return

		if fire_type=="normal":
			if len(self.__bullets)>1: return
			SoundManager.play_sound("shoot")
			self.__bullets.add(HeroBullet(self.position-vector(8,0)))
			self.__bullets.add(HeroBullet(self.position+vector(8,0)))

		if fire_type=="fast":
			if self.charge==0: return
			SoundManager.play_sound("shoot")
			self.charge-=1
			self.__cooldown_fast_fire=cfg("entities.hero.cooldown_fast_fire")
			self.__bullets.add(HeroBullet(self.position))

	def die(self):

		log.info("hero die")
		self.alive=False
		self.__respawn_time=cfg("entities.hero.respawn_time")
		self.lives-=1
		SoundManager.play_sound("hero_killed")

	def enemy_hit(self, scene):

		SoundManager.play_sound("enemy_killed")

		# incrementamos carga para disparo rápido
		self.charge+=1

		# control de puntuación
		score_add=100+5*(scene-1)
		gvar.score+=score_add
		if gvar.score>gvar.topscore:
			gvar.topscore=gvar.score

		# vida extra
		if self.lives<cfg("gameplay.max_lives"):
			if gvar.score//cfg("gameplay.score_extralife")!=(gvar.score-score_add)//cfg("gameplay.score_extralife"):
				self.lives+=1
				SoundManager.play_sound("extralife")

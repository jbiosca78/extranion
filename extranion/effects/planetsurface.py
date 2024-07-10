import random
import math
import pygame
from extranion.asset import asset
from extranion.tools import log,gvar

# Planet Surface generator like Exerion background

stripe_color=[
	#[ (10, 80, 20), (30, 100, 30) ], # verde (rueda)
	#[ (60, 60, 20), (100, 100, 30) ], # amarillo (pajaros)
	#[ (40, 20, 0), (90, 40, 0) ], # marron (mariposa)
	#[ (60, 20, 20), (100, 20, 20) ], # rojo (ovni)
	(30, 100, 30),
	(100, 100, 30),
	(90, 40, 0),
	(100, 20, 20),
]

class PlanetObject:
	distance = None
	posx = None
	sprite = None

class PlanetSurface:
	def __init__(self, canvas_rect):

		self.canvas_rect=canvas_rect
		#	self.width = width
		#	selself.height = height
		#	selself.surface = []
		#	selself.generate()

		self._nstart=1

		self.__objects=[]
		for _ in range(30):
			p=PlanetObject()
			p.distance=(random.randint(0,100)/100)**2
			p.posx=random.randint(0,500)
			p.sprite=asset.get("mountains")[random.randint(0,1)][random.randint(0,1)]
			self.__objects.append(p)

		self._stripeidx=0
		self.__shift_x=0
		self.__shift_y=0

	#def generate(self):
	#	for x in range(self.width):
	#		self.surface.append(random.randint(0, self.height))

	#def draw(self):
	#	for y in range(self.height):
	#		for x in range(self.width):
	#			if y < self.surface[x]:
	#				print(".", end="")
	#			else:
	#				print(" ", end="")
	#		print()

	def update(self, delta_time, hero):

		self._nstart+=0.03
		if self._nstart>2.71:
			self._nstart=1

		for obj in self.__objects:
			obj.distance+=0.0005+obj.distance*0.02
			if obj.distance>=1:
				obj.distance=0
				obj.posx=random.randint(0,500)

		self._stripeidx+=0.0042
		if self._stripeidx>0.2:
			self._stripeidx=0

		# dependiendo de la posición del héroe, la superficie y elementos se desplazan
		self.__shift_x=(hero.position.x-640/2)
		self.__shift_y=(360-hero.position.y)/4

	def render(self, canvas):

		x,y,w,h=self.canvas_rect
		horizon_y=int(h/2+y)+self.__shift_y

		# Stripes
		color=stripe_color[gvar.scene%4]
		# getcolor a bit darker
		color2=(color[0]*0.8, color[1]*0.8, color[2]*0.8)

		pygame.draw.rect(canvas, color, [x,horizon_y,x+w,y+h])
		# 0%-10% 20%-30% 40%-50% 60%-70% 80%-90%
		for d1 in 0, 0.2, 0.4, 0.6, 0.8:
			d1=d1+self._stripeidx
			d2=d1+0.1
			y1=horizon_y+(h-horizon_y)*(d1*d1*d1*d1)
			y2=horizon_y+(h-horizon_y)*(d2*d2*d2*d2)
			pygame.draw.rect(canvas, color2, [0+x,int(y1),w,int(y2-y1)])

		# Objetos
		for obj in self.__objects:
			# obtenemos la distancia, que es un porcentaje que indica si el objeto está en el
			# horizonte (0%) o ha llegado a nuestra posición actual (100)
			d=obj.distance
			# reducimos tamaño según la distancia, en el horizonte será practicamente 0
			# y en la posición actual lo ampliamos en un factor de 2.5
			sprite=pygame.transform.scale(obj.sprite, (int(48*(2.5*d+0.02)),int(48*(2.5*d+0.02))))
			# calculamos la posición del objeto según la distancia
			# la posición x se multiplica por 10 desde el centro
			# la posición y a una distancia de 0% será el horizonte y en 100% algo mas bajo
			# que el borde inferior de la pantalla (factor de 1.3) para evitar que desaparezca de repente
			obj_x=w/2-(w/2-obj.posx)*(1+d*9)-self.__shift_x*d
			obj_y=horizon_y+(h-horizon_y)*d*1.3
			# lo dibujamos
			canvas.blit(sprite, (int(obj_x)+x-sprite.get_width()/2, int(obj_y)+y-sprite.get_height()/2))
			# debug bordes
			if gvar.debug:
				pygame.draw.rect(canvas, (0,0,255), (int(obj_x)-sprite.get_width()/2+x, int(obj_y)-sprite.get_height()/2+y, sprite.get_width(), sprite.get_height()), 1)

		# debug
		if gvar.debug:
			# mostramos las líneas de fuga
			pygame.draw.line(canvas, (0,255,255), ((w/2)-(w/2)/10,horizon_y+y), (x+0,y+h))
			pygame.draw.line(canvas, (0,255,255), ((w/2)+(w/2)/10,horizon_y+y), (x+w,y+h))

	def release(self):
		pass


import random
import pygame

# Pixel 3D Stars by Jose Biosca (2024)

# A cada estrella se le asigna una posición aleatoria en pantalla y una distancia Z entre 0 y 999
# Las posiciones X e Y parten del centro de la pantalla.
# La posición X e Y en cada momento se divide por z/1000 de forma que a valores altos de Z, cada
# estrella estará en su posición inicial, y a medida que Z se acerque a 0, se irá al infinito
# Antes de que Z valga cero, se eliminará la estrella y se creará otra

# Además de la posición, hay un componente aleatorio de color, para crear estrellas blancas, rojas,
# amarillas y azules (no hay estrellas verdes).

class Stars3D:
	def __init__(self, size, numstars=800, speed=1):

		self.speed=speed
		self.fx,self.fy=size
		self.stars=[]
		# generamos estrellas
		for i in range(numstars):
			c=random.randint(0,3)
			r=g=b=0
			if c==0: r=g=b=1 # estrellas blancas
			if c==1: r=1 # estrellas rojas
			if c==2: r=g=1 # estrellas amarillas
			if c==3: b=1 # estrellas azules
			self.stars.append({
				"xs": random.randint(int(-self.fx/2), int(self.fx/2)),
				"ys": random.randint(int(-self.fy/2), int(self.fy/2)),
				"z": random.randint(1, 999),
				"speed": random.randint(1, 10),
				"r":r, "g":g, "b":b,
			})

	def update(self, delta_time):
		for s in self.stars:
			# movemos la estrella, mas lento cuanto mas lejana
			s["z"]-=delta_time/s["speed"]*self.speed
			if int(s["z"])<=0:
				s["xs"]=random.randint(int(-self.fx/2), int(self.fx/2))
				s["ys"]=random.randint(int(-self.fy/2), int(self.fy/2))
				s["speed"]=random.randint(1, 10)
				s["z"]=999


	def render(self, canvas):

		# draw stars
		for s in self.stars:
			# dibujamos la estrella el 90% de los frames, para simular el parpadeo de las estrellas
			if random.randint(0, 100)<90:
				# posición pseudo 3D
				z=int(s["z"])
				x=int(s["xs"]/(z/1000)+self.fx/2)
				y=int(s["ys"]/(z/1000)+self.fy/2)
				# el brillo depende de la velocidad y la distancia, entre 0 y 1
				brillo=((10-s["speed"])/10+0.1)*((1000-z)/1000)
				r=int(15+(s["r"]*240)*brillo)
				g=int(15+(s["g"]*240)*brillo)
				b=int(15+(s["b"]*240)*brillo)
				# dibujamos la estrella
				#canvas.set_at((x,y), (r,g,b)) # 1 pixel
				pygame.draw.rect(canvas, (r,g,b), (x,y,2,2)) # 2x2 pixels

	def release(self):
		self.stars.clear()
		pass

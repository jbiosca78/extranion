import random
import pygame

# Pixel Stars by Jose Biosca (2024)

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
				"xs": random.randint(-self.fx/2, self.fx/2),
				"ys": random.randint(-self.fy/2, self.fy/2),
				"z": random.randint(1, 2000),
				"speed": random.randint(1, 10),
				"r":r, "g":g, "b":b,
			})

	def update(self, delta_time):
		for s in self.stars:
			# movemos la estrella, mas lento cuanto mas lejana
			s["z"]-=delta_time/s["speed"]*self.speed
			if int(s["z"])<=0:
				s["xs"]=random.randint(-self.fx/2, self.fx/2)
				s["ys"]=random.randint(-self.fy/2, self.fy/2)
				s["speed"]=random.randint(1, 10)
				s["z"]=2000


	def render(self, canvas):
		# draw stars
		for s in self.stars:
			# dibujamos la estrella el 80% de los frames, para simular el parpadeo de las estrellas
			if random.randint(0, 100)<80:
				# posición pseudo 3D
				z=int(s["z"])
				x=int(s["xs"]/(z/2001)+self.fx/2)
				y=int(s["ys"]/(z/2001)+self.fy/2)
				# el brillo depende de la velocidad y la distancia
				brillo=((10-s["speed"])/10)*((2000-z)/2000)
				r=int(15+(80+s["r"]*160)*brillo)
				g=int(15+(80+s["g"]*160)*brillo)
				b=int(15+(80+s["b"]*160)*brillo)
				# dibujamos la estrella
				pygame.draw.rect(canvas, (r,g,b), (x,y,2,2))
				#canvas.set_at((x,y), (r,g,b))

	def release(self):
		self.stars.clear()
		pass

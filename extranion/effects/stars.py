import random

_SPEED=1.8

class Stars:
	def __init__(self, size, numstars=500):
		self.fx,self.fy=size
		self.stars=[]
		# generamos estrellas
		for i in range(numstars):
			c=random.randint(0,3)
			r=g=b=0
			# c==0: estrellas blancas
			if c==1: r=1 # estrellas rojas
			if c==2: r=g=1 # estrellas amarillas
			if c==3: b=1 # estrellas azules
			self.stars.append({
				"x": random.randint(0, self.fx),
				"y": random.randint(0, self.fy),
				"depth": random.randint(1, 6),
				"r":r, "g":g, "b":b,
			})

	def update(self, delta_time):
		for s in self.stars:
			# movemos la estrella, mas lento cuanto mas lejana
			depth=s["depth"]
			s["y"]+=depth/delta_time*_SPEED
			# si llega al borde inferior, generamos otra
			if s["y"]>self.fy:
				s["y"]=0
				s["x"]=random.randint(0,self.fx)

	def render(self, canvas):
		# draw stars
		for s in self.stars:
			depth=s["depth"]
			brillo=(depth-1)*20
			# dibujamos la estrella el 90% de los frames, para simular el parpadeo de las estrellas
			if random.randint(0, 100)<90:
				canvas.set_at((int(s["x"]),int(s["y"])), (brillo+s["r"]*40,brillo+s["g"]*40,brillo+s["b"]*40))

	def release(self):
		self.stars.clear()
		pass

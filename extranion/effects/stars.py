import random

# Pixel Stars by Jose Biosca (2024)

class Stars:
	def __init__(self, size, numstars=400, direction="down", speed=1.8):

		self.speed=speed
		self.dir=direction
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
				"x": random.randint(0, self.fx-1),
				"y": random.randint(0, self.fy-1),
				"depth": random.randint(1, 6),
				"r":r, "g":g, "b":b,
			})

	def update(self, delta_time):
		for s in self.stars:
			# movemos la estrella, mas lento cuanto mas lejana
			depth=s["depth"]
			lightyears=depth/delta_time*self.speed

			# hacia abajo
			if self.dir=="down":
				s["y"]+=lightyears
				# si llega al borde inferior, generamos otra
				if s["y"]>self.fy:
					s["y"]=0
					s["x"]=random.randint(0,self.fx)

			# hacia arriba
			if self.dir=="up":
				s["y"]-=lightyears
				# si llega al borde superior, generamos otra
				if s["y"]<0:
					s["y"]=self.fy
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

import pygame
import random

# Planet Surface generator like Exerion background

class PlanetSurface:
	def __init__(self, rect):

		self.rect=rect
		#	self.width = width
		#	selself.height = height
		#	selself.surface = []
		#	selself.generate()

		self._nstart=1

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

	def update(self, delta_time):

		self._nstart+=0.03
		if self._nstart>2.71:
			self._nstart=1
		pass

	def release(self):
		pass

	def render(self, canvas):

		#print(self.rect)
		# 0,20, 499,359
		#pass

		c=[[60,0,0,0],[60,20,0]]
		ci=0

		# draw box in canvas with size rect
		#pygame.draw.rect(canvas, (255,255,255), self.rect, 1)
		x,y,w,h=self.rect
		#print(x,y,w,h)
		i=int(h/2+y)
		n=self._nstart
		while i<(h):
			j=1+n
			n=n*1.6
			#print(i,j)
			pygame.draw.rect(canvas, c[ci], (x,y+i,w,j))
			ci=1-ci
			i+=int(j)

import pygame
from extranion.asset import asset
#from extranion.config import DEBUG
from extranion.config import gvar
from extranion.config import cfg
from extranion import log

# Esta clase representa una entidad del juego, y gestiona:
# El asset (spritesheet), y su animación
# La posición y dirección de movimiento (velocidad)
# La actualización de la posición y el renderizado

class Entity(pygame.sprite.Sprite):

	def __init__(self, name, position=(0,0), velocity=(0.0,0.0)):
		super().__init__()

		log.info(f"Creating entity {name}")

		self.position = pygame.math.Vector2(position)
		self.velocity = pygame.math.Vector2(velocity)

		self.config=cfg("entities", name)
		self.spritesheet=asset.get(self.config["spritesheet"])
		self.spriterow=self.config["animation"]["default"][0]
		self.spritecol=self.config["animation"]["default"][1]
		self.animframes=self.config["animation"]["default"][2]
		self.animspeed=self.config["animation"]["default"][3]
		self.animptr=0

		self.width=self.spritesheet[self.spriterow][self.spritecol].get_width()
		self.height=self.spritesheet[self.spriterow][self.spritecol].get_height()
		self.render_rect=self.spritesheet[self.spriterow][self.spritecol].get_rect()
		self.rect=self.render_rect.inflate(self.config["inflate_collider"])

		#self.rect=pygame.Rect

	def update(self, delta_time):

		# animación sprite
		self.animptr+=delta_time/self.animspeed
		if self.animptr>=self.animframes: self.animptr=0

		# desplazamiento
		self.position+=self.velocity*delta_time
		self.render_rect.center=self.rect.center=self.position

	def render(self, canvas):

		sprite=self.spritesheet[self.spriterow][self.spritecol+int(self.animptr)]
		canvas.blit(sprite, self.render_rect)

		if gvar.DEBUG:
			pygame.draw.rect(canvas, cfg("debug.rect_render_color"), self.render_rect, 1)
			pygame.draw.rect(canvas, cfg("debug.rect_collider_color"), self.rect, 1)

	def get_position(self):
		#return list(self.position)
		return self.position.copy()

	#def get_width(self):
	#	#return self.spritesheet[self.spriterow][self.spritecol].get_width()
	#	return self.width

	#def get_height(self):
	#	#return self.spritesheet[self.spriterow][self.spritecol].get_height()
	#	return self.height

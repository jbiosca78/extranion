import pygame

class EntityGroup(pygame.sprite.Group):

	def __init__(self):
		super().__init__()

	def render(self, surface):
		for sprite in self.sprites():
			sprite.render(surface)

	def release(self):
		for sprite in self.sprites():
			sprite.release()

import pygame
from extranion.states.state import State
from extranion.config import cfg
from extranion.asset import asset

class Intro(State):

	def __init__(self):
		super().__init__()
		self.next_state = "GamePlay"

	def enter(self):
		self.__render_fps_surface()

	def exit(self):
		pass

	def handle_input(self, event):
		if event.type == pygame.KEYDOWN:
			self.done = True

	def update(self, delta_time):
		pass

	def render(self, surface):
		surface.blit(self.__image, (100,100))

	def __render_fps_surface(self):
		font=asset.get("fonts.sansation")
		self.__image = font.render("Press any key to Continue", True, cfg("game", "foreground_color"), None)

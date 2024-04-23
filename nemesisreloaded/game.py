#!/usr/bin/env python3

import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame
import time

class Game:

	def __init__(self):
		pygame.init()

		self.__screen=None
		self.__screen=pygame.display.set_mode([640,480], 0, 32)
		pygame.display.set_caption("Hello World")

		#image=pygame.image.load("images/ship.png").convert_alpha()

		self.__running = True

	def run(self):

		while self.__running:
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					self.__running = False

			self.__screen.fill((0,0,0))

			pygame.display.update()

		time.sleep(2)
		self.__release()

	def __release(self):
		pygame.quit()

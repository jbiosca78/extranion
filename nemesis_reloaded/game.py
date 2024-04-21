#!/usr/bin/env python3

import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame
import time

class Game:

	def __init__(self):
		self.__screen=None

		#image=pygame.image.load("images/ship.png").convert_alpha()
		pass

	def run(self):
		pygame.init()

		screen=pygame.display.set_mode([640,480], 0, 32)
		pygame.display.set_caption("Hello World")

		time.sleep(2)
		self.__release()

	def __release(self):
		pygame.quit()

#!/usr/bin/env python3

import sys
import os
import time
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1' # oculta mensaje de bienvenida de pygame
import pygame
from importlib import resources
from extranion.tools import log,gvar
from extranion.config import cfg
from extranion.asset import asset
from extranion.sound.soundmanager import SoundManager
from extranion.states.statemanager import StateManager
from extranion.debug.memory_stats import debug_memory_log, debug_memory_render
from extranion.debug.fps_stats import FPS_Stats

class Game:

	def run(self):
		# si tenemos instalado rich, lo usamos para
		# mostrar excepciones mucho mas detalladas
		# apt install python3-rich
		Console=None
		try:
			from rich.console import Console
			console = Console()
		except Exception:
			pass

		try:
			# iniciamos logger si está activado
			if cfg("log.enabled"):
				#with resources.path("extranion.data", cfg("log.file")) as p: logfile=p
				logfile=resources.files("extranion.data").joinpath(cfg("log.file"))
				log.init(file=logfile, level=cfg("log.level"))
			log.info("* Game Start *")

			# lanzamos el juego
			self.__initialize()
			self.__mainloop()
			self.__release()

		except Exception as e:
			if Console:
				console.print_exception(extra_lines=2, show_locals=True)
			else:
				raise

	def __initialize(self):

		log.inside("Initialize")

		try:

			log.info("Initializing pygame")
			pygame.mixer.pre_init(44100, 16, 2, 4096)
			pygame.init()
			pygame.mouse.set_visible(False)
			pygame.display.set_caption(cfg("game.name"))

			log.info("Initializing screen")
			pgdi=pygame.display.Info()
			self.__desktop_size=(pgdi.current_w, pgdi.current_h)
			log.info(f"desktop_size: {self.__desktop_size}")
			self.__window_size=(pgdi.current_w//3*2, pgdi.current_h//3*2)
			log.info(f"window_size: {self.__window_size}")
			self.__screen=pygame.display.set_mode(self.__window_size, pygame.RESIZABLE|pygame.HWACCEL, 32)
			self.__fullscreen=False

			log.info("Initializing canvas")
			# canvas es el 'lienzo' donde vamos a dibujar, se escalará a la ventana del juego incluso
			# en modo ventana. así no dependemos de la resolución del usuario y evitamos que la ventana
			# se vea muy pequeña en displays 4k o superiores. además se consigue un bonito efecto pixelado
			canvas_x, canvas_y=cfg("game.canvas_size")
			self.__canvas=pygame.Surface((canvas_x,canvas_y))

			log.info("Initializing game")
			self.__time_per_frame=1000.0/cfg("game.fps")
			self.__fps_stats=FPS_Stats()
			self.__load_assets()
			SoundManager.init()
			StateManager.init()

		except Exception as e:
			log.fatal(f"Exception {type(e).__name__}: {str(e)}")
			log.outbreak()
			raise

		log.outside()

	def __load_assets(self):

		log.info("Loading main assets")
		asset.load('main','game.font_default')
	
	def __release(self):

		StateManager.release()
		self.__unload_assets()
		pygame.quit()

	def __unload_assets(self):

		asset.unload('main')

	def __mainloop(self):

		log.info("Starting mainloop")
		last_time = pygame.time.get_ticks()
		time_since_last_update = 0
		time_prev=last_time
		while gvar.running:
			# calculamos tiempo transcurrido
			current_time = pygame.time.get_ticks()
			delta_time = current_time-last_time
			last_time = current_time
			time_since_last_update += delta_time

			time_prev=pygame.time.get_ticks() # para contar lo que tarda en ejecutar el último update+render
			# actualizamos los frames necesarios para mantener el tiempo de actualización de juego (frames lógicos)
			while time_since_last_update > self.__time_per_frame:
				time_prev=pygame.time.get_ticks() # si tenemos que generar varios frames, sólo queremos el último
				time_since_last_update -= self.__time_per_frame
				self.__handle_events()
				self.__update(self.__time_per_frame)
			self.__render()
			time_post=pygame.time.get_ticks() # para contar lo que tarda en ejecutar el último update+render

			# si no estamos en debug, esperamos el tiempo sobrante entre frames
			# restando el tiempo que tardamos en generar un frame (time_post-time_prev)
			# así evitamos sobrecargar la CPU
			if not gvar.debug:
				if (time_post-time_prev)<self.__time_per_frame:
					time.sleep((self.__time_per_frame-(time_post-time_prev))/1000)

	def __handle_events(self):

		for event in pygame.event.get():
			if event.type == pygame.QUIT: gvar.running=False
			elif event.type == pygame.KEYDOWN:
				if event.key == pygame.K_F5: gvar.debug=not gvar.debug
				elif event.key == pygame.K_TAB: debug_memory_log()
				elif event.key == pygame.K_F11: self.__toggle_fullscreen()
				elif event.key == pygame.K_F12: self.self.__screenshot()
			StateManager.event(event)
		pass

	def __update(self, delta_time):

		StateManager.update(delta_time)
		self.__fps_stats.update(delta_time)
		#SoundManager.instance().update(delta_time)

	def __render(self):

		self.__canvas.fill(cfg("game.background_color"))
		StateManager.render(self.__canvas)
		if gvar.debug:
			self.__fps_stats.render(self.__canvas)
			debug_memory_render(self.__canvas)

		aspect_ratio_canvas=int(100*self.__canvas.get_width()/self.__canvas.get_height())
		aspect_ratio_screen=int(100*self.__screen.get_width()/self.__screen.get_height())

		if aspect_ratio_canvas==aspect_ratio_screen:
			# Escalado básico cuando el aspect ratio de la ventana coincide con el canvas del juego
			# A no ser que el usuario redimensione la ventana, será el caso normal en pantallas 16:9
			pygame.transform.scale(self.__canvas, self.__screen.get_size(), self.__screen)

		else:
			# Escalado manteniendo aspect ratio
			# Nota: Funciona bien pero perdemos bastante rendimiento se podría optimizar.
			# Por ejemplo creando previamente el canvas "expandcanvas" en lugar de crearlo cada vez.
			canvasratio=self.__canvas.get_width()/self.__canvas.get_height()
			screenratio=self.__screen.get_width()/self.__screen.get_height()
			if canvasratio>screenratio:
				# si el canvas es más ancho que la pantalla, ajustamos el ancho
				newwidth=int(self.__screen.get_width())
				newheight=int(self.__canvas.get_height()*newwidth/self.__canvas.get_width())
			else:
				# si el canvas es más alto que la pantalla, ajustamos el alto
				newheight=int(self.__screen.get_height())
				newwidth=int(self.__canvas.get_width()*newheight/self.__canvas.get_height())
			expandcanvas=pygame.Surface((newwidth,newheight))
			# Escalamos a un tamaño que cabe en la ventana
			pygame.transform.scale(self.__canvas, (newwidth,newheight), expandcanvas)
			# Transferimos el canvas escalado al centro de la pantalla
			self.__screen.fill(cfg("game.background_color"))
			self.__screen.blit(expandcanvas, ((self.__screen.get_width()-newwidth)/2, (self.__screen.get_height()-newheight)/2))

		pygame.display.update()
	
	def __screenshot(self):

		date=time.strftime("%Y%m%d_%H%M%S")
		pygame.image.save(self.__canvas, f"extranion-{date}.png")

	def __toggle_fullscreen(self):

		self.__fullscreen=not self.__fullscreen
		if self.__fullscreen:
			# guardamos el tamaño de la ventana actual para restaurarlo al pasar a ventana
			self.__window_size=self.__screen.get_size()
			# pasamos a fullscreen
			if sys.platform == 'win32':
				log.info(f"set fullscreen {self.__desktop_size}")
				self.__screen=pygame.display.set_mode(self.__desktop_size, pygame.FULLSCREEN|pygame.DOUBLEBUF)
			else:
				# en linux FULLSCREEN da problemas y es preferible ventana completa sin bordes
				# sería recomendable un menú de selección donde podamos elegir fullscreen o windowed fullscreen
				log.info(f"set windowed fullscreen {self.__desktop_size}")
				os.environ['SDL_VIDEO_WINDOW_POS'] = "0,0" # warning, se pondrá en el primer monitor
				pygame.display.quit()
				pygame.display.init()
				#pygame.display.set_mode(self.__desktop_size, pygame.NOFRAME|pygame.HWACCEL|pygame.DOUBLEBUF|pygame.HWSURFACE, 32)
				# HWACCEL y HWSURFACE están deprecados y ya no hacen nada
				# SDL no soporta DOUBLEBUF, sólo tiene sentido para el modo OPENGL
				self.__screen=pygame.display.set_mode(self.__desktop_size, pygame.NOFRAME)
		else:
			log.info(f"set window {self.__window_size}")
			self.__screen=pygame.display.set_mode(self.__window_size, pygame.RESIZABLE)


def main():
	game=Game()
	game.run()

if __name__ == "__main__":
	main()

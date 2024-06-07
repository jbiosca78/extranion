#!/usr/bin/env python3

import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1' # oculta mensaje de bienvenida de pygame
import pygame
from extranion.fps_stats import FPS_Stats
#from extranion.config import cfg_item, Config
from extranion.config import cfg
#from extranion.assets.assetmanager import AssetManager		# lanzamos el juego
import extranion.log as log
from importlib import resources

from extranion.asset import asset
import extranion.states.statemanager as statemanager
#from extranion.assets.soundmanager import SoundManager
import time

def main():
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
		# Iniciamos logger si el debug está activo
		if cfg("debug.enabled"):
			log.init(file=cfg("debug.logfile"), level=cfg("debug.loglevel"))
		log.info("* Game Start *")

		# lanzamos el juego
		_initialize()
		_mainloop()
		_release()
	except Exception:
		if Console:
			console.print_exception(extra_lines=2, show_locals=True)
		else:
			raise

def _initialize():

	log.inside("Initialize")

	try:
		log.info("Initializing pygame")
		pygame.mixer.pre_init(44100, 16, 2, 4096)
		pygame.init()
		pygame.mouse.set_visible(False)
		pygame.display.set_caption(cfg("game.name"))

		log.info("Initializing screen")
		global _desktop_size, _window_size, _screen, _fullscreen
		#_screen=pygame.display.set_mode(cfg("game.screen_size"), 0, 32)
		pgdi=pygame.display.Info()
		_desktop_size=(pgdi.current_w, pgdi.current_h)
		_window_size=(pgdi.current_w/2, pgdi.current_h/2)
		#window_w=_desktop_size[0]/2
		#window_h=_desktop_size[1]/2
		_screen=pygame.display.set_mode(_window_size, pygame.RESIZABLE, 32)
		_fullscreen=False

		log.info("Initializing canvas")
		# canvas es el 'lienzo' donde vamos a dibujar el scroll, se escalará a la ventana del juego
		# redimensionar es algo costoso pero de esta manera no dependemos de la resolución del usuario
		# (yo tengo pantalla 4k por ejemplo), y conseguimos un bonito efecto pixelado estilo retro
		global _canvas
		canvas_x, canvas_y=cfg("game.canvas_size")
		_canvas=pygame.Surface((canvas_x,canvas_y))

		log.info("Initializing game")
		global _debug, _time_per_frame, _fps_stats, _running
		_debug=cfg("debug.enabled")
		_time_per_frame=1000.0/cfg("timing.fps")
		_fps_stats=FPS_Stats()
		_load_assets()
		statemanager.init()
		_running=True
	except Exception as e:
		log.fatal("Error initializing game!")
		log.fatal(e)
		log.outbreak()
		raise

	log.outside()

def _load_assets():
	log.info("Loading main assets")
	asset.load('main','fonts.hack')

def _mainloop():
	global _running, _time_per_frame, _fps_stats, _state_manager

	log.info("Starting mainloop")
	last_time = pygame.time.get_ticks()
	time_since_last_update = 0
	time_prev=last_time
	while _running:
		#delta_time, last_time = _calc_delta_time(last_time)
		current_time = pygame.time.get_ticks()
		delta_time = current_time-last_time
		last_time=current_time
		time_since_last_update += delta_time

		time_prev=pygame.time.get_ticks() # para contar lo que tarda en ejecutar el último update y render
		# actualizamos los frames necesarios para mantener el tiempo de actualización de juego (frames lógicos)
		while time_since_last_update > _time_per_frame:
			time_prev=pygame.time.get_ticks() # si tenemos que generar varios frames, sólo contamos el último
			time_since_last_update -= _time_per_frame
			_handle_events()
			_update(_time_per_frame)
		_render()
		time_post=pygame.time.get_ticks() # para contar lo que tarda en ejecutar el último update y render

		# Si no estamos en debug, esperamos el tiempo sobrante entre frames
		# restando el tiempo que tardamos en generar un frame (time_post-time_prev)
		# para evitar sobrecargar la CPU
		if not _debug:
			if (time_post-time_prev)<_time_per_frame:
				time.sleep((_time_per_frame-(time_post-time_prev))/1000)

def _release():
	statemanager.release()
	_unload_assets()
	pygame.quit()

def _unload_assets():
	asset.unload('main')

def _handle_events():
	global _debug, _running

	for event in pygame.event.get():
		if event.type == pygame.QUIT: _running=False
		elif event.type == pygame.KEYDOWN:
			if event.key == pygame.K_ESCAPE:
				_running=False
				return
			elif event.key == pygame.K_F5:
				_debug=not _debug
				return
			elif event.key == pygame.K_F11:
				global _fullscreen
				_fullscreen=not _fullscreen
				if _fullscreen:
					#pygame.display.set_mode(_desktop_size, pygame.FULLSCREEN, 32)
					#pygame.display.set_mode(_window_size, pygame.RESIZABLE, 32)

					# guardamos el tamaño de la ventana actual para restaurarlo mas adelante
					global _window_size, _screen
					_window_size=_screen.get_size()
					# pasamos a fullscreen
					os.environ['SDL_VIDEO_WINDOW_POS'] = "0,0"
					screen=pygame.display.set_mode(_desktop_size, pygame.NOFRAME|pygame.RESIZABLE)
				else:
					_screen=pygame.display.set_mode(_window_size, pygame.RESIZABLE, 32)
				return
		statemanager.event(event)
	pass

def _update(delta_time):
	statemanager.update(delta_time)
	_fps_stats.update(delta_time)
	#SoundManager.instance().update(delta_time)

def _render():
	#_screen.fill(cfg("game.background_color"))
	_canvas.fill(cfg("game.background_color"))

	statemanager.render(_canvas)
	if _debug: _fps_stats.render(_canvas)

	pygame.transform.scale(_canvas, _screen.get_size(), _screen)
	pygame.display.update()

if __name__ == "__main__":
	main()

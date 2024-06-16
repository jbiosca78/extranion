#!/usr/bin/env python3

import sys
import os
import time
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1' # oculta mensaje de bienvenida de pygame
import pygame
from importlib import resources
from extranion import log
from extranion.config import cfg, gvar
from extranion.states import statemanager
from extranion.asset import asset
from extranion.fps_stats import FPS_Stats
from extranion.memory_stats import debug_memory_log, debug_memory_render

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
		# Iniciamos logger si está activado
		if cfg("log.enabled"):
			logfile=resources.files("extranion").joinpath(cfg("log.file"))
			log.init(file=logfile, level=cfg("log.level"))
		log.info("* Game Start *")

		# lanzamos el juego
		_initialize()
		_mainloop()
		_release()
	except Exception as e:
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
		pgdi=pygame.display.Info()
		_desktop_size=(pgdi.current_w, pgdi.current_h)
		_window_size=(pgdi.current_w/2, pgdi.current_h/2)
		_screen=pygame.display.set_mode(_window_size, pygame.RESIZABLE|pygame.HWACCEL, 32)
		_fullscreen=False

		# canvas es el 'lienzo' donde vamos a dibujar, se escalará a la ventana del juego incluso
		# en modo ventana. así no dependemos de la resolución del usuario y evitamos que la ventana
		# se vea muy pequeña en displays 4k o superiores. además se consigue un bonito efecto pixelado
		log.info("Initializing canvas")
		global _canvas
		canvas_x, canvas_y=cfg("game.canvas_size")
		_canvas=pygame.Surface((canvas_x,canvas_y))

		log.info("Initializing game")
		global _time_per_frame, _fps_stats, _running
		_time_per_frame=1000.0/cfg("game.fps")
		_fps_stats=FPS_Stats()
		_load_assets()
		statemanager.init()
		_running=True

	except Exception as e:
		log.fatal(f"Exception {type(e).__name__}: {str(e)}")
		log.outbreak()
		raise

	log.outside()

def _load_assets():
	log.info("Loading main assets")
	asset.load('main','font.default')

def _mainloop():
	global _running, _time_per_frame, _fps_stats, _state_manager

	log.info("Starting mainloop")
	last_time = pygame.time.get_ticks()
	time_since_last_update = 0
	time_prev=last_time
	while _running:
		# calculamos tiempo transcurrido
		current_time = pygame.time.get_ticks()
		delta_time = current_time-last_time
		last_time = current_time
		time_since_last_update += delta_time

		time_prev=pygame.time.get_ticks() # para contar lo que tarda en ejecutar el último update+render
		# actualizamos los frames necesarios para mantener el tiempo de actualización de juego (frames lógicos)
		while time_since_last_update > _time_per_frame:
			time_prev=pygame.time.get_ticks() # si tenemos que generar varios frames, sólo queremos el último
			time_since_last_update -= _time_per_frame
			_handle_events()
			_update(_time_per_frame)
		_render()
		time_post=pygame.time.get_ticks() # para contar lo que tarda en ejecutar el último update+render

		# si no estamos en debug, esperamos el tiempo sobrante entre frames
		# restando el tiempo que tardamos en generar un frame (time_post-time_prev)
		# así evitamos sobrecargar la CPU
		if not gvar.DEBUG:
			if (time_post-time_prev)<_time_per_frame:
				time.sleep((_time_per_frame-(time_post-time_prev))/1000)

def _release():
	statemanager.release()
	_unload_assets()
	pygame.quit()

def _unload_assets():
	asset.unload('main')

def _handle_events():
	global _running

	for event in pygame.event.get():
		if event.type == pygame.QUIT: _running=False
		elif event.type == pygame.KEYDOWN:
			if event.key == pygame.K_ESCAPE:
				if statemanager.current_state.name=="Intro": _running=False
			elif event.key == pygame.K_F5: gvar.DEBUG=not gvar.DEBUG
			elif event.key == pygame.K_F11: __toggle_fullscreen()
			elif event.key == pygame.K_F12: pygame.image.save(_canvas, "screenshot.png")
			elif event.key == pygame.K_TAB: debug_memory_log()
		statemanager.event(event)
	pass

def __toggle_fullscreen():
	global _fullscreen, _screen, _window_size
	_fullscreen=not _fullscreen
	if _fullscreen:
		# guardamos el tamaño de la ventana actual para restaurarlo al pasar a ventana
		_window_size=_screen.get_size()
		# pasamos a fullscreen
		if sys.platform == 'win32':
			#pygame.display.set_mode(_desktop_size, pygame.FULLSCREEN|pygame.SCALED)
			_screen=pygame.display.set_mode(_desktop_size, pygame.FULLSCREEN|pygame.DOUBLEBUF)
		else:
		#	# en linux da problemas fullscreen y es preferible ventana completa sin bordes
			os.environ['SDL_VIDEO_WINDOW_POS'] = "0,0"
			#pygame.display.set_mode(_desktop_size, pygame.NOFRAME|pygame.HWACCEL|pygame.DOUBLEBUF|pygame.HWSURFACE, 32)
			# HWACCEL y HWSURFACE están deprecados y ya no hacen nada
			# SDL no soporta DOUBLEBUF, sólo tiene sentido para el modo OPENGL
			_screen=pygame.display.set_mode(_desktop_size, pygame.NOFRAME)
	else:
		_screen=pygame.display.set_mode(_window_size, pygame.RESIZABLE)

def _update(delta_time):
	statemanager.update(delta_time)
	_fps_stats.update(delta_time)
	#SoundManager.instance().update(delta_time)

def _render():

	global _fullscreen

	_canvas.fill(cfg("game.background_color"))
	statemanager.render(_canvas)
	if gvar.DEBUG:
		_fps_stats.render(_canvas)
		debug_memory_render(_canvas)


	aspect_ratio_canvas=int(100*_canvas.get_width()/_canvas.get_height())
	aspect_ratio_screen=int(100*_screen.get_width()/_screen.get_height())

	if aspect_ratio_canvas==aspect_ratio_screen:
		# Escalado básico cuando el aspect ratio de la ventana coincide con el canvas del juego
		# A no ser que el usuario redimensione la ventana, será el caso normal en pantallas 16:9
		pygame.transform.scale(_canvas, _screen.get_size(), _screen)

	else:
		# Escalado manteniendo aspect ratio
		# Nota: Funciona bien pero perdemos bastante rendimiento, habría que optimizarlo.
		# Por ejemplo creando previamente el canvas "expandcanvas" en lugar de crearlo cada vez.

		canvasratio=_canvas.get_width()/_canvas.get_height()
		screenratio=_screen.get_width()/_screen.get_height()
		if canvasratio>screenratio:
			# si el canvas es más ancho que la pantalla, ajustamos el ancho
			newwidth=int(_screen.get_width())
			newheight=int(_canvas.get_height()*newwidth/_canvas.get_width())
		else:
			# si el canvas es más alto que la pantalla, ajustamos el alto
			newheight=int(_screen.get_height())
			newwidth=int(_canvas.get_width()*newheight/_canvas.get_height())
		expandcanvas=pygame.Surface((newwidth,newheight))
		# Escalamos a un tamaño que cabe en la ventana
		pygame.transform.scale(_canvas, (newwidth,newheight), expandcanvas)
		# Transferimos el canvas escalado al centro de la pantalla
		_screen.fill(cfg("game.background_color"))
		_screen.blit(expandcanvas, ((_screen.get_width()-newwidth)/2, (_screen.get_height()-newheight)/2))

	pygame.display.update()

if __name__ == "__main__":
	main()

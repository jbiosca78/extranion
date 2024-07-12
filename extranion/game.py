#!/usr/bin/env python3

import sys
import os
import time
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1' # oculta mensaje de bienvenida de pygame
import pygame
from importlib import resources
from extranion.tools import log,gvar
from extranion.config import cfg
from extranion.states import statemanager
from extranion.asset import asset
from extranion.fps_stats import FPS_Stats
from extranion.memory_stats import debug_memory_log, debug_memory_render
from extranion.soundmanager import SoundManager

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
		# iniciamos logger si está activado
		if cfg("log.enabled"):
			logfile=resources.files("extranion").joinpath(cfg("log.file"))
			log.init(file=logfile, level=cfg("log.level"))
		log.info("* Game Start *")

		# lanzamos el juego
		__initialize()
		__mainloop()
		__release()
	except Exception as e:
		if Console:
			console.print_exception(extra_lines=2, show_locals=True)
		else:
			raise

def __initialize():

	log.inside("Initialize")

	try:

		log.info("Initializing pygame")
		pygame.mixer.pre_init(44100, 16, 2, 4096)
		pygame.init()
		pygame.mouse.set_visible(False)
		pygame.display.set_caption(cfg("game.name"))

		log.info("Initializing screen")
		global __desktop_size, __window_size, __screen, __fullscreen
		pgdi=pygame.display.Info()
		__desktop_size=(pgdi.current_w, pgdi.current_h)
		log.info(f"desktop_size: {__desktop_size}")
		__window_size=(pgdi.current_w//3*2, pgdi.current_h//3*2)
		log.info(f"window_size: {__window_size}")
		__screen=pygame.display.set_mode(__window_size, pygame.RESIZABLE|pygame.HWACCEL, 32)
		__fullscreen=False

		# canvas es el 'lienzo' donde vamos a dibujar, se escalará a la ventana del juego incluso
		# en modo ventana. así no dependemos de la resolución del usuario y evitamos que la ventana
		# se vea muy pequeña en displays 4k o superiores. además se consigue un bonito efecto pixelado
		log.info("Initializing canvas")
		global __canvas
		canvas_x, canvas_y=cfg("game.canvas_size")
		__canvas=pygame.Surface((canvas_x,canvas_y))

		log.info("Initializing game")
		global __time_per_frame, __fps_stats
		__time_per_frame=1000.0/cfg("game.fps")
		__fps_stats=FPS_Stats()
		__load_assets()
		SoundManager.init()
		statemanager.init()

	except Exception as e:
		log.fatal(f"Exception {type(e).__name__}: {str(e)}")
		log.outbreak()
		raise

	log.outside()

def __load_assets():
	log.info("Loading main assets")
	asset.load('main','game.font_default')

def __mainloop():
	global __time_per_frame, __fps_stats

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
		while time_since_last_update > __time_per_frame:
			time_prev=pygame.time.get_ticks() # si tenemos que generar varios frames, sólo queremos el último
			time_since_last_update -= __time_per_frame
			__handle_events()
			__update(__time_per_frame)
		__render()
		time_post=pygame.time.get_ticks() # para contar lo que tarda en ejecutar el último update+render

		# si no estamos en debug, esperamos el tiempo sobrante entre frames
		# restando el tiempo que tardamos en generar un frame (time_post-time_prev)
		# así evitamos sobrecargar la CPU
		if not gvar.debug:
			if (time_post-time_prev)<__time_per_frame:
				time.sleep((__time_per_frame-(time_post-time_prev))/1000)

def __release():
	statemanager.release()
	__unload_assets()
	pygame.quit()

def __unload_assets():
	asset.unload('main')

def __handle_events():

	for event in pygame.event.get():
		if event.type == pygame.QUIT: gvar.running=False
		elif event.type == pygame.KEYDOWN:
			if event.key == pygame.K_F5: gvar.debug=not gvar.debug
			elif event.key == pygame.K_TAB: debug_memory_log()
			elif event.key == pygame.K_F11: __toggle_fullscreen()
			elif event.key == pygame.K_F12: __screenshot()
		statemanager.event(event)
	pass

def __screenshot():
	date=time.strftime("%Y%m%d_%H%M%S")
	pygame.image.save(__canvas, f"extranion-{date}.png")

def __toggle_fullscreen():
	global __fullscreen, __screen, __window_size
	__fullscreen=not __fullscreen
	if __fullscreen:
		# guardamos el tamaño de la ventana actual para restaurarlo al pasar a ventana
		__window_size=__screen.get_size()
		# pasamos a fullscreen
		if sys.platform == 'win32':
			log.info(f"set fullscreen {__desktop_size}")
			__screen=pygame.display.set_mode(__desktop_size, pygame.FULLSCREEN|pygame.DOUBLEBUF)
		else:
			# en linux FULLSCREEN da problemas y es preferible ventana completa sin bordes
			# sería recomendable un menú de selección donde podamos elegir fullscreen o windowed fullscreen
			log.info(f"set windowed fullscreen {__desktop_size}")
			os.environ['SDL_VIDEO_WINDOW_POS'] = "0,0"
			pygame.display.quit()
			pygame.display.init()
			#pygame.display.set_mode(__desktop_size, pygame.NOFRAME|pygame.HWACCEL|pygame.DOUBLEBUF|pygame.HWSURFACE, 32)
			# HWACCEL y HWSURFACE están deprecados y ya no hacen nada
			# SDL no soporta DOUBLEBUF, sólo tiene sentido para el modo OPENGL
			__screen=pygame.display.set_mode(__desktop_size, pygame.NOFRAME)
	else:
		log.info(f"set window {__window_size}")
		__screen=pygame.display.set_mode(__window_size, pygame.RESIZABLE)

def __update(delta_time):
	statemanager.update(delta_time)
	__fps_stats.update(delta_time)
	#SoundManager.instance().update(delta_time)

def __render():

	global __fullscreen

	__canvas.fill(cfg("game.background_color"))
	statemanager.render(__canvas)
	if gvar.debug:
		__fps_stats.render(__canvas)
		debug_memory_render(__canvas)

	aspect_ratio__canvas=int(100*__canvas.get_width()/__canvas.get_height())
	aspect_ratio__screen=int(100*__screen.get_width()/__screen.get_height())

	if aspect_ratio__canvas==aspect_ratio__screen:
		# Escalado básico cuando el aspect ratio de la ventana coincide con el canvas del juego
		# A no ser que el usuario redimensione la ventana, será el caso normal en pantallas 16:9
		pygame.transform.scale(__canvas, __screen.get_size(), __screen)

	else:
		# Escalado manteniendo aspect ratio
		# Nota: Funciona bien pero perdemos bastante rendimiento se podría optimizar.
		# Por ejemplo creando previamente el canvas "expandcanvas" en lugar de crearlo cada vez.
		canvasratio=__canvas.get_width()/__canvas.get_height()
		screenratio=__screen.get_width()/__screen.get_height()
		if canvasratio>screenratio:
			# si el canvas es más ancho que la pantalla, ajustamos el ancho
			newwidth=int(__screen.get_width())
			newheight=int(__canvas.get_height()*newwidth/__canvas.get_width())
		else:
			# si el canvas es más alto que la pantalla, ajustamos el alto
			newheight=int(__screen.get_height())
			newwidth=int(__canvas.get_width()*newheight/__canvas.get_height())
		expandcanvas=pygame.Surface((newwidth,newheight))
		# Escalamos a un tamaño que cabe en la ventana
		pygame.transform.scale(__canvas, (newwidth,newheight), expandcanvas)
		# Transferimos el canvas escalado al centro de la pantalla
		__screen.fill(cfg("game.background_color"))
		__screen.blit(expandcanvas, ((__screen.get_width()-newwidth)/2, (__screen.get_height()-newheight)/2))

	pygame.display.update()

if __name__ == "__main__":
	main()

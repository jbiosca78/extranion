import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1' # oculta mensaje de bienvenida de pygame
import pygame
from extranion.fps_stats import FPS_Stats
#from extranion.config import cfg_item, Config
from extranion.config import cfg
#from extranion.assets.assetmanager import AssetManager
#from extranion.assets.asset import AssetType
from extranion.asset import asset
import extranion.states.statemanager as statemanager
#from extranion.assets.soundmanager import SoundManager
import time

try:
	import pretty_errors
except Exception:
	pass

def run():

	global DEBUG, _running, _time_per_frame, _fps_stats, _state_manager

	_initialize()

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
			_handle_input()
			_update(_time_per_frame)
		_render()
		time_post=pygame.time.get_ticks() # para contar lo que tarda en ejecutar el último update y render

		# Si no estamos en debug, esperamos el tiempo sobrante entre frames
		# restando el tiempo que tardamos en generar un frame (time_post-time_prev)
		# para evitar sobrecargar la CPU
		if not DEBUG:
			if (time_post-time_prev)<_time_per_frame:
				time.sleep((_time_per_frame-(time_post-time_prev))/1000)

	_release()

def _initialize():

	global DEBUG, _screen, _running, _time_per_frame, _fps_stats, _state_manager

	DEBUG=cfg("game.debug.activated")

	if DEBUG: print("Init pygame")
	pygame.mixer.pre_init(44100, 16, 2, 4096)
	pygame.init()
	pygame.mouse.set_visible(False)

	if DEBUG: print("Init screen")
	_screen=pygame.display.set_mode(cfg("game.screen_size"), 0, 32)
	pygame.display.set_caption(cfg("game.name"))

	if DEBUG: print("Init game")
	_time_per_frame=1000.0/cfg("timing.fps")
	_fps_stats=FPS_Stats()
	_load_assets()
	statemanager.init()
	_running=True

def _release():
	statemanager.release()
	_unload_assets()
	pygame.quit()

def _load_assets():
	asset.load('main','fonts.sansation')

def _unload_assets():
	asset.unload('main')

def _handle_input():
	global DEBUG, _running

	for event in pygame.event.get():
		if event.type == pygame.QUIT: _running=False
		elif event.type == pygame.KEYDOWN:
			if event.key == pygame.K_ESCAPE:
				_running=False
				return
			elif event.key == pygame.K_F5:
				DEBUG=not DEBUG
				return
		statemanager.handle_input(event)
	pass

def _update(delta_time):
	statemanager.update(delta_time)
	_fps_stats.update(delta_time)
	#SoundManager.instance().update(delta_time)

def _render():
	_screen.fill(cfg("game.background_color"))
	statemanager.render(_screen)
	if DEBUG: _fps_stats.render(_screen)
	pygame.display.update()

if __name__ == "__main__":
	run()

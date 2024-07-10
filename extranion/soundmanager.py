import pygame
from extranion.config import cfg
from extranion.asset import asset

class SoundManager:

	@staticmethod
	def init():
		SoundManager.__sound_volume = cfg("sound.volume")
		SoundManager.__music_volume = cfg("music.volume")
		SoundManager.__current_music = None
		SoundManager.__next_music = None

	@staticmethod
	def play_sound(name):
		sound = asset.get(name)
		sound.set_volume(SoundManager.__sound_volume)
		sound.play()

	@staticmethod
	def stop_sound(name):
		sound = asset.get(name)
		sound.stop()

	@staticmethod
	def play_music(name):

		if name is SoundManager.__current_music: return
		music_conf = asset.get(name)
		pygame.mixer.music.load(music_conf["file"])
		pygame.mixer.music.set_volume(SoundManager.__music_volume*music_conf["volume_mult"])
		SoundManager.__current_music = name
		pygame.mixer.music.play(-1)

	@staticmethod
	def stop_music(time = 100):
		pygame.mixer.music.fadeout(time)
		SoundManager.__current_music = None

	@staticmethod
	def play_music_fade(name, time = 100):
		if name is SoundManager.__current_music: return
		SoundManager.__next_music = name
		pygame.mixer.music.fadeout(time)

	@staticmethod
	def update(SoundManager, delta_time):
		if SoundManager.__next_music is not None and not pygame.mixer.music.get_busy():
			SoundManager.play_music(SoundManager.__next_music)
			SoundManager.__current_music = SoundManager.__next_music
			SoundManager.__next_music = None

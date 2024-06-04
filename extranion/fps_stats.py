from extranion.config import cfg
from extranion.asset import asset

class FPS_Stats:

	def __init__(self):
		self.__refresh_update_time = cfg("timing.refresh_debug_fps")
		self.__update_time=0
		self.__logic_frames=0
		self.__render_frames=0
		self.__image=None

	def update(self, delta_time):
		self.__logic_frames += 1
		self.__update_time += delta_time
		if self.__update_time > self.__refresh_update_time:
			font=asset.get("fonts.sansation")
			self.__image=font.render(f"{self.__logic_frames} - {self.__render_frames}", True, cfg("game.foreground_color"), None)
			self.__update_time-=self.__refresh_update_time
			self.__logic_frames=0
			self.__render_frames=0

	def render(self, surface_dst):
		self.__render_frames+=1
		if self.__image is not None:
			surface_dst.blit(self.__image, cfg("timing.stats_pos"))

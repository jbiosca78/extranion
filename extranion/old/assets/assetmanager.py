from importlib import resources
from os import path
import pygame
from extranion.assets.asset import Asset, AssetType

class AssetManager:

	__instance = None

	@staticmethod
	def instance():
		if AssetManager.__instance is None:
			AssetManager()
		return AssetManager.__instance

	def __init__(self):
		if AssetManager.__instance is None:
			AssetManager.__instance = self

			self.__assets = {}
		else:
			raise Exception("There Can Be Only One Instance of AssetManager")

	def load(self, asset_type, category, asset_name, asset_filename, data_filename = None, font_size = 0, rows = 0, cols = 0):
		print("load_asset")
		with resources.path(asset_filename[0], asset_filename[1]) as asset_path:
			if path.isfile(asset_path) and asset_name not in self.__assets:
				print(f"asset loaded: {asset_name}")
				asset = Asset(asset_type, category)
				asset.load(asset_path, data_filename, font_size, rows, cols)
				self.__assets[asset_name] = asset

	def get(self, asset_name, sheet_name = None, sequence = 0):
		print("get asset")
		if sheet_name:
			if sheet_name in self.__assets:
				return self.__assets[sheet_name].payload.get_image(asset_name)
			return pygame.Surface((0,0)), pygame.Rect(0,0,0,0)
		else:
			if asset_name in self.__assets:
				if self.__assets[asset_name].asset_type == AssetType.Image:
					return self.__assets[asset_name].payload, self.__assets[asset_name].payload.get_rect()
				elif self.__assets[asset_name].asset_type == AssetType.FlipBook:
					return self.__assets[asset_name].payload.get_image(sequence)
				else:
					print("Found")
					return self.__assets[asset_name].payload
			else:
				print("Warning! asset get found none")
				return None

	def clear(self, category = None):
		if category:
			for k in list(self.__assets.keys()):
				if self.__assets[k].category == category:
					del self.__assets[k]
		else:
			self.__assets = {}

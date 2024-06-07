from importlib import resources
#from os import path
import pygame
#from extranion.asset.a import Asset, AssetType
from extranion.config import cfg
import extranion.log as log

class AssetItem:

	def __init__(self, category, type, filepath, conf):
		self.category = category
		self.type = type
		self.data = None
		if self.type == "image":
			self.data = pygame.image.load(filepath)
		elif self.type == "font":
			self.data = pygame.font.Font(filepath, conf["size"])
		elif self.type == "spritesheet":
			self.data = _load_spritesheet(filepath, conf["size"])

	def get(self):
		return self.data

def _load_spritesheet(filepath, size):
	size_x, size_y = size
	image = pygame.image.load(filepath)
	res_x = image.get_width()
	res_y = image.get_height()

	# calculamos cuantos sprites hay
	dim_x = res_x // size_x
	dim_y = res_y // size_y

	sheet=[]
	for y in range(dim_y):
		sheet.append([])
		for x in range(dim_x):
			rect = pygame.Rect(x * size_x+x+1, y * size_y+y+1, size_x, size_y)
			sheet[y].append(image.subsurface(rect))

	return sheet

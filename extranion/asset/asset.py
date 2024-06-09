from importlib import resources
from extranion import log
from extranion.config import cfg
from extranion.asset.assetitem import AssetItem

_assets={}

def load(category, config, name=None):
	global _assets
	if name is None: name = config
	log.debug(f"asset.load {category} {config} {name}")
	conf=cfg(f"{config}")
	type=conf["type"]
	filepath=str(resources.files("extranion.data").joinpath(type).joinpath(conf["file"]))
	asset = AssetItem(category, type, filepath, conf)
	_assets[name] = asset

def unload(category=None, name=None):
	global _assets
	if category:
		for k in list(_assets.keys()):
			if _assets[k].category == category:
				del _assets[k]
	elif name:
		if name in _assets:
			del _assets[name]
	else:
		_assets = {}

def get(name):
	global _assets
	if name in _assets:
		return _assets[name].get()
	else:
		log.error(f"ERROR: Asset {name} not found")
		return None

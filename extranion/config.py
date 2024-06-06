from importlib import resources
#import json
import yaml

def cfg(*items):

	# En lugar de varios argumentos, permitimos separar los campos por puntos
	if len(items)==1 and "." in items[0]:
		items=items[0].split(".")

	data=configdata
	for key in items:
		if key not in data:
			return None
		data = data[key]
	return data

# Cargamos la configuración al iniciar el módulo
# no le veo mucho sentido a crear una clase con un singleton programado para la carga inicial como en clase,
# me parece innecesariamente complicado y poco "pythonico" ya que los módulos python se cargan sólo una vez.
# También actualizamos el método de obtención del path, ya que importlib.resources.path está deprecado en python 3.11
#configdata=json.load(resources.files("extranion.data").joinpath("config.json").open('rt'))
configdata=yaml.safe_load(resources.files("extranion.data").joinpath("config.yaml").open('rt'))

# Establecemos variables globales
DEBUG = cfg("debug.activated")

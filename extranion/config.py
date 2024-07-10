from importlib import resources
#import json
import yaml

def cfg(itempath):

	data=configdata
	for key in itempath.split("."):
		if key not in data:
			return None
		data = data[key]
	return data

# Cargamos la configuración al iniciar el módulo
# no le veo mucho sentido a crear una clase con un singleton programado para la carga inicial como en clase,
# me parece innecesariamente complicado y poco "pythonico" ya que los módulos python se cargan sólo una vez.
# También actualizamos el método de obtención del path, ya que importlib.resources.path está deprecado en python 3.11
configpath=resources.files("extranion.data").joinpath("config.yaml")
configdata=yaml.safe_load(open(configpath,"rt"))

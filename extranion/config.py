from importlib import resources
import yaml

def cfg(itempath):

	data=configdata
	for key in itempath.split("."):
		if key not in data:
			return None
		data = data[key]
	return data

# Cargamos la configuración al iniciar el módulo
configpath=resources.files("extranion.data").joinpath("config.yaml")
configdata=yaml.safe_load(open(configpath,"rt"))

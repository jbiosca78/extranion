from extranion.tools import log
from extranion.config import cfg
from extranion.states import statemanager
from extranion.asset import asset

# Este módulo requiere pympler, no lo importo directamente porque es opcional, ya
# que sólo es útil durante el desarrollo del juego y no para su uso normal.
# En caso de no tenerlo instalado, simplemente no se mostrará la información.

# Si lo tenemos instalado, con TAB podemos ver en el log la memoria usada por los
# principales módulos del juego, y al activar debug con F5 podremos verlo en pantalla.

# El control de la memoria usada es muy útil para detectar memory leaks en fases
# tempranas de desarrollo.

def debug_memory_log():

	try:
		import pympler.asizeof
	except Exception:
		log.info("pympler not found, memory stats not available")
		return

	# Si tenemos pympler, mostramos la ram que ocupa nuestro estado actual
	# con esto podemos detectar memory leaks, por ejemplo si no estamos
	# destruyendo bien algún objeto
	mem_state=pympler.asizeof.asizeof(statemanager)//1024
	mem_assets=pympler.asizeof.asizeof(asset)//1024
	log.info(f"MEM used: state={mem_state}K assets={mem_assets}K")

def debug_memory_render(canvas):

	try:
		import pympler.asizeof
	except Exception:
		return

	mem=0
	mem+=pympler.asizeof.asizeof(statemanager)//1024
	mem+=pympler.asizeof.asizeof(asset)//1024

	font=asset.get("font.default")
	image=font.render(f"{mem}K", True, cfg("game.foreground_color"), None)
	canvas.blit(image, cfg("debug.mem_pos"))

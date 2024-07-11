from extranion.tools import log
from extranion.states.intro import Intro
from extranion.states.info import Info
from extranion.states.travel import Travel
from extranion.states.gameplay import Gameplay

# TODO: convertir a clase estática

states = {
	"intro": Intro(),
	"info": Info(),
	"travel": Travel(),
	"gameplay": Gameplay()
}

def init():
	global current_state
	current_state=states["intro"]
	current_state.enter()

def release():
	current_state.exit()

def event(event):
	current_state.event(event)

def update(delta_time):
	if current_state.change_state is not None: __change_state()
	current_state.update(delta_time)

def render(surface):
	current_state.render(surface)

def __change_state():

	global current_state

	prev_state = current_state.name
	new_state = current_state.change_state

	log.info(f"Change state from {prev_state} to {new_state}")

	current_state.exit()
	current_state=states[new_state]
	current_state.previous_state = prev_state
	current_state.change_state = None
	current_state.enter()

from extranion.states.intro import Intro
from extranion.states.gameplay import Gameplay
from extranion import log

_states = {
	"Intro": Intro(),
	"Gameplay": Gameplay()
}

def init():
	global _current_state, _current_state_name
	#_current_state_name="Intro"
	_current_state_name="Gameplay"
	_current_state=_states[_current_state_name]
	_current_state.enter()

def release():
	_current_state.release()

def event(event):
	_current_state.event(event)

def update(delta_time):
	if _current_state.change_state is not None:
		_change_state()
	_current_state.update(delta_time)

def render(surface):
	_current_state.render(surface)

def _change_state():

	global _current_state, _current_state_name

	log.info(f"Change state from {_current_state_name} to {_current_state.change_state}")

	_current_state.release()

	previous_state = _current_state_name
	_current_state_name = _current_state.change_state
	_current_state = _states[_current_state_name]
	_current_state.previous_state = previous_state

	_current_state.change_state = None
	_current_state.enter()

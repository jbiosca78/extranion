from extranion.states.intro import Intro
#from extranion.states.gameplay import Gameplay

_states = {
	"Intro": Intro(),
	#"GamePlay": Gameplay()
}

def init():
	global _current_state, _current_state_name

	_current_state_name = 'Intro'
	_current_state=_states[_current_state_name]
	_current_state.enter()

def release():
	_current_state.exit()

def handle_input(event):
	_current_state.handle_input(event)

def update(delta_time):
	if _current_state.done:
		_change_state()
	_current_state.update(delta_time)

def render(surface):
	_current_state.render(surface)

def _change_state():

	global _current_state, _current_state_name

	_current_state.exit()

	previous_state = _current_state_name
	_current_state_name = _current_state.next_state
	_current_state = _states[_current_state_name]
	_current_state.previous_state = previous_state

	_current_state.done = False
	_current_state.enter()

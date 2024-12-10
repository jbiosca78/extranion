from extranion.tools import log
from extranion.states.intro import Intro
from extranion.states.info import Info
from extranion.states.travel import Travel
from extranion.states.gameplay import Gameplay

class StateManager:

	__states = {
		"intro": Intro(),
		"info": Info(),
		"travel": Travel(),
		"gameplay": Gameplay()
	}

	@staticmethod
	def init():

		StateManager.__current_state=StateManager.__states["intro"]
		StateManager.__current_state.enter()

	@staticmethod
	def release():

		StateManager.__current_state.exit()

	@staticmethod
	def event(event):

		StateManager.__current_state.event(event)

	@staticmethod
	def update(delta_time):

		if StateManager.__current_state.change_state is not None:
			StateManager.__change_state()
		StateManager.__current_state.update(delta_time)

	@staticmethod
	def render(surface):

		StateManager.__current_state.render(surface)

	@staticmethod
	def __change_state():

		StateManager.__prev_state = StateManager.__current_state.name
		StateManager.__new_state = StateManager.__current_state.change_state

		log.info(f"Change state from {StateManager.__prev_state} to {StateManager.__new_state}")

		StateManager.__current_state.exit()
		StateManager.__current_state=StateManager.__states[StateManager.__new_state]
		StateManager.__current_state.previous_state = StateManager.__prev_state
		StateManager.__current_state.change_state = None
		StateManager.__current_state.enter()

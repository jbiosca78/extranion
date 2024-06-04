from abc import ABC, abstractmethod

class State(ABC):

    def __init__(self):
        self.done = False
        self.next_state = ""
        self.previous_state = ""

    @abstractmethod
    def enter(self):
        pass

    @abstractmethod
    def exit(self):
        pass

    @abstractmethod
    def handle_input(self, event):
        pass

    @abstractmethod
    def update(self, delta_time):
        pass

    @abstractmethod
    def render(self, surface):
        pass
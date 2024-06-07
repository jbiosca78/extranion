from abc import ABC, abstractmethod

class State(ABC):

    def __init__(self):
        self.previous_state = None
        self.change_state = None

    @abstractmethod
    def enter(self):
        pass

    @abstractmethod
    def release(self):
        pass

    @abstractmethod
    def event(self, event):
        pass

    @abstractmethod
    def update(self, delta_time):
        pass

    @abstractmethod
    def render(self, surface):
        pass

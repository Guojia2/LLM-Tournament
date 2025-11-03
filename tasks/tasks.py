from abc import ABC, abstractmethod


class Task(ABC):
    @abstractmethod
    def init(self, seed):
        """Initialize game state"""
        pass

    @abstractmethod
    def observe(self, state, agentId):
        """Return observation for specific agent"""
        pass

    @abstractmethod
    def step(self, state, actions):
        """Update state given actions"""
        pass

    @abstractmethod
    def score(self, state):
        """Return final scores"""
        pass

    def render(self, state):
        """Optional: render state for replay"""
        return str(state)
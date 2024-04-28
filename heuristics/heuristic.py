from abc import ABC, abstractmethod
from games import Observation

class Heuristic(ABC):
    """Abstract class that will define a heuristic for the game"""

    @abstractmethod
    def get_reward(self, observation: 'Observation') -> int:
        """Returns the reward of the observation"""
        pass
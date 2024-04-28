from abc import ABC, abstractmethod
from collections import defaultdict
from typing import Dict
from games import Action, Observation, ForwardModel

class Player(ABC):
    """Abstract class that will define a player of the game"""
    def __init__(self):
        self.verbose = False
        self.timeout = False
        self.forward_model_visits = 0
        self.visited_states = defaultdict(int)

    #@abstractmethod
    #def think(self, observation: 'Observation', forward_model: 'ForwardModel', budget: float) -> 'Action':
    #    """Returns the action to be executed"""
    #    pass

    @abstractmethod
    def think(self, observation: 'Observation', forward_model: 'ForwardModel', budget: float) -> None:
        """Returns the action to be executed"""
        pass

    @abstractmethod
    def get_action(self, index: int) -> 'Action':
        """Returns the action to be executed"""
        pass

    def set_verbose(self, verbose: bool):
        """Set the verbosity of the player"""
        self.verbose = verbose

    def set_timeout(self, timeout: bool = True):
        """Set the timeout of the player"""
        self.timeout = timeout

    def get_visited_states_count(self) -> int:
        """Returns the number of times the heuristic was called"""
        return len(self.visited_states.keys())
    
    def get_forward_model_visits(self) -> int:
        """Returns the number of times the forward model was called"""
        return self.forward_model_visits

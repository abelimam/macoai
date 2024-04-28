from abc import ABC, abstractmethod
from collections import defaultdict
from typing import List
from games import Action, Observation, ForwardModel

class FitnessEvaluator(ABC):
    """Abstract class that will define the fitness evaluator for the game"""

    @abstractmethod
    def evaluate(self, parameters: List[int], observation: 'Observation', forward_model: 'ForwardModel', visited_states: defaultdict) -> float:
        """Return the fitness of the observation"""
        pass

    @abstractmethod
    def ntboe_to_turn(self, ntboe_parameters: List[int]) -> List['Action']:
        """Converts a list of int parameters from NTBEA to a list of Action representing a turn."""
        pass

    @abstractmethod
    def get_action_from_parameter(self, parameter: int) -> 'Action':
        """Returns the action associated with the parameter."""
        pass

    @abstractmethod
    def get_parameter_from_action(self, action: 'Action') -> int:
        """Returns the parameter associated with the action."""
        pass
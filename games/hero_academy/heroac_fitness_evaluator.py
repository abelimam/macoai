from typing import List
from games.hero_academy.heroac_action import HeroAcademyAction
from games.hero_academy.heroac_observation import HeroAcademyObservation
from games.hero_academy.heroac_forward_model import HeroAcademyForwardModel
from players.ntuple_bandit_online_evolution import FitnessEvaluator
from heuristics import Heuristic

class HeroAcademyFitnessEvaluator(FitnessEvaluator):
    def __init__(self, heuristic: 'Heuristic'):
        self.heuristic = heuristic

# region Methods
    def evaluate(self, parameters: List[int], observation: 'HeroAcademyObservation', forward_model: 'HeroAcademyForwardModel') -> float:
        """Calculates the fitness of a turn given by N-Tuple Bandit Online Evolution as a parameter list, playing it from the given `Observation`."""
        turn = self.ntboe_to_turn(parameters)
        for action in turn:
            forward_model.step(observation, action)
        return self.heuristic.get_reward(observation)
    
    def ntboe_to_turn(self, ntboe_parameters: List[int]) -> List['HeroAcademyAction']:
        """Converts a list of int parameters from N-Tuple Bandit Online Evolution to a list of `Action` representing a turn."""
        turn = []
        for parameter in ntboe_parameters:
            turn.append(self.get_action_from_parameter(parameter))
        return turn
    
    def get_action_from_parameter(self, parameter: int) -> 'HeroAcademyAction':
        """Converts an int parameter from N-Tuple Bandit Online Evolution  to an `Action`."""
        pass
    
    def get_parameter_from_action(self, action: 'HeroAcademyAction') -> int:
        """Converts an `Action` to an int parameter for N-Tuple Bandit Online Evolution."""
        pass
# endregion
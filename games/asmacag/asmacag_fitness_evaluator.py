from collections import defaultdict
from typing import List
from games.asmacag.asmacag_card_type import AsmacagCardType
from games.asmacag.asmacag_card import AsmacagCard
from games.asmacag.asmacag_action import AsmacagAction
from games.asmacag.asmacag_observation import AsmacagObservation
from games.asmacag.asmacag_forward_model import AsmacagForwardModel
from heuristics import Heuristic
from players.ntuple_bandit_online_evolution import FitnessEvaluator

class AsmacagFitnessEvaluator(FitnessEvaluator):
    def __init__(self, heuristic: 'Heuristic'):
        self.heuristic = heuristic

# region Methods
    def evaluate(self, parameters: List[int], observation: 'AsmacagObservation', forward_model: 'AsmacagForwardModel', visited_states: defaultdict) -> float:
        """Calculates the fitness of a turn given by N-Tuple Bandit Online Evolution as a parameter list, playing it from the given `Observation`."""
        turn = self.ntboe_to_turn(parameters)
        for action in turn:
            forward_model.step(observation, action)
            visited_states[observation] += 1
        return self.heuristic.get_reward(observation)
    
    def ntboe_to_turn(self, ntboe_parameters: List[int]) -> List['AsmacagAction']:
        """Converts a list of int parameters from N-Tuple Bandit Online Evolution to a list of `Action` representing a turn."""
        turn = []
        for parameter in ntboe_parameters:
            turn.append(self.get_action_from_parameter(parameter))
        return turn
    
    def get_action_from_parameter(self, parameter: int) -> 'AsmacagAction':
        """Converts an int parameter from N-Tuple Bandit Online Evolution  to an `Action`."""
        if parameter < 2:
            return AsmacagAction(AsmacagCard(AsmacagCardType(parameter+2)))
        elif parameter < 8:
            return AsmacagAction(AsmacagCard(AsmacagCardType.NUMBER, 1), AsmacagCard(AsmacagCardType.NUMBER, parameter - 1))
        elif parameter < 14:
            return AsmacagAction(AsmacagCard(AsmacagCardType.NUMBER, 2), AsmacagCard(AsmacagCardType.NUMBER, parameter - 7))
        elif parameter < 20:
            return AsmacagAction(AsmacagCard(AsmacagCardType.NUMBER, 3), AsmacagCard(AsmacagCardType.NUMBER, parameter - 13))
        elif parameter < 26:
            return AsmacagAction(AsmacagCard(AsmacagCardType.NUMBER, 4), AsmacagCard(AsmacagCardType.NUMBER, parameter - 19))
        elif parameter < 32:
            return AsmacagAction(AsmacagCard(AsmacagCardType.NUMBER, 5), AsmacagCard(AsmacagCardType.NUMBER, parameter - 25))
        elif parameter < 38:
            return AsmacagAction(AsmacagCard(AsmacagCardType.NUMBER, 6), AsmacagCard(AsmacagCardType.NUMBER, parameter - 31))
    
    def get_parameter_from_action(self, action: 'AsmacagAction') -> int:
        """Converts an `Action` to an int parameter for N-Tuple Bandit Online Evolution."""
        if action.get_played_card().get_type() == AsmacagCardType.DIV2 \
                or action.get_played_card().get_type() == AsmacagCardType.MULT2:
            return action.get_played_card().get_type().value - 2
        elif action.get_played_card().get_type() == AsmacagCardType.NUMBER:
            return (action.get_played_card().get_number() - 1) * 6 + action.get_board_card().get_number() + 1
# endregion
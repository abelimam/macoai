from games import Observation
from heuristics.heuristic import Heuristic

class SimpleHeuristic(Heuristic):
    """Defines a simple reward for the current player."""

    def get_reward(self, observation: 'Observation'):
        """Returns a reward for the current player."""
        if observation.get_current_turn() == 0:
            return observation.get_player_0_score() - observation.get_player_1_score()
        else:
            return observation.get_player_1_score() - observation.get_player_0_score()
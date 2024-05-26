from games import Action, Observation, ForwardModel
from heuristics import Heuristic
from players.montecarlo_tree_search import MontecarloTreeSearchNode
from players import Player
import time

# Ali

class MontecarloTreeSearchPlayer(Player):
    """Entity that plays a game by using the Monte Carlo Tree Search algorithm to choose all actions in a turn."""
    def __init__(self, heuristic: 'Heuristic', c_value: float):
        super().__init__()
        self.heuristic = heuristic
        self.c_value = c_value
        self.turn = []
        self.full_rollout = False

    def set_full_rollout_on(self):
        self.full_rollout = False

# region Methods
    def think(self, observation: 'Observation', forward_model: 'ForwardModel', budget: float) -> None:
        self.turn.clear()

        # compute the turn
        t0 = time.time()
        root = MontecarloTreeSearchNode(observation, self.heuristic, None)
        self.forward_model_visits += root.extend(forward_model, self.visited_states)
        current_node = root
        action_points_per_turn = observation.get_game_parameters().get_action_points_per_turn()

        while time.time() - t0 < budget - 0.12:
            best_child = current_node.get_best_child_by_ucb(self.c_value)
            if best_child.get_amount_of_children() > 0:
                current_node = best_child
            else:
                if not best_child.get_is_unvisited() and not best_child.get_is_terminal(forward_model):
                    self.forward_model_visits += best_child.extend(forward_model, self.visited_states)
                    best_child = best_child.get_random_child()

                if self.full_rollout:
                    reward, fm_visits = best_child.full_rollout(forward_model, self.visited_states)
                else:
                    reward, fm_visits = best_child.rollout(forward_model, self.visited_states)
                self.forward_model_visits += fm_visits
                best_child.backpropagate(reward)
                current_node = root

        # retrieve the turn
        current_node = root
        for _ in range(action_points_per_turn):
            best_child = current_node.get_best_child_by_average()
            if best_child is None:
                break
            self.turn.append(best_child.get_action())
            current_node = best_child

    def get_action(self, index: int) -> 'Action':
        """Returns the next action in the turn."""
        if index < len(self.turn):
            return self.turn[index]
        return None
# endregion

# region Override
    def __str__(self):
        return f"MontecarloTreeSearchPlayer[{self.c_value}]"
# endregion
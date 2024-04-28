from games import Action, Observation, ForwardModel
from heuristics import Heuristic
from players.montecarlo_tree_search.montecarlo_tree_search_node import MontecarloTreeSearchNode
from players.player import Player
import time

class BridgeBurningMontecarloTreeSearchPlayer(Player):
    def __init__(self, heuristic: 'Heuristic', c_value: float):
        super().__init__()
        self.heuristic = heuristic
        self.c_value = c_value
        self.turn = []

# region Methods
    def think(self, observation: 'Observation', forward_model: 'ForwardModel', budget: float) -> None:
        """Computes a list of actions for a complete turn using the Bridge Burning Monte Carlo Tree Search algorithm and returns them in order each time it's called during the turn."""
        self.turn.clear()

        # compute the turn
        root = MontecarloTreeSearchNode(observation, self.heuristic, None)
        self.forward_model_visits += root.extend(forward_model, self.visited_states)
        current_node = root

        budget_round = budget / observation.get_game_parameters().get_action_points_per_turn()
        for _ in range(observation.get_game_parameters().get_action_points_per_turn()):
            t0 = time.time()
            while time.time() - t0 < budget_round - 0.05:
                best_child = current_node.get_best_child_by_ucb(self.c_value)
                if best_child.get_amount_of_children() > 0:
                    current_node = best_child
                else:
                    if not best_child.get_is_unvisited() and not best_child.get_is_terminal(forward_model):
                        self.forward_model_visits += best_child.extend(forward_model, self.visited_states)
                        best_child = best_child.get_random_child()
                    reward, fm_visits = best_child.full_rollout(forward_model, self.visited_states)
                    self.forward_model_visits += fm_visits
                    best_child.backpropagate(reward)
                    current_node = root

            # retrieve the turn
            current_node = root
            best_child = current_node.get_best_child_by_average()
            if best_child is None:
                break
            self.turn.append(best_child.get_action())
            root = best_child
            if root.get_amount_of_children() == 0:
                root.extend(forward_model, self.visited_states)
            current_node = best_child

    def get_action(self, index: int) -> 'Action':
        """Returns the next action in the turn."""
        if index < len(self.turn):
            return self.turn[index]
        return None
# endregion

# region Override
    def __str__(self):
        return f"BridgeBurningMontecarloTreeSearchPlayer[{self.c_value}]"
# endregion
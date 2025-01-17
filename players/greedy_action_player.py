from typing import List
from games import Action, Observation, ForwardModel
from players.player import Player
import time

# Ali
class GreedyActionPlayer(Player):
    def __init__(self, heuristic):
        super().__init__()
        self.heuristic = heuristic
        self.actions: List[Action] = []

    def think(self, observation: 'Observation', forward_model: 'ForwardModel', budget: float) -> None:
        self.actions = []
        current_observation = observation.clone()
        t0 = time.time()

        while time.time() - t0 < budget - 0.05 and len(self.actions) < observation.get_game_parameters().get_action_points_per_turn():
            best_action = None
            best_score = float('-inf')

            for action in current_observation.get_actions():
                next_observation = current_observation.clone()
                forward_model.step(next_observation, action)
                score = self.heuristic.get_reward(next_observation)
                self.forward_model_visits += 1
                self.visited_states[next_observation] += 1
                if score > best_score:
                    best_score = score
                    best_action = action

            if best_action is not None:
                self.actions.append(best_action)
                forward_model.step(current_observation, best_action)

    def get_action(self, index: int) -> 'Action':
        if index < len(self.actions):
            return self.actions[index]
        return None

    def __str__(self):
        return "GreedyActionPlayer"
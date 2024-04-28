from typing import List
from games import Action, Observation, ForwardModel
from players.player import Player

# Ali
class AlwaysFirstPlayer(Player):
    def __init__(self):
        super().__init__()
        self.actions: List[Action] = []

    def think(self, observation: 'Observation', forward_model: 'ForwardModel', budget: float) -> None:
        self.actions = []
        current_observation = observation.clone()

        for _ in range(observation.get_game_parameters().get_action_points_per_turn()):
            actions = current_observation.get_actions()
            if actions:
                action = actions[0]
                self.actions.append(action)
                forward_model.step(current_observation, action)

    def get_action(self, index: int) -> 'Action':
        if index < len(self.actions):
            return self.actions[index]
        return None

    def __str__(self):
        return "AlwaysFirstPlayer"
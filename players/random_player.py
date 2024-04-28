from typing import List
from games import Action, Observation, ForwardModel
from players.player import Player

# Ali
class RandomPlayer(Player):
    def __init__(self):
        super().__init__()
        self.actions: List[Action] = []

    def think(self, observation: 'Observation', forward_model: 'ForwardModel', budget: float) -> None:
        self.actions = []
        for _ in range(observation.get_game_parameters().get_action_points_per_turn()):
            action = observation.get_random_action()
            if action is not None:
                self.actions.append(action)

    def get_action(self, index: int) -> 'Action':
        if index < len(self.actions):
            return self.actions[index]
        return None

    def __str__(self):
        return "RandomPlayer"
from games import Action, Observation, ForwardModel
from players import Player

class RandomPlayer(Player):
    def __init__(self):
        """Player class implemented for Random players."""
        super().__init__()
        self.turn = []

# region Methods
    def think(self, observation: 'Observation', forward_model: 'ForwardModel', budget: float) -> 'Action':
        """Think about the next action to take randomly."""
        self.turn.clear()
        new_observation = observation.clone()
        for _ in range(observation.get_game_parameters().get_action_points_per_turn()):
            action = new_observation.get_random_action()
            self.turn.append(action)
            forward_model.step(new_observation, action)
    
    def get_action(self, index: int) -> 'Action':
        """Returns the next action in the turn."""
        if index < len(self.turn):
            return self.turn[index]
        return None

# endregion

# region Override
    def __str__(self):
        return "RandomPlayer"
# endregion
from games import Action, Observation, ForwardModel
from players import Player

class HumanPlayer(Player):
    """Player class implemented for Human players."""
    def __init__(self) -> None:
        super().__init__()

# region Methods
    def think(self, observation: 'Observation', forward_model: 'ForwardModel', budget: float) -> 'Action':
        """Think about the next action to take."""
        actions = observation.get_actions()
        for i, action in enumerate(actions):
            print(f"{i}: {action}")

        selection = -1
        while selection < 0 or selection >= len(actions):
            selection = int(input("Select an action: "))

        return actions[selection]
# endregion

# region Override
    def __str__(self):
        return "HumanPlayer"
# endregion
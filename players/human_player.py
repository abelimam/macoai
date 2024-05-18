from games import Action, Observation, ForwardModel
from players import Player


class HumanPlayer(Player):
    """Player class implemented for Human players."""
    def init(self) -> None:
        super().init()
        self.selected_action = None
# region Methods

    def think(self, observation: 'Observation', forward_model: 'ForwardModel', budget: float) -> 'Action':
        """Think about the next action to take."""
        actions = observation.get_actions()
        for i, action in enumerate(actions):
            print(f"{i}: {action}")

        selection = -1
        while selection < 0 or selection >= len(actions):
            selection = int(input("Select an action: "))

        self.selected_action = actions[selection]

    def get_action(self, index: int) -> 'Action':
        """Get the selected action."""
        return self.selected_action

# endregion

# region Override
    def __str__(self):
        return "HumanPlayer"

# endregion

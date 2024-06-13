from games import Action, Observation, ForwardModel
from players import Player


class HumanPlayer(Player):
    """Player class implemented for Human players."""
    def __init__(self) -> None:
        super().__init__()
        self.selected_actions = []

    def think(self, observation: 'Observation', forward_model: 'ForwardModel', budget: float) -> None:
        """Think about the next action to take."""
        self.selected_actions = []
        action_points = observation.get_game_parameters().get_action_points_per_turn()
        
        for i in range(action_points):
            print(f"\nAction Point {i+1}/{action_points}")
            actions = observation.get_actions()
            for j, action in enumerate(actions):
                print(f"{j}: {action}")

            selection = -1
            while selection < 0 or selection >= len(actions):
                try:
                    selection = int(input("Select an action: "))
                except ValueError:
                    print("Invalid input. Please enter a valid action index.")

            self.selected_actions.append(actions[selection])

    def get_action(self, index: int) -> 'Action':
        """Get the selected action at the specified index."""
        if index < len(self.selected_actions):
            return self.selected_actions[index]
        return None

    def __str__(self):
        return "HumanPlayer"
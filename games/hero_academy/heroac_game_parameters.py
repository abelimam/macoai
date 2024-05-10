from typing import Optional
from games import GameParameters

class HeroAcademyGameParameters(GameParameters):
    """Class that holds all the game parameters."""
    
    def __init__(self,
            board_size=(5, 9),
            action_points_per_turn=5,
            seed=None,
            cards_on_deck = 45,
            cards_on_hand = 5,
            crystal_positions = [(1, 2), (3, 1)]) -> None:
        self.board_size = board_size
        self.action_points_per_turn = action_points_per_turn
        self.seed = seed
        self.cards_on_deck = cards_on_deck
        self.cards_on_hand = cards_on_hand
        self.crystal_positions = crystal_positions
        self.attack_positions = [(2, 2)]
        self.speed_positions = [(0, 0), (4, 0)]

# region Overrides
    def get_action_points_per_turn(self) -> int:
        return self.action_points_per_turn
    
    def get_seed(self) -> Optional[int]:
        return self.seed
    
    def __str__(self) -> str:
        return (
            f"GameParameters("
            f"board_size={self.board_size}, "
            f"action_points_per_turn={self.action_points_per_turn}, "
            f"attack_positions={self.attack_positions}, "
            f"speed_positions={self.speed_positions}, "
            f")")
# endregion
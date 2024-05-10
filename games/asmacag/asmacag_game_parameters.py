from typing import Optional
from games import GameParameters

class AsmacagGameParameters(GameParameters):
    """Contains the parameters for a `Game`. Note that these are assumed to be static and therefore are always shallow copied. Do not modify them after instatiating."""
    def __init__(self,
                 amount_cards_on_hand=9,
                 amount_cards_on_board=20,
                 action_points_per_turn=3,
                 min_number=1,
                 max_number=6,
                 amount_cards_limit_number=5,
                 amount_cards_normal_number=8,
                 amount_cards_mult2=6,
                 amount_cards_div2=6,
                 seed=None,
                 randomise_hidden_info=True):
        self.amount_cards_on_hand = amount_cards_on_hand
        self.amount_cards_on_board = amount_cards_on_board
        self.action_points_per_turn = action_points_per_turn
        self.min_number = min_number
        self.max_number = max_number
        self.amount_cards_limit_number = amount_cards_limit_number
        self.amount_cards_normal_number = amount_cards_normal_number
        self.amount_cards_mult2 = amount_cards_mult2
        self.amount_cards_div2 = amount_cards_div2
        self.seed = seed
        self.randomise_hidden_info = randomise_hidden_info

# region Overrides
    def get_action_points_per_turn(self) -> int:
        return self.action_points_per_turn
    
    def get_seed(self) -> Optional[int]:
        return self.seed

    def __str__(self):
        return f"{self.amount_cards_on_hand} {self.amount_cards_on_board} {self.action_points_per_turn} " \
               f"{self.min_number} {self.max_number} {self.amount_cards_limit_number} " \
               f"{self.amount_cards_normal_number} {self.amount_cards_mult2} {self.amount_cards_div2} {self.seed} "
# endregion
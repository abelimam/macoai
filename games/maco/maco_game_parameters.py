from typing import Optional
from games import GameParameters

class MacoGameParameters(GameParameters):
    def __init__(self,
                 board_size: int = 7,
                 action_points_per_turn: int = 3,
                 pieces_per_player: int = 50,
                 special_pieces_per_type: int = 2,
                 win_condition_length: int = 7,
                 seed: Optional[int] = None):
        self.board_size = board_size
        self.action_points_per_turn = action_points_per_turn
        self.pieces_per_player = pieces_per_player
        self.special_pieces_per_type = special_pieces_per_type
        self.win_condition_length = win_condition_length
        self.seed = seed

    def get_board_size(self) -> int:
        return self.board_size

    def get_action_points_per_turn(self) -> int:
        return self.action_points_per_turn

    def get_pieces_per_player(self) -> int:
        return self.pieces_per_player

    def get_special_pieces_per_type(self) -> int:
        return self.special_pieces_per_type

    def get_win_condition_length(self) -> int:
        return self.win_condition_length

    def get_seed(self) -> Optional[int]:
        return self.seed

    def __str__(self):
        return (
            f"MacoGameParameters("
            f"board_size={self.board_size}, "
            f"action_points_per_turn={self.action_points_per_turn}, "
            f"pieces_per_player={self.pieces_per_player}, "
            f"special_pieces_per_type={self.special_pieces_per_type}, "
            f"win_condition_length={self.win_condition_length}, "
            f"seed={self.seed})"
        )
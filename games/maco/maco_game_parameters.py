from typing import Optional
from games import GameParameters

class MacoGameParameters(GameParameters):
    def __init__(self,
                 board_size: int = 8,
                 action_points_per_turn: int = 3,
                 pieces_per_player: int = 100,
                 explode_per_player: int = 0,
                 block_per_player: int = 0,
                 win_condition_length: int = 6,
                 seed: Optional[int] = None):
        self.board_size = board_size
        self.action_points_per_turn = action_points_per_turn
        self.pieces_per_player = pieces_per_player
        self.explode_per_player = explode_per_player
        self.block_per_player = block_per_player
        self.win_condition_length = win_condition_length
        self.seed = seed

    def get_board_size(self) -> int:
        return self.board_size

    def get_action_points_per_turn(self) -> int:
        return self.action_points_per_turn

    def get_pieces_per_player(self) -> int:
        return self.pieces_per_player

    def get_explode_per_player(self) -> int:
        return self.explode_per_player

    def get_block_per_player(self) -> int:
        return self.block_per_player

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
            f"explode_per_player={self.explode_per_player}, "
            f"block_per_player={self.block_per_player}, "
            f"win_condition_length={self.win_condition_length}, "
            f"seed={self.seed})"
        )
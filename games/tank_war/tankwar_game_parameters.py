from typing import Optional
from games import GameParameters

class TankWarGameParameters(GameParameters):
    """Class that holds all the game parameters."""
    
    def __init__(self,
            board_size=10,
            init_tank_pos=[(-1, 0), (0, 1), (1, 0)],
            tank_possible_moves=[(-1, 0), (0, 1), (1, 0), (0, -1)],
            init_trash_count=10,
            action_points_per_turn=5,
            seed=None,
            resources_count_to_build=10) -> None:
        self.board_size = board_size
        self.init_tank_pos = init_tank_pos
        self.init_trash_count = init_trash_count
        self.action_points_per_turn = action_points_per_turn
        self.seed = seed
        self.player_0_spawn_pos = (int(self.board_size * 3 / 4), int(self.board_size / 4))
        self.player_1_spawn_pos = (int(self.board_size / 4), int(self.board_size * 3 / 4))
        self.tank_possible_moves = tank_possible_moves
        self.resources_count_to_build = resources_count_to_build

# region Overrides
    def get_action_points_per_turn(self) -> int:
        return self.action_points_per_turn
    
    def get_seed(self) -> Optional[int]:
        return self.seed
    
    def __str__(self) -> str:
        return (
            f"GameParameters("
            f"board_size={self.board_size}, "
            f"init_tank_pos={self.init_tank_pos}, "
            f"tank_possible_moves={self.tank_possible_moves}, "
            f"init_trash_count={self.init_trash_count}, "
            f"action_points_per_turn={self.action_points_per_turn}, "
            f"player_0_spawn_pos={self.player_0_spawn_pos}, "
            f"player_1_spawn_pos={self.player_1_spawn_pos}, "
            f"resources_count_to_build={self.resources_count_to_build}, "
            f")")
# endregion
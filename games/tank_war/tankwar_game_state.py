from typing import Any, Dict, List, Tuple
from games import GameState
from games.tank_war.tankwar_unit_type import TankWarUnitType
from games.tank_war.tankwar_unit import TankWarUnit
from games.tank_war.tankwar_unit_collection import TankWarUnitCollection
from games.tank_war.tankwar_game_parameters import TankWarGameParameters
from games.tank_war.tankwar_observation import TankWarObservation
import random

class TankWarGameState(GameState):
    def __init__(self, game_parameters: 'TankWarGameParameters') -> None:
        """GameState class represents the state of the game."""
        self.game_parameters = game_parameters
        self.current_turn = 0
        self.action_points_left = 0
        self.board = self.initiliaze_board_dict(game_parameters.board_size, game_parameters.init_trash_count)
        self.player_0_units = self.inittialize_player_units(game_parameters.player_0_spawn_pos, game_parameters.init_tank_pos)
        self.player_1_units = self.inittialize_player_units(game_parameters.player_1_spawn_pos, game_parameters.init_tank_pos)
        self.player_0_resources = 10
        self.player_1_resources = 10
        self.player_0_resources_next_round = 0
        self.player_1_resources_next_round = 0
        self.player_0_score = 0
        self.player_1_score = 0

# region Methods
    def get_observation(self) -> 'TankWarObservation':
        """Return the observation of the game state."""
        return TankWarObservation(self.get_state_info(), False)

    def reset(self) -> None:
        """Reset the game state."""
        self.current_turn = 0
        self.player_0_resources = 10
        self.player_1_resources = 10
        self.player_0_resources_next_round = 0
        self.player_1_resources_next_round = 0
        self.player_0_score = 0
        self.player_1_score = 0
        self.action_points_left = self.game_parameters.action_points_per_turn
        self.board = self.initiliaze_board_dict(self.game_parameters.board_size, self.game_parameters.init_trash_count)
        self.player_0_units = self.inittialize_player_units(self.game_parameters.player_0_spawn_pos, self.game_parameters.init_tank_pos)
        self.player_1_units = self.inittialize_player_units(self.game_parameters.player_1_spawn_pos, self.game_parameters.init_tank_pos)
#endregion

#region Helpers
    def inittialize_player_units(self, init_pos: Tuple[int, int], tank_pos: List[Tuple]) -> 'TankWarUnitCollection':
        """Initialize player initial tank units."""
        units = TankWarUnitCollection()
        for x_offset, y_offset in tank_pos:
            units.add_unit(TankWarUnit(TankWarUnitType.TANK, (init_pos[0] + x_offset, init_pos[1] + y_offset)))
            units.add_unit(TankWarUnit(TankWarUnitType.TILE, (init_pos[0] + x_offset, init_pos[1] + y_offset)))
            self.board[(init_pos[0] + x_offset, init_pos[1] + y_offset)] = self.game_parameters.init_trash_count
        units.add_unit(TankWarUnit(TankWarUnitType.TILE, init_pos))
        self.board[init_pos] = self.game_parameters.init_trash_count
        return units

    def initiliaze_board_dict(self, board_size: int, trash_count: int) -> Dict[Tuple[int, int], int]:
        """Initialize the board of the game."""
        return {(i, j): random.randint(1, trash_count) for i in range(board_size) for j in range(board_size)}
#endregion

#region Override
    def get_current_turn(self) -> int:
        return self.current_turn
    
    def get_action_points_left(self) -> int:
        return self.action_points_left

    def get_game_parameters(self) -> 'TankWarGameParameters':
        return self.game_parameters
    
    def get_player_0_score(self) -> int:
        return self.player_0_score
    
    def get_player_1_score(self) -> int:
        return self.player_1_score
    
    def get_state_info(self) -> Dict[str, Any]:
        return {
            "current_turn": self.current_turn,
            "board": self.board.copy(),
            "player_0_score": self.player_0_score,
            "player_0_units": self.player_0_units.clone(),
            "player_0_resources": self.player_0_resources,
            "player_0_resources_next_round": self.player_0_resources_next_round,
            "player_1_score": self.player_1_score,
            "player_1_units": self.player_1_units.clone(),
            "player_1_resources": self.player_1_resources,
            "player_1_resources_next_round": self.player_1_resources_next_round,
            "action_points_left": self.action_points_left,
            "game_parameters": self.game_parameters
        }

    def __str__(self):
        return (f"TURN: {self.current_turn!s}\n"
                #f"BOARD: {self.board!s}\n"
                f"UNITS P1: {self.player_0_units!s}\n"
                f"SCORE P1: {self.player_0_score!s}\n"
                f"UNITS P2: {self.player_1_units!s}\n"
                f"SCORE P2: {self.player_1_score!s}\n"
                f"ACTION POINTS LEFT: {self.action_points_left!s}")
#endregion
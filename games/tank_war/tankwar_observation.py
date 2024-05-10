from typing import Any, Dict, List, Tuple
from copy import deepcopy
from games.observation import Observation
from games.tank_war.tankwar_action import TankWarAction
from games.tank_war.tankwar_unit_type import TankWarUnitType
from games.tank_war.tankwar_unit import TankWarUnit
from games.tank_war.tankwar_unit_collection import TankWarUnitCollection
from games.tank_war.tankwar_game_parameters import TankWarGameParameters
import random

class TankWarObservation(Observation):
    def __init__(self, game_state: Dict[str, Any], randomise_hidden_info: bool = False):
        if game_state is not None:
            self.game_parameters: 'TankWarGameParameters' = game_state['game_parameters']
            self.current_turn = game_state['current_turn']
            self.action_points_left = game_state['action_points_left']
            self.player_0_units: 'TankWarUnitCollection' = game_state['player_0_units']
            self.player_1_units: 'TankWarUnitCollection' = game_state['player_1_units']
            self.board: Dict[Tuple[int, int], int] = game_state['board']
            self.player_0_resources = game_state['player_0_resources']
            self.player_1_resources = game_state['player_1_resources']
            self.player_0_resources_next_round = game_state['player_0_resources_next_round']
            self.player_1_resources_next_round = game_state['player_1_resources_next_round']
            self.player_0_score = game_state['player_0_score']
            self.player_1_score = game_state['player_1_score']

# region Methods
    def clone(self) -> 'TankWarObservation':
        """Clone the observation."""
        new_observation = TankWarObservation(None)
        new_observation.game_parameters = self.game_parameters
        new_observation.current_turn = self.current_turn
        new_observation.action_points_left = self.action_points_left
        new_observation.player_0_units = self.player_0_units.clone()
        new_observation.player_1_units = self.player_1_units.clone()
        new_observation.board = self.board.copy()
        new_observation.player_0_resources = self.player_0_resources
        new_observation.player_1_resources = self.player_1_resources
        new_observation.player_0_resources_next_round = self.player_0_resources_next_round
        new_observation.player_1_resources_next_round = self.player_1_resources_next_round
        new_observation.player_0_score = self.player_0_score
        new_observation.player_1_score = self.player_1_score
        return new_observation

    def copy_into(self, other: 'TankWarObservation') -> None:
        """Copy the observation into another one."""
        other.game_parameters = self.game_parameters
        other.current_turn = self.current_turn
        other.action_points_left = self.action_points_left
        other.player_0_units = self.player_0_units.clone()
        other.player_1_units = self.player_1_units.clone()
        other.board = self.board.copy()
        other.player_0_resources = self.player_0_resources
        other.player_1_resources = self.player_1_resources
        other.player_0_resources_next_round = self.player_0_resources_next_round
        other.player_1_resources_next_round = self.player_1_resources_next_round
        other.player_0_score = self.player_0_score
        other.player_1_score = self.player_1_score

    def is_action_valid(self, action: 'TankWarAction') -> bool:
        """Checks if the given action is currently valid."""
        units = self.get_current_player_units()
        unit_pos = action.get_unit().get_pos()
        if action.get_unit().get_unit_type() == TankWarUnitType.TANK:
            movement = action.get_unit_movement()
            destination = action.get_pos()
            return self.tank_move_is_valid(movement, destination) or (destination is None and self.tank_spawn_is_valid(unit_pos))
        else:
            return unit_pos not in units.get_tanks_positions() and unit_pos not in units.get_recyclers_positions() and unit_pos in units.get_tiles_positions()
# endregion

# region Getters
    def get_actions(self) -> List['TankWarAction']:
        """Get all the possible actions for the current player."""
        actions = []
        units = self.get_current_player_units()

        if self.get_current_player_resources() >= self.game_parameters.resources_count_to_build:
            available_positions = units.get_tank_and_available_tiles_positions()
        else:
            available_positions = units.get_tanks_positions()

        for pos in available_positions:
            unit_pos = deepcopy(pos)
            if unit_pos in units.get_tanks_positions():
                for (x_offset, y_offset) in self.game_parameters.tank_possible_moves:
                    destination = (unit_pos[0] + x_offset, unit_pos[1] + y_offset)
                    if not self.pos_out_of_bounds(destination):
                        actions.append(TankWarAction(units.get_tank_in_position(unit_pos).clone(), destination))
                actions.append(TankWarAction(TankWarUnit(TankWarUnitType.TANK, unit_pos)))
            elif unit_pos not in units.get_tanks_positions() and unit_pos not in units.get_recyclers_positions():
                actions.append(TankWarAction(TankWarUnit(TankWarUnitType.TANK, unit_pos)))
                actions.append(TankWarAction(TankWarUnit(TankWarUnitType.RECYCLER, unit_pos)))
        return actions

    def get_random_action(self) -> 'TankWarAction':
        """Gets a random action that is currently valid."""
        units = self.get_current_player_units()
        if self.get_current_player_resources() >= self.game_parameters.resources_count_to_build:
            unit = random.choice(units.get_tank_and_available_tiles_units())
        else:
            unit = random.choice(units.get_tank_units())

        if unit.unit_type == TankWarUnitType.TANK:
            moves = unit.get_possible_moves(self.game_parameters.board_size, self.game_parameters.tank_possible_moves)
            return TankWarAction(unit.clone(), random.choice(moves))
        else:
            unit_pos = deepcopy(unit.pos)
            if unit.pos not in units.get_tanks_positions():
                spawn_type = random.choice([TankWarUnitType.TANK, TankWarUnitType.RECYCLER])
                return TankWarAction(TankWarUnit(spawn_type, unit_pos), None)
            else:
                return TankWarAction(TankWarUnit(TankWarUnitType.TANK, unit_pos), None)
# endregion

# region Helpers
    def get_current_player_units(self) -> 'TankWarUnitCollection':
        """Get the current player units."""
        return self.player_0_units if self.current_turn == 0 else self.player_1_units

    def get_current_player_resources(self) -> int:
        """Get the current player resources."""
        return self.player_0_resources if self.current_turn == 0 else self.player_1_resources

    def pos_out_of_bounds(self, pos: Tuple[int, int]) -> bool:
        """Checks if the given position is out of bounds."""
        return pos[0] < 0 or pos[0] >= self.game_parameters.board_size or pos[1] < 0 or pos[1] >= self.game_parameters.board_size
    
    def tank_move_is_valid(self, movement: Tuple[int, int], destination: Tuple[int, int]) -> bool:
        """Checks if the given tank move is valid."""
        units = self.get_current_player_units()
        return destination is not None and movement in self.game_parameters.tank_possible_moves and destination not in units.get_recyclers_positions() \
            and not self.pos_out_of_bounds(destination)
    
    def tank_spawn_is_valid(self, unit_pos: Tuple[int, int]) -> bool:
        """Checks if the given tank spawn is valid."""
        units = self.get_current_player_units()
        return unit_pos not in units.get_recyclers_positions() and unit_pos in units.get_tiles_positions()
# endregion

#region Override
    def get_game_parameters(self) -> 'TankWarGameParameters':
        return self.game_parameters
    
    def get_action_points_left(self) -> int:
        return self.action_points_left
    
    def get_current_turn(self) -> int:
        return self.current_turn
    
    def get_player_0_score(self) -> int:
        return self.player_0_score
    
    def get_player_1_score(self) -> int:
        return self.player_1_score
    
    def __str__(self):
        return (f"TURN: {self.current_turn!s}\n"
                f"UNITS P1: {self.player_0_units!s}\n"
                f"SCORE P1: {self.player_0_score!s}\n"
                f"UNITS P2: {self.player_1_units!s}\n"
                f"SCORE P2: {self.player_1_score!s}\n"
                f"ACTION POINTS LEFT: {self.action_points_left!s}")
    
    def __eq__(self, __o: object) -> bool:
        if not isinstance(__o, TankWarObservation):
            return False
        return self.current_turn == __o.current_turn and self.player_0_units == __o.player_0_units and self.player_0_score == __o.player_0_score \
            and self.player_1_units == __o.player_1_units and self.player_1_score == __o.player_1_score and self.action_points_left == __o.action_points_left \
            and self.player_0_resources == __o.player_0_resources and self.player_1_resources == __o.player_1_resources and self.player_0_resources_next_round == __o.player_0_resources_next_round \
            and self.player_1_resources_next_round == __o.player_1_resources_next_round
    
    def __hash__(self) -> int:
        hashed = f"{self.current_turn}{self.action_points_left}{self.player_0_score}{self.player_1_score}"
        hashed += f"{self.player_0_units.__hash__()}{self.player_1_units.__hash__()}"
        hashed += f"{self.player_0_resources}{self.player_1_resources}{self.player_0_resources_next_round}{self.player_1_resources_next_round}"
        return hash(hashed)
#endregion
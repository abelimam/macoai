from typing import Union, Tuple
from copy import deepcopy
from games import ForwardModel
from games.tank_war.tankwar_unit_type import TankWarUnitType
from games.tank_war.tankwar_unit import TankWarUnit
from games.tank_war.tankwar_action import TankWarAction
from games.tank_war.tankwar_observation import TankWarObservation
from games.tank_war.tankwar_game_state import TankWarGameState

class TankWarForwardModel(ForwardModel):
    def __init__(self):
        super().__init__()

# region Methods
    def step(self, game_state: Union['TankWarGameState', 'TankWarObservation'], action: 'TankWarAction') -> bool:
        game_state.action_points_left -= 1
        units = game_state.player_0_units if game_state.current_turn == 0 else game_state.player_1_units

        if action is None:
            return False

        action_pos = deepcopy(action.get_pos())
        action_unit = action.get_unit().clone()
        if action_pos is not None and action_unit.get_unit_type() == TankWarUnitType.TANK:
            # A tank is moving
            if action.get_unit_movement() not in game_state.game_parameters.tank_possible_moves or self.pos_out_of_bounds(game_state, action_pos):
                # Illegal move
                return False
            enemy_units = game_state.player_0_units if game_state.current_turn == 1 else game_state.player_1_units
            if action_pos in enemy_units.get_tanks_positions():
                # Tank finds enemy tank
                self.resolve_clash_with_tank(game_state, action_unit, action_pos)
            elif action_pos in enemy_units.get_recyclers_positions():
                # Tank finds enemy recycler
                self.resolve_clash_with_recycler(game_state, action_unit, action_pos)
            elif action_pos in enemy_units.get_tiles_positions():
                # Tank finds enemy tile
                self.resolve_clash_with_tile(game_state, action_unit, action_pos)
            else:
                # Tank moves to empty tile
                units.move_unit(units.get_tank_in_position(action_unit.get_pos()), action_pos)
                if action_pos not in units.get_tiles_positions():
                    units.add_unit(TankWarUnit(TankWarUnitType.TILE, action_pos))
            self.update_score(game_state)
            return True

        if action_pos is None and action.get_unit().get_unit_type() == TankWarUnitType.TANK:
            # A tank is spawning
            unit_pos = action.get_unit().get_pos()
            if unit_pos not in units.get_tiles_positions() or unit_pos in units.get_recyclers_positions():
                # A tank can spawn in an empty tile or on a tank tile
                return False
            units.add_unit(action_unit.clone())
            self.remove_resources(game_state)
            self.update_score(game_state)
            return True
        
        if action_pos is None and action.get_unit().get_unit_type() == TankWarUnitType.RECYCLER:
            # A recycler is spawning
            unit_pos = action.get_unit().get_pos()
            if unit_pos not in units.get_tiles_positions() or unit_pos in units.get_recyclers_positions() or unit_pos in units.get_tanks_positions():
                # A tank can spawn in an empty tile
                return False
            units.add_unit(action_unit.clone())
            self.remove_resources(game_state)
            game_state.board[unit_pos] = 0
            self.update_score(game_state)
            return True
        
        return False

    def on_turn_ended(self, game_state: Union['TankWarGameState', 'TankWarObservation']) -> None:
        if self.is_turn_finished(game_state):
            self.update_turn_resources(game_state)
            game_state.current_turn = (game_state.current_turn + 1) % 2
            game_state.action_points_left = game_state.game_parameters.action_points_per_turn

    def is_terminal(self, game_state: Union['TankWarGameState', 'TankWarObservation']) -> bool:
        return len(game_state.player_0_units.get_tiles_positions()) == game_state.game_parameters.board_size ** 2 \
            or len(game_state.player_1_units.get_tiles_positions()) == game_state.game_parameters.board_size ** 2 \
            or (len(game_state.player_0_units.get_tanks_positions()) == 0 and game_state.player_0_resources < game_state.game_parameters.resources_count_to_build) \
            or (len(game_state.player_1_units.get_tanks_positions()) == 0 and game_state.player_1_resources < game_state.game_parameters.resources_count_to_build) \
            or len(game_state.player_0_units.get_tiles_positions()) == 0 \
            or len(game_state.player_1_units.get_tiles_positions()) == 0 \
            or all(x == 0 for x in game_state.board.values())

    def is_turn_finished(self, game_state: Union['TankWarGameState', 'TankWarObservation']) -> bool:
        return game_state.action_points_left == 0
# endregion

# region Helpers
    def pos_out_of_bounds(self, game_state: Union['TankWarGameState', 'TankWarObservation'], pos: Tuple[int, int]) -> bool:
        """Checks if the given position is out of bounds."""
        return pos[0] < 0 or pos[0] >= game_state.game_parameters.board_size or pos[1] < 0 or pos[1] >= game_state.game_parameters.board_size

    def remove_resources(self, game_state: Union['TankWarGameState', 'TankWarObservation']) -> bool:
        exec(f"game_state.player_{game_state.current_turn}_resources -= {game_state.game_parameters.resources_count_to_build}")
        return True

    def update_turn_resources(self, game_state: Union['TankWarGameState', 'TankWarObservation']) -> bool:
        exec(f"game_state.player_{game_state.current_turn}_resources += {self.future_player_resources(game_state)}")
        return True

    def get_score(self, game_state: Union['TankWarGameState', 'TankWarObservation']) -> int:
        future_resources = self.future_player_resources(game_state)
        player_units = game_state.player_0_units if game_state.current_turn == 0 else game_state.player_1_units
        current_units = len(player_units.get_units())
        return (current_units + future_resources) // 10

    def update_score(self, game_state: Union['TankWarGameState', 'TankWarObservation']) -> bool:
        score = self.get_score(game_state)
        exec(f"game_state.player_{game_state.current_turn}_score += {score}")
        return True

    def future_player_resources(self, game_state: Union['TankWarGameState', 'TankWarObservation']) -> int:
        future_resources = 0
        units = game_state.player_0_units if game_state.current_turn == 0 else game_state.player_1_units
        for tile in units.get_tiles_positions():
            if tile in units.get_tanks_positions():
                future_resources += game_state.board[tile]
        return future_resources

    def resolve_clash_with_tank(self, game_state: Union['TankWarGameState', 'TankWarObservation'], unit: 'TankWarUnit', destination: Tuple[int, int]) -> None:
        player_units = game_state.player_0_units if game_state.current_turn == 0 else game_state.player_1_units
        enemy_units = game_state.player_0_units if game_state.current_turn == 1 else game_state.player_1_units

        player_units_count = player_units.get_count_tanks_in_position(unit.get_pos())
        enemy_units_count = enemy_units.get_count_tanks_in_position(destination)
        units_diff = player_units_count - enemy_units_count
        
        if units_diff > 0:
            # The curent player has more tanks
            current_pos = unit.get_pos()
            player_units.move_unit(player_units.get_tank_in_position(unit.get_pos()), destination)
            player_units.add_unit(TankWarUnit(TankWarUnitType.TILE, destination))
            player_units.remove_tanks_in_position(current_pos, enemy_units_count)
            enemy_units.remove_all_units_in_position(destination)
        elif units_diff < 0:
            # The curent player has less tanks
            enemy_units.remove_tanks_in_position(destination, player_units_count)
            player_units.remove_all_units_in_position(unit.get_pos())
        else:
            # The curent player has the same number of tanks
            enemy_units.remove_tanks_in_position(destination, enemy_units_count)
            player_units.remove_tanks_in_position(unit.get_pos(), player_units_count)

    def resolve_clash_with_recycler(self, game_state: Union['TankWarGameState', 'TankWarObservation'], unit: 'TankWarUnit', destination: Tuple[int, int]) -> None:
        enemy_units = game_state.player_0_units if game_state.current_turn == 1 else game_state.player_1_units
        player_units = game_state.player_0_units if game_state.current_turn == 0 else game_state.player_1_units
        
        player_units.move_unit(player_units.get_tank_in_position(unit.get_pos()), destination)
        player_units.add_unit(TankWarUnit(TankWarUnitType.TILE, destination))
        enemy_units.remove_all_units_in_position(destination)

    def resolve_clash_with_tile(self, game_state: Union['TankWarGameState', 'TankWarObservation'], unit: 'TankWarUnit', destination: Tuple[int, int]) -> None:
        enemy_units = game_state.player_0_units if game_state.current_turn == 1 else game_state.player_1_units
        player_units = game_state.player_0_units if game_state.current_turn == 0 else game_state.player_1_units

        player_units.move_unit(player_units.get_tank_in_position(unit.get_pos()), destination)
        player_units.add_unit(TankWarUnit(TankWarUnitType.TILE, destination))
        enemy_units.remove_all_units_in_position(destination)
# endregion    
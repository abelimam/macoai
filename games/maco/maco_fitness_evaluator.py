from typing import List, Tuple
from games.maco.maco_action import MacoAction
from games.maco.maco_piece import MacoPiece, MacoPieceType
from games.maco.maco_observation import MacoObservation
from games.maco.maco_forward_model import MacoForwardModel
from heuristics import Heuristic
from players.ntuple_bandit_online_evolution import FitnessEvaluator

class MacoFitnessEvaluator(FitnessEvaluator):
    def __init__(self, heuristic: 'Heuristic'):
        self.heuristic = heuristic

    def evaluate(self, parameters: List[int], observation: 'MacoObservation', forward_model: 'MacoForwardModel', visited_states: dict) -> float:
        """Calculates the fitness of a turn given by N-Tuple Bandit Online Evolution as a parameter list, playing it from the given `Observation`."""
        turn = self.ntboe_to_turn(parameters, observation)
        for action in turn:
            forward_model.step(observation, action)
            visited_states[observation] = visited_states.get(observation, 0) + 1
        return self.heuristic.get_reward(observation)

    def ntboe_to_turn(self, ntboe_parameters: List[int], observation: 'MacoObservation') -> List['MacoAction']:
        """Converts a list of int parameters from N-Tuple Bandit Online Evolution to a list of `Action` representing a turn."""
        turn = []
        for parameter in ntboe_parameters:
            turn.append(self.get_action_from_parameter(parameter, observation))
        return turn

    def get_action_from_parameter(self, parameter: int, observation: 'MacoObservation') -> 'MacoAction':
        """Converts an int parameter from N-Tuple Bandit Online Evolution  to an `Action`."""
        board_size = observation.game_parameters.board_size
        total_positions = board_size * board_size

        if parameter < total_positions:
            # Place a regular piece
            row = parameter // board_size
            col = parameter % board_size
            piece = MacoPiece(MacoPieceType.REGULAR)
            return MacoAction(piece, (row, col))
        elif parameter < total_positions + 4:
            # Use an explode piece
            explode_pos = parameter - total_positions
            row, col = self.get_adjacent_position(explode_pos)
            piece = MacoPiece(MacoPieceType.EXPLODE)
            return MacoAction(piece, (row, col))
        elif parameter < total_positions + 4 + board_size:
            # Use a block piece
            row = parameter - (total_positions + 4)
            piece = MacoPiece(MacoPieceType.BLOCK)
            return MacoAction(piece, (row, None))
        else:
            # Invalid parameter
            return None

    def get_parameter_from_action(self, action: 'MacoAction') -> int:
        """Converts an `Action` to an int parameter for N-Tuple Bandit Online Evolution."""
        if action.get_piece().get_piece_type() == MacoPieceType.REGULAR:
            # Convert the position to a parameter value
            pos = action.get_position()
            if pos is not None:
                row, col = pos
                return row * 10 + col  # Assuming a 10x10 board size
            else:
                return -1
        elif action.get_piece().get_piece_type() == MacoPieceType.EXPLODE:
            # Convert the explode action to a parameter value
            pos = action.get_position()
            if pos is not None:
                row, col = pos
                explode_pos = self.get_adjacent_position_index(row, col)
                return 100 + explode_pos  # Assuming 100 is the offset for explode actions
            else:
                return -1
        elif action.get_piece().get_piece_type() == MacoPieceType.BLOCK:
            # Convert the block action to a parameter value
            pos = action.get_position()
            if pos is not None:
                row, _ = pos
                return 200 + row  # Assuming 200 is the offset for block actions
            else:
                return -1
        else:
            # Invalid action
            return -1

    def get_adjacent_position(self, explode_pos: int) -> Tuple[int, int]:
        # Implement the logic to get the adjacent position based on the explode_pos index
        if explode_pos == 0:
            return (-1, 0)  # Up
        elif explode_pos == 1:
            return (0, 1)  # Right
        elif explode_pos == 2:
            return (1, 0)  # Down
        elif explode_pos == 3:
            return (0, -1)  # Left
        else:
            raise ValueError(f"Invalid explode_pos value: {explode_pos}")

    def get_adjacent_position_index(self, row: int, col: int) -> int:
        # Implement the logic to get the index of the adjacent position
        if row == -1 and col == 0:
            return 0  # Up
        elif row == 0 and col == 1:
            return 1  # Right
        elif row == 1 and col == 0:
            return 2  # Down
        elif row == 0 and col == -1:
            return 3  # Left
        else:
            raise ValueError(f"Invalid adjacent position coordinates: ({row}, {col})")
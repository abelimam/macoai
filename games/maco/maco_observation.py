from typing import Any, Dict, List, Tuple
from games import Observation
from games.maco.maco_piece import MacoPiece, MacoPieceType
from games.maco.maco_action import MacoAction
from games.maco.maco_game_parameters import MacoGameParameters
import random

class MacoObservation(Observation):
    def __init__(self, game_state_info: Dict[str, Any]):
        if game_state_info is not None:
            self.game_parameters: 'MacoGameParameters' = game_state_info["game_parameters"]
            self.current_turn = game_state_info['current_turn']
            self.board = game_state_info['board']
            self.action_points_left = game_state_info['action_points_left']
            self.player_0_pieces = game_state_info['player_0_pieces']
            self.player_1_pieces = game_state_info['player_1_pieces']
            self.player_0_score = game_state_info['player_0_score']
            self.player_1_score = game_state_info['player_1_score']
            self.blocked_rows = game_state_info['blocked_rows']

    def clone(self) -> 'MacoObservation':
        new_observation = MacoObservation(None)
        new_observation.game_parameters = self.game_parameters
        new_observation.current_turn = self.current_turn
        new_observation.board = self.board.copy()
        new_observation.action_points_left = self.action_points_left
        new_observation.player_0_pieces = self.player_0_pieces.clone()
        new_observation.player_1_pieces = self.player_1_pieces.clone()
        new_observation.player_0_score = self.player_0_score
        new_observation.player_1_score = self.player_1_score
        new_observation.blocked_rows = self.blocked_rows.copy()
        return new_observation

    def copy_into(self, other: 'MacoObservation') -> None:
        other.game_parameters = self.game_parameters
        other.current_turn = self.current_turn
        other.board = self.board.copy()
        other.action_points_left = self.action_points_left
        other.player_0_pieces = self.player_0_pieces.clone()
        other.player_1_pieces = self.player_1_pieces.clone()
        other.player_0_score = self.player_0_score
        other.player_1_score = self.player_1_score
        other.blocked_rows = self.blocked_rows.copy()

    def is_action_valid(self, action: 'MacoAction') -> bool:
        pieces = self.player_0_pieces if self.current_turn == 0 else self.player_1_pieces
        piece = action.get_piece()
        position = action.get_position()
        if not self.can_place_piece(position):
            return False
        return True

    def can_place_piece(self, position: Tuple[int, int]) -> bool:
        return self.board[position] is None

    def get_actions(self) -> List['MacoAction']:
        actions = []
        pieces = self.player_0_pieces if self.current_turn == 0 else self.player_1_pieces

        # Generate actions for regular pieces
        regular_pieces = pieces.get_regular_pieces()
        if regular_pieces:
            piece = regular_pieces[0]
            for position in self.get_empty_positions():
                actions.append(MacoAction(piece, position))

        # Generate actions for explode pieces
        explode_pieces = pieces.get_explode_pieces()
        if explode_pieces:
            piece = explode_pieces[0]
            for position in self.get_empty_positions():
                actions.append(MacoAction(piece, position))

        # Generate actions for block pieces
        block_pieces = pieces.get_block_pieces()
        if block_pieces:
            piece = block_pieces[0]
            for position in self.get_empty_positions():
                actions.append(MacoAction(piece, position))

        return actions

    def get_random_action(self) -> 'MacoAction':
        actions = self.get_actions()
        if not actions:
            return None
        return random.choice(actions)

    def get_empty_positions(self) -> List[Tuple[int, int]]:
        empty_positions = []
        for i in range(self.game_parameters.board_size):
            for j in range(self.game_parameters.board_size):
                if self.board[(i, j)] is None:
                    empty_positions.append((i, j))
        return empty_positions

    def get_game_parameters(self) -> 'MacoGameParameters':
        return self.game_parameters

    def get_current_turn(self) -> int:
        return self.current_turn

    def get_action_points_left(self) -> int:
        return self.action_points_left

    def get_player_0_score(self) -> int:
        return self.player_0_score

    def get_player_1_score(self) -> int:
        return self.player_1_score

    def __str__(self):
        board_str = ""
        for i in range(self.game_parameters.board_size):
            row_str = " ".join(str(self.board[(i, j)] or "_") for j in range(self.game_parameters.board_size))
            board_str += row_str + "\n"

        return (
            f"TURN: {self.current_turn!s}\n"
            f"BOARD:\n{board_str}"
            f"PIECES P1: {self.player_0_pieces!s}\n"
            f"SCORE P1: {self.player_0_score!s}\n"
            f"PIECES P2: {self.player_1_pieces!s}\n"
            f"SCORE P2: {self.player_1_score!s}\n"
            f"ACTION POINTS LEFT: {self.action_points_left!s}"
        )

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, MacoObservation):
            return False
        return (
            self.game_parameters == other.game_parameters and
            self.current_turn == other.current_turn and
            self.board == other.board and
            self.action_points_left == other.action_points_left and
            self.player_0_pieces == other.player_0_pieces and
            self.player_1_pieces == other.player_1_pieces and
            self.player_0_score == other.player_0_score and
            self.player_1_score == other.player_1_score
        )

    def __hash__(self) -> int:
        return hash((
            self.game_parameters,
            self.current_turn,
            tuple(tuple(row) for row in self.board),
            self.action_points_left,
            self.player_0_pieces,
            self.player_1_pieces,
            self.player_0_score,
            self.player_1_score
        ))
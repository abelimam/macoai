import copy
from typing import Any, Dict, Tuple, Optional, Type
from games import GameState
from games.maco.maco_piece import MacoPiece, MacoPieceType
from games.maco.maco_game_parameters import MacoGameParameters
from games.maco.maco_observation import MacoObservation
from games.maco.maco_piece_collection import MacoPieceCollection


class MacoGameState(GameState):
    def __init__(self, game_parameters: 'MacoGameParameters') -> None:
        self.game_parameters = game_parameters
        self.current_turn = 0
        self.action_points_left = game_parameters.action_points_per_turn
        self.board = self.initialize_board_dict(self.game_parameters.board_size)
        self.player_0_pieces = self.initialize_player_pieces(self.game_parameters.pieces_per_player)
        self.player_1_pieces = self.initialize_player_pieces(self.game_parameters.pieces_per_player)
        self.player_0_score = 0
        self.player_1_score = 0
        self.blocked_rows = {}

    # region Methods
    def get_observation(self) -> 'MacoObservation':
        return MacoObservation(self.get_state_info())

    def reset(self) -> None:
        self.current_turn = 0
        self.action_points_left = self.game_parameters.action_points_per_turn
        self.board = self.initialize_board_dict(self.game_parameters.board_size)
        self.player_0_pieces = self.initialize_player_pieces(self.game_parameters.pieces_per_player)
        self.player_1_pieces = self.initialize_player_pieces(self.game_parameters.pieces_per_player)
        self.player_0_score = 0
        self.player_1_score = 0

    def board_to_string(self) -> str:
        board_str = ""
        for i in range(self.game_parameters.board_size):
            row_str = ""
            for j in range(self.game_parameters.board_size):
                cell = self.board.get((i, j))
                if cell == 0:
                    row_str += "0 "
                elif cell == 1:
                    row_str += "1 "
                else:
                    row_str += "_ "
            board_str += row_str.rstrip() + "\n"
        return board_str

    # endregion

    # region Helpers
    def initialize_player_pieces(self, pieces_per_player: int) -> 'MacoPieceCollection':
        pieces = MacoPieceCollection()
        for _ in range(pieces_per_player):
            pieces.add_piece(MacoPiece(MacoPieceType.REGULAR))
        for _ in range(self.game_parameters.special_pieces_per_type):
            pieces.add_piece(MacoPiece(MacoPieceType.EXPLODE))
            pieces.add_piece(MacoPiece(MacoPieceType.BLOCK))
        return pieces

    def initialize_board_dict(self, board_size: int) -> Dict[Tuple[int, int], Optional[int]]:
        return {(i, j): None for i in range(board_size) for j in range(board_size)}

    # endregion

    # region Override
    def get_current_turn(self) -> int:
        return self.current_turn

    def get_action_points_left(self) -> int:
        return self.action_points_left

    def get_game_parameters(self) -> 'MacoGameParameters':
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
            "player_0_pieces": self.player_0_pieces.clone(),
            "player_1_score": self.player_1_score,
            "player_1_pieces": self.player_1_pieces.clone(),
            "action_points_left": self.action_points_left,
            "game_parameters": self.game_parameters,
            "blocked_rows": self.blocked_rows.copy()
        }

    def __str__(self):

        return (
            f"TURN: {self.current_turn!s}\n"
            f"BOARD:\n{self.board_to_string()}"
            f"BOARD:\n{self.board}"
            # f"PIECES P1: {self.player_0_pieces!s}\n"
            # f"SCORE P1: {self.player_0_score!s}\n"
            # f"PIECES P2: {self.player_1_pieces!s}\n"
            # f"SCORE P2: {self.player_1_score!s}\n"
            # f"ACTION POINTS LEFT: {self.action_points_left!s}"
        )
# endregion
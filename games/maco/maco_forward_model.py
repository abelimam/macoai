from typing import Union, Tuple, List, Any

from games.maco.maco_piece_type import MacoPieceType
from games.maco.maco_game_state import MacoGameState
from games.maco.maco_action import MacoAction
from games.forward_model import ForwardModel
from games.maco.maco_observation import MacoObservation

class MacoForwardModel(ForwardModel):
    def __init__(self):
        super().__init__()

    def step(self, game_state: Union['MacoGameState', 'MacoObservation'], action: 'MacoAction') -> bool:
        game_state.action_points_left -= 1
        pieces = game_state.player_0_pieces if game_state.current_turn == 0 else game_state.player_1_pieces

        if action is None:
            return False

        action_pos = action.get_position()
        action_piece = action.get_piece()

        if action_pos is not None and action_piece.get_piece_type() == MacoPieceType.REGULAR:
            x, y = action_pos
            if game_state.board[action_pos] is not None or x in game_state.blocked_rows:
                return False  # Disallow placing a piece in a blocked row or occupied position
            game_state.board[action_pos] = game_state.current_turn
            pieces.remove_piece(action_piece)
            self.update_score(game_state)
            return True

        if action_pos is not None and action_piece.get_piece_type() == MacoPieceType.EXPLODE:
            x, y = action_pos
            if x in game_state.blocked_rows:
                return False  # Disallow exploding a piece in a blocked row
            if not self.explode_position(game_state, action_pos):
                return False
            pieces.remove_piece(action_piece)
            self.update_score(game_state)
            return True

        if action_pos is not None and action_piece.get_piece_type() == MacoPieceType.BLOCK:
            if not self.block_position(game_state, action_pos):
                return False
            pieces.remove_piece(action_piece)
            self.update_score(game_state)
            return True

        return False

    def on_turn_ended(self, game_state: Union['MacoGameState', 'MacoObservation']) -> None:
        if self.is_turn_finished(game_state):
            game_state.current_turn = (game_state.current_turn + 1) % 2
            game_state.action_points_left = game_state.game_parameters.action_points_per_turn

        rows_to_remove: list[Any] = []

        for row, duration in game_state.blocked_rows.items():
            game_state.blocked_rows[row] -= 1
            if game_state.blocked_rows[row] == 0:
                rows_to_remove.append(row)

        for row in rows_to_remove:
            del game_state.blocked_rows[row]
    def is_terminal(self, game_state: Union['MacoGameState', 'MacoObservation']) -> bool:
        return self.check_for_win(game_state) or self.check_for_draw(game_state)

    def is_turn_finished(self, observation: Union['MacoGameState', 'MacoObservation']) -> bool:
        return observation.get_action_points_left() == 0

    def check_for_win(self, game_state: Union['MacoGameState', 'MacoObservation']) -> bool:
        board_size = game_state.game_parameters.board_size
        win_length = game_state.game_parameters.win_condition_length

        for i in range(board_size):
            for j in range(board_size):
                if game_state.board[(i, j)] is not None:
                    player = game_state.board[(i, j)]
                    if self.check_direction(game_state, i, j, 1, 0, win_length, player) or \
                            self.check_direction(game_state, i, j, 0, 1, win_length, player) or \
                            self.check_direction(game_state, i, j, 1, 1, win_length, player) or \
                            self.check_direction(game_state, i, j, 1, -1, win_length, player):
                        return True
        return False

    def check_direction(self, game_state: Union['MacoGameState', 'MacoObservation'],
                        x: int, y: int, dx: int, dy: int, length: int, player: int) -> bool:
        board_size = game_state.game_parameters.board_size
        for i in range(length):
            nx, ny = x + i * dx, y + i * dy
            if nx < 0 or nx >= board_size or ny < 0 or ny >= board_size or game_state.board[(nx, ny)] != player:
                return False
        return True

    def check_for_draw(self, game_state: Union['MacoGameState', 'MacoObservation']) -> bool:
        board_size = game_state.game_parameters.board_size
        for i in range(board_size):
            for j in range(board_size):
                if game_state.board[(i, j)] is None:
                    return False
        return True

    def explode_position(self, game_state: Union['MacoGameState', 'MacoObservation'], position: Tuple[int, int]) -> bool:
        board_size = game_state.game_parameters.board_size
        x, y = position
        if game_state.board[(x, y)] is None:
            return False

        for dx, dy in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            nx, ny = x + dx, y + dy
            if 0 <= nx < board_size and 0 <= ny < board_size:
                game_state.board[(nx, ny)] = None

        game_state.board[(x, y)] = None
        return True

    def block_position(self, game_state: Union['MacoGameState', 'MacoObservation'], position: Tuple[int, int]) -> bool:
        x, y = position
        if game_state.board[(x, y)] is not None:
            return False

        game_state.board[(x, y)] = "B"
        game_state.blocked_rows[x] = 3  # Store the blocked row and set the duration to 3 moves
        return True

    def update_score(self, game_state: Union['MacoGameState', 'MacoObservation']) -> bool:
        # Check for a winner
        if self.check_for_win(game_state):
            # If there is a winner, set their score to 1 and the opponent's score to 0
            if game_state.current_turn == 0:
                game_state.player_0_score = 1
            else:
                game_state.player_1_score = 1

        return True

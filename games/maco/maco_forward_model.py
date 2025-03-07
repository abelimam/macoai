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

        if isinstance(game_state, MacoGameState):
            observation = game_state.get_observation()
        else:
            observation = game_state

        if action is None or not observation.is_action_valid(action):
            self.give_invalid_action_penalty(game_state)
            return False

        action_pos = action.get_position()
        action_piece = action.get_piece()

        if action_pos is not None and action_piece.get_piece_type() == MacoPieceType.REGULAR:
            x, y = action_pos
            if game_state.board[action_pos] is not None or x in game_state.blocked_rows:
                self.give_invalid_action_penalty(game_state)
                return False  # Disallow placing a piece in a blocked row or occupied position
            game_state.board[action_pos] = game_state.current_turn
            pieces.remove_piece(action_piece)
            self.update_score(game_state)
            return True

        if action_pos is not None and action_piece.get_piece_type() == MacoPieceType.EXPLODE:
            if not self.explode_position(game_state, action_pos):
                self.give_invalid_action_penalty(game_state)
                return False
            pieces.remove_piece(action_piece)
            self.update_score(game_state)
            return True

        if action_pos is not None and action_piece.get_piece_type() == MacoPieceType.BLOCK:
            if not self.block_position(game_state, action_pos):
                self.give_invalid_action_penalty(game_state)
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
        if self.check_for_win(game_state):
            return True
        elif self.check_for_draw(game_state):
            game_state.player_0_score = 0
            game_state.player_1_score = 0
            return True
        else:
            return False

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

    def explode_position(self, game_state: Union['MacoGameState', 'MacoObservation'],
                         position: Tuple[int, int]) -> bool:
        board_size = game_state.game_parameters.board_size
        x, y = position

        if game_state.board[(x, y)] is not None:
            return False

        for dx, dy in [(0, 0), (0, 1), (0, -1), (1, 0), (-1, 0)]:
            nx, ny = x + dx, y + dy
            if 0 <= nx < board_size and 0 <= ny < board_size:
                game_state.board[(nx, ny)] = None
        return True

    def block_position(self, game_state: Union['MacoGameState', 'MacoObservation'], position: Tuple[int, int]) -> bool:
        x, y = position
        if game_state.board[(x, y)] is not None:
            return False

        game_state.blocked_rows[x] = game_state.game_parameters.action_points_per_turn
        game_state.board[(x, y)] = None
        return True

    def update_score(self, game_state: Union['MacoGameState', 'MacoObservation']) -> bool:
        board_size = game_state.game_parameters.board_size

        # Calculate scores for each player based on the longest line
        player_0_score = self.calculate_player_score(game_state, game_state.board, board_size, 0)
        player_1_score = self.calculate_player_score(game_state, game_state.board, board_size, 1)

        # Check for a winner
        if self.check_for_win(game_state):
            # If there is a winner, significantly increase their score
            if game_state.current_turn == 0:
                player_0_score += 1000000
            else:
                player_1_score += 1000000
        elif self.is_terminal(game_state):
            # If the game has ended without a winner, set the scores to be equal (tie)
            player_0_score = 0
            player_1_score = 0

        game_state.player_0_score = player_0_score
        game_state.player_1_score = player_1_score

        return True

    def calculate_player_score(self, game_state, board, board_size, player):
        """Calculates the score for a player based on the longest line."""
        max_line_length = 0
        win_length = game_state.game_parameters.win_condition_length

        def check_direction(start_x, start_y, dx, dy):
            consecutive_count = 0
            empty_count = 0
            x, y = start_x, start_y

            while 0 <= x < board_size and 0 <= y < board_size:
                if board[(x, y)] == player:
                    consecutive_count += 1
                elif board[(x, y)] is None:
                    empty_count += 1
                else:
                    break

                if consecutive_count + empty_count >= win_length:
                    break

                x += dx
                y += dy

            if consecutive_count > 0 and consecutive_count + empty_count >= win_length:
                return consecutive_count
            return 0

        # Check vertical lines
        for col in range(board_size):
            for row in range(board_size):
                max_line_length = max(max_line_length, check_direction(row, col, 1, 0))

        # Check horizontal lines
        for row in range(board_size):
            for col in range(board_size):
                max_line_length = max(max_line_length, check_direction(row, col, 0, 1))

        # Check diagonal lines (top-left to bottom-right)
        for i in range(board_size):
            max_line_length = max(max_line_length, check_direction(i, 0, 1, 1))
            max_line_length = max(max_line_length, check_direction(0, i, 1, 1))

        # Check diagonal lines (top-right to bottom-left)
        for i in range(board_size):
            max_line_length = max(max_line_length, check_direction(i, board_size - 1, 1, -1))
            max_line_length = max(max_line_length, check_direction(0, i, 1, -1))

        return max_line_length

    def give_invalid_action_penalty(self, game_state: Union['MacoGameState', 'MacoObservation']) -> None:
        """Applies a penalty score to the current player for an invalid action."""
        penalty_score = -10
        if game_state.current_turn == 0:
            game_state.player_0_score += penalty_score
        else:
            game_state.player_1_score += penalty_score


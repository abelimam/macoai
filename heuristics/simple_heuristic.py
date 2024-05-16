from games import Observation
from heuristics.heuristic import Heuristic

# Ali
class SimpleHeuristic(Heuristic):
    """Defines a simple reward for the current player."""

    def get_reward(self, observation: 'Observation'):
        board = observation.board
        board_size = observation.game_parameters.board_size

        player_0_score = self.calculate_player_score(board, board_size, 0)
        player_1_score = self.calculate_player_score(board, board_size, 1)

        # Calculate the reward based on the player scores
        reward = player_0_score - player_1_score

        # Adjust the reward based on the current player's turn
        if observation.get_current_turn() == 1:
            reward *= -1

        # Add additional reward for disturbing opponent's line
        reward += self.calculate_disturbance_reward(observation)

        return reward

    def calculate_player_score(self, board, board_size, player):
        """Calculates the score for a player based on the longest line."""
        max_line_length = 0

        # Check vertical lines
        for col in range(board_size):
            consecutive_count = 0
            for row in range(board_size):
                if board[(row, col)] == player:
                    consecutive_count += 1
                else:
                    max_line_length = max(max_line_length, consecutive_count)
                    consecutive_count = 0
            max_line_length = max(max_line_length, consecutive_count)

        # Check horizontal lines
        for row in range(board_size):
            consecutive_count = 0
            for col in range(board_size):
                if board[(row, col)] == player:
                    consecutive_count += 1
                else:
                    max_line_length = max(max_line_length, consecutive_count)
                    consecutive_count = 0
            max_line_length = max(max_line_length, consecutive_count)

        # Check diagonal lines (top-left to bottom-right)
        for i in range(board_size):
            consecutive_count = 0
            for j in range(board_size - i):
                if board[(i + j, j)] == player:
                    consecutive_count += 1
                else:
                    max_line_length = max(max_line_length, consecutive_count)
                    consecutive_count = 0
            max_line_length = max(max_line_length, consecutive_count)

        # Check diagonal lines (top-right to bottom-left)
        for i in range(board_size):
            consecutive_count = 0
            for j in range(board_size - i):
                if board[(j, i + j)] == player:
                    consecutive_count += 1
                else:
                    max_line_length = max(max_line_length, consecutive_count)
                    consecutive_count = 0
            max_line_length = max(max_line_length, consecutive_count)

        return max_line_length ** 10

    def calculate_disturbance_reward(self, observation: 'Observation'):
        board = observation.board
        board_size = observation.game_parameters.board_size
        current_player = observation.get_current_turn()
        opponent_player = 1 - current_player

        disturbance_reward = 0

        # Check for disturbance by placing a piece
        for i in range(board_size):
            for j in range(board_size):
                if board.get((i, j)) == current_player:
                    if self.disturbs_opponent_line(board, i, j, opponent_player, observation.game_parameters):
                        disturbance_reward += 1

        # Check for disturbance by exploding
        for piece in observation.player_0_pieces.get_pieces() if current_player == 0 else observation.player_1_pieces.get_pieces():
            if piece.get_piece_type() == "EXPLODE":
                for position in observation.get_actions():
                    if self.disturbs_opponent_line(board, position[0], position[1], opponent_player, observation.game_parameters):
                        disturbance_reward += 1

        # Check for disturbance by blocking
        for piece in observation.player_0_pieces.get_pieces() if current_player == 0 else observation.player_1_pieces.get_pieces():
            if piece.get_piece_type() == "BLOCK":
                for position in observation.get_actions():
                    if self.disturbs_opponent_line(board, position[0], position[1], opponent_player, observation.game_parameters):
                        disturbance_reward += 1

        return disturbance_reward

    def disturbs_opponent_line(self, board, row, col, opponent_player, game_parameters):
        directions = [(0, 1), (1, 0), (1, 1), (1, -1)]
        winning_length = game_parameters.win_condition_length

        for dx, dy in directions:
            count = 0
            r, c = row, col
            while 0 <= r < len(board) and 0 <= c < len(board) and board.get((r, c)) == opponent_player:
                count += 1
                r += dx
                c += dy

            r, c = row - dx, col - dy
            while 0 <= r < len(board) and 0 <= c < len(board) and board.get((r, c)) == opponent_player:
                count += 1
                r -= dx
                c -= dy

            if count == winning_length - 2 or count == winning_length - 1:
                return True

        return False
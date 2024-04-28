from games import Observation
from heuristics.heuristic import Heuristic

# Ali
class SimpleHeuristic(Heuristic):
    """Defines a simple reward for the current player."""

    def get_reward(self, observation: 'Observation'):
        """Returns a reward for the current player."""
        board = observation.board
        board_size = observation.game_parameters.board_size

        player_0_score = self.calculate_player_score(board, board_size, 0)
        player_1_score = self.calculate_player_score(board, board_size, 1)

        # Calculate the reward based on the player scores
        reward = player_0_score - player_1_score

        # Adjust the reward based on the current player's turn
        if observation.get_current_turn() == 1:
            reward *= -1

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
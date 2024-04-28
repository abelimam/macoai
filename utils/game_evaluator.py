from games import Game
from heuristics import Heuristic
from players import Player, RandomPlayer, GreedyActionPlayer, GreedyTurnPlayer
from typing import List


class GameEvaluator:
    def __init__(self, game: Game, heuristic: Heuristic):
        self.game = game
        self.heuristic = heuristic

    def evaluate(self, player: Player, n_games: int, budget: float, rounds: int) -> float:
        """Play n_games OE vs random_player and greedy_action_player and return the pct of wins of the first."""
        p2 = RandomPlayer()
        p3 = GreedyActionPlayer(self.heuristic)
        p4 = GreedyTurnPlayer(self.heuristic)

        points = 0
        [w1, w2, ties] = self.play_games(int(n_games / 6), budget, rounds, player, p2)
        points += w1 + ties/2
        [w1, w2, ties] = self.play_games(int(n_games / 6), budget, rounds, p2, player)
        points += w2 + ties / 2
        [w1, w2, ties] = self.play_games(int(n_games / 6), budget, rounds, player, p3)
        points += w1 + ties / 2
        [w1, w2, ties] = self.play_games(int(n_games / 6), budget, rounds, p3, player)
        points += w2 + ties / 2
        [w1, w2, ties] = self.play_games(int(n_games / 6), budget, rounds, player, p4)
        points += w1 + ties / 2
        [w1, w2, ties] = self.play_games(int(n_games / 6), budget, rounds, p4, player)
        points += w2 + ties / 2
        return points / n_games

    def play_games(self, n_games: int, budget: float, rounds: int, p1: Player, p2: Player) -> List[int]:
        """Play n_games between p1 and p2 and return the number of wins of p1."""
        w1 = 0
        w2 = 0
        ties = 0
        for i in range(n_games):
            self.game.run(p1, p2, budget, rounds, False, True)
            if self.game.get_winner() == 0:
                w1 += 1
            elif self.game.get_winner() == 1:
                w2 += 1
            elif self.game.get_winner() == -1:
                ties += 1
        return [w1, w2, ties]
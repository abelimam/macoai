import math
import sys
from typing import List
import scipy.stats as ss
import time
import datetime
from tqdm import tqdm
from games import GameParameters, ForwardModel, Game
from games.maco import *
from players import *
from heuristics import *
from utils import ConfigurationReader, ResultsWriter


def get_game(game_name: str) -> 'Game':
    """Given the name of the game to be played, create the corresponding game objects."""
    parameters = get_parameters(game_name)
    forward_model = get_forward_model(game_name)
    return eval(game_name + 'Game')(parameters, forward_model)


def get_player(game: str, player_name: str, heuristic: 'Heuristic', conf: dict = None) -> 'Player':
    """Given the name of the player to be used, create the corresponding Player object."""
    player_name += 'Player'
    if player_name == 'RandomPlayer' or player_name == 'HumanPlayer':
        return eval(player_name)()
    if conf is None:
        return eval(player_name)(heuristic)
    if player_name == 'OnlineEvolutionPlayer':
        random_new_valid_action = conf.pop('random_new_valid_action', False)
        player = eval(player_name)(heuristic, **conf)
        player.set_random_new_valid_action(random_new_valid_action)
        return player
    if player_name == 'MontecarloTreeSearchPlayer':
        full_rollout_on = conf.pop('full_rollout_on', False)
        player = eval(player_name)(heuristic, **conf)
        if full_rollout_on:
            player.set_full_rollout_on()
        return player
    if player_name == 'GeneticPlayer':
        return eval(player_name)(heuristic, **conf)
    return eval(player_name)(heuristic, **conf)


def get_heuristic(heuristic_name: str) -> 'Heuristic':
    """Given the heuristic name, create the corresponding Heuristic object."""
    return eval(heuristic_name + 'Heuristic')()


def get_parameters(game: str) -> 'GameParameters':
    """Given the game name, create the corresponding GameParameters object."""
    return eval(game + 'GameParameters')()


def get_forward_model(game: str) -> 'ForwardModel':
    """Given the game name, create the corresponding ForwardModel object."""
    return eval(game + 'ForwardModel')()


def run_n_games(gm: 'Game', pl1: 'Player', pl2: 'Player', n_gms: int,
                budget: int, rounds: int, verbose: bool, enforce_time: bool) -> List[int]:
    """Run n_gms games and return the number of wins for each player and the number of ties."""
    wins1 = 0
    wins2 = 0
    ties = 0
    for _ in tqdm(range(n_gms), desc="Games"):
        winner = gm.run(pl1, pl2, budget, rounds, verbose, enforce_time)
        if winner == 0:
            wins1 += 1
        elif winner == 1:
            wins2 += 1
        else:
            ties += 1
    return [wins1, wins2, ties]


def stat_test(point1: int, point2: int, n: int) -> float:
    """two-proportion z-test to compare the performance of two bots"""
    # Number of games played
    n1 = n
    n2 = n

    # Number of games won by each bot
    w1 = point1
    w2 = point2

    # Proportions of games won by each bot
    p1 = w1 / n1
    p2 = w2 / n2

    # Pooled proportion
    p = (w1 + w2) / (n1 + n2)
    
    if p == 0:
        p = 1e-16
    elif p == 1:
        p = 1 - 1e-16
    
    # Standard error
    se = math.sqrt(p*(1-p)*(1/n1 + 1/n2))

    # z-score
    z = (p1 - p2) / se

    # Two-tailed p-value
    p_value = 2 * (1 - ss.norm.cdf(abs(z)))
    return p_value


if __name__ == '__main__':
    """ Play n matches of a game between two players."""
    """ Usage: python play_n_games.py configuration_file.json"""

    if len(sys.argv) != 2:
        print("Usage: python play_n_games.py configuration_file.json")
        sys.exit(1)

    conf = ConfigurationReader(sys.argv[1])

    game_name = conf.get("game_name")
    player1_name = conf.get("player1_name")
    player1_config = conf.get("player1_config")
    player2_name = conf.get("player2_name")
    player2_config = conf.get("player2_config")
    n_games = conf.get("n_games")
    heuristic_name = conf.get("heuristic_name")
    verbose = conf.get("verbose")
    enforce_time = conf.get("enforce_time")
    budget = conf.get("budget")
    rounds = conf.get("rounds")

    game = get_game(game_name)
    heuristic = get_heuristic(heuristic_name)
    player1 = get_player(game_name, player1_name, heuristic, player1_config)
    player2 = get_player(game_name, player2_name, heuristic, player2_config)

    print("\nGame           : {}".format(game_name))
    print("Heuristic      : {}".format(heuristic_name))
    print("Player1        : {}".format(player1_name))
    print("Player2        : {}".format(player2_name))
    print("Number of games: {}".format(n_games))
    print("Budget         : {}".format(budget))

    wins1 = 0
    wins2 = 0
    ties = 0
    t0 = time.time()
    w1, w2, t = run_n_games(game, player1, player2, int(n_games/2), budget, rounds, verbose, enforce_time)
    wins1 += w1
    wins2 += w2
    ties += t

    w1, w2, t = run_n_games(game, player2, player1, int(n_games/2), budget, rounds, verbose, enforce_time)
    wins2 += w1
    wins1 += w2
    ties += t
    tf = time.time() - t0

    if wins1 > wins2:
        p_value = stat_test(wins1, wins2, n_games)
    else:
        p_value = stat_test(wins2, wins1, n_games)

    print("Player 1 won   : {} games ".format(wins1))
    print("Player 2 won   : {} games ".format(wins2))
    print("Ties           : {} games ".format(ties))
    print("Two-proportion z-test (0.05): {}".format(p_value))

    if wins1 > wins2:
        if p_value < 0.05:
            print("Player {} is significantly better than Player {}".format(player1_name, player2_name))
        else:
            print("Player {} is not significantly better than Player {}".format(player1_name, player2_name))
    else:
        if p_value < 0.05:
            print("Player {} is significantly better than Player {}".format(player2_name, player1_name))
        else:
            print("Player {} is not significantly better than Player {}".format(player2_name, player1_name))

    output_filename = conf.get("result_file")
    result = ResultsWriter()
    result.set("game_name", game_name)
    result.set("heuristic_name", heuristic_name)
    result.set("player1_name", player1_name)
    result.set("player2_name", player2_name)
    result.set("n_games", n_games)
    result.set("budget", budget)
    result.set("wins1", wins1)
    result.set("wins2", wins2)
    result.set("ties", ties)
    result.set("player_1_forward_model_visits", player1.get_forward_model_visits() / n_games)
    result.set("player_1_visited_states", player1.get_visited_states_count() / n_games)
    result.set("player_2_forward_model_visits", player2.get_forward_model_visits() / n_games)
    result.set("player_2_visited_states", player2.get_visited_states_count() / n_games)
    result.set("p_value", p_value)
    result.set("processing_time", tf)
    result.set("date", datetime.datetime.now().strftime("%Y-%m-%d"))
    result.set("hour", datetime.datetime.now().strftime("%H:%M:%S"))
    result.write(output_filename)
import math
from sys import argv

from joblib import Parallel, delayed
import multiprocessing as mp

from games import Game
from games.maco import MacoGameParameters, MacoForwardModel, MacoGame
from heuristics import SimpleHeuristic
from players import MontecarloTreeSearchPlayer, BridgeBurningMontecarloTreeSearchPlayer
from utils import GameEvaluator, Ntbea


def evaluate_mcts(param_c: float, evaluator: GameEvaluator, n_games: int, budget: float, rounds: int):
    mcts_player = MontecarloTreeSearchPlayer(SimpleHeuristic(), param_c)
    score = evaluator.evaluate(mcts_player, n_games, budget, rounds)
    return param_c, score


def evaluate_mctsfull(param_c: float, evaluator: GameEvaluator, n_games: int, budget: float, rounds: int):
    mcts_player = MontecarloTreeSearchPlayer(SimpleHeuristic(), param_c)
    mcts_player.set_full_rollout_on()
    score = evaluator.evaluate(mcts_player, n_games, budget, rounds)
    return param_c, score


def evaluate_bbmcts(param_c: float, evaluator: GameEvaluator, n_games: int, budget: float, rounds: int):
    mcts_player = BridgeBurningMontecarloTreeSearchPlayer(SimpleHeuristic(), param_c)
    score = evaluator.evaluate(mcts_player, n_games, budget, rounds)
    return param_c, score


def do_mcts_style(game: Game, budget: float, out_filename: str, mcts_type: str, cores: int):
    evaluator = GameEvaluator(game, SimpleHeuristic())
    params_c = [round(0.35 + i*0.35, 2) for i in range(30)]
    n_games = 30
    rounds = 100

    results = []
    if cores == 1:
        for c in params_c:
            score = 0
            if mcts_type == "vanilla":
                score = evaluate_mcts(c, evaluator, n_games, budget, rounds)
            elif mcts_type == "full":
                score = evaluate_mctsfull(c, evaluator, n_games, budget, rounds)
            elif mcts_type == "bb":
                score = evaluate_bbmcts(c, evaluator, n_games, budget, rounds)
            results.append([c, score])
    else:
        if mcts_type == "vanilla":
            results = Parallel(n_jobs=cores)(
                delayed(evaluate_mcts)(c, evaluator, n_games, budget, rounds)
                for c in params_c
            )
        elif mcts_type == "full":
            results = Parallel(n_jobs=cores)(
                delayed(evaluate_mctsfull)(c, evaluator, n_games, budget, rounds)
                for c in params_c
            )
        elif mcts_type == "bb":
            results = Parallel(n_jobs=cores)(
                delayed(evaluate_bbmcts)(c, evaluator, n_games, budget, rounds)
                for c in params_c
            )

    best_c = None
    best_score = -math.inf
    out_str = ""
    for param_c, score in results:
        # if score >= best_score:
        #     best_score = score
        #     best_c = param_c
        out_str += str(param_c) + "," + str(score) + " \n"

    #out_str += "Best paramameters: " + str(best_c)
    with open(out_filename, "w") as f:
        f.write(out_str + " \n")


def do_mcts(game: Game, budget: float, out_filename: str, cores: int):
    do_mcts_style(game, budget, out_filename, "vanilla", cores)


def do_mcts_full(game: Game, budget: float, out_filename: str, cores: int):
    do_mcts_style(game, budget, out_filename, "full", cores)


def do_bbmcts(game: Game, budget: float, out_filename: str, cores: int):
    do_mcts_style(game, budget, out_filename, "bb", cores)


def do_oe(game: Game, budget: float, out_filename: str, oe_type: str, cores:int):
    evaluator = GameEvaluator(game, SimpleHeuristic())

    c_value = 1.4
    n_neighbours = 100
    n_initializations = 100
    n_games = 30
    rounds = 100
    n_iterations = 100

    param_population_size = [50, 100, 150, 200, 250, 300, 350, 400, 450, 500]
    param_mutation_rate = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9]
    param_survival_rate = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9]
    params = [param_population_size, param_mutation_rate, param_survival_rate]

    ntbea = Ntbea(params, evaluator, c_value, n_neighbours, n_initializations)
    ntbea.set_cores(cores)
    ntbea.set_str_debug_on()
    ntbea.set_algorithm(oe_type)
    ntbea.set_algorithm_heuristic(SimpleHeuristic())
    ntbea.set_verbose_on()
    best_params = ntbea.run(n_games, budget, n_iterations, rounds)

    out_str = ntbea.get_str_debug()
    out_str += "Best paramameters: " + \
              str(param_population_size[best_params[0]]) + "," + \
              str(param_mutation_rate[best_params[1]]) + "," + \
              str(param_survival_rate[best_params[2]])

    with open(out_filename, "w") as f:
        f.write(out_str + " \n")



def run_one(l_params: list):
    game_name = l_params[0]
    algorithm = l_params[1]
    budget = l_params[2]
    cores = l_params[3]

    out_filename = "out/hyper_" + game_name + "_" + algorithm + "_" + str(budget) + ".txt"

    game = None
    if game_name == "maco":
        parameters = MacoGameParameters()
        forward_model = MacoForwardModel()
        game = MacoGame(parameters, forward_model)

    if algorithm == "oerandom":
        do_oe(game, budget, out_filename, "oerandom", cores)
    elif algorithm == "oegreedy":
        do_oe(game, budget, out_filename, "oegreedy", cores)
    elif algorithm == "mcts":
        do_mcts(game, budget, out_filename, cores)
    elif algorithm == "mctsfull":
        do_mcts_full(game, budget, out_filename, cores)
    elif algorithm == "bbmcts":
        do_bbmcts(game, budget, out_filename, cores)



def run_many():
    runs = [
        ["maco", "mcts", 1, 1],
        ["maco", "mctsfull", 1, 1],
        ["maco", "bbmcts", 1, 1],
        ["maco", "oerandom", 1, 1],
        ["maco", "oegreedy", 1, 1],
    ]
    cores = min(mp.cpu_count()-2, len(runs))
    pool = mp.Pool(cores)

    _ = pool.map(run_one, runs)
    pool.close()


if __name__ == '__main__':
    # game_name = argv[1]
    # algorithm = argv[2]
    # budget = float(argv[3])
    # cores = int(argv[4])
    # run_one([game_name, algorithm, budget, cores])

    run_many()
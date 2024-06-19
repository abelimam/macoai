import json
from conf.players_config import *

def generate_parameter_combinations(base_config, parameters):
    combinations = []
    keys = list(parameters.keys())

    def backtrack(start_index, curr_config):
        if start_index == len(keys):
            combinations.append(curr_config.copy())
            return

        key = keys[start_index]
        for value in parameters[key]:
            curr_config[key] = value
            backtrack(start_index + 1, curr_config)

    backtrack(0, base_config)
    return combinations

if __name__ == '__main__':
    budgets = [5]
    players = ['Genetic', 'MontecarloTreeSearch', 'BridgeBurningMontecarloTreeSearch', 'OnlineEvolution']
    players_code = ['gen', 'mcts', 'mctsbb', 'oe']
    opponents = ['GreedyAction']
    parameters = {
        'Genetic': {
            'population_size': [5, 10, 20, 30],
            'mutation_rate': [0.1, 0.2, 0.3, 0.4],
            'elite_rate': [0.1, 0.2, 0.3, 0.4],
            'generations': [50, 75, 100, 125]
        },
        'MontecarloTreeSearch': {
            'c_value': [1.4, 2.8, 3.5, 4.2]
        },
        'BridgeBurningMontecarloTreeSearch': {
            'c_value': [1.4, 2.8, 3.5, 4.2]
        },
        'OnlineEvolution': {
            'population_size': [5, 10, 20, 30],
            'mutation_rate': [0.1, 0.2, 0.3, 0.4],
            'survival_rate': [0.1, 0.2, 0.3, 0.4]
        }
    }
    games = ['Maco']

    for game in games:
        for budget in budgets:
            for player, player_code in zip(players, players_code):
                for opponent in opponents:
                    base_config = eval(f"get_{player.lower()}_conf(budget)")
                    config_combinations = generate_parameter_combinations(base_config, parameters[player])

                    for i, player_config in enumerate(config_combinations, start=1):
                        conf = {
                            "game_name": game,
                            "n_games": 10,
                            "budget": budget,
                            "rounds": 100,
                            "verbose": False,
                            "enforce_time": True,
                            "heuristic_name": "Simple",
                            "player1_name": player,
                            "player1_config": player_config,
                            "player2_name": opponent
                        }

                        player1_str_conf = "_".join(f"{value}" for key, value in player_config.items())
                        out = f"out/{game.lower()}/"
                        filename = f"conf/{game.lower()}/"
                        simple_conf = f"{player_code}_grac_simple_100_{budget}"
                        out += f"{simple_conf}_{player1_str_conf}.json"
                        filename += f"{simple_conf}_{player1_str_conf}.json"
                        conf["result_file"] = out

                        with open(filename, 'w') as f:
                            json.dump(conf, f, indent=4)
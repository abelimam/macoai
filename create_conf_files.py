import json

if __name__ == '__main__':
    budgets = [0.5, 1, 3, 5]
    players = ['GreedyAction', 'GreedyTurn', 'MontecarloTreeSearch', 'MontecarloTreeSearch_Full', 'BridgeBurningMontecarloTreeSearch', 'NonExploringMontecarloTreeSearch', 'OnlineEvolution', 'OnlineEvolution_Random', 'Random', 'Genetic']
    players_code = ['grac', 'grtu', 'mcts', 'mctsf', 'bbmcts', 'nemcts', 'oe', 'oer', 'rand', 'gen']
    non_config = ['Random', 'GreedyAction', 'GreedyTurn', 'NonExploringMontecarloTreeSearch']

    for budget in budgets:
        for i in range(len(players)):
            for j in range(i + 1, len(players)):
                if players[i] in non_config and players[j] in non_config:
                    continue

                # Basic configuration
                conf = {
                    "game_name": "Maco",
                    "n_games": 10,
                    "budget": budget,
                    "rounds": 100,
                    "verbose": False,
                    "enforce_time": True,
                    "heuristic_name": "Simple",
                }

                # Player 1 configuration
                player = players[i]
                conf["player1_name"] = player.replace('_Random', '').replace('_Full', '')
                player1_str_conf = None
                if player not in non_config:
                    if player == "MontecarloTreeSearch" or player == "MontecarloTreeSearch_Full" or player == "BridgeBurningMontecarloTreeSearch":
                        p_conf = {"c_value": 1.4}
                        if player == "MontecarloTreeSearch_Full":
                            p_conf["full_rollout_on"] = True
                        conf["player1_config"] = p_conf
                        player1_str_conf = "_".join(str(val).replace('.', '') for val in p_conf.values())
                    elif player == "OnlineEvolution" or player == "OnlineEvolution_Random":
                        p_conf = {
                            "population_size": 125,
                            "mutation_rate": 0.15,
                            "survival_rate": 0.15
                        }
                        if player == "OnlineEvolution_Random":
                            p_conf["random_new_valid_action"] = True
                        conf["player1_config"] = p_conf
                        player1_str_conf = "_".join(str(val).replace('.', '') for val in p_conf.values())
                    elif player == "Genetic":
                        p_conf = {
                            "population_size": 150,
                            "mutation_rate": 0.2,
                            "elite_rate": 0.15,
                            "generations": 100
                        }
                        conf["player1_config"] = p_conf
                        player1_str_conf = "_".join(str(val).replace('.', '') for val in p_conf.values())

                # Player 2 configuration
                conf["player2_name"] = players[j].replace('_Random', '').replace('_Full', '')
                player2_str_conf = None
                if players[j] not in non_config:
                    if players[j] == "MontecarloTreeSearch" or players[j] == "MontecarloTreeSearch_Full" or players[j] == "BridgeBurningMontecarloTreeSearch":
                        p_conf = {"c_value": 1.4}
                        if players[j] == "MontecarloTreeSearch_Full":
                            p_conf["full_rollout_on"] = True
                        conf["player2_config"] = p_conf
                        player2_str_conf = "_".join(str(val).replace('.', '') for val in p_conf.values())
                    elif players[j] == "OnlineEvolution" or players[j] == "OnlineEvolution_Random":
                        p_conf = {
                            "population_size": 125,
                            "mutation_rate": 0.15,
                            "survival_rate": 0.15
                        }
                        if players[j] == "OnlineEvolution_Random":
                            p_conf["random_new_valid_action"] = True
                        conf["player2_config"] = p_conf
                        player2_str_conf = "_".join(str(val).replace('.', '') for val in p_conf.values())
                    elif players[j] == "Genetic":
                        p_conf = {
                            "population_size": 150,
                            "mutation_rate": 0.2,
                            "elite_rate": 0.15,
                            "generations": 100
                        }
                        conf["player2_config"] = p_conf
                        player2_str_conf = "_".join(str(val).replace('.', '') for val in p_conf.values())

                # Out file configuration
                out = f"out/maco/"
                filename = f"conf/maco/"
                simple_conf = f"{players_code[i]}_{players_code[j]}_simple_100_{budget if budget != 0.5 else '05'}"
                out += simple_conf
                filename += simple_conf
                if player1_str_conf:
                    out += f"_{player1_str_conf}"
                    filename += f"_{player1_str_conf}"
                if player2_str_conf:
                    out += f"_{player2_str_conf}"
                    filename += f"_{player2_str_conf}"
                out += ".json"
                filename += ".json"
                conf["result_file"] = out

                with open(filename, 'w') as f:
                    json.dump(conf, f, indent=4)
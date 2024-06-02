import json
from conf.players_config import *


if __name__ == '__main__':
    budgets = [0.5, 1, 3, 5]
    players = ['GreedyAction', 'GreedyTurn', 'MontecarloTreeSearch', 'MontecarloTreeSearch_Full', 'BridgeBurningMontecarloTreeSearch', 'NonExploringMontecarloTreeSearch', \
                'Genetic', 'OnlineEvolution', 'OnlineEvolution_Random', 'Random']
    players_code = ['grac', 'grtu', 'mcts', 'mcts', 'mctsbb', 'mctsne', 'gen', 'oe', 'oe', 'rand']
    non_config = ['Random', 'GreedyAction', 'GreedyTurn', 'NonExploringMontecarloTreeSearch']
    games = ['Maco']

    for game in games:
        for buget in budgets:
            for i in range(len(players)):
                for j in range(i + 1, len(players)):
                    if (players[i] in non_config and players[j] in non_config) or (players[i] == 'NTupleBanditOnlineEvolution' or players[j] == 'NTupleBanditOnlineEvolution'):
                        continue

                    # Basic configuration
                    conf = {
                        "game_name": game,
                        "n_games": 2,
                        "budget": buget,
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
                        p_conf = eval('get_' + player.lower() + '_conf')(buget)
                        conf["player1_config"] = p_conf
                        player1_str_conf = "_".join(str(int(val)) if isinstance(val, bool) else str(val).replace('.', '') for val in p_conf.values())
    
                    # Player 2 configuration
                    conf["player2_name"] = players[j].replace('_Random', '').replace('_Full', '')
                    player2_str_conf = None
                    if players[j] not in non_config:
                        p_conf = eval('get_' + players[j].lower() + '_conf')(buget)
                        conf["player2_config"] = p_conf
                        player2_str_conf = "_".join(str(int(val)) if isinstance(val, bool) else str(val).replace('.', '') for val in p_conf.values())

                    # Out file configuration
                    out = f"out/{game.lower()}/"
                    filename = f"conf/{game.lower()}/"
                    simple_conf = f"{players_code[i]}_{players_code[j]}_simple_100_{buget if buget != 0.5 else '05'}"
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
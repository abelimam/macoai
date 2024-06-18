import os  #

from games.maco import *
from heuristics import SimpleHeuristic
from players import *


if __name__ == '__main__':
    # Players parameters
    ## Greedy Action
    greedy_heuristic = SimpleHeuristic()
    ## Greedy Turn
    greedyt_heuristic = SimpleHeuristic()    
    ## Monte Carlo Tree Search
    mcts_heuristic = SimpleHeuristic()
    ## Online Evolution
    oe_heuristic = SimpleHeuristic()
    ## Genetic
    genetic_heuristic = SimpleHeuristic()

    ## NTuple Bandit Online Evolution
    dimensions = [38, 38, 38]  # Update based on Maco's action space
    ntboe_heuristic = SimpleHeuristic()

    save_name = "out/maco_output.txt"  # Where the game is going to be saved, can be None
    save_directory = os.path.dirname(save_name)  # Extracts the directory part from the save_name path
    if save_directory and not os.path.exists(save_directory):  # Checks if the directory part is not empty and does not exist
        os.makedirs(save_directory)  # Creates the directory and any intermediate directories if they don't exist

    # Common parameters
    budget = 5                                  # Time to think for the players (in seconds)
    rounds = 100                                # Number of rounds to play
    verbose = True                              # Whether to print messages
    enforce_time = True                         # Whether the player time to think is going to be enforced
    save_name = "out/maco_output.txt"           # Where the game is going to be saved, can be None

    # MACO parameters
    parameters = MacoGameParameters()
    forward_model = MacoForwardModel()
    game = MacoGame(parameters, forward_model)

    # players
    random_player = RandomPlayer()
    human_player = HumanPlayer()
    always_first = AlwaysFirstPlayer()
    greedy = GreedyActionPlayer(greedy_heuristic)
    greedyt = GreedyTurnPlayer(greedyt_heuristic)
    mcts = MontecarloTreeSearchPlayer(mcts_heuristic, 1.5)
    bbmcts = BridgeBurningMontecarloTreeSearchPlayer(mcts_heuristic, 2.8)
    nemcts = NonExploringMontecarloTreeSearchPlayer(mcts_heuristic)
    oe = OnlineEvolutionPlayer(oe_heuristic, 80, 0.2, 0.2)
    genetic = GeneticPlayer(genetic_heuristic, 10, 0.2, 0.2, 100)


    players = [greedy, genetic]  # List of players

    game.set_save_file(save_name)

    game.run(players[0], players[1], budget, rounds, verbose, enforce_time)

    if verbose:
        print("\n*** ------------------------------------------------- ")
        if game.get_winner() != -1:
            print(f"*** The winner is player: {game.get_winner()} [{players[game.get_winner()]}]")
        else:
            print("*** There is a Tie.")
        print("*** ------------------------------------------------- ")
    else:
        print(f"The winner is player: {game.get_winner()} [{players[game.get_winner()]}]")

    print(game.game_state.board_to_string())

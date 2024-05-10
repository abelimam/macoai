import func_timeout
from games.asmacag import *
from games.hero_academy import *
from games.tank_war import *
from players import *
from heuristics import SimpleHeuristic

if __name__ == '__main__':
    # Players parameters
    ## Greedy Action
    greedy_hueristic = SimpleHeuristic()
    ## Greedy Turn
    greedyt_hueristic = SimpleHeuristic()    
    ## Monte Carlo Tree Search
    mcts_heuristic = SimpleHeuristic()
    ## Online Evolution
    oe_heuristic = SimpleHeuristic()
    ## NTuple Bandit Online Evolution
    dimensions = [38, 38, 38]
    ntboe_heuristic = SimpleHeuristic()

    # Common parameters
    budget = 1                                  # time to think for the players (in seconds)
    rounds = 10                                # number of rounds to play
    verbose = True                              # whether to print messages
    enforce_time = True                         # whether the player time to think is going to be enforced
    save_name = "out/sample_output.txt"         # where the game is going to be saved, can be None

    # ASMACAG parameters
    # parameters = AsmacagGameParameters()
    # forward_model = AsmacagForwardModel()
    # fitness_asmacag = AsmacagFitnessEvaluator(ntboe_heuristic)
    # game = AsmacagGame(parameters, forward_model)

    # Hero Academy parameters
    parameters = HeroAcademyGameParameters()
    forward_model = HeroAcademyForwardModel()
    fitness_heroac = HeroAcademyFitnessEvaluator(ntboe_heuristic)
    game = HeroAcademyGame(parameters, forward_model)

    # Tank war parameters
    # parameters = TankWarGameParameters()
    # forward_model = TankWarForwardModel()
    # fitness_tankwar = TankWarFitnessEvaluator(ntboe_heuristic)
    # game = TankWarGame(parameters, forward_model)

    # Common players
    random = RandomPlayer()
    greedy = GreedyActionPlayer(greedy_hueristic)
    greedyt = GreedyTurnPlayer(greedyt_hueristic)
    mcts = MontecarloTreeSearchPlayer(mcts_heuristic, 8)
    bbmcts = BridgeBurningMontecarloTreeSearchPlayer(mcts_heuristic, 8)
    nemcts = NonExploringMontecarloTreeSearchPlayer(mcts_heuristic)
    oe = OnlineEvolutionPlayer(oe_heuristic, 125, 0.15, 0.15)

    # ASMACAG players
    # ntboe_asmacag = NTupleBanditOnlineEvolutionPlayer(ntboe_heuristic, fitness_asmacag, dimensions, 8, 5, 0.55, 1000)

    # Hero Academy players
    ntboe_heroac = NTupleBanditOnlineEvolutionPlayer(ntboe_heuristic, fitness_heroac, dimensions, 8, 5, 0.55, 1000)

    # Tank war players
    # ntboe_tankwar = NTupleBanditOnlineEvolutionPlayer(ntboe_heuristic, fitness_tankwar, dimensions, 8, 5, 0.55, 1000)
    
    players = [greedyt, ntboe_heroac]                       # list of players

    game.set_save_file(save_name)

    game.run(players[0], players[1], budget, rounds, verbose, enforce_time)

    if verbose:
        print("")
        print("*** ------------------------------------------------- ")
        if game.get_winner() != -1:
            print(f"*** The winner is the player: {game.get_winner()!s} [{players[game.get_winner()]!s}]")
        else:
            print("*** There is a Tie.")
        print("*** ------------------------------------------------- ")
    else:
        print(f"The winner is the player: {game.get_winner()!s} [{players[game.get_winner()]!s}]")
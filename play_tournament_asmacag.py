from games.asmacag import *
from players import *
from heuristics import SimpleHeuristic

def actualize_points(points, winner, i1, i2):
    if winner == 0:
        points[i1] += 1
    elif winner == 1:
        points[i2] += 1
    else:
        points[i1] += 0.5
        points[i2] += 0.5


def play_tournament(l_players, game, budget, verbose, enforce_time, n_matches):
    rounds = 1
    points = [0, 0, 0, 0, 0]
    i1 = 0
    for p1 in l_players:
        i2 = 0
        for p2 in l_players:
            if p1 != p2:
                print("Playing ", str(p1), " vs ", str(p2))
                for m in range(int(n_matches/2)):
                    game.run(p1, p2, budget, rounds, verbose, enforce_time)
                    actualize_points(points, game.get_winner(), i1, i2)
                print(points)
            i2 += 1

        i1 += 1
    return points


if __name__ == '__main__':
    # ASMACAG parameters
    parameters = AsmacagGameParameters()
    forward_model = AsmacagForwardModel()
    fitness_asmacag = AsmacagFitnessEvaluator(SimpleHeuristic())
    game = AsmacagGame(parameters, forward_model)

    # Create players
    random = RandomPlayer()
    greedy = GreedyActionPlayer(SimpleHeuristic())
    mcts = MontecarloTreeSearchPlayer(SimpleHeuristic(), 8)
    oe = OnlineEvolutionPlayer(SimpleHeuristic(), 125, 0.15, 0.15)
    ntboe_asmacag = NTupleBanditOnlineEvolutionPlayer(SimpleHeuristic(), fitness_asmacag, [38, 38, 38], 8, 5, 0.55, 1000)

    l_players = [random, greedy, mcts, oe, ntboe_asmacag]

    budget = 1                                  # time to think for the players (in seconds)
    verbose = False                              # whether to print messages
    enforce_time = True                         # whether the player time to think is going to be enforced
    n_matches = 10

    points = play_tournament(l_players, game, budget, verbose, enforce_time, n_matches)
    print("Points: ", points)

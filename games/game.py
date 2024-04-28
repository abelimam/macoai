from abc import abstractmethod
from io import TextIOWrapper
from typing import List, Optional
from games.action import Action
from games.observation import Observation
from games.game_state import GameState
from games.forward_model import ForwardModel
from players import Player
import random
import sys
import func_timeout

class Game:
    def __init__(self, game_state: 'GameState', forward_model: 'ForwardModel', save_file: Optional[TextIOWrapper] = None) -> None:
        """Class that will define how to play the game"""
        self.game_state = game_state
        self.forward_model = forward_model
        self.save_file = save_file
        self.current_round = 0

# region Methods
    def reset(self) -> None:
        """Resets the `GameState` so that is ready for a new `Game`."""
        self.game_state.reset()
        self.current_round = 0

    def run(self, player_0: 'Player', player_1: 'Player', budget: float, rounds: int, verbose: bool, enforce_time: bool) -> int:
        """Runs a `Game`."""
        save_str = ""

        if self.game_state.get_game_parameters().get_seed() is None:
            seed = random.randrange(sys.maxsize)
        else:
            seed = self.game_state.get_game_parameters().get_seed()

        random.seed(seed)
        if self.save_file is not None:
            save_str += f"{seed}\n"
        if verbose:
            print("")
            print("*** ------------------------------------------------- ")
            print(f"*** Game started with seed {seed}")
            print("*** ------------------------------------------------- ")

        self.reset()

        if self.save_file is not None:
            save_str += f"{self.game_state.get_game_parameters()}\n"
            save_str += f"{player_0!s} {player_1!s}\n"
            save_str += self.add_custom_info_to_save_file()

        players = [player_0, player_1]

        # Run players' turns while the game is not finished
        while not self.forward_model.is_terminal(self.game_state) and self.current_round < rounds:
            for action in self.play_turn(players[self.game_state.get_current_turn()], budget, verbose, enforce_time):
                if self.save_file is not None:
                    save_str += f"{self.game_state.get_current_turn()!s} {action!s}\n"
                
            self.forward_model.on_turn_ended(self.game_state)
            self.current_round += 1

        if self.save_file is not None:
            self.save_file.write(save_str)
            self.save_file.close()

        return self.get_winner()

    def play_turn(self, player: 'Player', budget: float, verbose: bool, enforce_time: bool) -> None:
        """Performs a `Player` turn."""
        if verbose:
            print("")
            print("---------------------------------------- ")
            print(f"Player {self.game_state.get_current_turn()} [{player!s}] turn")
            print("---------------------------------------- ")
            print(f"{self.game_state}\n")

        observation = self.game_state.get_observation()
        if enforce_time:
            try:
                func_timeout.func_timeout(budget, self.think, args=[player, observation, budget])
            except func_timeout.FunctionTimedOut:
                if verbose:
                    print("Too much time thinking!")
        else:
            self.think(player, observation, budget)

        for i in range(self.game_state.get_game_parameters().get_action_points_per_turn()):
            action = player.get_action(i)
            if action is None:
                if verbose:
                    print("Player didn't return an action. A random action was selected!")
                action = self.get_random_action(self.game_state.get_observation())

            if verbose:
                print(f"Player {self.game_state.get_current_turn()} selects {action!s}.")

            self.forward_model.step(self.game_state, action)
            
            yield action
        
    def think(self, player: 'Player', observation: 'Observation', budget: float) -> 'Action':
        """Requires the `Player` to decide, given an `Observation`, what `Action` to play and returns it."""
        return player.think(observation, self.forward_model, budget)

    def get_random_action(self, observation: 'Observation') -> 'Action':
        """Returns a random valid `Action` for the state defined in the given `Observation`."""
        return observation.get_random_action()
# endregion

# region Getters and Setters
    def set_save_file(self, filename: Optional[str]) -> None:
        """Sets the save file"""
        self.save_file = open(filename, "w") if filename is not None else None

    def get_winner(self) -> int:
        """Returns the index of the `Player` that is winning the `Game`."""
        if self.game_state.get_player_0_score() > self.game_state.get_player_1_score():
            return 0
        elif self.game_state.get_player_1_score() > self.game_state.get_player_0_score():
            return 1
        else:
            return -1
# endregion
        
# region Overridable
    def add_custom_info_to_save_file(self):
        """Adds custom information to the save file"""
        pass
# endregion
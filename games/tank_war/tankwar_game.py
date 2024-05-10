from games import Game
from games.tank_war.tankwar_game_parameters import TankWarGameParameters
from games.tank_war.tankwar_game_state import TankWarGameState
from games.tank_war.tankwar_forward_model import TankWarForwardModel

class TankWarGame(Game):
    def __init__(self, parameters: 'TankWarGameParameters', forward_model: 'TankWarForwardModel'):
        self.save_file = None
        self.game_state: 'TankWarGameState' = TankWarGameState(parameters)
        self.forward_model = forward_model

# region Overrides
    def add_custom_info_to_save_file(self) -> str:
        info = f"{self.game_state.player_0_resources!s}\n"
        info += f"{self.game_state.player_1_resources!s}\n"
        info += f"{self.game_state.player_0_units!s}\n"
        info += f"{self.game_state.player_1_units!s}\n"
        return info
# endregion
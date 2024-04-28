from games import Game
from games.maco.maco_game_parameters import MacoGameParameters
from games.maco.maco_game_state import MacoGameState
from games.maco.maco_forward_model import MacoForwardModel

class MacoGame(Game):
    def __init__(self, parameters: 'MacoGameParameters', forward_model: 'MacoForwardModel'):
        self.game_state: 'MacoGameState' = MacoGameState(parameters)
        self.forward_model = forward_model
        self.save_file = None

    def add_custom_info_to_save_file(self) -> str:
        info = f"{self.game_state.player_0_pieces!s}\n"
        info += f"{self.game_state.player_1_pieces!s}\n"
        info += f"{self.game_state.player_0_score!s}\n"
        info += f"{self.game_state.player_1_score!s}\n"
        return info
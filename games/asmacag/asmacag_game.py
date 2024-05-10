from games import Game
from games.asmacag.asmacag_game_parameters import AsmacagGameParameters
from games.asmacag.asmacag_game_state import AsmacagGameState
from games.asmacag.asmacag_forward_model import AsmacagForwardModel

class AsmacagGame(Game):
    def __init__(self, parameters: 'AsmacagGameParameters', forward_model: 'AsmacagForwardModel'):
        self.save_file = None
        self.game_state: 'AsmacagGameState' = AsmacagGameState(parameters)
        self.forward_model = forward_model

# region Overrides
    def add_custom_info_to_save_file(self) -> str:
        info = f"{self.game_state.board!s}\n"
        info += f"{self.game_state.player_0_hand!s}\n"
        info += f"{self.game_state.player_1_hand!s}\n"
        return info
# endregion
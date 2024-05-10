from games import Game
from games.hero_academy.heroac_game_parameters import HeroAcademyGameParameters
from games.hero_academy.heroac_game_state import HeroAcademyGameState
from games.hero_academy.heroac_forward_model import HeroAcademyForwardModel

class HeroAcademyGame(Game):
    def __init__(self, parameters: 'HeroAcademyGameParameters', forward_model: 'HeroAcademyForwardModel'):
        self.save_file = None
        self.game_state: 'HeroAcademyGameState' = HeroAcademyGameState(parameters)
        self.forward_model = forward_model

# region Overrides
    def add_custom_info_to_save_file(self) -> str:
        info = f"{self.game_state.player_0_cards!s}\n"
        info += f"{self.game_state.player_1_cards!s}\n"
        info += f"{self.game_state.player_0_units!s}\n"
        info += f"{self.game_state.player_1_units!s}\n"
        return info
# endregion
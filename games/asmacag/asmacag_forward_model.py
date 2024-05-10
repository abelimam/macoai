from typing import Union
from games.asmacag.asmacag_card_type import AsmacagCardType
from games.asmacag.asmacag_action import AsmacagAction
from games.asmacag.asmacag_observation import AsmacagObservation
from games.asmacag.asmacag_game_state import AsmacagGameState
from games.forward_model import ForwardModel

class AsmacagForwardModel(ForwardModel):
    """Defines a basic default set of rules for a `Game`."""

    # region Methods
    def step(self, game_state: Union['AsmacagGameState', 'AsmacagObservation'], action: 'AsmacagAction') -> bool:
        """Moves a `GameState` or `Observation` forward by playing the `Action`. Returns false if the `Action` couldn't be played."""
        game_state.action_points_left -= 1
        hand = game_state.player_0_hand if game_state.current_turn == 0 else game_state.player_1_hand
        
        if action is None:
            # invalid action: no action returned
            game_state.discard_deck.add_card(hand.get_cards()[0])
            hand.remove(hand.get_cards()[0])
            self.give_min_score(game_state)
            return False
        elif action.get_played_card() not in hand:
            # invalid action: selected card is not in hand, give min score and remove first card in hand
            game_state.discard_deck.add_card(hand.get_cards()[0])
            hand.remove(hand.get_cards()[0])
            self.give_min_score(game_state)
            return False
        else:
            if action.get_played_card().get_type() == AsmacagCardType.NUMBER:
                # number action
                if action.get_board_card() is None or action.get_board_card() not in game_state.board:
                    # invalid number action: no card on board to play, give min score and remove played card form hand
                    game_state.discard_deck.add_card(action.get_played_card())
                    hand.remove(action.get_played_card())
                    self.give_min_score(game_state)
                    return False
                else:
                    # valid number action
                    score = action.get_played_card().get_number() - action.get_board_card().get_number()
                    if game_state.factor != 1:
                        score *= game_state.factor
                        game_state.factor = 1

                    exec(f"game_state.player_{game_state.current_turn}_score += {score}")

                    game_state.discard_deck.add_card(action.get_played_card())
                    game_state.discard_deck.add_card(action.get_board_card())
                    hand.remove(action.get_played_card())
                    game_state.board.remove(action.get_board_card())
            else:
                # special action
                game_state.factor *= 2 if action.get_played_card().get_type() == AsmacagCardType.MULT2 else game_state.factor / 2

                game_state.discard_deck.add_card(action.get_played_card())
                hand.remove(action.get_played_card())

    def on_turn_ended(self, game_state: Union['AsmacagGameState', 'AsmacagObservation']) -> None:
        """Moves the `GameState` or `Observation` when the `ASMACAG.Players.Player.Player` turn is finished."""
        if self.is_turn_finished(game_state):
            game_state.current_turn = (game_state.current_turn + 1) % 2
            game_state.action_points_left = game_state.game_parameters.action_points_per_turn

    def is_terminal(self, game_state: Union['AsmacagGameState', 'AsmacagObservation']) -> bool:
        """Tests a `GameState` or `Observation` against a finish condition and returns whether it has finished."""
        return game_state.player_0_hand.get_empty() and game_state.player_1_hand.get_empty() \
            or game_state.board.get_empty()

    def is_turn_finished(self, game_state: Union['AsmacagGameState', 'AsmacagObservation']) -> bool:
        """Tests a `GameState` or `Observation` against the end turn condition and returns whether the turn has finished."""
        return game_state.action_points_left <= 0 \
            or (game_state.current_turn == 0 and game_state.player_0_hand.get_empty()) \
            or (game_state.current_turn == 1 and game_state.player_1_hand.get_empty())

    def give_min_score(self, game_state: Union['AsmacagGameState', 'AsmacagObservation']) -> None:
        """Calculates the minimum possible score for the `GameState` or `Observation` and adds it to the current player."""
        score = pow(2, game_state.game_parameters.action_points_per_turn - 1) \
            * (game_state.game_parameters.min_number - game_state.game_parameters.max_number)
        
        exec(f"game_state.player_{game_state.current_turn}_score += {score}")
# endregion

# region Overrides
    def __str__(self):
        return "SimpleForwardModel"
# endregion
from typing import Any, Dict
from games import GameState
from games.asmacag.asmacag_card_type import AsmacagCardType
from games.asmacag.asmacag_card import AsmacagCard
from games.asmacag.asmacag_card_collection import AsmacagCardCollection
from games.asmacag.asmacag_game_parameters import AsmacagGameParameters
from games.asmacag.asmacag_observation import AsmacagObservation

class AsmacagGameState(GameState):
    """Contains the state of a `Game`."""
    def __init__(self, game_parameters: 'AsmacagGameParameters'):
        self.game_parameters: 'AsmacagGameParameters' = game_parameters
        self.current_turn = 0
        self.player_0_hand = AsmacagCardCollection()
        self.player_1_hand = AsmacagCardCollection()
        self.board = AsmacagCardCollection()
        self.main_deck = AsmacagCardCollection()
        self.discard_deck = AsmacagCardCollection()
        self.player_0_score = 0
        self.player_1_score = 0
        self.factor = 1
        self.action_points_left = 0

# region Methods
    def get_observation(self) -> 'AsmacagObservation':
        """Gets a `Observation` representing this `GameState` with its non-observable parts randomised."""
        return AsmacagObservation(self.get_state_info(), self.game_parameters.randomise_hidden_info)

    def reset(self) -> None:
        """Resets and sets up the `GameState` so that is ready for a new `Game`. Must be called by `Game.run`."""
        self.current_turn = 0
        self.player_0_hand.clear()
        self.player_1_hand.clear()
        self.board.clear()
        self.main_deck.clear()
        self.discard_deck.clear()
        self.player_0_score = 0
        self.player_1_score = 0
        self.factor = 1
        self.action_points_left = self.game_parameters.action_points_per_turn

        # add number cards to the deck
        for n in range(self.game_parameters.min_number, self.game_parameters.max_number + 1):
            if n == self.game_parameters.min_number or n == self.game_parameters.max_number:
                for _ in range(self.game_parameters.amount_cards_limit_number):
                    self.main_deck.add_card(AsmacagCard(AsmacagCardType.NUMBER, n))
            else:
                for _ in range(self.game_parameters.amount_cards_normal_number):
                    self.main_deck.add_card(AsmacagCard(AsmacagCardType.NUMBER, n))

        # add special cards to the deck
        for _ in range(self.game_parameters.amount_cards_mult2):
            self.main_deck.add_card(AsmacagCard(AsmacagCardType.MULT2))
        for _ in range(self.game_parameters.amount_cards_div2):
            self.main_deck.add_card(AsmacagCard(AsmacagCardType.DIV2))

        # shuffle the deck
        self.main_deck.shuffle()
        
        # draw cards into players' hands
        for _ in range(self.game_parameters.amount_cards_on_hand):
            self.player_0_hand.add_card(self.main_deck.draw())
            self.player_1_hand.add_card(self.main_deck.draw())

        # draw cards into the board, only number cards
        special_cards = AsmacagCardCollection()
        for _ in range(self.game_parameters.amount_cards_on_board):
            card = self.main_deck.draw()
            while card.get_type() != AsmacagCardType.NUMBER:
                special_cards.add_card(card)
                card = self.main_deck.draw()
            self.board.add_card(card)

        # add special cards again and shuffle the deck
        self.main_deck.add_cards(special_cards)
        self.main_deck.shuffle()
# endregion

# region Overrides
    def get_current_turn(self) -> int:
        return self.current_turn
    
    def get_action_points_left(self) -> int:
        return self.action_points_left
    
    def get_game_parameters(self) -> 'AsmacagGameParameters':
        return self.game_parameters
    
    def get_player_0_score(self) -> int:
        return self.player_0_score
    
    def get_player_1_score(self) -> int:
        return self.player_1_score
    
    def get_state_info(self) -> Dict[str, Any]:
        return {
            "current_turn": self.current_turn,
            "player_0_hand": self.player_0_hand.clone(),
            "player_1_hand": self.player_1_hand.clone(),
            "board": self.board.clone(),
            "main_deck": self.main_deck.clone(),
            "discard_deck": self.discard_deck.clone(),
            "player_0_score": self.player_0_score,
            "player_1_score": self.player_1_score,
            "factor": self.factor,
            "action_points_left": self.action_points_left,
            "game_parameters": self.game_parameters
        }

    def __str__(self):
        return (f"TURN: {self.current_turn!s}\n"
                f"BOARD: {self.board!s}\n"
                f"HAND P1: {self.player_0_hand!s}\n"
                f"SCORE P1: {self.player_0_score!s}\n"
                f"HAND P2: {self.player_1_hand!s}\n"
                f"SCORE P2: {self.player_1_score!s}\n"
                f"FACTOR: {self.factor!s}\n"
                f"ACTION POINTS LEFT: {self.action_points_left!s}")
# endregion
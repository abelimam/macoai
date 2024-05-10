from typing import Union, Tuple
from copy import deepcopy
from games import ForwardModel
from games.hero_academy.heroac_tile_type import HeroAcademyTileType
from games.hero_academy.heroac_card_value import HeroAcademyCardValue
from games.hero_academy.heroac_card import HeroAcademyCard
from games.hero_academy.heroac_unit import HeroAcademyUnit
from games.hero_academy.heroac_action import HeroAcademyAction
from games.hero_academy.heroac_observation import HeroAcademyObservation
from games.hero_academy.heroac_game_state import HeroAcademyGameState

class HeroAcademyForwardModel(ForwardModel):
    def __init__(self):
        super().__init__()

# region Methods
    def step(self, game_state: Union['HeroAcademyGameState', 'HeroAcademyObservation'], action: 'HeroAcademyAction') -> bool:
        """Perform an action on the game state."""
        game_state.action_points_left -= 1

        if action is None:
            return False
        
        action_pos = deepcopy(action.get_position()) if action.get_position() is not None else None
        unit = action.get_unit().clone() if action.get_unit() is not None else None
        
        cards = game_state.player_0_cards if game_state.current_turn == 0 else game_state.player_1_cards
        units = game_state.player_0_units if game_state.current_turn == 0 else game_state.player_1_units
        enemy_units = game_state.player_1_units if game_state.current_turn == 0 else game_state.player_0_units

        if type(action.get_subject()) is HeroAcademyCard:
            card = action.get_subject().clone()
            if card not in cards.get_cards():
                return False
            if unit is None and action_pos is None:
                cards.remove_card(card)
                self.update_score(game_state)
                return True
            elif unit is not None:
                units.get_unit_in_position(deepcopy(unit.get_pos())).get_equipement().append(card)
                cards.remove_card(card)
                self.update_score(game_state)
                return True
            elif action_pos is not None:
                if card.get_value().is_spell_value():
                    target = enemy_units.get_unit_in_position(action_pos)
                    if target is None:
                        return False
                    target.set_hp(target.get_hp() - 400)
                    if target.get_hp() <= 0:
                        enemy_units.remove_unit(target)
                elif card.get_value() == HeroAcademyCardValue.HEAL_POTION:
                    target = units.get_unit_in_position(action_pos)
                    if target is None:
                        return False
                    target.set_hp(target.get_hp() + 300)
                else:
                    units.add_unit(HeroAcademyUnit.create(card, action_pos))
                cards.remove_card(card)
                self.update_score(game_state)
                return True
            else:
                return False
        else:
            subject = action.get_subject().clone()
            if action_pos is None:
                if subject.get_card().get_value() == HeroAcademyCardValue.CLERIC and unit in units.get_units():
                    target = units.get_unit_in_position(unit.get_pos())
                    if target is None:
                        return False
                    target.set_hp(target.get_hp() + unit.get_power())
                else:
                    target = enemy_units.get_unit_in_position(unit.get_pos())
                    if target is None:
                        return False
                    subject.attack_unit(target, game_state.board[subject.get_pos()] == HeroAcademyTileType.ATTACK)
                    if target.get_hp() <= 0:
                        enemy_units.remove_unit(target)
            else:
                target = units.get_unit_in_position(subject.get_pos())
                if target is None:
                    return False
                target.set_pos(action_pos)

            self.update_score(game_state)
            return True

    def on_turn_ended(self, game_state: Union['HeroAcademyGameState', 'HeroAcademyObservation']) -> None:
        if self.is_turn_finished(game_state):
            player_cards = game_state.player_0_cards if game_state.current_turn == 0 else game_state.player_1_cards
            deck = game_state.player_0_deck if game_state.current_turn == 0 else game_state.player_1_deck
            for _ in range(game_state.game_parameters.cards_on_hand - player_cards.get_number_cards()):
                card_add = deck.get_first_card()
                if card_add is not None:
                    player_cards.add_card(card_add)
            game_state.current_turn = (game_state.current_turn + 1) % 2
            game_state.action_points_left = game_state.game_parameters.action_points_per_turn

    def is_terminal(self, game_state: Union['HeroAcademyGameState', 'HeroAcademyObservation']) -> bool:
        terminal = not game_state.player_0_units.crystals_alive() or not game_state.player_1_units.crystals_alive() \
            or self.current_player_cant_play(game_state)
        if self.current_player_cant_play(game_state):
            self.update_terminal_score(game_state)
        return terminal

    def is_turn_finished(self, game_state: Union['HeroAcademyGameState', 'HeroAcademyObservation']) -> bool:
        return game_state.action_points_left <= 0 or self.current_player_cant_play(game_state)
# endregion

# region Helpers
    def current_player_cant_play(self, game_state: Union['HeroAcademyGameState', 'HeroAcademyObservation']) -> bool:
        """Return if the player can't play."""
        current_units = game_state.player_0_units if game_state.current_turn == 0 else game_state.player_1_units
        current_cards = game_state.player_0_cards if game_state.current_turn == 0 else game_state.player_1_cards

        return current_units.get_units_alive() == 0 and current_cards.is_empty()
    
    def next_player_has_units(self, game_state: Union['HeroAcademyGameState', 'HeroAcademyObservation']) -> bool:
        """Return if the player can't play."""
        next_units = game_state.player_1_units if game_state.current_turn == 0 else game_state.player_0_units
        next_cards = game_state.player_1_cards if game_state.current_turn == 0 else game_state.player_0_cards
        next_deck = game_state.player_1_deck if game_state.current_turn == 0 else game_state.player_0_deck

        return next_units.get_units_alive() > 0 or len(next_cards.get_unit_cards()) > 0 or len(next_deck.get_unit_cards()) > 0
    
    def update_terminal_score(self, game_state: Union['HeroAcademyGameState', 'HeroAcademyObservation']) -> None:
        if self.current_player_cant_play(game_state) and self.next_player_has_units(game_state):
            game_state.set_enemy_player_score(self.get_absolute_score(game_state))
        if not self.current_player_cant_play(game_state) and not self.next_player_has_units(game_state):
            game_state.set_current_player_score(self.get_absolute_score(game_state))

    def get_absolute_score(self, game_state: Union['HeroAcademyGameState', 'HeroAcademyObservation']) -> int:
        return abs(game_state.player_0_score) + abs(game_state.player_1_score)

    def update_score(self, game_state: Union['HeroAcademyGameState', 'HeroAcademyObservation']) -> None:
        """Update score."""
        current_units = game_state.player_0_units if game_state.current_turn == 0 else game_state.player_1_units
        enemy_units = game_state.player_1_units if game_state.current_turn == 0 else game_state.player_0_units

        current_hp = sum(map(lambda unit: unit.get_hp(), current_units.get_crystals()))
        enemy_hp = sum(map(lambda unit: unit.get_hp(), enemy_units.get_crystals()))
        current_attack = sum(map(lambda unit: unit.get_bonus_attack(), current_units.get_units()))
        enemy_attack = sum(map(lambda unit: unit.get_bonus_attack(), enemy_units.get_units()))

        score = int((current_hp - enemy_hp) * 0.01)
        score += int((current_attack - enemy_attack) * 0.1)
        score += current_units.get_units_alive() - enemy_units.get_units_alive()

        exec(f"game_state.player_{game_state.current_turn}_score += {score}")
# endregion    